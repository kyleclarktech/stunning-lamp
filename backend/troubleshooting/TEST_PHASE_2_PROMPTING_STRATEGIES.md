# Test Phase 2: Prompting Strategy Optimization

ultrathink use sequential thinking mcp, use memory mcp
## Objective
Test the top 3-5 models from Phase 1 with various prompting strategies to find the optimal model-strategy combination. This phase focuses on prompt engineering techniques.

## Prerequisites
- Completed Phase 1 testing
- Top 3-5 models identified from Phase 1
- Phase 1 results file available

## Input from Phase 1
Load the top models from Phase 1 results:
```python
# Example: Top 3 models from Phase 1
TOP_MODELS = [
    "granite3.3:8b-largectx",  # Fastest
    "phi4:14b",                 # Current default
    "qwen2.5-coder:7b"         # Best coding model
]
```

## Prompting Strategies to Test

### 1. Template Variations
- **Minimal** (10-20 lines): Just schema and instruction
- **Simple** (current, 58 lines): Basic schema with examples
- **Enhanced** (100 lines): Schema + reasoning guidelines
- **Structured** (150 lines): Step-by-step instructions

### 2. Prompting Techniques
- **Zero-shot**: Current approach
- **Few-shot**: Include 3 example query pairs
- **Chain-of-Thought**: Add reasoning steps
- **Self-Consistency**: Generate 3 queries, pick best

### 3. Context Variations
- **No History**: Fresh context each time
- **Recent Context**: Last 3 messages
- **Selective Context**: Only related queries

## Test Implementation

Create `tools/test_phase2_prompting_strategies.py`:

```python
#!/usr/bin/env python3
"""Phase 2: Test prompting strategies with top models."""

import asyncio
import json
from datetime import datetime
from typing import Dict, List, Any

# Test queries focused on different challenge types
STRATEGY_TEST_QUERIES = [
    # Clear intent queries
    "Find all data team members",
    "List security policies with high severity",
    
    # Ambiguous queries  
    "Show me the important people",
    "Find compliance stuff",
    
    # Complex multi-step
    "Who are the Python experts reporting to the CTO?",
    "Find all teams affected by GDPR policies"
]

# Prompting strategies to test
PROMPTING_STRATEGIES = {
    "minimal": {
        "template": "generate_query_minimal.txt",
        "lines": 15,
        "technique": "zero-shot"
    },
    "simple_current": {
        "template": "generate_query_simple.txt", 
        "lines": 58,
        "technique": "zero-shot"
    },
    "enhanced_few_shot": {
        "template": "generate_query_enhanced.txt",
        "lines": 100,
        "technique": "few-shot",
        "examples": 3
    },
    "cot_reasoning": {
        "template": "generate_query_cot.txt",
        "lines": 120,
        "technique": "chain-of-thought"
    },
    "self_consistency": {
        "template": "generate_query_simple.txt",
        "lines": 58,
        "technique": "self-consistency",
        "iterations": 3
    }
}

async def test_strategy_combination(model: str, strategy: Dict) -> Dict[str, Any]:
    """Test a specific model-strategy combination."""
    # Implementation:
    # 1. Load strategy template
    # 2. Configure technique (few-shot examples, CoT, etc.)
    # 3. Run test queries
    # 4. Measure quality and performance
    # 5. Return detailed metrics
    pass

async def main():
    """Run Phase 2 prompting strategy tests."""
    print("PHASE 2: Prompting Strategy Optimization")
    print("=" * 60)
    
    # Load top models from Phase 1
    with open("phase1_summary.json", 'r') as f:
        phase1_results = json.load(f)
        top_models = phase1_results["top_models"][:3]
    
    results = {
        "phase": 2,
        "timestamp": datetime.now().isoformat(),
        "models": top_models,
        "strategies_tested": [],
        "optimal_combinations": []
    }
    
    # Test each model-strategy combination
    for model in top_models:
        for strategy_name, strategy_config in PROMPTING_STRATEGIES.items():
            print(f"\nTesting {model} with {strategy_name}")
            result = await test_strategy_combination(model, strategy_config)
            results["strategies_tested"].append(result)
    
    # Analyze and rank combinations
    analyze_phase2_results(results)
```

## Template Examples to Create

### 1. Minimal Template (`generate_query_minimal.txt`)
```
Convert this question to a Cypher query:
"{{ user_message }}"

Schema: Person, Team, Policy, Group
Relationships: MEMBER_OF, REPORTS_TO, RESPONSIBLE_FOR

Return only the Cypher query.
```

### 2. Enhanced Few-Shot Template (`generate_query_enhanced.txt`)
```
You are a Cypher query expert. Convert natural language to graph queries.

EXAMPLES:
Q: "Who manages the data team?"
A: MATCH (p:Person)-[:MEMBER_OF {is_lead: true}]->(t:Team {name: 'Data'}) RETURN p

Q: "Find Python developers"  
A: MATCH (p:Person)-[:HAS_SKILL]->(s:Skill {name: 'Python'}) RETURN p

[Full schema details...]

Question: "{{ user_message }}"
Query:
```

### 3. Chain-of-Thought Template (`generate_query_cot.txt`)
```
Analyze this request step by step:
"{{ user_message }}"

1. Identify entities mentioned:
2. Determine relationships needed:
3. Consider filters/conditions:
4. Construct the query:

Final Cypher query:
```

## Metrics to Collect

### Quality Metrics
- **Semantic Accuracy**: Does query match intent?
- **Syntax Validity**: Is it valid Cypher?
- **Result Relevance**: Are results useful?
- **Ambiguity Handling**: How well does it handle unclear requests?

### Performance Metrics
- **Generation Time**: Time to create query
- **Token Efficiency**: Tokens used per query
- **Consistency**: Variance in results for same query

### Strategy-Specific Metrics
- **Few-shot Benefit**: Improvement over zero-shot
- **CoT Clarity**: Quality of reasoning steps
- **Self-consistency Agreement**: How often queries agree

## Expected Output

### 1. Detailed Results
`phase2_strategies_[timestamp].json` containing:
- All model-strategy combinations tested
- Performance metrics per combination
- Quality scores and examples

### 2. Optimization Report
`phase2_optimization_report.md` with:
- Best strategy per model
- Best overall combination
- Strategy effectiveness analysis
- Specific recommendations

### 3. Strategy Comparison Matrix
```
Model,Zero-shot,Few-shot,CoT,Self-Consistency,Best
granite3.3,85%,92%,88%,90%,Few-shot
phi4,90%,91%,93%,89%,CoT
```

## Execution Instructions

1. **Prepare Templates**
   ```bash
   cd backend/prompts
   # Create new template files as specified
   ```

2. **Run Phase 2**
   ```bash
   python tools/test_phase2_prompting_strategies.py \
     --top-models 3 \
     --test-all-strategies
   ```

3. **Expected Duration**
   - 3 models × 5 strategies × 6 queries = 90 tests
   - ~3-5 seconds per test
   - Total time: 5-10 minutes per model

## Success Criteria

Phase 2 is successful if:
1. Clear strategy winners emerge per model
2. Overall best combination identified
3. Performance improvements over baseline
4. Reproducible results
5. Strategy benefits quantified

## Decision Points

After Phase 2, we should know:
1. **Best Model-Strategy Pair**: Which combination to use
2. **Fallback Strategy**: Secondary option if primary fails
3. **Complexity Trade-off**: Is added complexity worth it?
4. **Production Config**: Final recommendation

## Next Step
Proceed to `TEST_PHASE_3_PRODUCTION_VALIDATION.md` with the winning configuration.