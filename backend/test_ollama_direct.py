#!/usr/bin/env python3
"""
Test the Ollama model directly with the analyze_message.txt template
to diagnose if it's returning valid JSON.
"""

import json
import httpx
from jinja2 import Template
import os
import sys
import asyncio

async def test_ollama_response():
    # Read the template
    template_path = "/app/prompts/analyze_message.txt"
    with open(template_path, 'r') as f:
        template_content = f.read()
    
    template = Template(template_content)
    
    # Prepare test data
    test_query = "Who manages the data team?"
    
    # Mock context data (simplified version)
    context = {
        "user_message": test_query,
        "intent_context": {
            "primary_intent": "information_gathering",
            "actual_goal": "find out who manages or leads the data team",
            "information_depth": "specific",
            "urgency": "normal",
            "complexity": "simple",
            "domain": "organizational",
            "confidence": 0.9,
            "suggested_approach": "Use custom_query to find the data team and its leadership"
        },
        "database_context": {
            "people_count": 100,
            "sample_departments": ["Engineering", "Sales", "HR", "Finance", "Data"],
            "teams_count": 20,
            "sample_teams": [
                {"name": "Data Analytics", "department": "Data"},
                {"name": "Backend", "department": "Engineering"}
            ],
            "groups_count": 10,
            "sample_groups": [
                {"name": "Tech Council", "type": "technical"}
            ],
            "policies_count": 50
        }
    }
    
    # Render the prompt
    prompt = template.render(**context)
    
    print("=" * 80)
    print("RENDERED PROMPT (first 500 chars):")
    print("=" * 80)
    print(prompt[:500] + "...")
    print("=" * 80)
    
    # Call Ollama API
    ollama_host = os.getenv("OLLAMA_HOST", "http://ollama:11434")
    ollama_model = os.getenv("OLLAMA_MODEL", "phi4:14b")
    
    payload = {
        "model": ollama_model,
        "prompt": prompt,
        "stream": False,
        "temperature": 0.1,
        "options": {
            "num_predict": 500
        }
    }
    
    print(f"\nCalling Ollama at {ollama_host} with model {ollama_model}...")
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(
                f"{ollama_host}/api/generate",
                json=payload
            )
            response.raise_for_status()
            
            result = response.json()
            
            print("\n" + "=" * 80)
            print("RAW OLLAMA RESPONSE KEYS:")
            print("=" * 80)
            print("Keys in response:", list(result.keys()))
            
            if "response" in result:
                ai_response = result["response"]
                print("\n" + "=" * 80)
                print("AI MODEL OUTPUT:")
                print("=" * 80)
                print(ai_response)
                print("=" * 80)
                
                # Try to parse as JSON
                try:
                    parsed_json = json.loads(ai_response)
                    print("\n✅ VALID JSON RESPONSE:")
                    print(json.dumps(parsed_json, indent=2))
                    
                    # Verify expected fields
                    if all(key in parsed_json for key in ["reasoning", "tools", "response_type"]):
                        print("\n✅ All required fields present!")
                    else:
                        print("\n❌ Missing required fields!")
                        print("Expected: reasoning, tools, response_type")
                        print("Got:", list(parsed_json.keys()))
                        
                except json.JSONDecodeError as e:
                    print(f"\n❌ INVALID JSON! Error: {e}")
                    print("First 200 chars:", ai_response[:200])
                    
                    # Check for common issues
                    if ai_response.strip().startswith("```"):
                        print("\n⚠️  Response starts with markdown code blocks")
                    if "I" in ai_response[:50] or "You" in ai_response[:50]:
                        print("\n⚠️  Response appears to be conversational instead of JSON")
                    if ai_response.strip().startswith("{") and not ai_response.strip().endswith("}"):
                        print("\n⚠️  Response starts with { but doesn't end with } - might be truncated")
                        
        except Exception as e:
            print(f"\n❌ ERROR calling Ollama: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(asyncio.run(test_ollama_response()))