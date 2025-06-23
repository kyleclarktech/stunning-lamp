#!/usr/bin/env python3
"""Test the remaining models that weren't tested in Phase 1."""

import asyncio
import json
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the Phase 1 test functions
from test_phase1_model_baseline import (
    test_model_baseline, 
    check_model_available,
    generate_summary_report,
    generate_csv_report
)

# Remaining models to test
REMAINING_MODELS = [
    # Priority 2 - Already downloaded
    {"name": "qwen2.5-coder:7b", "priority": 2, "type": "coding"},
    
    # Priority 2 - Still need to pull
    {"name": "granite-code:8b", "priority": 2, "type": "coding"},
    {"name": "deepseek-coder:1.3b", "priority": 2, "type": "coding"},
    
    # Priority 3 - Quick to download due to size
    {"name": "llama3.2:3b", "priority": 3, "type": "general"},
    {"name": "phi3-mini:3.8b", "priority": 3, "type": "general"},
]

async def main():
    """Test remaining models."""
    print("TESTING REMAINING MODELS FROM PHASE 1")
    print("=" * 60)
    
    # Check which models are available
    print("\nChecking model availability...")
    for model in REMAINING_MODELS:
        available = await check_model_available(model['name'])
        print(f"  {model['name']}: {'✓ Available' if available else '✗ Not available'}")
    
    # Load existing Phase 1 results
    try:
        with open('phase1_baseline_20250622_142809.json', 'r') as f:
            existing_results = json.load(f)
    except:
        existing_results = {
            "phase": 1,
            "timestamp": datetime.now().isoformat(),
            "models_tested": []
        }
    
    print(f"\nContinuing from {len(existing_results['models_tested'])} previously tested models...")
    
    # Test qwen2.5-coder:7b first since it's already available
    qwen_model = {"name": "qwen2.5-coder:7b", "priority": 2, "type": "coding"}
    if await check_model_available(qwen_model['name']):
        print(f"\nTesting {qwen_model['name']} (already available)...")
        try:
            result = await test_model_baseline(qwen_model)
            existing_results["models_tested"].append(result)
            
            # Save updated results
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            with open(f"phase1_extended_{timestamp}.json", 'w') as f:
                json.dump(existing_results, f, indent=2)
                
            print(f"\n✓ Successfully tested {qwen_model['name']}")
            
            # Quick summary
            if not result.get('skipped'):
                metrics = result['metrics']
                print(f"  - Average time: {metrics['average_time']:.2f}s")
                print(f"  - Syntax validity: {metrics['syntax_validity_rate']:.1%}")
                print(f"  - VRAM usage: {result['resource_usage']['vram_delta_mb']}MB")
                
        except Exception as e:
            print(f"✗ Error testing {qwen_model['name']}: {e}")
    
    # Optional: Test small models that download quickly
    print("\n" + "=" * 60)
    print("RECOMMENDATIONS FOR REMAINING MODELS")
    print("=" * 60)
    
    print("\n1. **High Priority - Test qwen2.5-coder:7b** (already done if available)")
    print("   - Coding-optimized model, could excel at Cypher generation")
    
    print("\n2. **Medium Priority - Small models for quick testing:**")
    print("   - llama3.2:3b - Very small, fast to download")
    print("   - phi3-mini:3.8b - Compact but capable")
    print("   - deepseek-coder:1.3b - Tiny coding model")
    
    print("\n3. **Lower Priority - Larger models:**")
    print("   - granite-code:8b - Another coding model")
    print("   - mistral:7b - General purpose")
    
    print("\nTo test a specific model manually:")
    print("docker exec stunning-lamp-api-1 ollama pull <model-name>")
    print("Then re-run this script or the full Phase 1 test")
    
    # Generate updated summary if we tested qwen
    if any(m['model'] == 'qwen2.5-coder:7b' for m in existing_results['models_tested'] if not m.get('skipped')):
        print("\nGenerating updated summary with qwen2.5-coder results...")
        summary = generate_summary_report(existing_results)
        with open("phase1_extended_summary.md", 'w') as f:
            f.write(summary)
        print("✓ Updated summary saved to phase1_extended_summary.md")

if __name__ == "__main__":
    asyncio.run(main())