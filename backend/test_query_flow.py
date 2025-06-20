#!/usr/bin/env python3
"""Test the complete query flow from websocket to results"""

import asyncio
import json
import logging
from main import (
    get_database_context,
    load_prompt,
    call_ai_model,
    execute_tools,
    execute_custom_query
)

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

async def test_query_flow():
    """Test the complete query flow"""
    test_query = "how many people in engineering?"
    
    print(f"\n=== Testing query: '{test_query}' ===\n")
    
    try:
        # 1. Get database context
        print("1. Getting database context...")
        db_context = await get_database_context()
        print(f"   Found {db_context['people_count']} people, {db_context['teams_count']} teams\n")
        
        # 2. Analyze message
        print("2. Analyzing message...")
        prompt = load_prompt("analyze_message", user_message=test_query, database_context=db_context)
        ai_response = await call_ai_model(prompt, websocket=None)
        
        # Parse AI response
        response_text = ai_response.strip()
        if "```json" in response_text:
            start = response_text.find("```json") + 7
            end = response_text.find("```", start)
            if end > start:
                response_text = response_text[start:end].strip()
        
        analysis = json.loads(response_text)
        print(f"   AI Analysis: {json.dumps(analysis, indent=2)}\n")
        
        # 3. Execute tools
        print("3. Executing recommended tools...")
        tools_to_execute = analysis.get("tools", [])
        results = await execute_tools(tools_to_execute, test_query, websocket=None)
        
        # 4. Display results
        print("\n=== RESULTS ===")
        if "custom_query" in tools_to_execute:
            custom_results = results.get("custom_results", {})
            print(f"Query: {custom_results.get('query', 'N/A')}")
            print(f"Results: {custom_results.get('results', [])}")
            print(f"Count: {custom_results.get('count', 0)}")
        else:
            print(json.dumps(results, indent=2))
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_query_flow())