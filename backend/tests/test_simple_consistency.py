#!/usr/bin/env python3
import asyncio
import websockets
import json

async def get_generated_query(query_text):
    """Get the generated Cypher query for a given input."""
    uri = "ws://localhost:8000/ws"
    
    try:
        async with websockets.connect(uri) as websocket:
            await websocket.send(query_text)
            
            # Collect messages
            messages = []
            try:
                for _ in range(5):  # Collect up to 5 messages
                    message = await asyncio.wait_for(websocket.recv(), timeout=2.0)
                    try:
                        data = json.loads(message)
                        messages.append(data)
                        if data.get('type') == 'query':
                            # Extract Cypher query
                            msg = data.get('message', '')
                            if '`' in msg:
                                start = msg.find('`') + 1
                                end = msg.rfind('`')
                                if start < end:
                                    return msg[start:end]
                    except json.JSONDecodeError:
                        pass
            except asyncio.TimeoutError:
                pass
                
            # Return None if no query found
            return None
            
    except Exception as e:
        print(f"Error: {e}")
        return None

async def test_consistency():
    """Test if the same query produces the same result multiple times."""
    
    test_query = "list all members of engineering"
    print(f"Testing consistency for: '{test_query}'")
    print("="*60)
    
    # Run the same query 5 times
    results = []
    for i in range(5):
        print(f"\nAttempt {i+1}:")
        result = await get_generated_query(test_query)
        if result:
            print(f"✓ Generated: {result[:80]}...")
            results.append(result)
        else:
            print("✗ Failed to get query")
            results.append(None)
        
        # Small delay between requests
        await asyncio.sleep(0.5)
    
    # Check consistency
    print("\n" + "="*60)
    print("CONSISTENCY CHECK:")
    
    # Filter out None values
    valid_results = [r for r in results if r is not None]
    
    if not valid_results:
        print("❌ All attempts failed!")
        return False
    
    # Check if all valid results are identical
    unique_results = set(valid_results)
    
    if len(unique_results) == 1:
        print(f"✅ CONSISTENT: All {len(valid_results)} successful attempts produced the same query")
        print(f"Query: {list(unique_results)[0]}")
        return True
    else:
        print(f"❌ INCONSISTENT: {len(unique_results)} different queries generated:")
        for i, query in enumerate(unique_results):
            print(f"  {i+1}. {query}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_consistency())
    print("\n" + "="*60)
    print(f"Test Result: {'PASS' if success else 'FAIL'}")
    exit(0 if success else 1)