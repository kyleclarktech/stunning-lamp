#!/usr/bin/env python3
"""
Comprehensive test suite for Cypher query generation and execution.
Tests the system's ability to convert natural language to Cypher queries
and validate results.
"""

import asyncio
import websockets
import json
import time
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import falkordb
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'query_test_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class QueryType(Enum):
    """Types of queries the system should handle"""
    BASIC_ENTITY = "basic_entity"
    RELATIONSHIP = "relationship"
    AGGREGATION = "aggregation"
    COMPLEX = "complex"
    EDGE_CASE = "edge_case"
    FALLBACK = "fallback"


@dataclass
class TestCase:
    """Structure for a single test case"""
    id: str
    description: str
    query: str
    query_type: QueryType
    expected_tool: str  # "custom_query", "search_database", or "pig_latin"
    validation: Optional[Callable[[Dict], bool]] = None
    expected_min_results: int = 0
    expected_max_results: int = 1000
    should_trigger_fallback: bool = False
    tags: List[str] = None


class QueryTestRunner:
    """Main test runner for query system"""
    
    def __init__(self, websocket_url: str = "ws://localhost:8000/ws"):
        self.websocket_url = websocket_url
        self.results = []
        self.falkor_client = None
        self._setup_database_connection()
    
    def _setup_database_connection(self):
        """Setup direct database connection for validation"""
        try:
            host = os.getenv('FALKOR_HOST', 'localhost')
            port = int(os.getenv('FALKOR_PORT', 6379))
            self.falkor_client = falkordb.FalkorDB(host=host, port=port)
            self.db = self.falkor_client.select_graph("agent_poc")
            logger.info(f"Connected to FalkorDB at {host}:{port}")
        except Exception as e:
            logger.error(f"Failed to connect to FalkorDB: {e}")
            self.falkor_client = None
    
    async def run_single_test(self, test_case: TestCase) -> Dict[str, Any]:
        """Run a single test case and return results"""
        logger.info(f"Running test {test_case.id}: {test_case.description}")
        
        result = {
            "test_id": test_case.id,
            "description": test_case.description,
            "query": test_case.query,
            "start_time": time.time(),
            "messages": [],
            "success": False,
            "error": None,
            "validation_passed": False,
            "execution_time": 0,
            "generated_cypher": None,
            "result_count": 0
        }
        
        try:
            async with websockets.connect(self.websocket_url) as websocket:
                # Send the query
                await websocket.send(test_case.query)
                logger.debug(f"Sent query: {test_case.query}")
                
                # Collect all messages until connection closes
                while True:
                    try:
                        message = await asyncio.wait_for(websocket.recv(), timeout=30)
                        
                        # Try to parse as JSON first
                        try:
                            data = json.loads(message)
                            result["messages"].append(data)
                            
                            # Extract Cypher query if present
                            if data.get("type") == "query":
                                cypher_match = data.get("message", "")
                                if "**Database Query:**" in cypher_match:
                                    cypher = cypher_match.split("`")[1] if "`" in cypher_match else ""
                                    result["generated_cypher"] = cypher
                                elif "**Fallback Query:**" in cypher_match:
                                    cypher = cypher_match.split("`")[1] if "`" in cypher_match else ""
                                    result["generated_cypher"] = cypher
                                    result["used_fallback"] = True
                            
                            # Track errors
                            if data.get("type") == "error":
                                result["error"] = data.get("message")
                                
                        except json.JSONDecodeError:
                            # Plain text message (final response)
                            result["messages"].append({"type": "response", "content": message})
                            logger.debug("Received final response")
                            
                    except asyncio.TimeoutError:
                        logger.warning("Timeout waiting for response")
                        result["error"] = "Timeout waiting for response"
                        break
                    except websockets.exceptions.ConnectionClosed:
                        logger.debug("Connection closed normally")
                        break
                
                result["execution_time"] = time.time() - result["start_time"]
                
                # Validate results
                result["success"] = result["error"] is None
                if result["success"] and test_case.validation:
                    result["validation_passed"] = test_case.validation(result)
                else:
                    result["validation_passed"] = result["success"]
                
                # Extract result count if available
                for msg in result["messages"]:
                    if isinstance(msg, dict) and msg.get("type") == "results":
                        # Try to count results from markdown table
                        content = msg.get("message", "")
                        if "rows)" in content:
                            try:
                                count_str = content.split("(")[1].split(" rows")[0]
                                result["result_count"] = int(count_str)
                            except:
                                pass
                
        except Exception as e:
            logger.error(f"Test failed with exception: {e}")
            result["error"] = str(e)
            result["execution_time"] = time.time() - result["start_time"]
        
        return result
    
    async def run_all_tests(self, test_cases: List[TestCase]) -> Dict[str, Any]:
        """Run all test cases and generate summary"""
        logger.info(f"Starting test suite with {len(test_cases)} test cases")
        
        results = []
        for test_case in test_cases:
            result = await self.run_single_test(test_case)
            results.append(result)
            
            # Brief pause between tests
            await asyncio.sleep(2)
        
        # Generate summary
        summary = self._generate_summary(results)
        
        # Save detailed results
        self._save_results(results, summary)
        
        return summary
    
    def _generate_summary(self, results: List[Dict]) -> Dict[str, Any]:
        """Generate test summary statistics"""
        total = len(results)
        successful = sum(1 for r in results if r["success"])
        validated = sum(1 for r in results if r["validation_passed"])
        with_errors = sum(1 for r in results if r["error"])
        used_fallback = sum(1 for r in results if r.get("used_fallback", False))
        
        avg_execution_time = sum(r["execution_time"] for r in results) / total if total > 0 else 0
        
        # Group by query type
        by_type = {}
        for result in results:
            test_id = result["test_id"]
            query_type = next((tc.query_type.value for tc in test_cases if tc.id == test_id), "unknown")
            if query_type not in by_type:
                by_type[query_type] = {"total": 0, "successful": 0, "validated": 0}
            by_type[query_type]["total"] += 1
            if result["success"]:
                by_type[query_type]["successful"] += 1
            if result["validation_passed"]:
                by_type[query_type]["validated"] += 1
        
        return {
            "total_tests": total,
            "successful": successful,
            "validated": validated,
            "failed": total - successful,
            "with_errors": with_errors,
            "used_fallback": used_fallback,
            "success_rate": (successful / total * 100) if total > 0 else 0,
            "validation_rate": (validated / total * 100) if total > 0 else 0,
            "avg_execution_time": avg_execution_time,
            "by_query_type": by_type,
            "timestamp": datetime.now().isoformat()
        }
    
    def _save_results(self, results: List[Dict], summary: Dict):
        """Save test results to file"""
        output = {
            "summary": summary,
            "results": results
        }
        
        filename = f'query_test_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(filename, 'w') as f:
            json.dump(output, f, indent=2)
        
        logger.info(f"Test results saved to {filename}")
    
    def validate_database_state(self) -> Dict[str, Any]:
        """Validate that the database is properly seeded"""
        if not self.falkor_client:
            return {"error": "No database connection"}
        
        validations = {}
        
        try:
            # Check node counts
            node_types = ["Person", "Team", "Group", "Policy"]
            for node_type in node_types:
                result = self.db.query(f"MATCH (n:{node_type}) RETURN count(n) as count")
                count = result.result_set[0][0] if result.result_set else 0
                validations[f"{node_type.lower()}_count"] = count
            
            # Check relationships
            rel_queries = [
                ("person_team_memberships", "MATCH (:Person)-[r:MEMBER_OF]->(:Team) RETURN count(r)"),
                ("person_group_memberships", "MATCH (:Person)-[r:MEMBER_OF]->(:Group) RETURN count(r)"),
                ("team_policies", "MATCH (:Team)-[r:RESPONSIBLE_FOR]->(:Policy) RETURN count(r)"),
                ("group_policies", "MATCH (:Group)-[r:RESPONSIBLE_FOR]->(:Policy) RETURN count(r)"),
                ("reporting_relationships", "MATCH (:Person)-[r:REPORTS_TO]->(:Person) RETURN count(r)")
            ]
            
            for name, query in rel_queries:
                result = self.db.query(query)
                count = result.result_set[0][0] if result.result_set else 0
                validations[name] = count
            
            # Check for common data issues
            issues = []
            
            # People without teams
            result = self.db.query("MATCH (p:Person) WHERE NOT (p)-[:MEMBER_OF]->(:Team) RETURN count(p)")
            orphan_people = result.result_set[0][0] if result.result_set else 0
            if orphan_people > 0:
                issues.append(f"{orphan_people} people without team membership")
            
            # Policies without owners
            result = self.db.query("MATCH (p:Policy) WHERE NOT (()-[:RESPONSIBLE_FOR]->(p)) RETURN count(p)")
            orphan_policies = result.result_set[0][0] if result.result_set else 0
            if orphan_policies > 0:
                issues.append(f"{orphan_policies} policies without owners")
            
            validations["issues"] = issues
            validations["healthy"] = len(issues) == 0
            
        except Exception as e:
            validations["error"] = str(e)
            validations["healthy"] = False
        
        return validations


# Define test cases
test_cases = [
    # Basic Entity Queries
    TestCase(
        id="BE001",
        description="Find people by department",
        query="show me people in Engineering",
        query_type=QueryType.BASIC_ENTITY,
        expected_tool="custom_query",
        expected_min_results=10,
        tags=["person", "department"]
    ),
    
    TestCase(
        id="BE002", 
        description="Find specific person",
        query="find John Smith",
        query_type=QueryType.BASIC_ENTITY,
        expected_tool="search_database",
        tags=["person", "name"]
    ),
    
    TestCase(
        id="BE003",
        description="List all teams",
        query="show me all teams",
        query_type=QueryType.BASIC_ENTITY,
        expected_tool="custom_query",
        expected_min_results=20,
        tags=["team"]
    ),
    
    TestCase(
        id="BE004",
        description="Find policies by category",
        query="show security policies",
        query_type=QueryType.BASIC_ENTITY,
        expected_tool="custom_query",
        expected_min_results=3,
        tags=["policy", "security"]
    ),
    
    # Relationship Queries
    TestCase(
        id="REL001",
        description="Team membership query",
        query="who's on the Core Platform team?",
        query_type=QueryType.RELATIONSHIP,
        expected_tool="custom_query",
        expected_min_results=1,
        tags=["team", "membership"]
    ),
    
    TestCase(
        id="REL002",
        description="Manager hierarchy",
        query="who reports to the VP of Engineering",
        query_type=QueryType.RELATIONSHIP,
        expected_tool="custom_query",
        tags=["hierarchy", "manager"]
    ),
    
    TestCase(
        id="REL003",
        description="Policy ownership",
        query="who owns the Code Review Policy?",
        query_type=QueryType.RELATIONSHIP,
        expected_tool="custom_query",
        expected_min_results=1,
        tags=["policy", "ownership"]
    ),
    
    TestCase(
        id="REL004",
        description="Group membership",
        query="who's in the Security Council group?",
        query_type=QueryType.RELATIONSHIP,
        expected_tool="custom_query",
        tags=["group", "membership"]
    ),
    
    # Complex Queries
    TestCase(
        id="CX001",
        description="Multi-condition search",
        query="find senior engineers in the Platform team",
        query_type=QueryType.COMPLEX,
        expected_tool="custom_query",
        tags=["complex", "filter"]
    ),
    
    TestCase(
        id="CX002",
        description="Cross-functional query",
        query="show me people who are in both Engineering teams and Security groups",
        query_type=QueryType.COMPLEX,
        expected_tool="custom_query",
        tags=["complex", "cross-functional"]
    ),
    
    TestCase(
        id="CX003",
        description="Task-oriented query",
        query="I need to implement a new security feature, what policies apply?",
        query_type=QueryType.COMPLEX,
        expected_tool="custom_query",
        tags=["task", "policy"]
    ),
    
    # Aggregation Queries
    TestCase(
        id="AGG001",
        description="Count by department",
        query="how many people in each department?",
        query_type=QueryType.AGGREGATION,
        expected_tool="custom_query",
        expected_min_results=5,
        tags=["aggregation", "count"]
    ),
    
    TestCase(
        id="AGG002",
        description="Team size analysis",
        query="what's the size of each team?",
        query_type=QueryType.AGGREGATION,
        expected_tool="custom_query",
        tags=["aggregation", "team"]
    ),
    
    # Edge Cases
    TestCase(
        id="EDGE001",
        description="No results expected",
        query="find people named Zzyzx",
        query_type=QueryType.EDGE_CASE,
        expected_tool="custom_query",
        should_trigger_fallback=True,
        expected_max_results=0,
        tags=["edge", "no-results"]
    ),
    
    TestCase(
        id="EDGE002",
        description="Typo in query",
        query="show me the Enginerring team",
        query_type=QueryType.EDGE_CASE,
        expected_tool="custom_query",
        tags=["edge", "typo"]
    ),
    
    TestCase(
        id="EDGE003",
        description="Ambiguous query",
        query="security",
        query_type=QueryType.EDGE_CASE,
        expected_tool="search_database",
        tags=["edge", "ambiguous"]
    ),
    
    TestCase(
        id="EDGE004",
        description="Natural language variation",
        query="who's the boss of the Platform team?",
        query_type=QueryType.EDGE_CASE,
        expected_tool="custom_query",
        tags=["edge", "natural-language"]
    ),
    
    # Fallback Queries
    TestCase(
        id="FB001",
        description="Overly specific query",
        query="find Senior Staff Principal Engineers in Underwater Basketweaving",
        query_type=QueryType.FALLBACK,
        expected_tool="custom_query",
        should_trigger_fallback=True,
        tags=["fallback"]
    ),
    
    # Conversational Queries
    TestCase(
        id="CONV001",
        description="Casual greeting",
        query="hello there!",
        query_type=QueryType.EDGE_CASE,
        expected_tool="pig_latin",
        tags=["conversation"]
    )
]


async def main():
    """Main test execution"""
    logger.info("Starting Cypher Query System Test Suite")
    
    # Initialize test runner
    runner = QueryTestRunner()
    
    # Validate database state first
    logger.info("Validating database state...")
    db_state = runner.validate_database_state()
    logger.info(f"Database validation: {json.dumps(db_state, indent=2)}")
    
    if not db_state.get("healthy", False):
        logger.warning("Database has issues, but continuing with tests...")
    
    # Run all tests
    summary = await runner.run_all_tests(test_cases)
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Total Tests: {summary['total_tests']}")
    print(f"Successful: {summary['successful']} ({summary['success_rate']:.1f}%)")
    print(f"Validated: {summary['validated']} ({summary['validation_rate']:.1f}%)")
    print(f"Failed: {summary['failed']}")
    print(f"Used Fallback: {summary['used_fallback']}")
    print(f"Average Execution Time: {summary['avg_execution_time']:.2f}s")
    
    print("\nResults by Query Type:")
    for query_type, stats in summary['by_query_type'].items():
        print(f"  {query_type}: {stats['successful']}/{stats['total']} successful, "
              f"{stats['validated']}/{stats['total']} validated")
    
    print("\nDetailed results saved to JSON file")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(main())