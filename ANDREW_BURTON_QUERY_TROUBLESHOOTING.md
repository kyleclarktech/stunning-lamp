# Andrew Burton Query Failure Analysis

## Summary
The query "list all available information for andrew burton" fails to return person information due to the intent processor misclassifying the request as "exploration" instead of "information_gathering" about a specific person.

## Root Cause
1. **Intent Processor Path Issue**: When the intent processor runs from certain directories (like tools/), it cannot find `prompts/understand_intent.txt` due to relative path resolution
2. **Fallback Parsing**: Without the prompt file, the system falls back to basic parsing that:
   - Classifies the query as "exploration" (confidence: 0.2)
   - Sets information depth to "detailed_explanation" instead of "comprehensive"
   - Misses the person-specific context

## Impact on Query Pipeline

### 1. Intent Misclassification
```
ACTUAL (Fallback):
- Primary Intent: exploration
- Actual Goal: Explore topic: list all available information for andrew burton
- Confidence: 0.2

EXPECTED:
- Primary Intent: information_gathering  
- Actual Goal: Get comprehensive information about person 'Andrew Burton'
- Confidence: 0.8+
```

### 2. Tool Selection Impact
With "exploration" intent, the system may:
- Route to wrong tool (generic exploration vs person search)
- Generate less specific Cypher queries
- Miss implicit information needs (contact info, manager, skills)

### 3. Query Generation Impact
- Exploration queries are broader and less focused
- Person-specific optimizations (CONTAINS matching, relationship traversal) may not be applied
- Fallback queries may not trigger when no results found

## Testing the Issue

### Check if Andrew Burton exists:
```bash
docker exec -it stunning-lamp-falkordb-1 redis-cli
> GRAPH.QUERY agent_poc "MATCH (p:Person) WHERE p.name CONTAINS 'Burton' RETURN p.name"
```

### Test with Docker services running:
```bash
# This would work correctly with all services running
docker exec -it stunning-lamp-api-1 python -c "
import asyncio
from main import process_message
asyncio.run(process_message('list all available information for andrew burton', None))
"
```

## Solutions

### 1. Immediate Fix - Path Resolution
Update `intent_processor.py` line 207:
```python
# Change from:
prompt_path = Path("prompts/understand_intent.txt")

# To:
import os
base_dir = Path(os.path.dirname(os.path.abspath(__file__)))
prompt_path = base_dir / "prompts" / "understand_intent.txt"
```

### 2. Robust Fallback
Enhance fallback parsing for person queries:
```python
def _create_fallback_intent(self, user_message: str) -> UserIntent:
    # Detect person-specific patterns
    person_patterns = [
        "information for", "info about", "details on", 
        "find", "show me", "who is", "profile"
    ]
    
    if any(pattern in user_message.lower() for pattern in person_patterns):
        # Extract potential name (last 2-3 words)
        words = user_message.split()
        potential_name = " ".join(words[-2:])
        
        return UserIntent(
            primary_intent=PrimaryIntent.INFORMATION_GATHERING,
            actual_goal=f"Get information about person '{potential_name}'",
            confidence=0.6,
            information_depth=InformationDepth.COMPREHENSIVE,
            # ... other fields
        )
```

### 3. Direct Query Override
Add person-specific patterns to `analyze_message.txt`:
```
# Add to QUICK PERSON LOOKUPS section
- "list all available information for [name]"
- "get complete profile for [name]"
- "show everything about [name]"
```

## Verification Steps

1. **Confirm person exists in database**
2. **Fix intent processor path resolution**
3. **Test query with corrected intent parsing**
4. **Verify proper tool selection (search_database or custom_query)**
5. **Check generated Cypher query includes comprehensive fields**

## Prevention

1. **Add integration tests** for person lookup queries
2. **Include path resolution tests** in CI/CD
3. **Add confidence threshold alerts** when intent parsing falls below 0.5
4. **Create person-specific test cases** in query generation tests

## Note on Test Data
Andrew Burton does not exist in the seeded test data. All person names are randomly generated using Faker library. To test person queries reliably:
1. Query the database first to find existing person names
2. Use those actual names in test queries
3. Or manually add test persons with known names