# Test Phase 1: LLM Model Baseline Performance

## Objective
Establish baseline performance metrics for all available LLM models using the current simple prompt template. This phase focuses on model comparison without varying prompting strategies.

## Prerequisites
- Docker services running (API, Ollama, FalkorDB)
- At least 16GB VRAM available
- Current working directory: `/home/kyle/projects/stunning-lamp/backend`

## Models to Test

### Priority 1 (Already Available)
- phi4:14b (current default)
- granite3.3:8b
- granite3.3:8b-largectx

### Priority 2 (Coding-Optimized Models)
- qwen2.5-coder:7b
- granite-code:8b
- deepseek-coder:1.3b
- codeqwen:7b

### Priority 3 (General Purpose)
- mistral:7b
- llama3.2:3b
- phi3-mini:3.8b

## Test Implementation

Create `tools/test_phase1_model_baseline.py`:

```python
#!/usr/bin/env python3
"""Phase 1: Test baseline performance of all LLM models."""

import asyncio
import json
import time
import os
from datetime import datetime
from typing import Dict, List, Any
import httpx

# Core test queries (keep it focused)
BASELINE_QUERIES = [
    # Simple queries (3)
    "Who manages the data team?",
    "List all compliance policies",
    "Find people with Python skills",
    
    # Medium complexity (3)
    "What are the critical security policies and who's responsible?",
    "Find senior engineers in Europe with React skills",
    "Which teams are working on customer projects?",
    
    # Complex queries (2)
    "Show the complete org structure with reporting lines",
    "Find all paths between the CTO and data team members",
    
    # Edge cases (2)
    "xyz123 nonexistent query",
    "Find people in the quantum department"
]

# Model configurations
MODELS_TO_TEST = [
    # Priority 1
    {"name": "phi4:14b", "priority": 1, "type": "general"},
    {"name": "granite3.3:8b", "priority": 1, "type": "general"},
    {"name": "granite3.3:8b-largectx", "priority": 1, "type": "general"},
    
    # Priority 2
    {"name": "qwen2.5-coder:7b", "priority": 2, "type": "coding"},
    {"name": "granite-code:8b", "priority": 2, "type": "coding"},
    {"name": "deepseek-coder:1.3b", "priority": 2, "type": "coding"},
    
    # Priority 3
    {"name": "mistral:7b", "priority": 3, "type": "general"},
    {"name": "llama3.2:3b", "priority": 3, "type": "general"},
]

async def test_model_baseline(model_config: Dict) -> Dict[str, Any]:
    """Test a single model with baseline queries."""
    # Implementation:
    # 1. Check if model is available (pull if needed)
    # 2. Record initial VRAM usage
    # 3. Test cold start (first query after load)
    # 4. Run all baseline queries
    # 5. Measure: response time, validity, VRAM usage
    # 6. Test concurrent queries (3 simultaneous)
    # 7. Return comprehensive metrics
    pass

async def main():
    """Run Phase 1 baseline tests."""
    print("PHASE 1: LLM Model Baseline Performance Testing")
    print("=" * 60)
    
    results = {
        "phase": 1,
        "timestamp": datetime.now().isoformat(),
        "models_tested": [],
        "summary": {}
    }
    
    # Test each model
    for model in MODELS_TO_TEST:
        print(f"\nTesting {model['name']} (Priority {model['priority']})")
        result = await test_model_baseline(model)
        results["models_tested"].append(result)
        
        # Save intermediate results
        with open(f"phase1_baseline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", 'w') as f:
            json.dump(results, f, indent=2)
    
    # Generate summary report
    generate_phase1_summary(results)
```

## Metrics to Collect

### Performance Metrics
- **Cold Start Time**: Time for first query after model load
- **Average Query Time**: Mean response time across all queries
- **P95 Query Time**: 95th percentile response time
- **Throughput**: Queries per second capability

### Quality Metrics
- **Syntax Validity**: % of valid Cypher queries generated
- **Execution Success**: % of queries that execute without error
- **Empty Result Handling**: How well model handles no-result cases

### Resource Metrics
- **VRAM Usage**: Peak memory consumption
- **VRAM Delta**: Increase from baseline
- **Model Load Time**: Time to load model into memory
- **Context Window**: Effective context size

## Expected Output

### 1. Raw Results File
`phase1_baseline_[timestamp].json` containing:
- All query results per model
- Timing measurements
- Resource usage stats
- Error logs

### 2. Summary Report
`phase1_summary.md` containing:
- Model ranking by speed
- Model ranking by accuracy
- Model ranking by resource efficiency
- Top 3 recommended models for Phase 2

### 3. Quick Reference
`phase1_quick_ref.csv` with:
```
Model,Avg_Time,Success_Rate,VRAM_Usage,Overall_Score
granite3.3:8b-largectx,3.66s,100%,8GB,95
phi4:14b,4.49s,100%,14GB,85
...
```

## Execution Instructions

1. **Ensure Clean Environment**
   ```bash
   docker-compose restart ollama
   nvidia-smi  # Check VRAM is available
   ```

2. **Run Phase 1 Tests**
   ```bash
   cd /home/kyle/projects/stunning-lamp/backend
   python tools/test_phase1_model_baseline.py
   ```

3. **Monitor Progress**
   - Tests will save intermediate results
   - Each model takes ~5-10 minutes
   - Total time: 45-90 minutes

4. **Review Results**
   - Check `phase1_summary.md` for recommendations
   - Select top 3-5 models for Phase 2 testing

## Success Criteria

Phase 1 is successful if:
1. All available models are tested
2. Clear performance differences are identified
3. Top 3-5 models are selected for Phase 2
4. No system crashes or OOM errors
5. Results are reproducible

## Next Step
After Phase 1 completion, proceed to `TEST_PHASE_2_PROMPTING_STRATEGIES.md` with the top-performing models.