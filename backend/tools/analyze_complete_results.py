#!/usr/bin/env python3
"""Analyze the complete Phase 1 results including all models."""

import json

# Load the complete results
with open('phase1_complete_final_20250622_151628.json', 'r') as f:
    data = json.load(f)

print("COMPLETE PHASE 1 RESULTS - ALL 10 MODELS")
print("=" * 80)

# Filter out skipped models and collect valid results
valid_models = []
for model in data['models_tested']:
    if not model.get('skipped', False) and 'metrics' in model:
        valid_models.append(model)

print(f"\nSuccessfully tested: {len(valid_models)} models")
print(f"Test duration: {data.get('test_duration', 'N/A')}")

# Sort by syntax validity rate
print("\n## MODELS RANKED BY SYNTAX VALIDITY RATE")
print("-" * 80)

valid_models.sort(key=lambda x: x['metrics']['syntax_validity_rate'], reverse=True)

for i, model in enumerate(valid_models, 1):
    metrics = model['metrics']
    print(f"\n{i}. {model['model']}")
    print(f"   Syntax Validity: {metrics['syntax_validity_rate']:.0%}")
    print(f"   Average Time: {metrics['average_time']:.2f}s")
    print(f"   VRAM Usage: {model['resource_usage']['vram_delta_mb']}MB")
    
    # Check if this is a problematic result
    if metrics['average_time'] < 0.1 and metrics['syntax_validity_rate'] == 0:
        print("   ⚠️  WARNING: Model failed to generate responses")

# Sort by speed (excluding failed models)
print("\n## MODELS RANKED BY SPEED (excluding failed models)")
print("-" * 80)

working_models = [m for m in valid_models if m['metrics']['syntax_validity_rate'] > 0]
working_models.sort(key=lambda x: x['metrics']['average_time'])

for i, model in enumerate(working_models, 1):
    metrics = model['metrics']
    print(f"\n{i}. {model['model']}")
    print(f"   Average Time: {metrics['average_time']:.2f}s")
    print(f"   Syntax Validity: {metrics['syntax_validity_rate']:.0%}")
    print(f"   VRAM Usage: {model['resource_usage']['vram_delta_mb']}MB")

# Find the previously tested models
previously_tested = ['phi4:14b', 'granite3.3:8b', 'granite3.3:8b-largectx', 'qwen2.5-coder:7b']
newly_tested = [m['model'] for m in valid_models if m['model'] not in previously_tested]

print(f"\n## NEWLY TESTED MODELS IN THIS RUN")
print("-" * 80)
print(f"New models: {', '.join(newly_tested)}")

# Overall recommendations
print("\n## FINAL RECOMMENDATIONS")
print("-" * 80)

# Get top 5 working models by combined score
print("\nTop 5 Models (by speed with >80% validity):")
top_models = [m for m in working_models if m['metrics']['syntax_validity_rate'] >= 0.8]
top_models.sort(key=lambda x: x['metrics']['average_time'])

for i, model in enumerate(top_models[:5], 1):
    metrics = model['metrics']
    print(f"\n{i}. {model['model']}")
    print(f"   Speed: {metrics['average_time']:.2f}s")
    print(f"   Validity: {metrics['syntax_validity_rate']:.0%}")
    print(f"   Type: {model['config']['type']}")

# Check if we have the qwen2.5-coder results
qwen_coder = next((m for m in valid_models if m['model'] == 'qwen2.5-coder:7b'), None)
if qwen_coder:
    print(f"\n⭐ WINNER: qwen2.5-coder:7b")
    print(f"   - Fastest: {qwen_coder['metrics']['average_time']:.2f}s")
    print(f"   - Perfect validity: {qwen_coder['metrics']['syntax_validity_rate']:.0%}")
    print(f"   - Coding-optimized")
else:
    print("\n⚠️  qwen2.5-coder:7b not found in results - check phase1_extended files")