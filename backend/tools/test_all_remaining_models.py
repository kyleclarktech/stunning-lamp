#!/usr/bin/env python3
"""Test ALL remaining models from Phase 1 for completeness."""

import asyncio
import json
import sys
import os
import time
from datetime import datetime
from typing import Dict, List, Any

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import functions from the original test script
from test_phase1_model_baseline import (
    test_model_baseline,
    check_model_available,
    pull_model,
    get_vram_usage,
    generate_summary_report,
    generate_csv_report
)

# ALL remaining models to test
REMAINING_MODELS = [
    # Priority 2 - Coding-optimized models
    {"name": "granite-code:8b", "priority": 2, "type": "coding"},
    {"name": "deepseek-coder:1.3b", "priority": 2, "type": "coding"},
    {"name": "codeqwen:7b", "priority": 2, "type": "coding"},
    
    # Priority 3 - General purpose models
    {"name": "mistral:7b", "priority": 3, "type": "general"},
    {"name": "llama3.2:3b", "priority": 3, "type": "general"},
    {"name": "phi3-mini:3.8b", "priority": 3, "type": "general"},
]

async def test_model_with_pull(model_config: Dict) -> Dict[str, Any]:
    """Test a model, pulling it first if necessary."""
    model_name = model_config['name']
    
    # Check if model is available
    available = await check_model_available(model_name)
    
    if not available:
        print(f"\nPulling {model_name}...")
        success = await pull_model(model_name)
        if not success:
            print(f"Failed to pull {model_name}")
            return {
                'model': model_name,
                'config': model_config,
                'available': False,
                'skipped': True,
                'error': 'Failed to pull model'
            }
        # Small delay after pulling
        await asyncio.sleep(5)
    
    # Test the model
    print(f"\nTesting {model_name}...")
    try:
        result = await test_model_baseline(model_config)
        return result
    except Exception as e:
        print(f"Error testing {model_name}: {e}")
        return {
            'model': model_name,
            'config': model_config,
            'available': True,
            'skipped': True,
            'error': str(e)
        }

async def main():
    """Test all remaining models comprehensively."""
    print("COMPREHENSIVE PHASE 1 TESTING - ALL REMAINING MODELS")
    print("=" * 60)
    print(f"\nModels to test: {len(REMAINING_MODELS)}")
    for model in REMAINING_MODELS:
        print(f"  - {model['name']} (Priority {model['priority']}, {model['type']})")
    
    # Load existing results
    existing_files = [
        'phase1_baseline_20250622_142809.json',  # Original 3 models
        'phase1_extended_20250622_145037.json'   # qwen2.5-coder
    ]
    
    all_tested_models = []
    for file in existing_files:
        if os.path.exists(file):
            with open(file, 'r') as f:
                data = json.load(f)
                all_tested_models.extend(data.get('models_tested', []))
    
    print(f"\nAlready tested: {len(all_tested_models)} models")
    already_tested_names = {m['model'] for m in all_tested_models if not m.get('skipped')}
    print(f"Successfully tested: {', '.join(already_tested_names)}")
    
    # Prepare results structure
    results = {
        "phase": "1-complete",
        "timestamp": datetime.now().isoformat(),
        "models_tested": all_tested_models.copy(),  # Start with existing results
        "summary": {}
    }
    
    # Test each remaining model
    start_time = time.time()
    newly_tested = 0
    
    for i, model_config in enumerate(REMAINING_MODELS, 1):
        print(f"\n{'='*60}")
        print(f"Testing model {i}/{len(REMAINING_MODELS)}")
        print(f"{'='*60}")
        
        # Check VRAM before proceeding
        vram = await get_vram_usage()
        print(f"Current VRAM: {vram['used_mb']}MB / {vram['total_mb']}MB ({vram['percentage']:.1f}%)")
        
        if vram['percentage'] > 85:
            print("WARNING: VRAM usage high. Waiting 30s for cleanup...")
            await asyncio.sleep(30)
        
        # Test the model
        result = await test_model_with_pull(model_config)
        results["models_tested"].append(result)
        
        if not result.get('skipped'):
            newly_tested += 1
            
            # Save intermediate results after each successful test
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            with open(f"phase1_complete_{timestamp}.json", 'w') as f:
                json.dump(results, f, indent=2)
            print(f"\nSaved intermediate results to phase1_complete_{timestamp}.json")
        
        # Small delay between models
        await asyncio.sleep(5)
    
    # Calculate total test duration
    total_duration = (time.time() - start_time) / 60
    results['test_duration'] = f"{total_duration:.1f} minutes"
    results['newly_tested'] = newly_tested
    results['total_models'] = len(results['models_tested'])
    
    # Generate final comprehensive report
    print("\n" + "="*60)
    print("GENERATING COMPREHENSIVE REPORTS")
    print("="*60)
    
    # Save final complete results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    final_file = f"phase1_complete_final_{timestamp}.json"
    with open(final_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    # Generate comprehensive summary
    summary_report = generate_summary_report(results)
    with open("phase1_complete_summary.md", 'w') as f:
        f.write(summary_report)
    
    # Generate comprehensive CSV
    csv_report = generate_csv_report(results)
    with open("phase1_complete_results.csv", 'w') as f:
        f.write(csv_report)
    
    # Print quick summary
    print(f"\nTesting complete!")
    print(f"  - Total models tested: {len([m for m in results['models_tested'] if not m.get('skipped')])}")
    print(f"  - Newly tested in this run: {newly_tested}")
    print(f"  - Total duration: {total_duration:.1f} minutes")
    print(f"\nReports generated:")
    print(f"  - Complete results: {final_file}")
    print(f"  - Summary report: phase1_complete_summary.md")
    print(f"  - CSV results: phase1_complete_results.csv")
    
    # Print top 5 models by speed
    tested_models = [m for m in results['models_tested'] if not m.get('skipped')]
    tested_models.sort(key=lambda x: x['metrics']['average_time'])
    
    print("\n" + "="*60)
    print("TOP 5 MODELS BY SPEED")
    print("="*60)
    for i, model in enumerate(tested_models[:5], 1):
        metrics = model['metrics']
        print(f"{i}. {model['model']}: {metrics['average_time']:.2f}s avg "
              f"({metrics['syntax_validity_rate']:.0%} validity)")

if __name__ == "__main__":
    # Set event loop policy for Windows compatibility
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    asyncio.run(main())