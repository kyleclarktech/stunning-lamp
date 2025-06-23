# Comprehensive Model Evaluation Prompt

## Overview

This evaluation tests the top 3 models (deepseek-coder:1.3b, llama3.2:3b, qwen2.5-coder:7b) on their ability to translate complex organizational queries into FalkorDB-compatible Cypher queries with actual execution and result validation.

## How to Run the Evaluation

### Option 1: Run Inside Docker (Recommended)
This ensures proper FalkorDB connectivity:

```bash
# From your host machine
docker exec -it stunning-lamp-api-1 python tools/comprehensive_model_evaluation.py
```

### Option 2: Run with Environment Variable
If you must run from host:

```bash
cd /home/kyle/projects/stunning-lamp/backend
export FALKOR_HOST=localhost
python tools/comprehensive_model_evaluation.py
```

## What This Evaluation Tests

### 1. Query Categories (30 test queries total)

#### Simple Lookups (3 queries)
- Basic entity retrieval
- Department/team listings
- Location-based searches

#### Filtered Searches (3 queries)
- Multi-criteria filtering
- Skill combinations
- Policy severity filters

#### Aggregations (3 queries)
- Counting and grouping
- Statistical calculations
- Distribution analysis

#### Multi-hop Relationships (3 queries)
- Indirect reporting structures
- Cross-entity relationships
- Client-team-project connections

#### Path Finding (3 queries)
- Shortest path algorithms
- Reporting chains
- Collaboration networks

#### Complex Patterns (3 queries)
- Circular dependencies
- Unique skill identification
- Gap analysis

#### Ambiguous Requests (3 queries)
- "Important people"
- "Problematic areas"
- Informal language handling

#### Organizational Insights (3 queries)
- Bus factor analysis
- Compliance violations
- Knowledge silos

#### Edge Cases (3 queries)
- Name variations
- Impact analysis
- Emoji handling

### 2. Evaluation Metrics

#### Primary Metrics
- **Syntax Validity**: Is the generated Cypher syntactically correct?
- **Execution Success**: Does the query run without errors?
- **Has Results**: Does the query return meaningful data?
- **Pattern Match**: Does the query structure match expected patterns?

#### Performance Metrics
- **Generation Time**: How fast is query generation?
- **Execution Time**: How fast does the query run?
- **Overall Score**: Weighted combination of all metrics

#### Quality Assessments
- **Complexity Appropriateness**: Does query complexity match the request?
- **Ambiguity Handling**: How well are unclear requests interpreted?
- **Result Relevance**: Are the results useful for the query intent?

### 3. Expected Outputs

The evaluation generates:

1. **Individual Model Reports**: 
   - `comprehensive_eval_[model]_[timestamp].json`
   - Detailed results for each query

2. **Comparative Analysis**:
   - `comprehensive_evaluation_final_[timestamp].json`
   - Side-by-side model comparison

3. **Markdown Report**:
   - `comprehensive_evaluation_report_[timestamp].md`
   - Human-readable summary with rankings

## Sample Output Format

```
COMPREHENSIVE MODEL EVALUATION
================================================================================

[SIMPLE_LOOKUPS]
1. Who is the CTO?
   Generated: MATCH (p:Person {role: 'CTO'}) RETURN p.name, p.email...
   Generation time: 0.85s
   Execution: βœ" (0.12s)
   Results: 1 rows

[Final Rankings]
1. deepseek-coder:1.3b - Score: 87.5/100
   Syntax Valid: 30/30 (100%)
   Execution Success: 28/30 (93%)
   Pattern Matches: 26/30 (87%)
   Avg Generation Time: 0.92s

2. qwen2.5-coder:7b - Score: 85.0/100
   ...
```

## Key Features of This Evaluation

1. **Real Execution**: Actually runs queries against FalkorDB
2. **Pattern Validation**: Checks if queries match expected structures
3. **Complexity Analysis**: Ensures appropriate query complexity
4. **Ambiguity Testing**: Tests handling of unclear requests
5. **Performance Measurement**: Both generation and execution timing
6. **Category Scoring**: Performance breakdown by query type

## Why This Evaluation Matters

This comprehensive test will reveal:
- Which model best understands organizational query intent
- How well each model handles ambiguous requests
- Real-world performance characteristics
- Edge case handling capabilities
- The best model for production deployment

## Expected Results

Based on Phase 1 testing, we expect:
- **deepseek-coder:1.3b**: Fastest generation, may excel at simple queries
- **llama3.2:3b**: Balanced performance across categories
- **qwen2.5-coder:7b**: Best at complex queries, slightly slower

This evaluation will confirm or challenge these expectations with real execution data.