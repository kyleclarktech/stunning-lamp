#!/usr/bin/env python3
"""Test different prompt configurations for query generation - simplified version."""

import asyncio
import json
import time
import sys
import os
from typing import Dict, List, Any
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import call_ai_model, load_prompt, clean_ai_generated_query

# Test queries covering different use cases
TEST_QUERIES = [
    # Simple queries
    "Who manages the data team?",
    "List all compliance policies",
    "Find people with Python skills",
    
    # Complex queries
    "What are the critical security policies and who's responsible for them?",
    "Find all senior engineers in Europe who know React and TypeScript",
    "Which teams are working on customer-facing projects?",
    
    # Ambiguous queries
    "Show me the org structure",
    "Who should I talk to about data privacy?",
    "What's our compliance status?",
]

async def test_prompt_configuration(use_simple: bool) -> Dict[str, Any]:
    """Test a specific prompt configuration."""
    results = []
    
    # Get the current environment value
    use_simple_prompts = os.environ.get('USE_SIMPLE_PROMPTS', 'true').lower() == 'true'
    
    print(f"\n{'='*60}")
    print(f"Testing {'SIMPLE' if use_simple else 'COMPLEX'} prompt template")
    print(f"{'='*60}")
    
    template_name = "generate_query_simple" if use_simple else "generate_query"
    
    for query in TEST_QUERIES:
        print(f"\nQuery: {query}")
        start_time = time.time()
        
        try:
            # Generate prompt without intent context
            prompt = load_prompt(template_name, user_message=query)
            prompt += f"\n\nQuestion: \"{query}\"\nQuery:"
            
            # Call AI model
            raw_response = await call_ai_model(prompt, timeout=30)
            
            # Clean up the query
            cypher_query = clean_ai_generated_query(raw_response)
            
            elapsed_time = time.time() - start_time
            
            # Check if query looks valid
            is_valid = (
                cypher_query and 
                'MATCH' in cypher_query and 
                len(cypher_query) > 10 and
                not cypher_query.startswith("I ") and  # Avoid responses that are explanations
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
                print(f"  Cypher: {cypher_query[:100]}...")
            
        except Exception as e:
            print(f"  ERROR: {str(e)}")
            results.append({
                'query': query,
                'cypher': None,
                'time': time.time() - start_time,
                'valid': False,
                'error': str(e)
            })
            
        # Small delay to avoid overwhelming the system
        await asyncio.sleep(2)
    
    return {
        'configuration': 'simple' if use_simple else 'complex',
        'results': results,
        'summary': calculate_summary(results)
    }

def calculate_summary(results: List[Dict]) -> Dict[str, Any]:
    """Calculate summary statistics."""
    valid_count = sum(1 for r in results if r.get('valid', False))
    total_count = len(results)
    avg_time = sum(r['time'] for r in results) / total_count if total_count > 0 else 0
    
    return {
        'total_queries': total_count,
        'valid_queries': valid_count,
        'success_rate': valid_count / total_count if total_count > 0 else 0,
        'average_time': avg_time,
        'errors': sum(1 for r in results if 'error' in r)
    }

async def main():
    """Run the prompt configuration tests."""
    print("Prompt Configuration Comparison Test")
    print("=" * 60)
    
    # Check current configuration
    current_config = os.environ.get('USE_SIMPLE_PROMPTS', 'true')
    print(f"Current USE_SIMPLE_PROMPTS setting: {current_config}")
    
    # Test both configurations
    simple_results = await test_prompt_configuration(use_simple=True)
    
    print("\n\nWaiting 5 seconds before testing complex template...")
    await asyncio.sleep(5)
    
    complex_results = await test_prompt_configuration(use_simple=False)
    
    # Save results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    results_file = f"prompt_comparison_{timestamp}.json"
    
    with open(results_file, 'w') as f:
        json.dump({
            'timestamp': timestamp,
            'current_env_setting': current_config,
            'simple': simple_results,
            'complex': complex_results,
            'comparison': {
                'simple_success_rate': simple_results['summary']['success_rate'],
                'complex_success_rate': complex_results['summary']['success_rate'],
                'simple_avg_time': simple_results['summary']['average_time'],
                'complex_avg_time': complex_results['summary']['average_time'],
            }
        }, f, indent=2)
    
    # Print comparison
    print("\n" + "=" * 60)
    print("COMPARISON SUMMARY")
    print("=" * 60)
    
    print(f"\nSimple Template:")
    print(f"  Success Rate: {simple_results['summary']['success_rate']:.1%}")
    print(f"  Average Time: {simple_results['summary']['average_time']:.2f}s")
    print(f"  Errors: {simple_results['summary']['errors']}")
    
    print(f"\nComplex Template:")
    print(f"  Success Rate: {complex_results['summary']['success_rate']:.1%}")
    print(f"  Average Time: {complex_results['summary']['average_time']:.2f}s")
    print(f"  Errors: {complex_results['summary']['errors']}")
    
    # Performance comparison
    print(f"\nPerformance Comparison:")
    time_diff = complex_results['summary']['average_time'] - simple_results['summary']['average_time']
    print(f"  Simple template is {abs(time_diff):.2f}s {'faster' if time_diff > 0 else 'slower'}")
    
    success_diff = simple_results['summary']['success_rate'] - complex_results['summary']['success_rate']
    print(f"  Simple template has {abs(success_diff)*100:.1f}% {'higher' if success_diff > 0 else 'lower'} success rate")
    
    print(f"\nResults saved to: {results_file}")
    
    # Print detailed comparison
    print("\n" + "=" * 60)
    print("DETAILED RESULTS")
    print("=" * 60)
    
    for i, query in enumerate(TEST_QUERIES):
        simple_result = simple_results['results'][i]
        complex_result = complex_results['results'][i]
        
        print(f"\nQuery: {query}")
        print(f"  Simple: {'✓' if simple_result['valid'] else '✗'} ({simple_result['time']:.2f}s)")
        if simple_result['cypher']:
            print(f"    {simple_result['cypher'][:80]}...")
        print(f"  Complex: {'✓' if complex_result['valid'] else '✗'} ({complex_result['time']:.2f}s)")
        if complex_result['cypher']:
            print(f"    {complex_result['cypher'][:80]}...")

if __name__ == "__main__":
    asyncio.run(main())