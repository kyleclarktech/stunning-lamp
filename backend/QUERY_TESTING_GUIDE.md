# Query Testing Guide

This guide explains how to test and troubleshoot the Cypher query generation system.

## Overview

The system converts natural language queries to Cypher queries through:
1. **AI Analysis** - Determines intent using `analyze_message.txt` prompt
2. **Query Generation** - Creates Cypher using `generate_query.txt` prompt  
3. **Execution** - Runs against FalkorDB with 15-second timeout
4. **Fallback** - Generates broader query if no results using `fallback_query.txt`
5. **Formatting** - Presents results using `format_results.txt` prompt

## Testing Tools

### 1. Comprehensive Test Suite (`test_query_system.py`)

Automated testing of various query patterns:

```bash
cd backend
python test_query_system.py
```

**Features:**
- Tests 20+ query patterns across 6 categories
- Validates query generation, execution, and results
- Tracks success rates and execution times
- Logs all queries and responses
- Generates detailed JSON report

**Test Categories:**
- **Basic Entity** - Simple lookups: "find John Smith", "show all teams"
- **Relationship** - Traversals: "who's on Platform team", "who reports to VP"
- **Complex** - Multi-condition: "senior engineers in Platform team"
- **Aggregation** - Counts/stats: "how many people per department"
- **Edge Cases** - No results, typos, ambiguous queries
- **Fallback** - Triggers broader search when overly specific

### 2. Interactive Debug Tool (`debug_query_tool.py`)

Manual query testing and troubleshooting:

```bash
cd backend
python debug_query_tool.py --interactive
```

**Commands:**
- Direct Cypher: `MATCH (p:Person) RETURN p.name LIMIT 5`
- Natural language: `nl: who's on the security team?`
- Explain plan: `explain: MATCH (p:Person) RETURN p`
- Validate schema: `validate`
- Test patterns: `patterns`

**CLI Options:**
```bash
# Execute single query
python debug_query_tool.py -q "MATCH (t:Team) RETURN count(t)"

# Test natural language conversion
python debug_query_tool.py --nl "find security policies"

# Validate schema
python debug_query_tool.py --validate

# Test common patterns
python debug_query_tool.py --patterns
```

### 3. Data Validator (`validate_data.py`)

Ensures database integrity:

```bash
cd backend
python validate_data.py
```

**Validates:**
- Node counts within expected ranges
- Required properties are non-null
- Relationship consistency
- Business rules (e.g., everyone has a team)
- No circular hierarchies
- Balanced data distribution

**Output:**
- Issues that must be fixed
- Warnings for potential problems
- Suggested Cypher fixes
- JSON validation report

## Common Query Patterns

### 1. Person Queries

```cypher
-- Find by name
MATCH (p:Person) WHERE p.name CONTAINS 'Smith' RETURN p

-- Find by department
MATCH (p:Person) WHERE p.department = 'Engineering' RETURN p

-- Find by role
MATCH (p:Person) WHERE p.role CONTAINS 'Senior' RETURN p

-- Find with manager
MATCH (p:Person)-[:REPORTS_TO]->(m:Person) 
WHERE m.name = 'John Smith' 
RETURN p
```

### 2. Team Queries

```cypher
-- Team members
MATCH (p:Person)-[:MEMBER_OF]->(t:Team {name: 'Core Platform'})
RETURN p.name, p.role

-- Team leads  
MATCH (p:Person)-[r:MEMBER_OF]->(t:Team)
WHERE r.is_lead = true
RETURN t.name, p.name

-- Teams by department
MATCH (t:Team) WHERE t.department = 'Engineering'
RETURN t.name, t.focus
```

### 3. Policy Queries

```cypher
-- Policies by category
MATCH (p:Policy) WHERE p.category = 'security'
RETURN p.name, p.severity

-- Policy owners
MATCH (owner)-[:RESPONSIBLE_FOR]->(p:Policy)
WHERE p.name CONTAINS 'Data'
RETURN labels(owner), owner.name, p.name

-- Critical policies
MATCH (p:Policy) WHERE p.severity = 'critical'
RETURN p.name, p.responsible_type
```

### 4. Complex Queries

```cypher
-- Cross-functional members
MATCH (p:Person)-[:MEMBER_OF]->(t:Team),
      (p)-[:MEMBER_OF]->(g:Group)
WHERE t.department = 'Engineering' 
  AND g.type = 'governance'
RETURN DISTINCT p.name

-- Hierarchy depth
MATCH path = (p:Person)-[:REPORTS_TO*]->(top:Person)
WHERE NOT (top)-[:REPORTS_TO]->()
RETURN p.name, length(path) as levels

-- Department statistics
MATCH (p:Person)
RETURN p.department, 
       count(p) as people,
       count(DISTINCT p.role) as roles
ORDER BY people DESC
```

## Troubleshooting Guide

### Query Generation Issues

**Problem:** Natural language not converting to correct Cypher
```bash
# Debug with interactive tool
python debug_query_tool.py -i
> nl: find the security team lead

# Check what prompt is sent
# Review backend/prompts/generate_query.txt
```

**Solutions:**
- Update prompt templates with more examples
- Add specific patterns to `analyze_message.txt`
- Check if schema in prompts matches actual database

### No Results Issues

**Problem:** Valid query returns empty results
```bash
# Test query directly
python debug_query_tool.py -q "MATCH (t:Team {name: 'Security'}) RETURN t"

# Check if fallback triggers
python test_websocket.py
# Send: "find the Underwater Basketweaving team"
```

**Solutions:**
- Verify data exists: `python validate_data.py`
- Check exact property values in database
- Test if fallback query is broader enough

### Performance Issues

**Problem:** Queries timing out
```bash
# Check execution plan
python debug_query_tool.py -i
> explain: MATCH (p:Person)-[:REPORTS_TO*]->(m) RETURN p, m
```

**Solutions:**
- Add LIMIT clauses
- Create indexes for frequently searched properties
- Simplify complex traversals
- Increase timeout in `main.py:execute_custom_query`

### Schema Mismatches

**Problem:** Generated queries use wrong property names
```bash
# Validate schema
python debug_query_tool.py --validate

# Compare with prompts
grep -n "Node Types:" backend/prompts/*.txt
```

**Solutions:**
- Update prompt files with correct schema
- Regenerate seed data if schema changed
- Ensure all prompts use consistent property names

## Best Practices

### 1. Testing New Query Patterns

1. Add test case to `test_query_system.py`
2. Run single test first with debugger
3. Verify generated Cypher is correct
4. Check results match expectations
5. Add to documentation

### 2. Debugging Failed Queries

1. Enable debug logging in `main.py`
2. Run `test_websocket.py` with problem query
3. Check logs for:
   - Generated Cypher query
   - Execution errors
   - Fallback attempts
4. Test query directly with debug tool
5. Validate data exists

### 3. Performance Testing

1. Use `debug_query_tool.py` to time queries
2. Test with different data sizes
3. Monitor timeout rates in test suite
4. Profile slow queries with EXPLAIN
5. Add indexes for common searches

## Query Pattern Examples

### Task-Oriented Queries
These should trigger policy/ownership lookups:
- "I need to implement authentication"
- "Who approves security changes?"
- "What's required for GDPR compliance?"
- "Starting a new ML project"

### Organizational Queries
These should use relationship traversals:
- "Who reports to the CTO?"
- "Find team leads in Engineering"
- "Show me Sarah's team members"
- "Who works with John?"

### Search Queries
These should use full-text search or filters:
- "Find security policies"
- "Search for data privacy"
- "Show engineering teams"
- "List senior developers"

## Monitoring Query Health

### Success Metrics
- Query success rate > 90%
- Average execution time < 2s
- Fallback usage < 20%
- Validation warnings = 0

### Key Indicators
```bash
# Run full test suite
python test_query_system.py

# Check test summary for:
# - Success rate by query type
# - Which patterns fail most
# - Average execution times
# - Fallback trigger rate
```

### Regular Validation
```bash
# Weekly data check
python validate_data.py

# Query pattern testing  
python test_query_system.py

# Manual spot checks
python debug_query_tool.py --patterns
```