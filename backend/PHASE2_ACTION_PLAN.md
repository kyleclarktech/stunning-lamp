# Phase 2 Action Plan: Prompting Strategy Optimization

## Overview

Based on Phase 1 results, we have identified the top 3 models for Phase 2 prompting strategy testing. This document outlines the specific action plan for optimizing query generation through advanced prompting techniques.

## Selected Models for Phase 2

1. **granite3.3:8b-largectx** (Primary)
   - 100% syntax validity in Phase 1
   - Best balance of speed and resources
   - 3.31s average response time

2. **phi4:14b** (High Quality)
   - Most sophisticated query generation
   - 90% syntax validity
   - Higher VRAM usage but worth testing for complex queries

3. **qwen2.5-coder:7b** (Coding-Optimized)
   - Already downloaded during Phase 1
   - Specialized for code generation
   - Could excel at Cypher query creation

## Prompting Strategies to Test

### 1. **Minimal Template** (Baseline)
- Ultra-concise prompt (15 lines)
- Just schema and instruction
- Test if models can work with minimal guidance

### 2. **Simple Current** (Control)
- Current production template (58 lines)
- Already proven effective (90-100% validity)
- Baseline for comparison

### 3. **Enhanced Few-Shot**
- Include 3 example query pairs
- Help model understand patterns
- Expected to improve ambiguous query handling

### 4. **Chain-of-Thought (CoT)**
- Step-by-step reasoning process
- Should improve complex query generation
- May increase response time

### 5. **Self-Consistency**
- Generate 3 queries, select best
- Higher quality at cost of 3x generation time
- Good for critical queries

## Test Query Categories

### Clear Intent (2 queries)
- "Find all data team members"
- "List security policies with high severity"

### Ambiguous Requests (2 queries)
- "Show me the important people"
- "Find compliance stuff"

### Complex Multi-hop (2 queries)
- "Who are the Python experts reporting to the CTO?"
- "Find all teams affected by GDPR policies"

## Implementation Steps

### Step 1: Create Prompt Templates
Create the following templates in `/backend/prompts/`:

1. `generate_query_minimal.txt`
2. `generate_query_enhanced.txt` (with few-shot examples)
3. `generate_query_cot.txt` (chain-of-thought)

### Step 2: Fix Connection Issues
Before running Phase 2, resolve the FalkorDB connection:
```bash
# Option 1: Run from Docker container
docker exec stunning-lamp-api-1 python tools/test_phase2_prompting_strategies.py

# Option 2: Set environment variable
export FALKOR_HOST=localhost
python tools/test_phase2_prompting_strategies.py
```

### Step 3: Run Tests
Execute Phase 2 testing:
- 3 models × 5 strategies × 6 queries = 90 tests
- Estimated time: 15-30 minutes total

## Expected Outcomes

### Best Case Scenarios

1. **Few-Shot Dominance**: Enhanced few-shot template significantly improves ambiguous query handling
2. **Model Specialization**: Different models excel with different strategies
3. **CoT for Complexity**: Chain-of-thought excels at multi-hop queries

### Likely Results Based on Phase 1

- **granite3.3:8b-largectx** + Simple template: Strong baseline (already 100% syntax validity)
- **phi4:14b** + CoT: Best for complex queries
- **qwen2.5-coder:7b** + Few-shot: Potentially best overall

## Success Metrics

### Primary Metrics
1. **Syntax Validity**: Must maintain 90%+ from Phase 1
2. **Execution Success**: Target 80%+ (with proper FalkorDB connection)
3. **Response Time**: Keep under 5s average

### Secondary Metrics
1. **Ambiguity Resolution**: Improvement on unclear queries
2. **Consistency**: Low variance for same queries
3. **Token Efficiency**: Optimize prompt length vs. quality

## Risk Mitigation

1. **Connection Issues**: Test FalkorDB connectivity before full run
2. **Model Availability**: Ensure models stay loaded during tests
3. **Timeout Handling**: Set appropriate timeouts for self-consistency strategy

## Next Steps After Phase 2

Based on results:
1. **Phase 3**: Test winning combinations on production-like workload
2. **Deployment**: Update production configuration with optimal model-strategy pair
3. **Monitoring**: Track real-world performance metrics

## Quick Start Commands

```bash
# 1. Ensure Docker services are running
docker-compose ps

# 2. Create test script (if not exists)
cd /home/kyle/projects/stunning-lamp/backend
# [Create test_phase2_prompting_strategies.py]

# 3. Run Phase 2 tests
docker exec stunning-lamp-api-1 python tools/test_phase2_prompting_strategies.py

# 4. Analyze results
python tools/analyze_phase2_results.py
```

## Timeline

- Template Creation: 30 minutes
- Test Execution: 30 minutes  
- Analysis & Reporting: 15 minutes
- **Total**: ~1.5 hours

## Conclusion

Phase 2 will identify the optimal model-prompting strategy combination for production use. Based on Phase 1 results showing 90-100% syntax validity with the simple template, we expect modest improvements with advanced prompting techniques, particularly for ambiguous queries and complex multi-hop scenarios.