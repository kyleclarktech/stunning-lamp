#!/usr/bin/env python3
"""
Debug tool for directly testing Cypher queries and troubleshooting issues.
Provides direct database access and query analysis capabilities.
"""

import asyncio
import json
import os
import sys
import time
import argparse
import falkordb
from datetime import datetime
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv
import httpx
from pathlib import Path
from jinja2 import Template

# Load environment variables
load_dotenv()


class QueryDebugger:
    """Debug tool for Cypher query analysis"""
    
    def __init__(self):
        self.falkor_client = None
        self.db = None
        self.ollama_host = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
        self.ollama_model = os.getenv('OLLAMA_MODEL', 'granite3.3:8b')
        self._setup_database()
    
    def _setup_database(self):
        """Setup database connection"""
        try:
            host = os.getenv('FALKOR_HOST', 'localhost')
            port = int(os.getenv('FALKOR_PORT', 6379))
            self.falkor_client = falkordb.FalkorDB(
                host=host, 
                port=port,
                socket_connect_timeout=10,
                socket_timeout=10
            )
            self.db = self.falkor_client.select_graph("agent_poc")
            print(f"✅ Connected to FalkorDB at {host}:{port}")
        except Exception as e:
            print(f"❌ Failed to connect to FalkorDB: {e}")
            sys.exit(1)
    
    def execute_query(self, cypher_query: str) -> Dict[str, Any]:
        """Execute a Cypher query and return results with timing"""
        print(f"\n📊 Executing query: {cypher_query}")
        
        start_time = time.time()
        try:
            result = self.db.query(cypher_query)
            execution_time = time.time() - start_time
            
            # Format results
            results = []
            if result.result_set:
                columns = [col[1] for col in result.header] if result.header else []
                for row in result.result_set:
                    if columns:
                        results.append(dict(zip(columns, row)))
                    else:
                        results.append(row)
            
            return {
                "success": True,
                "execution_time": execution_time,
                "result_count": len(results),
                "columns": columns if 'columns' in locals() else [],
                "results": results,
                "error": None
            }
            
        except Exception as e:
            execution_time = time.time() - start_time
            return {
                "success": False,
                "execution_time": execution_time,
                "result_count": 0,
                "results": [],
                "error": str(e)
            }
    
    def analyze_query_performance(self, cypher_query: str) -> Dict[str, Any]:
        """Analyze query performance using EXPLAIN"""
        explain_query = f"EXPLAIN {cypher_query}"
        
        try:
            result = self.db.query(explain_query)
            plan = []
            if result.result_set:
                for row in result.result_set:
                    plan.append(str(row))
            
            return {
                "query": cypher_query,
                "execution_plan": plan
            }
        except Exception as e:
            return {
                "query": cypher_query,
                "error": str(e)
            }
    
    def test_query_generation(self, natural_language: str) -> Dict[str, Any]:
        """Test AI query generation from natural language"""
        print(f"\n🤖 Testing query generation for: '{natural_language}'")
        
        # Load prompt template
        prompt_path = Path("prompts/generate_query.txt")
        if not prompt_path.exists():
            return {"error": "Prompt template not found"}
        
        with open(prompt_path, 'r') as f:
            template_content = f.read()
        
        template = Template(template_content)
        prompt = template.render() + f"\n\nQuestion: \"{natural_language}\"\nQuery:"
        
        # Call Ollama
        try:
            response = httpx.post(
                f"{self.ollama_host}/api/chat",
                json={
                    "model": self.ollama_model,
                    "messages": [{"role": "user", "content": prompt}],
                    "stream": False
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                generated_query = data.get('message', {}).get('content', '')
                
                # Clean up the query
                if "```" in generated_query:
                    start = generated_query.find("```")
                    if start >= 0:
                        start = generated_query.find("\n", start) + 1
                        end = generated_query.find("```", start)
                        if end > start:
                            generated_query = generated_query[start:end].strip()
                
                return {
                    "natural_language": natural_language,
                    "generated_query": generated_query,
                    "success": True
                }
            else:
                return {
                    "natural_language": natural_language,
                    "error": f"Ollama returned status {response.status_code}",
                    "success": False
                }
                
        except Exception as e:
            return {
                "natural_language": natural_language,
                "error": str(e),
                "success": False
            }
    
    def validate_schema(self) -> Dict[str, Any]:
        """Validate that the database schema matches expectations"""
        print("\n🔍 Validating database schema...")
        
        expected_nodes = {
            "Person": ["id", "name", "email", "department", "role", "hire_date", "location", "manager_id"],
            "Team": ["id", "name", "department", "focus"],
            "Group": ["id", "name", "description", "type", "lead_department"],
            "Policy": ["id", "name", "description", "category", "severity", "responsible_type", "compliance_frameworks"]
        }
        
        expected_relationships = [
            "MEMBER_OF",
            "REPORTS_TO", 
            "RESPONSIBLE_FOR"
        ]
        
        validation_results = {
            "nodes": {},
            "relationships": {},
            "issues": []
        }
        
        # Check node types and properties
        for node_type, expected_props in expected_nodes.items():
            try:
                # Get sample node
                result = self.execute_query(f"MATCH (n:{node_type}) RETURN n LIMIT 1")
                if result["success"] and result["results"]:
                    node = result["results"][0]["n"] if "n" in result["results"][0] else result["results"][0]
                    actual_props = list(node.keys()) if isinstance(node, dict) else []
                    
                    missing_props = set(expected_props) - set(actual_props)
                    extra_props = set(actual_props) - set(expected_props)
                    
                    validation_results["nodes"][node_type] = {
                        "exists": True,
                        "expected_properties": expected_props,
                        "actual_properties": actual_props,
                        "missing_properties": list(missing_props),
                        "extra_properties": list(extra_props)
                    }
                    
                    if missing_props:
                        validation_results["issues"].append(
                            f"{node_type} missing properties: {missing_props}"
                        )
                else:
                    validation_results["nodes"][node_type] = {
                        "exists": False,
                        "error": "No nodes found"
                    }
                    validation_results["issues"].append(f"No {node_type} nodes found")
                    
            except Exception as e:
                validation_results["nodes"][node_type] = {
                    "exists": False,
                    "error": str(e)
                }
                validation_results["issues"].append(f"Error checking {node_type}: {e}")
        
        # Check relationships
        for rel_type in expected_relationships:
            try:
                result = self.execute_query(f"MATCH ()-[r:{rel_type}]->() RETURN count(r) as count")
                if result["success"]:
                    count = result["results"][0]["count"] if result["results"] else 0
                    validation_results["relationships"][rel_type] = {
                        "exists": count > 0,
                        "count": count
                    }
                    if count == 0:
                        validation_results["issues"].append(f"No {rel_type} relationships found")
                else:
                    validation_results["relationships"][rel_type] = {
                        "exists": False,
                        "error": result["error"]
                    }
            except Exception as e:
                validation_results["relationships"][rel_type] = {
                    "exists": False,
                    "error": str(e)
                }
        
        validation_results["valid"] = len(validation_results["issues"]) == 0
        
        return validation_results
    
    def test_query_patterns(self) -> List[Dict[str, Any]]:
        """Test common query patterns"""
        print("\n🧪 Testing common query patterns...")
        
        test_patterns = [
            {
                "name": "Simple node match",
                "query": "MATCH (p:Person) RETURN p.name LIMIT 5",
                "expected": "Should return person names"
            },
            {
                "name": "Relationship traversal",
                "query": "MATCH (p:Person)-[:MEMBER_OF]->(t:Team) RETURN p.name, t.name LIMIT 5",
                "expected": "Should return person-team relationships"
            },
            {
                "name": "Full-text search",
                "query": "CALL db.idx.fulltext.queryNodes('all_text_search', 'Engineering') YIELD node, score RETURN node, score LIMIT 5",
                "expected": "Should return nodes matching 'Engineering'"
            },
            {
                "name": "Aggregation",
                "query": "MATCH (p:Person) RETURN p.department, count(p) as count ORDER BY count DESC",
                "expected": "Should return department counts"
            },
            {
                "name": "Complex pattern",
                "query": "MATCH (p:Person)-[:MEMBER_OF]->(t:Team {department: 'Engineering'}) WHERE p.role CONTAINS 'Senior' RETURN p.name, p.role, t.name",
                "expected": "Should return senior engineers"
            },
            {
                "name": "Multi-hop traversal",
                "query": "MATCH (p:Person)-[:REPORTS_TO]->(m:Person)-[:MEMBER_OF]->(t:Team) RETURN p.name, m.name as manager, t.name as manager_team LIMIT 10",
                "expected": "Should return people with their manager's team"
            }
        ]
        
        results = []
        for pattern in test_patterns:
            result = self.execute_query(pattern["query"])
            results.append({
                "pattern": pattern["name"],
                "query": pattern["query"],
                "expected": pattern["expected"],
                "success": result["success"],
                "result_count": result["result_count"],
                "execution_time": result["execution_time"],
                "error": result.get("error")
            })
        
        return results
    
    def interactive_mode(self):
        """Run in interactive mode for manual query testing"""
        print("\n🔧 Interactive Query Debug Mode")
        print("Commands:")
        print("  - Type a Cypher query to execute it")
        print("  - Type 'nl: <text>' to test natural language conversion")
        print("  - Type 'explain: <query>' to see execution plan")
        print("  - Type 'validate' to check schema")
        print("  - Type 'patterns' to test common patterns")
        print("  - Type 'quit' to exit")
        print("-" * 60)
        
        while True:
            try:
                user_input = input("\n> ").strip()
                
                if user_input.lower() == 'quit':
                    break
                elif user_input.lower() == 'validate':
                    validation = self.validate_schema()
                    print(json.dumps(validation, indent=2))
                elif user_input.lower() == 'patterns':
                    patterns = self.test_query_patterns()
                    for p in patterns:
                        status = "✅" if p["success"] else "❌"
                        print(f"{status} {p['pattern']}: {p['result_count']} results in {p['execution_time']:.3f}s")
                        if p["error"]:
                            print(f"   Error: {p['error']}")
                elif user_input.startswith('nl:'):
                    nl_query = user_input[3:].strip()
                    result = self.test_query_generation(nl_query)
                    if result["success"]:
                        print(f"Generated query: {result['generated_query']}")
                        # Execute the generated query
                        exec_result = self.execute_query(result['generated_query'])
                        self._print_results(exec_result)
                    else:
                        print(f"Error: {result['error']}")
                elif user_input.startswith('explain:'):
                    query = user_input[8:].strip()
                    plan = self.analyze_query_performance(query)
                    print(json.dumps(plan, indent=2))
                else:
                    # Execute as Cypher query
                    result = self.execute_query(user_input)
                    self._print_results(result)
                    
            except KeyboardInterrupt:
                print("\nUse 'quit' to exit")
            except Exception as e:
                print(f"Error: {e}")
    
    def _print_results(self, result: Dict[str, Any]):
        """Pretty print query results"""
        if result["success"]:
            print(f"✅ Success - {result['result_count']} results in {result['execution_time']:.3f}s")
            
            if result["results"]:
                # Print first 10 results
                print("\nResults (first 10):")
                for i, row in enumerate(result["results"][:10]):
                    print(f"  {i+1}. {json.dumps(row, default=str)}")
                
                if result["result_count"] > 10:
                    print(f"  ... and {result['result_count'] - 10} more")
        else:
            print(f"❌ Error: {result['error']}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Debug tool for Cypher queries")
    parser.add_argument("--query", "-q", help="Execute a single query")
    parser.add_argument("--nl", help="Test natural language to Cypher conversion")
    parser.add_argument("--validate", action="store_true", help="Validate database schema")
    parser.add_argument("--patterns", action="store_true", help="Test common query patterns")
    parser.add_argument("--interactive", "-i", action="store_true", help="Run in interactive mode")
    
    args = parser.parse_args()
    
    debugger = QueryDebugger()
    
    if args.query:
        result = debugger.execute_query(args.query)
        debugger._print_results(result)
    elif args.nl:
        result = debugger.test_query_generation(args.nl)
        if result["success"]:
            print(f"Generated query: {result['generated_query']}")
            exec_result = debugger.execute_query(result['generated_query'])
            debugger._print_results(exec_result)
        else:
            print(f"Error: {result['error']}")
    elif args.validate:
        validation = debugger.validate_schema()
        print(json.dumps(validation, indent=2))
    elif args.patterns:
        patterns = debugger.test_query_patterns()
        for p in patterns:
            status = "✅" if p["success"] else "❌"
            print(f"{status} {p['pattern']}: {p['result_count']} results in {p['execution_time']:.3f}s")
            if p["error"]:
                print(f"   Error: {p['error']}")
    else:
        # Default to interactive mode
        debugger.interactive_mode()


if __name__ == "__main__":
    main()