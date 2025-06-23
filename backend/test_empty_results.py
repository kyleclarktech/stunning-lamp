#!/usr/bin/env python3
"""
Test what happens when format_results is called with empty results
"""

import json
import httpx
from jinja2 import Template
import os
import asyncio

async def test_empty_results_formatting():
    # Load the format_results template
    template_path = "/app/prompts/format_results.txt"
    with open(template_path, 'r') as f:
        template_content = f.read()
    
    template = Template(template_content)
    
    # Test with empty results
    test_cases = [
        {
            "name": "Empty search results",
            "user_message": "Who manages the data team?",
            "results": {"people": [], "teams": [], "groups": [], "policies": [], "error": None},
            "intent_context": {
                "actual_goal": "find out who manages the data team",
                "primary_intent": "information_gathering",
                "information_depth": "specific"
            }
        },
        {
            "name": "Empty custom query results",
            "user_message": "Find all compliance policies for GDPR",
            "results": {
                "query": "MATCH (p:Policy) WHERE p.name CONTAINS 'GDPR' RETURN p",
                "count": 0,
                "results": []
            },
            "intent_context": {
                "actual_goal": "find GDPR compliance policies",
                "primary_intent": "task_completion",
                "information_depth": "detailed_explanation"
            }
        }
    ]
    
    ollama_host = os.getenv("OLLAMA_HOST", "http://ollama:11434")
    ollama_model = os.getenv("OLLAMA_MODEL", "phi4:14b")
    
    for test in test_cases:
        print(f"\n{'='*80}")
        print(f"TEST: {test['name']}")
        print(f"User message: {test['user_message']}")
        print(f"Results: {json.dumps(test['results'], indent=2)}")
        print("="*80)
        
        # Render the prompt
        prompt = template.render(
            user_message=test['user_message'],
            results=test['results'],
            intent_context=test['intent_context']
        )
        
        # Call Ollama
        payload = {
            "model": ollama_model,
            "prompt": prompt,
            "stream": False,
            "temperature": 0.1,
            "options": {
                "num_predict": 300
            }
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(
                    f"{ollama_host}/api/generate",
                    json=payload
                )
                response.raise_for_status()
                result = response.json()
                
                ai_response = result.get('response', 'NO RESPONSE')
                print("\nAI RESPONSE:")
                print("-" * 40)
                print(ai_response)
                print("-" * 40)
                
                # Check if response is meaningful
                if len(ai_response.strip()) < 20:
                    print("⚠️  VERY SHORT RESPONSE")
                if "no" in ai_response.lower() and "found" in ai_response.lower():
                    print("✅ Correctly states no results found")
                if "i can" in ai_response.lower() or "i'll" in ai_response.lower():
                    print("⚠️  Response seems conversational/unhelpful")
                if ai_response.strip() == "":
                    print("❌ EMPTY RESPONSE!")
                    
            except Exception as e:
                print(f"ERROR: {e}")

if __name__ == "__main__":
    asyncio.run(test_empty_results_formatting())