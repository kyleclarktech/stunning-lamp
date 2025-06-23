#!/usr/bin/env python3
"""Test different prompt configurations for query generation."""

import asyncio
import json
import time
import sys
import os
from typing import Dict, List, Any
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import call_ai_model, load_prompt, clean_ai_generated_query, get_falkor_client
from intent_processor import IntentProcessor

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
    
    # Edge cases
    "xyz123 random query",
    "Find",
    "Help with compliance and security policies for GDPR"
]

async def test_prompt_configuration(use_simple: bool) -> Dict[str, Any]:
    """Test a specific prompt configuration."""
    results = []
    
    # Temporarily set the environment variable
    original_value = os.environ.get('USE_SIMPLE_PROMPTS', 'true')
    os.environ['USE_SIMPLE_PROMPTS'] = 'true' if use_simple else 'false'
    
    # Initialize intent processor
    intent_processor = IntentProcessor()
    
    try:
        print(f"\n{'='*60}")
        print(f"Testing {'SIMPLE' if use_simple else 'COMPLEX'} prompt template")
        print(f"{'='*60}")
        
        template_name = "generate_query_simple" if use_simple else "generate_query"
        
        for query in TEST_QUERIES:
            print(f"\nQuery: {query}")
            start_time = time.time()
            
            try:
                # Analyze intent
                intent = await intent_processor.analyze_intent(query)
                intent_context = intent.to_context_dict()
                
                # Generate prompt
                prompt = load_prompt(template_name, 
                                   user_message=query,
                                   intent_context=intent_context)
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
                    not cypher_query.startswith("I ")  # Avoid responses that are explanations
                )
                
                test_result = {
                    'query': query,
                    'cypher': cypher_query,
                    'time': elapsed_time,
                    'valid': is_valid,
                    'intent': intent_context.get('primary_intent'),
                    'confidence': intent.confidence
                }
                
                results.append(test_result)
                
                print(f"  Time: {elapsed_time:.2f}s")
                print(f"  Valid: {'✓' if is_valid else '✗'}")
                print(f"  Intent: {intent_context.get('primary_intent')} (confidence: {intent.confidence:.2f})")
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
            
    finally:
        # Restore original environment variable
        os.environ['USE_SIMPLE_PROMPTS'] = original_value
    
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
    
    # Calculate average confidence for valid queries
    valid_confidences = [r.get('confidence', 0) for r in results if r.get('valid', False)]
    avg_confidence = sum(valid_confidences) / len(valid_confidences) if valid_confidences else 0
    
    return {
        'total_queries': total_count,
        'valid_queries': valid_count,
        'success_rate': valid_count / total_count if total_count > 0 else 0,
        'average_time': avg_time,
        'average_confidence': avg_confidence,
        'errors': sum(1 for r in results if 'error' in r)
    }

async def main():
    """Run the prompt configuration tests."""
    print("Prompt Configuration Comparison Test")
    print("=" * 60)
    
    # Database connection will be handled by get_falkor_client() in main.py
    
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
            'simple': simple_results,
            'complex': complex_results,
            'comparison': {
                'simple_success_rate': simple_results['summary']['success_rate'],
                'complex_success_rate': complex_results['summary']['success_rate'],
                'simple_avg_time': simple_results['summary']['average_time'],
                'complex_avg_time': complex_results['summary']['average_time'],
                'simple_avg_confidence': simple_results['summary']['average_confidence'],
                'complex_avg_confidence': complex_results['summary']['average_confidence'],
            }
        }, f, indent=2)
    
    # Print comparison
    print("\n" + "=" * 60)
    print("COMPARISON SUMMARY")
    print("=" * 60)
    
    print(f"\nSimple Template:")
    print(f"  Success Rate: {simple_results['summary']['success_rate']:.1%}")
    print(f"  Average Time: {simple_results['summary']['average_time']:.2f}s")
    print(f"  Average Confidence: {simple_results['summary']['average_confidence']:.2f}")
    print(f"  Errors: {simple_results['summary']['errors']}")
    
    print(f"\nComplex Template:")
    print(f"  Success Rate: {complex_results['summary']['success_rate']:.1%}")
    print(f"  Average Time: {complex_results['summary']['average_time']:.2f}s")
    print(f"  Average Confidence: {complex_results['summary']['average_confidence']:.2f}")
    print(f"  Errors: {complex_results['summary']['errors']}")
    
    # Performance comparison
    print(f"\nPerformance Comparison:")
    time_diff = complex_results['summary']['average_time'] - simple_results['summary']['average_time']
    print(f"  Simple template is {abs(time_diff):.2f}s {'faster' if time_diff > 0 else 'slower'}")
    
    success_diff = simple_results['summary']['success_rate'] - complex_results['summary']['success_rate']
    print(f"  Simple template has {abs(success_diff)*100:.1f}% {'higher' if success_diff > 0 else 'lower'} success rate")
    
    print(f"\nResults saved to: {results_file}")

if __name__ == "__main__":
    asyncio.run(main())