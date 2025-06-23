#!/usr/bin/env python3
"""
Simple test to check if Ollama is returning meaningful responses
"""

import json
import httpx
import os
import asyncio
from pathlib import Path
from jinja2 import Template

async def test_simple_ollama():
    # Test 1: Simple direct prompt
    print("TEST 1: Direct simple prompt")
    print("=" * 80)
    
    ollama_host = os.getenv("OLLAMA_HOST", "http://ollama:11434")
    ollama_model = os.getenv("OLLAMA_MODEL", "phi4:14b")
    
    simple_prompt = "Who manages the data team? Respond with a brief answer."
    
    payload = {
        "model": ollama_model,
        "prompt": simple_prompt,
        "stream": False,
        "temperature": 0.1,
        "options": {
            "num_predict": 200
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
            
            print(f"Response: {result.get('response', 'NO RESPONSE')}")
            print(f"Done: {result.get('done', False)}")
            print(f"Model: {result.get('model', 'UNKNOWN')}")
            
        except Exception as e:
            print(f"ERROR: {e}")
    
    # Test 2: JSON instruction prompt
    print("\n\nTEST 2: JSON instruction prompt")
    print("=" * 80)
    
    json_prompt = '''Respond with ONLY a valid JSON object, no other text. The JSON must contain:
- "answer": Your answer to the question
- "confidence": A number between 0 and 1

Question: Who manages the data team?'''
    
    payload["prompt"] = json_prompt
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(
                f"{ollama_host}/api/generate",
                json=payload
            )
            response.raise_for_status()
            result = response.json()
            
            ai_response = result.get('response', 'NO RESPONSE')
            print(f"Raw response: {ai_response}")
            
            # Try to parse as JSON
            try:
                parsed = json.loads(ai_response.strip())
                print(f"✅ Valid JSON: {parsed}")
            except:
                print("❌ Not valid JSON")
                # Check for markdown blocks
                if "```" in ai_response:
                    print("Contains markdown code blocks")
                
        except Exception as e:
            print(f"ERROR: {e}")
    
    # Test 3: Check if model is loaded
    print("\n\nTEST 3: Check model status")
    print("=" * 80)
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            # Check loaded models
            response = await client.get(f"{ollama_host}/api/tags")
            response.raise_for_status()
            models = response.json()
            
            print("Available models:")
            for model in models.get("models", []):
                print(f"- {model.get('name', 'unknown')} (size: {model.get('size', 'unknown')})")
                
            # Check if our model is loaded
            our_model_loaded = any(m.get('name', '').startswith(ollama_model.split(':')[0]) 
                                 for m in models.get("models", []))
            print(f"\n{ollama_model} loaded: {'✅ YES' if our_model_loaded else '❌ NO'}")
            
        except Exception as e:
            print(f"ERROR checking models: {e}")

if __name__ == "__main__":
    asyncio.run(test_simple_ollama())