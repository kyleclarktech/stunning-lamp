#!/usr/bin/env python3
"""
Quick test of improvements with granite3.3:8b-largectx model
Focused on measuring the improvement from baseline 70.4%
"""

import asyncio
import json
import time
import sys
import os
from datetime import datetime
import httpx

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import load_prompt, clean_ai_generated_query, get_falkor_client
from query_processor import process_query
from query_validator import validate_query

# Test queries that commonly fail
TEST_QUERIES = [
    # Function name issues
    "Find people whose names start with 'john' (case insensitive)",
    "Show employees with lowercase role containing 'engineer'",
    "List teams where the department name in uppercase is 'ENGINEERING'",
    
    # Multiple statement issues
    "List all employees; show their departments",
    "Find all teams in engineering; count them",
    
    # Aggregation in WHERE issues
    "Show teams where count of members is greater than 10",
    "Find departments where average salary is above 100000",
    
    # Date function issues
    "Show policies updated this year",
    "Find employees hired in the last month",
    
    # Basic queries that should work
    "List all employees",
    "Who manages the data team?",
    "Show security policies",
    "How many developers are there?",
    "Find people with Python skills",
    "Who reports to Sarah Chen?",
    "Find employees in London",
    "Show all compliance policies",
    "Find senior engineers",
    "List all projects"
]

async def call_model(prompt_text: str, timeout: int = 30) -> str:
    """Call granite model with the prompt."""
    url = os.getenv("OLLAMA_HOST", "http://ollama:11434") + "/api/generate"
    
    async with httpx.AsyncClient(timeout=timeout) as client:
        payload = {
            "model": "granite3.3:8b-largectx",
            "prompt": prompt_text,
            "stream": False
        }
        
        resp = await client.post(url, json=payload)
        
        if resp.status_code != 200:
            raise Exception(f"Model returned status {resp.status_code}")
        
        data = resp.json()
        return data.get('response', '')

async def test_query(query_text: str) -> dict:
    """Test a single query with improvements."""
    result = {
        "query": query_text,
        "success": False,
        "improvements_applied": [],
        "error": None,
        "execution_time": 0
    }
    
    try:
        # Generate query
        prompt = load_prompt("generate_query_simple", user_message=query_text)
        prompt += f"\n\nQuestion: \"{query_text}\"\nQuery:"
        
        raw_response = await call_model(prompt)
        generated_query = clean_ai_generated_query(raw_response)
        result["generated_query"] = generated_query
        
        # Apply post-processing
        processed_query = process_query(generated_query)
        result["processed_query"] = processed_query
        
        if generated_query != processed_query:
            result["improvements_applied"].append("post-processing")
        
        # Validate
        is_valid, errors, warnings = validate_query(processed_query)
        result["validation"] = {"valid": is_valid, "errors": errors[:2] if errors else []}
        
        # Execute
        start_time = time.time()
        falkor = get_falkor_client()
        db = falkor.select_graph("agent_poc")
        query_result = db.query(processed_query)
        result["execution_time"] = time.time() - start_time
        
        result["success"] = True
        result["has_results"] = bool(query_result.result_set)
        
    except Exception as e:
        result["error"] = str(e)
        
        # Check if it's a function error we can retry
        if 'unknown function' in str(e).lower():
            result["improvements_applied"].append("function_error_detected")
    
    return result

async def main():
    """Run focused test of improvements."""
    print("TESTING QUERY GENERATION IMPROVEMENTS")
    print("Model: granite3.3:8b-largectx (baseline 70.4%)")
    print("=" * 60)
    
    results = []
    successful = 0
    improvements_used = 0
    
    for i, query in enumerate(TEST_QUERIES, 1):
        print(f"\n[{i}/{len(TEST_QUERIES)}] {query}")
        
        result = await test_query(query)
        results.append(result)
        
        if result["success"]:
            successful += 1
            print(f"  ✓ SUCCESS")
        else:
            print(f"  ✗ FAILED: {result['error']}")
        
        if result.get("improvements_applied"):
            improvements_used += 1
            print(f"  🔧 Improvements: {', '.join(result['improvements_applied'])}")
        
        if result.get("validation", {}).get("errors"):
            print(f"  ⚠️  Validation: {', '.join(result['validation']['errors'])}")
    
    # Summary
    success_rate = (successful / len(TEST_QUERIES)) * 100
    print("\n" + "=" * 60)
    print("RESULTS SUMMARY")
    print("=" * 60)
    print(f"Total queries: {len(TEST_QUERIES)}")
    print(f"Successful: {successful} ({success_rate:.1f}%)")
    print(f"Failed: {len(TEST_QUERIES) - successful}")
    print(f"Queries improved by post-processing: {improvements_used}")
    
    print(f"\nBASELINE: 70.4%")
    print(f"CURRENT: {success_rate:.1f}%")
    print(f"IMPROVEMENT: {success_rate - 70.4:+.1f} percentage points")
    
    # Analyze failures
    print("\nFAILURE ANALYSIS:")
    for r in results:
        if not r["success"]:
            print(f"- {r['query'][:50]}...")
            print(f"  Error: {r['error'][:100]}...")
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"granite_improvement_test_{timestamp}.json"
    with open(filename, 'w') as f:
        json.dump({
            "timestamp": timestamp,
            "model": "granite3.3:8b-largectx",
            "success_rate": success_rate,
            "baseline_rate": 70.4,
            "improvement": success_rate - 70.4,
            "results": results
        }, f, indent=2)
    
    print(f"\n📊 Detailed results saved to: {filename}")

if __name__ == "__main__":
    asyncio.run(main())