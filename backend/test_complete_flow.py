#!/usr/bin/env python3
"""
Test complete flow from user message to final response
"""

import json
import httpx
import os
import asyncio
import sys
from pathlib import Path
from jinja2 import Template

# Add backend to path
sys.path.append("/app")

async def simulate_websocket_flow(user_message: str):
    """Simulate the complete WebSocket message handling flow"""
    
    print(f"\nSimulating flow for: '{user_message}'")
    print("=" * 80)
    
    ollama_host = os.getenv("OLLAMA_HOST", "http://ollama:11434")
    ollama_model = os.getenv("OLLAMA_MODEL", "phi4:14b")
    
    # Step 1: Load analyze_message template
    analyze_template_path = "/app/prompts/analyze_message.txt"
    with open(analyze_template_path, 'r') as f:
        analyze_template = Template(f.read())
    
    # Mock database context
    db_context = {
        "people_count": 100,
        "sample_departments": ["Engineering", "Sales", "Data"],
        "teams_count": 20,
        "sample_teams": [
            {"name": "Data Analytics", "department": "Data"},
            {"name": "Backend", "department": "Engineering"}
        ],
        "groups_count": 10,
        "sample_groups": [{"name": "Tech Council", "type": "technical"}],
        "policies_count": 50
    }
    
    # Mock intent context
    intent_context = {
        "primary_intent": "information_gathering",
        "actual_goal": "find out who manages the data team",
        "information_depth": "specific",
        "urgency": "normal",
        "complexity": "simple",
        "domain": "organizational",
        "confidence": 0.9,
        "suggested_approach": "Use custom_query"
    }
    
    # Render analyze prompt
    analyze_prompt = analyze_template.render(
        user_message=user_message,
        database_context=db_context,
        intent_context=intent_context
    )
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Step 2: Call Ollama for analysis
        print("\n1. ANALYSIS PHASE:")
        payload = {
            "model": ollama_model,
            "prompt": analyze_prompt,
            "stream": False,
            "temperature": 0.1,
            "options": {"num_predict": 500}
        }
        
        response = await client.post(f"{ollama_host}/api/generate", json=payload)
        response.raise_for_status()
        
        ai_response = response.json().get("response", "")
        print(f"Raw analysis response: {ai_response[:200]}...")
        
        # Extract JSON
        if "```json" in ai_response:
            start = ai_response.find("```json") + 7
            end = ai_response.find("```", start)
            if end > start:
                ai_response = ai_response[start:end].strip()
        
        analysis = json.loads(ai_response)
        print(f"Tools selected: {analysis.get('tools', [])}")
        print(f"Response type: {analysis.get('response_type', 'unknown')}")
        
        # Step 3: If custom_query selected, generate query
        if "custom_query" in analysis.get("tools", []):
            print("\n2. QUERY GENERATION PHASE:")
            
            generate_template_path = "/app/prompts/generate_query.txt"
            with open(generate_template_path, 'r') as f:
                generate_template = Template(f.read())
            
            generate_prompt = generate_template.render(
                user_message=user_message,
                database_context=db_context,
                intent_context=intent_context
            )
            
            payload["prompt"] = generate_prompt
            response = await client.post(f"{ollama_host}/api/generate", json=payload)
            response.raise_for_status()
            
            query_response = response.json().get("response", "")
            print(f"Generated query: {query_response}")
            
            # Step 4: Simulate empty results
            print("\n3. SIMULATING EMPTY RESULTS:")
            empty_results = {
                "query": query_response.strip(),
                "count": 0,
                "results": []
            }
            
            # Step 5: Format empty results
            print("\n4. FORMATTING PHASE:")
            format_template_path = "/app/prompts/format_results.txt"
            with open(format_template_path, 'r') as f:
                format_template = Template(f.read())
            
            format_prompt = format_template.render(
                user_message=user_message,
                results=empty_results,
                intent_context=intent_context
            )
            
            payload["prompt"] = format_prompt
            response = await client.post(f"{ollama_host}/api/generate", json=payload)
            response.raise_for_status()
            
            final_response = response.json().get("response", "")
            
            print("\nFINAL RESPONSE TO USER:")
            print("-" * 40)
            print(final_response)
            print("-" * 40)
            
            # Check response quality
            if len(final_response.strip()) < 20:
                print("\n❌ ISSUE: Very short response!")
            if final_response.strip() == "":
                print("\n❌ ISSUE: Empty response!")
            if "```" in final_response and len(final_response) < 100:
                print("\n❌ ISSUE: Response might be code block only!")
            if "no" in final_response.lower() and ("found" in final_response.lower() or "results" in final_response.lower()):
                print("\n✅ Good: Correctly indicates no results")

# Test various queries
test_queries = [
    "Who manages the data team?",
    "Find all GDPR compliance policies",
    "Show me the engineering team leads",
    "hello",
    "What are the security policies?"
]

async def main():
    for query in test_queries:
        try:
            await simulate_websocket_flow(query)
        except Exception as e:
            print(f"\n❌ ERROR processing '{query}': {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())