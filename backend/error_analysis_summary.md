# Error Analysis Summary - Comprehensive Evaluation Results

## Overview
- **Total unique errors**: 78
- **Total error occurrences**: 107
- **Files analyzed**: 12 comprehensive evaluation JSON files

## Top Error Categories

### 1. **ShortestPaths Limitation** (11 occurrences)
- **Error**: "FalkorDB currently only supports shortestPaths in WITH or RETURN clauses"
- **Models affected**: codeqwen_7b, granite3.3_8b, granite3.3_8b-largectx, llama3.2_3b, qwen2.5-coder_7b
- **Query categories**: ambiguous_requests, complex_patterns, multi_hop_relationships, organizational_insights, path_finding
- **Example query**: "What's the reporting chain from junior developers to the CEO?"
- **Issue**: Models attempting to use shortestPath() in MATCH clauses instead of WITH/RETURN

### 2. **Multi-Statement Query** (11 occurrences)
- **Error**: "Error: query with more than one statement is not supported"
- **Models affected**: deepseek-coder_1.3b, granite3.3_8b, llama3.2_3b
- **Query categories**: aggregations, ambiguous_requests, complex_patterns, edge_cases, filtered_searches
- **Example**: Queries containing multiple semicolons or attempting to execute multiple statements
- **Issue**: Models generating queries with multiple statements separated by semicolons

### 3. **Unknown Function Errors** (19 total)
- **lower** (9 occurrences): Models using `lower()` instead of `toLower()`
  - Affected: codeqwen_7b, deepseek-coder_1.3b, granite-code_8b, llama3.2_3b, qwen2.5-coder_7b
- **date** (4 occurrences): Using `date()` function which doesn't exist in FalkorDB
  - Affected: granite-code_8b, granite3.3_8b, phi4_14b, qwen2.5-coder_7b
- **LOWER** (3 occurrences): Uppercase variant of the function name issue
- **Other functions**: year, datetime, filters, locate, single, apoc.coll.contains

### 4. **Filtered Alias Resolution** (9 occurrences)
- **Error**: "Unable to resolve filtered alias"
- **Models affected**: codeqwen_7b, granite-code_8b, granite3.3_8b, granite3.3_8b-largectx, mistral_7b, qwen2.5-coder_7b
- **Common pattern**: Using `size((t)<-[:MEMBER_OF]-(:Person))` in WHERE clauses
- **Example**: "Which teams have more than 10 members?"

### 5. **Syntax Errors** (Various)
- **Invalid input errors**: Multiple variations of syntax errors with specific characters
- **Common issues**:
  - Using SQL syntax instead of Cypher (SELECT statements)
  - Incorrect relationship syntax
  - Missing or extra punctuation
  - Invalid property access patterns

### 6. **Undefined Variables** (5 occurrences)
- Variables like 'p', 'v', 't', 'team', 'col', 'securityPerson' not properly defined
- **Models affected**: llama3.2_3b, mistral_7b, phi4_14b, granite3.3_8b-largectx
- **Issue**: Using variables before they're defined in MATCH clauses

### 7. **Aggregation Issues** (2 occurrences)
- **Error**: "Invalid use of aggregating function"
- **Model affected**: mistral_7b
- **Issue**: Using `count()` in WHERE clauses instead of WITH clauses

### 8. **WITH Clause Issues** (2 occurrences)
- **Error**: "WITH clause projections must be aliased"
- **Model affected**: granite-code_8b
- **Issue**: Not providing aliases for expressions in WITH clauses

## Model-Specific Issues

### deepseek-coder_1.3b
- Generates invalid syntax frequently
- Sometimes outputs explanatory text instead of Cypher
- Issues with proper relationship syntax

### codeqwen_7b
- Occasionally generates SQL instead of Cypher
- Uses non-existent APOC procedures
- Multi-statement query issues

### llama3.2_3b
- Function name case sensitivity issues
- Complex syntax errors with non-existent keywords (LOAD RECURSION)
- Variable scope problems

### granite3.3_8b & granite3.3_8b-largectx
- ShortestPath placement issues
- Complex syntax errors with property access
- Multi-statement query problems

### phi4_14b
- Generally better performance but still has:
  - Unknown function issues (date, single)
  - Variable scope problems
  - UNION clause structure issues

## Recommendations

1. **Prompt Engineering**:
   - Explicitly mention to use `toLower()` instead of `lower()`
   - Clarify that shortestPath must be used in WITH or RETURN clauses
   - Emphasize single-statement queries only

2. **Schema Clarification**:
   - Provide clear examples of proper aggregation usage
   - Show correct patterns for counting related nodes

3. **Model Selection**:
   - phi4_14b and granite3.3_8b-largectx show better overall accuracy
   - Avoid deepseek-coder_1.3b for complex queries

4. **Validation Layer**:
   - Implement pre-execution validation for common issues
   - Function name mapping (lower → toLower)
   - Multi-statement detection and prevention