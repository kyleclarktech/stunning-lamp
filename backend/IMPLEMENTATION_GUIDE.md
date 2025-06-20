# Implementation Guide: Fixing "How many employees are there?" Query

## Quick Fix

To immediately fix the query issue, update `/home/kyle/projects/stunning-lamp/backend/main.py`:

```python
# Line ~40-50 (find the import)
# Change from:
from query_patterns import match_and_generate_query

# To:
from query_patterns_improved import match_and_generate_query
```

## Complete Implementation Steps

### 1. Backup Current Files
```bash
cp backend/query_patterns.py backend/query_patterns.py.bak
cp backend/prompts/generate_query.txt backend/prompts/generate_query.txt.bak
```

### 2. Apply Pattern Matcher Update
```bash
# Option A: Rename improved file
mv backend/query_patterns_improved.py backend/query_patterns.py

# Option B: Update import in main.py (recommended)
# Edit main.py and change the import as shown above
```

### 3. Update Query Generation Prompt
```bash
cp backend/prompts/generate_query_improved.txt backend/prompts/generate_query.txt
```

### 4. Test the Fix
```bash
# Test the specific query
python backend/test_employee_query_fix.py

# Run comprehensive tests
python backend/test_semantic_queries.py
```

### 5. Rebuild and Deploy
```bash
docker-compose down
docker-compose up -d --build
```

### 6. Verify in UI
1. Navigate to http://localhost:5173
2. Connect to WebSocket
3. Test queries:
   - "How many employees are there?" → Should return 625
   - "List all staff" → Should list Person nodes
   - "Show me all developers" → Should list engineering roles

## What This Fixes

### Before (Incorrect)
- Query: "How many employees are there?"
- Searches for: `role CONTAINS 'employee'`
- Result: 0 (no roles contain the word "employee")

### After (Correct)
- Query: "How many employees are there?"
- Searches for: ALL Person nodes
- Result: 625 (total number of people in the database)

## Additional Improvements

The framework also improves:
- "List all staff/people/workforce" → Lists all Person nodes
- "Show me developers" → Finds all engineering roles
- "Count managers" → Counts leadership roles
- "Engineers in Data Platform" → Combines role and department filters

## Rollback Instructions

If needed, restore original files:
```bash
cp backend/query_patterns.py.bak backend/query_patterns.py
cp backend/prompts/generate_query.txt.bak backend/prompts/generate_query.txt
docker-compose up -d --build
```

## Monitoring

Watch for improved query matching:
```bash
docker-compose logs -f api | grep "Matched pattern"
```

## Next Steps

1. Monitor query performance and accuracy
2. Add more semantic mappings as needed
3. Consider implementing the streaming and caching improvements from FUTURE_IMPROVEMENTS_PROMPT.md