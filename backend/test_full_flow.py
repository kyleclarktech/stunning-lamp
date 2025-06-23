#!/usr/bin/env python3
"""
Test the full flow of message processing to diagnose where "meaningless responses" come from
"""

import json
import httpx
from jinja2 import Template
import os
import sys
import asyncio
from pathlib import Path

# Add the backend directory to the path
sys.path.append("/app")

from main import load_prompt, get_database_context
from intent_processor import IntentProcessor

async def test_full_flow():
    test_query = "Who manages the data team?"
    print(f"Testing query: '{test_query}'")
    print("=" * 80)
    
    # Step 1: Intent Processing
    print("\n1. INTENT PROCESSING:")
    intent_processor = IntentProcessor()
    user_intent = await intent_processor.analyze_intent(test_query)
    print(f"Intent: {user_intent.primary_intent}")
    print(f"Confidence: {user_intent.confidence}")
    print(f"Actual goal: {user_intent.actual_goal}")
    
    # Step 2: Database Context
    print("\n2. DATABASE CONTEXT:")
    db_context = await get_database_context()
    print(f"People count: {db_context['people_count']}")
    print(f"Teams count: {db_context['teams_count']}")
    
    # Step 3: Analyze Message
    print("\n3. ANALYZE MESSAGE PROMPT:")
    prompt = load_prompt("analyze_message", 
                        user_message=test_query, 
                        database_context=db_context,
                        intent_context=user_intent.to_context_dict())
    print(f"Prompt length: {len(prompt)} chars")
    print("First 300 chars of prompt:")
    print(prompt[:300] + "...")
    
    # Step 4: Call Ollama
    print("\n4. CALLING OLLAMA:")
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
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(
                f"{ollama_host}/api/generate",
                json=payload
            )
            response.raise_for_status()
            result = response.json()
            ai_response = result.get("response", "")
            
            print("AI Response (raw):")
            print(ai_response[:500] + "..." if len(ai_response) > 500 else ai_response)
            
            # Step 5: Parse Response
            print("\n5. PARSING RESPONSE:")
            response_text = ai_response.strip()
            
            # Look for JSON in markdown code blocks
            if "```json" in response_text:
                start = response_text.find("```json") + 7
                end = response_text.find("```", start)
                if end > start:
                    response_text = response_text[start:end].strip()
                    print("Extracted from ```json block")
            
            analysis = json.loads(response_text)
            print("✅ Successfully parsed JSON!")
            print(f"Tools: {analysis.get('tools', [])}")
            print(f"Response type: {analysis.get('response_type', 'unknown')}")
            
            # Step 6: Check if custom_query is selected
            if "custom_query" in analysis.get("tools", []):
                print("\n6. CUSTOM QUERY GENERATION:")
                print("Would proceed to generate Cypher query...")
                
                # Test query generation prompt
                generate_prompt = load_prompt("generate_query",
                                            user_message=test_query,
                                            database_context=db_context,
                                            intent_context=user_intent.to_context_dict())
                
                print(f"Generate query prompt length: {len(generate_prompt)} chars")
                
                # Call Ollama for query generation
                payload["prompt"] = generate_prompt
                response = await client.post(
                    f"{ollama_host}/api/generate",
                    json=payload
                )
                response.raise_for_status()
                result = response.json()
                query_response = result.get("response", "")
                
                print("\nGenerated Cypher query:")
                print(query_response[:500] + "..." if len(query_response) > 500 else query_response)
                
        except Exception as e:
            print(f"❌ ERROR: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_full_flow())