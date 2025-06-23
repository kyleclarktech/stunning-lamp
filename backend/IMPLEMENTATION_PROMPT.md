# Implementation Task: Fix FalkorDB Query Generation Failures
ultrathink use sequential thinking mcp, use memory mcp                                            
## Context
We've completed a comprehensive evaluation of 9 AI models generating Cypher queries for FalkorDB. The best model (granite3.3:8b-largectx) achieves only 70.4% success rate. We've identified clear failure patterns and need to implement solutions to improve query generation success rates to 85-90%.

## Current State
- **Location**: `/home/kyle/projects/stunning-lamp/backend/`
- **Best Model**: granite3.3:8b-largectx (70.4% success)
- **Current Setup**: USE_SIMPLE_PROMPTS=true, Ollama integration
- **Evaluation Tool**: `tools/comprehensive_model_evaluation.py`
- **Failure Analysis**: `FAILURE_THEME_ANALYSIS.md`

## Top 5 Failure Patterns Identified

1. **Function Name Mismatches (18% of failures)**
   - `lower()` → `toLower()`
   - `LOWER()` → `toLower()`
   - `date()`, `year()`, `datetime()` → Not supported

2. **Multi-Statement Queries (10% of failures)**
   - Queries with multiple semicolons
   - Comments after semicolons

3. **ShortestPath Placement (10% of failures)**
   - Must be in WITH or RETURN, not MATCH

4. **Complex Filtering (8% of failures)**
   - Filtered alias resolution issues
   - Size calculations with patterns

5. **Aggregation Misuse**
   - COUNT() in WHERE instead of WITH

## Implementation Tasks

### Task 1: Update Query Generation Prompts
**File**: `backend/prompts/generate_query.txt`
- Add FalkorDB-specific rules section
- Include function mapping guidance
- Add examples of correct vs incorrect syntax
- Emphasize single-statement requirement

### Task 2: Create Query Post-Processing Layer
**New File**: `backend/query_processor.py`
- Function to fix common function names
- Remove extra semicolons and comments
- Fix shortestPath placement
- Validate variable definitions

### Task 3: Implement Query Validation
**New File**: `backend/query_validator.py`
- Check for multiple semicolons
- Verify all variables are defined
- Check aggregation function usage
- Validate FalkorDB function names

### Task 4: Add Fallback Strategies
**Update**: `backend/main.py`
- Implement retry logic with simplified queries
- Add query rewriting for common failures
- Create fallback patterns for complex queries

### Task 5: Test Implementation
**Update**: `backend/tools/comprehensive_model_evaluation.py`
- Add post-processing to evaluation pipeline
- Re-run evaluation to measure improvement
- Document success rate changes

## Expected Outcomes
- Increase success rate from 70.4% to 85-90%
- Reduce function name errors by 95%
- Eliminate multi-statement query errors
- Handle complex queries with fallback strategies

## Key Files to Reference
1. `backend/main.py` - Main query execution logic
2. `backend/prompts/generate_query.txt` - Current prompt template
3. `backend/tools/comprehensive_model_evaluation.py` - Testing framework
4. `backend/FAILURE_THEME_ANALYSIS.md` - Detailed error analysis

## Testing Command
```bash
docker exec -it stunning-lamp-api-1 python tools/comprehensive_model_evaluation.py
```

## Success Metrics
- Function name errors: 0
- Multi-statement errors: 0
- Overall success rate: >85%
- No regression in query generation speed

Please implement these solutions focusing on practical fixes that can be deployed quickly. Start with Task 1 (updating prompts) as it requires no code changes and can provide immediate improvement.