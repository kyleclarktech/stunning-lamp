#!/usr/bin/env python3
"""Test a single additional model - qwen2.5-coder:7b"""

import asyncio
import json
import time
import sys
import os
from typing import Dict, List, Any
from datetime import datetime
import httpx

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import load_prompt, clean_ai_generated_query

# Test queries
TEST_QUERIES = [
    "Who manages the data team?",
    "List all compliance policies", 
    "Find people with Python skills",
]

async def pull_model(model_name: str) -> bool:
    """Pull a model if not available."""
    print(f"Pulling model {model_name}...")
    try:
        async with httpx.AsyncClient(timeout=1200) as client:
            # Use streaming to show progress
            async with client.stream(
                "POST",
                "http://ollama:11434/api/pull",
                json={"name": model_name}
            ) as response:
                async for line in response.aiter_lines():
                    if line:
                        try:
                            data = json.loads(line)
                            status = data.get('status', '')
                            if 'pulling' in status or 'downloading' in status:
                                print(f"  {status}")
                        except:
                            pass
                            
        print(f"Successfully pulled {model_name}")
        return True
    except Exception as e:
        print(f"Error pulling {model_name}: {e}")
        return False

async def call_model(prompt_text: str, model_name: str, timeout: int = 60) -> str:
    """Call a specific model."""
    url = "http://ollama:11434/api/generate"
    
    async with httpx.AsyncClient(timeout=timeout) as client:
        payload = {
            "model": model_name,
            "prompt": prompt_text,
            "stream": False,
            "context": []
        }
        
        resp = await client.post(url, json=payload)
        
        if resp.status_code != 200:
            raise Exception(f"Model returned status {resp.status_code}")
        
        data = resp.json()
        return data.get('response', '')

async def test_model(model_name: str) -> Dict[str, Any]:
    """Test a specific model."""
    results = []
    
    print(f"\n{'='*60}")
    print(f"Testing model: {model_name}")
    print(f"{'='*60}")
    
    # Use simple template
    template_name = "generate_query_simple"
    
    for query in TEST_QUERIES:
        print(f"\nQuery: {query}")
        start_time = time.time()
        
        try:
            # Generate prompt
            prompt = load_prompt(template_name, user_message=query)
            prompt += f"\n\nQuestion: \"{query}\"\nQuery:"
            
            # Call model
            raw_response = await call_model(prompt, model_name, timeout=30)
            
            # Clean up the query
            cypher_query = clean_ai_generated_query(raw_response)
            
            elapsed_time = time.time() - start_time
            
            # Check if query looks valid
            is_valid = (
                cypher_query and 
                'MATCH' in cypher_query and 
                len(cypher_query) > 10 and
                not cypher_query.startswith("I ") and
                not "I can" in cypher_query and
                not "To " in cypher_query
            )
            
            test_result = {
                'query': query,
                'cypher': cypher_query,
                'time': elapsed_time,
                'valid': is_valid,
            }
            
            results.append(test_result)
            
            print(f"  Time: {elapsed_time:.2f}s")
            print(f"  Valid: {'✓' if is_valid else '✗'}")
            if cypher_query:
                print(f"  Cypher: {cypher_query[:80]}...")
            
        except Exception as e:
            print(f"  ERROR: {str(e)}")
            results.append({
                'query': query,
                'cypher': None,
                'time': time.time() - start_time,
                'valid': False,
                'error': str(e)
            })
            
        # Small delay
        await asyncio.sleep(1)
    
    # Calculate summary
    valid_count = sum(1 for r in results if r.get('valid', False))
    total_count = len(results)
    avg_time = sum(r['time'] for r in results) / total_count if total_count > 0 else 0
    
    summary = {
        'total_queries': total_count,
        'valid_queries': valid_count,
        'success_rate': valid_count / total_count if total_count > 0 else 0,
        'average_time': avg_time,
        'errors': sum(1 for r in results if 'error' in r)
    }
    
    return {
        'model': model_name,
        'results': results,
        'summary': summary
    }

async def main():
    """Test qwen2.5-coder model."""
    model_name = "qwen2.5-coder:7b"
    
    print(f"Testing {model_name} model")
    print("=" * 60)
    
    # Pull the model
    print("\nPulling model (this may take a few minutes)...")
    success = await pull_model(model_name)
    
    if not success:
        print("Failed to pull model. Exiting.")
        return
    
    # Test the model
    result = await test_model(model_name)
    
    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Model: {result['model']}")
    print(f"Success Rate: {result['summary']['success_rate']:.1%}")
    print(f"Average Time: {result['summary']['average_time']:.2f}s")
    print(f"Errors: {result['summary']['errors']}")
    
    # Compare with existing results
    print("\nComparison with tested models:")
    print("Model                    | Success | Avg Time")
    print("-------------------------|---------|----------")
    print("granite3.3:8b-largectx   | 100.0%  | 3.66s")
    print("phi4:14b (current)       | 100.0%  | 4.49s") 
    print("granite3.3:8b            | 100.0%  | 4.75s")
    print(f"qwen2.5-coder:7b         | {result['summary']['success_rate']:5.1%}  | {result['summary']['average_time']:.2f}s")

if __name__ == "__main__":
    asyncio.run(main())