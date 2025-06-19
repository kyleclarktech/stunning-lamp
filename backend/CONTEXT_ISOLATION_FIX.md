# Context Isolation Fix for Ollama Integration

## Problem Statement

The current Ollama integration is not managing context properly, potentially causing:
- Context pollution between queries
- Inconsistent responses
- Performance degradation
- Memory bloat

## Evidence

From the logs, Ollama returns a `context` field with every response:
```json
{
  "response": "...",
  "context": [49152, 2946, 49153, ...],  // Large array of tokens
  "done": true
}
```

This context is being ignored, and Ollama may be maintaining state internally.

## Quick Fix (Immediate)

Update `call_ai_model` in `main.py` to explicitly pass an empty context:

```python
async def call_ai_model(prompt_text, websocket=None, timeout=60):
    """Call Ollama HTTP API with explicit context reset"""
    host, model = get_ollama_client()
    url = f"{host}/api/generate"
    
    payload = {
        "model": model,
        "prompt": prompt_text,
        "stream": False,
        "context": []  # ADD THIS LINE - Force empty context
    }
    # ... rest of implementation
```

## Comprehensive Solution

Create isolated context functions for each AI operation:

```python
# Add to main.py

async def call_ai_isolated(prompt_text, purpose="general", timeout=30):
    """Call AI with isolated context - no history maintained"""
    host, model = get_ollama_client()
    url = f"{host}/api/generate"
    
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            payload = {
                "model": model,
                "prompt": prompt_text,
                "stream": False,
                "context": [],  # Always start fresh
                "options": {
                    "num_predict": 500,  # Limit output length
                    "temperature": 0.1 if purpose == "query" else 0.7
                }
            }
            
            resp = await client.post(url, json=payload)
            if resp.status_code == 200:
                data = resp.json()
                return data.get('response', '')
            else:
                raise Exception(f"Ollama error: {resp.status_code}")
                
    except Exception as e:
        logging.error(f"Isolated AI call failed: {e}")
        raise

# Specific purpose functions
async def generate_query_isolated(user_message: str):
    """Generate Cypher query with isolated context"""
    prompt = load_prompt("generate_query", user_message=user_message)
    return await call_ai_isolated(prompt, purpose="query", timeout=15)

async def analyze_message_isolated(user_message: str):
    """Analyze message intent with isolated context"""
    prompt = load_prompt("analyze_message", user_message=user_message)
    return await call_ai_isolated(prompt, purpose="analysis", timeout=15)

async def format_results_isolated(user_message: str, results: dict):
    """Format results with isolated context"""
    prompt = load_prompt("format_results", 
                        user_message=user_message,
                        results=results)
    return await call_ai_isolated(prompt, purpose="formatting", timeout=20)
```

## Update WebSocket Handler

Replace existing AI calls with isolated versions:

```python
# In websocket_endpoint function

# Replace:
analysis_response = await call_ai_model(analysis_prompt, websocket)

# With:
analysis_response = await analyze_message_isolated(data)

# Replace:
cypher_query = await call_ai_model(query_prompt, websocket)

# With:
cypher_query = await generate_query_isolated(data)

# Replace:
final_response = await call_ai_model(format_prompt, websocket)

# With:
final_response = await format_results_isolated(data, results)
```

## Benefits

1. **No Context Pollution**: Each query starts fresh
2. **Consistent Results**: Same input = same output
3. **Better Performance**: No accumulated context overhead
4. **Easier Debugging**: Reproducible behavior
5. **Memory Efficient**: No growing context arrays

## Testing

Create a test to verify isolation:

```python
async def test_context_isolation():
    """Verify that context is truly isolated between calls"""
    
    # Prime with one type of query
    await generate_query_isolated("show all policies")
    
    # Test with different query - should not be influenced
    result1 = await generate_query_isolated("list engineering members")
    
    # Test same query again - should be identical
    result2 = await generate_query_isolated("list engineering members")
    
    assert result1 == result2, "Context isolation test failed"
    print("✓ Context isolation verified")
```

## Rollout Plan

1. **Phase 1**: Add `"context": []` to existing `call_ai_model` (5 min)
2. **Phase 2**: Create isolated wrapper functions (30 min)
3. **Phase 3**: Update all AI calls to use isolated functions (1 hour)
4. **Phase 4**: Add monitoring for context size/performance (optional)