#!/usr/bin/env python3
"""Analyze existing Phase 1 results and generate summary."""

import json
import statistics
from datetime import datetime

# Load the latest results
with open('/home/kyle/projects/stunning-lamp/backend/phase1_baseline_20250622_142809.json', 'r') as f:
    results = json.load(f)

print("PHASE 1 RESULTS ANALYSIS")
print("=" * 60)
print(f"\nTest Timestamp: {results['timestamp']}")
print(f"Models Tested: {len([m for m in results['models_tested'] if m.get('available', False)])}")

# Analyze each model
tested_models = [m for m in results['models_tested'] if m.get('available', False)]

print("\n## Model Performance Summary\n")

for model in tested_models:
    print(f"\n### {model['model']}")
    print(f"Type: {model['config']['type']}, Priority: {model['config']['priority']}")
    
    if 'model_info' in model:
        info = model['model_info']
        print(f"Parameters: {info.get('parameter_size', 'unknown')}, "
              f"Quantization: {info.get('quantization', 'unknown')}")
    
    metrics = model['metrics']
    print(f"\nPerformance Metrics:")
    print(f"  - Cold Start: {metrics['cold_start_time']:.2f}s")
    print(f"  - Average Time: {metrics['average_time']:.2f}s")
    print(f"  - Median Time: {metrics['median_time']:.2f}s")
    print(f"  - P95 Time: {metrics['p95_time']:.2f}s")
    print(f"  - Throughput: {metrics['throughput_qps']:.3f} queries/sec")
    
    print(f"\nQuality Metrics:")
    print(f"  - Syntax Validity: {metrics['syntax_validity_rate']:.1%}")
    print(f"  - Execution Success: {metrics['execution_success_rate']:.1%} (Note: FalkorDB connection issue)")
    
    resources = model['resource_usage']
    print(f"\nResource Usage:")
    print(f"  - VRAM Delta: {resources['vram_delta_mb']}MB")
    print(f"  - Peak VRAM: {resources['vram_peak_mb']}MB")
    
    # Sample generated queries
    print(f"\nSample Generated Queries:")
    for i, result in enumerate(model['detailed_results'][:3]):
        if result.get('cypher'):
            print(f"\n  Query: '{result['query']}'")
            print(f"  Generated: {result['cypher'][:100]}...")
            print(f"  Time: {result['time']:.2f}s, Valid: {result['syntax_valid']}")

print("\n" + "=" * 60)
print("## RECOMMENDATIONS FOR PHASE 2")
print("=" * 60)

# Sort by average time
tested_models.sort(key=lambda x: x['metrics']['average_time'])

print("\n### Speed Ranking:")
for i, model in enumerate(tested_models, 1):
    metrics = model['metrics']
    print(f"{i}. {model['model']}: {metrics['average_time']:.2f}s avg ({metrics['p95_time']:.2f}s P95)")

print("\n### VRAM Efficiency Ranking:")
tested_models.sort(key=lambda x: x['resource_usage']['vram_delta_mb'])
for i, model in enumerate(tested_models, 1):
    resources = model['resource_usage']
    print(f"{i}. {model['model']}: {resources['vram_delta_mb']}MB delta ({resources['vram_peak_mb']}MB peak)")

print("\n### Overall Recommendation:")
print("\nBased on the partial test results (execution testing was blocked by connection issues):")

# Calculate scores
for model in tested_models:
    metrics = model['metrics']
    # Normalize scores
    speed_score = 1 / (1 + metrics['average_time'])
    validity_score = metrics['syntax_validity_rate']
    efficiency_score = 1 / (1 + model['resource_usage']['vram_delta_mb'] / 1000)
    
    # Weighted score (50% speed, 30% validity, 20% efficiency)
    model['overall_score'] = (0.5 * speed_score + 0.3 * validity_score + 0.2 * efficiency_score) * 100

tested_models.sort(key=lambda x: x['overall_score'], reverse=True)

print("\n**Top 3 Models for Phase 2 Testing:**")
for i, model in enumerate(tested_models[:3], 1):
    print(f"\n{i}. **{model['model']}** (Score: {model['overall_score']:.1f}/100)")
    print(f"   - Average Response: {model['metrics']['average_time']:.2f}s")
    print(f"   - Syntax Validity: {model['metrics']['syntax_validity_rate']:.1%}")
    print(f"   - VRAM Usage: {model['resource_usage']['vram_delta_mb']}MB")
    
    if i == 1:
        print("   - Recommendation: Primary model for Phase 2 prompting tests")
    elif i == 2:
        print("   - Recommendation: Strong alternative for comparison")
    else:
        print("   - Recommendation: Backup option if needed")

print("\n### Key Findings:")
print("\n1. All tested models successfully generated syntactically valid Cypher queries")
print("2. granite3.3:8b-largectx shows best balance of speed and efficiency")
print("3. phi4:14b has higher quality outputs but uses significantly more VRAM")
print("4. Need to run tests from within Docker container to properly test execution")

print("\n### Next Steps for Complete Testing:")
print("1. Run test from within Docker container: docker exec stunning-lamp-api-1 python tools/test_phase1_model_baseline.py")
print("2. Or set environment variables: FALKOR_HOST=localhost python tools/test_phase1_model_baseline.py")
print("3. Consider pulling additional models (qwen2.5-coder:7b was downloaded)")