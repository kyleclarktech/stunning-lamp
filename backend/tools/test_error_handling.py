#!/usr/bin/env python3
"""Test error handling and fallback mechanisms."""

import asyncio
import json
import sys
import os
from typing import Dict, List, Any

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import execute_custom_query, clean_ai_generated_query, call_ai_model, load_prompt
from error_handler import handle_query_error

# Test cases for error handling
TEST_CASES = [
    {
        "name": "Syntax Error - Invalid Property",
        "query": "MATCH (p:Person) WHERE p.invalid_property = 'test' RETURN p",
        "expected_error": "Property",
        "description": "Tests handling of non-existent properties"
    },
    {
        "name": "Syntax Error - Invalid Relationship",
        "query": "MATCH (p:Person)-[:INVALID_REL]->(t:Team) RETURN p",
        "expected_error": "relationship",
        "description": "Tests handling of non-existent relationships"
    },
    {
        "name": "No Results - Very Specific Query",
        "query": "MATCH (p:Person {name: 'NonExistentPerson12345'}) RETURN p",
        "expected_error": "No results",
        "description": "Tests fallback query generation"
    },
    {
        "name": "Ambiguous Natural Language",
        "natural_language": "Find the xyz123 quantum department",
        "expected_behavior": "fallback",
        "description": "Tests handling of nonsensical queries"
    },
    {
        "name": "Timeout Simulation",
        "query": "MATCH (p1:Person)-[:REPORTS_TO*1..10]->(p2:Person) RETURN p1, p2",
        "expected_behavior": "possible timeout",
        "description": "Tests timeout handling with complex query"
    }
]

async def test_direct_query_error(query: str, test_name: str) -> Dict[str, Any]:
    """Test direct query execution with error handling."""
    print(f"\nTesting: {test_name}")
    print(f"Query: {query}")
    
    result = {
        "test": test_name,
        "query": query,
        "error_handled": False,
        "fallback_attempted": False,
        "error_message": None,
        "suggestions": []
    }
    
    try:
        # Direct execution to trigger errors
        from main import get_falkor_client
        falkor = get_falkor_client()
        db = falkor.select_graph("agent_poc")
        db_result = db.query(query)
        
        result["success"] = True
        result["result_count"] = len(db_result.result_set)
        print(f"  ✓ Query succeeded with {result['result_count']} results")
        
    except Exception as e:
        # Test error handler
        error_response = handle_query_error(e, f"Test query: {query}", query)
        
        result["error_handled"] = True
        result["error_message"] = error_response["message"]
        result["suggestions"] = error_response.get("help", {}).get("suggestions", [])
        result["alternative_queries"] = error_response.get("help", {}).get("alternative_queries", [])
        
        print(f"  ✗ Error: {error_response['message']}")
        if result["suggestions"]:
            print(f"  Suggestions: {result['suggestions']}")
        if result["alternative_queries"]:
            print(f"  Alternatives: {result['alternative_queries']}")
    
    return result

async def test_natural_language_query(nl_query: str, test_name: str) -> Dict[str, Any]:
    """Test natural language query with error handling and fallback."""
    print(f"\nTesting: {test_name}")
    print(f"Natural Language: {nl_query}")
    
    result = {
        "test": test_name,
        "natural_language": nl_query,
        "generated_query": None,
        "fallback_used": False,
        "error_handled": False
    }
    
    try:
        # Generate Cypher query
        prompt = load_prompt("generate_query_simple", user_message=nl_query)
        prompt += f"\n\nQuestion: \"{nl_query}\"\nQuery:"
        
        cypher_query = await call_ai_model(prompt, timeout=30)
        cypher_query = clean_ai_generated_query(cypher_query)
        
        result["generated_query"] = cypher_query
        print(f"  Generated Query: {cypher_query[:80]}...")
        
        # Try to execute
        from main import get_falkor_client
        falkor = get_falkor_client()
        db = falkor.select_graph("agent_poc")
        
        try:
            db_result = db.query(cypher_query)
            result["success"] = True
            result["result_count"] = len(db_result.result_set)
            print(f"  ✓ Query succeeded with {result['result_count']} results")
            
            # If no results, test fallback
            if result["result_count"] == 0:
                print("  → No results, testing fallback mechanism...")
                
                # Generate fallback query
                fallback_prompt = load_prompt("fallback_query", 
                                            user_message=nl_query, 
                                            previous_query=cypher_query)
                fallback_query = await call_ai_model(fallback_prompt, timeout=30)
                fallback_query = clean_ai_generated_query(fallback_query)
                
                result["fallback_query"] = fallback_query
                result["fallback_used"] = True
                print(f"  Fallback Query: {fallback_query[:80]}...")
                
                # Execute fallback
                fallback_result = db.query(fallback_query)
                result["fallback_result_count"] = len(fallback_result.result_set)
                print(f"  Fallback Results: {result['fallback_result_count']}")
                
        except Exception as e:
            # Test error handler
            error_response = handle_query_error(e, nl_query, cypher_query)
            result["error_handled"] = True
            result["error_message"] = error_response["message"]
            print(f"  ✗ Error: {error_response['message']}")
            
    except Exception as e:
        result["generation_error"] = str(e)
        print(f"  ✗ Query generation failed: {str(e)}")
    
    return result

async def test_timeout_handling() -> Dict[str, Any]:
    """Test timeout handling mechanism."""
    print("\nTesting: Timeout Handling")
    
    result = {
        "test": "Timeout Handling",
        "timeout_triggered": False,
        "error_message": None
    }
    
    # Create a query that might timeout
    complex_query = """
    MATCH path = (p1:Person)-[:REPORTS_TO*1..5]->(p2:Person)
    WHERE p1.department <> p2.department
    WITH path, length(path) as pathLength
    ORDER BY pathLength DESC
    LIMIT 1000
    RETURN path, pathLength
    """
    
    print(f"  Testing with complex query that might timeout...")
    
    try:
        # Use a very short timeout to force timeout
        import asyncio
        from main import get_falkor_client
        
        def execute_query():
            falkor = get_falkor_client()
            db = falkor.select_graph("agent_poc")
            return db.query(complex_query)
        
        # Test with 1 second timeout
        await asyncio.wait_for(
            asyncio.get_event_loop().run_in_executor(None, execute_query),
            timeout=1
        )
        
        result["success"] = True
        print("  ✓ Query completed within timeout")
        
    except asyncio.TimeoutError:
        result["timeout_triggered"] = True
        result["error_message"] = "Query timeout after 1 second"
        print("  ✓ Timeout correctly triggered")
        
        # Test error handler for timeout
        error_response = handle_query_error(
            Exception("timeout"), 
            "Complex organizational query", 
            complex_query
        )
        result["timeout_handled"] = True
        result["handler_message"] = error_response["message"]
        print(f"  Handler message: {error_response['message']}")
        
    except Exception as e:
        result["other_error"] = str(e)
        print(f"  ✗ Unexpected error: {str(e)}")
    
    return result

async def main():
    """Run all error handling tests."""
    print("Error Handling and Fallback Test Suite")
    print("=" * 60)
    
    all_results = []
    
    # Test direct query errors
    for test_case in TEST_CASES[:3]:  # First 3 are direct queries
        if "query" in test_case:
            result = await test_direct_query_error(
                test_case["query"], 
                test_case["name"]
            )
            all_results.append(result)
    
    # Test natural language queries
    nl_test = TEST_CASES[3]
    if "natural_language" in nl_test:
        result = await test_natural_language_query(
            nl_test["natural_language"],
            nl_test["name"]
        )
        all_results.append(result)
    
    # Test timeout handling
    timeout_result = await test_timeout_handling()
    all_results.append(timeout_result)
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    error_handled_count = sum(1 for r in all_results if r.get("error_handled", False))
    fallback_used_count = sum(1 for r in all_results if r.get("fallback_used", False))
    timeout_handled_count = sum(1 for r in all_results if r.get("timeout_triggered", False))
    
    print(f"\nTests run: {len(all_results)}")
    print(f"Errors properly handled: {error_handled_count}")
    print(f"Fallback queries used: {fallback_used_count}")
    print(f"Timeouts handled: {timeout_handled_count}")
    
    # Save results
    import json
    from datetime import datetime
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    results_file = f"error_handling_test_{timestamp}.json"
    
    with open(results_file, 'w') as f:
        json.dump({
            'timestamp': timestamp,
            'results': all_results,
            'summary': {
                'total_tests': len(all_results),
                'errors_handled': error_handled_count,
                'fallbacks_used': fallback_used_count,
                'timeouts_handled': timeout_handled_count
            }
        }, f, indent=2)
    
    print(f"\nResults saved to: {results_file}")

if __name__ == "__main__":
    asyncio.run(main())