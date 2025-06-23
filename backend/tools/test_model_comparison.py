#!/usr/bin/env python3
"""Test different LLM models for query generation performance."""

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
    "What are the critical security policies and who's responsible for them?",
    "Find all senior engineers in Europe who know React and TypeScript",
]

# Models to test (from available and suggested)
MODELS_TO_TEST = [
    {"name": "phi4:14b", "available": True},
    {"name": "granite3.3:8b", "available": True},
    {"name": "granite3.3:8b-largectx", "available": True},
    {"name": "mistral:7b", "available": False},
    {"name": "qwen2.5-coder:7b", "available": False},
]

async def pull_model(model_name: str) -> bool:
    """Pull a model if not available."""
    print(f"Pulling model {model_name}...")
    try:
        async with httpx.AsyncClient(timeout=600) as client:
            response = await client.post(
                "http://ollama:11434/api/pull",
                json={"name": model_name}
            )
            if response.status_code == 200:
                print(f"Successfully pulled {model_name}")
                return True
            else:
                print(f"Failed to pull {model_name}: {response.status_code}")
                return False
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

async def get_model_info(model_name: str) -> Dict[str, Any]:
    """Get model information."""
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            "http://ollama:11434/api/show",
            json={"name": model_name}
        )
        if response.status_code == 200:
            data = response.json()
            # Extract size information from details
            details = data.get('details', {})
            param_size = details.get('parameter_size', 'unknown')
            quantization = details.get('quantization', 'unknown')
            return {
                "parameter_size": param_size,
                "quantization": quantization,
                "family": details.get('family', 'unknown')
            }
        return {}

async def test_model(model_name: str, available: bool) -> Dict[str, Any]:
    """Test a specific model."""
    results = []
    
    # Check if model needs to be pulled
    if not available:
        print(f"\nModel {model_name} not available. Skipping...")
        return {
            'model': model_name,
            'available': False,
            'skipped': True,
            'results': [],
            'summary': {}
        }
    
    print(f"\n{'='*60}")
    print(f"Testing model: {model_name}")
    print(f"{'='*60}")
    
    # Get model info
    model_info = await get_model_info(model_name)
    print(f"Model info: {model_info}")
    
    # Use simple template which performed better
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
        'available': True,
        'model_info': model_info,
        'results': results,
        'summary': summary
    }

async def check_vram_usage():
    """Check current VRAM usage."""
    try:
        proc = await asyncio.create_subprocess_exec(
            'nvidia-smi',
            '--query-gpu=memory.used,memory.total',
            '--format=csv,noheader,nounits',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        
        if proc.returncode == 0:
            output = stdout.decode().strip()
            used, total = map(int, output.split(', '))
            return {
                'used_mb': used,
                'total_mb': total,
                'percentage': (used / total) * 100
            }
    except FileNotFoundError:
        # nvidia-smi not available in container
        return {
            'used_mb': 0,
            'total_mb': 0,
            'percentage': 0,
            'note': 'nvidia-smi not available in container'
        }
    return None

async def main():
    """Run model comparison tests."""
    print("LLM Model Comparison Test")
    print("=" * 60)
    
    # Check initial VRAM
    initial_vram = await check_vram_usage()
    print(f"Initial VRAM usage: {initial_vram['used_mb']}MB / {initial_vram['total_mb']}MB ({initial_vram['percentage']:.1f}%)")
    
    all_results = []
    
    for model_config in MODELS_TO_TEST:
        model_name = model_config['name']
        available = model_config['available']
        
        # Check VRAM before testing
        vram_before = await check_vram_usage()
        
        # Test model
        result = await test_model(model_name, available)
        
        # Check VRAM after testing
        vram_after = await check_vram_usage()
        
        result['vram_usage'] = {
            'before': vram_before,
            'after': vram_after,
            'delta': vram_after['used_mb'] - vram_before['used_mb'] if vram_before and vram_after else 0
        }
        
        all_results.append(result)
        
        # Unload model to free VRAM (except phi4:14b which is our default)
        if model_name != "phi4:14b" and available:
            print(f"\nUnloading model {model_name} to free VRAM...")
            # Unfortunately Ollama doesn't have an unload API, so we'll just wait
            await asyncio.sleep(5)
    
    # Save results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    results_file = f"model_comparison_{timestamp}.json"
    
    with open(results_file, 'w') as f:
        json.dump({
            'timestamp': timestamp,
            'results': all_results,
        }, f, indent=2)
    
    # Print comparison
    print("\n" + "=" * 60)
    print("MODEL COMPARISON SUMMARY")
    print("=" * 60)
    
    # Sort by average time
    tested_models = [r for r in all_results if not r.get('skipped', False)]
    tested_models.sort(key=lambda x: x['summary']['average_time'])
    
    print("\nModels ranked by speed (fastest first):")
    for i, result in enumerate(tested_models, 1):
        print(f"\n{i}. {result['model']}:")
        print(f"   Success Rate: {result['summary']['success_rate']:.1%}")
        print(f"   Average Time: {result['summary']['average_time']:.2f}s")
        print(f"   VRAM Delta: {result['vram_usage']['delta']}MB")
        if result.get('model_info'):
            print(f"   Parameters: {result['model_info'].get('parameter_size', 'unknown')}")
    
    # Find best model
    if tested_models:
        # Prioritize success rate, then speed
        best_model = max(tested_models, key=lambda x: (x['summary']['success_rate'], -x['summary']['average_time']))
        print(f"\n🏆 Best overall model: {best_model['model']}")
        print(f"   Success rate: {best_model['summary']['success_rate']:.1%}")
        print(f"   Average time: {best_model['summary']['average_time']:.2f}s")
    
    print(f"\nResults saved to: {results_file}")

if __name__ == "__main__":
    asyncio.run(main())