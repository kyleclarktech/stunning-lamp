#!/usr/bin/env python3
import asyncio
import websockets
import json

async def test_queries():
    """Test both engineering queries to verify the fix."""
    uri = "ws://localhost:8000/ws"
    
    queries = [
        "how many people in engineering?",
        "list all members of engineering"
    ]
    
    for query in queries:
        print(f"\n{'='*60}")
        print(f"Testing: {query}")
        print('='*60)
        
        try:
            async with websockets.connect(uri) as websocket:
                await websocket.send(query)
                
                results_found = False
                
                # Collect all messages until connection closes or timeout
                try:
                    while True:
                        message = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                        data = json.loads(message)
                        
                        if data.get('type') == 'info':
                            print(f"Info: {data.get('message', '')}")
                        elif data.get('type') == 'query':
                            print(f"Query executed: {data.get('query', 'N/A')[:100]}...")
                        elif data.get('type') == 'results':
                            count = data.get('count', 0)
                            results = data.get('results', [])
                            print(f"\n✅ Results Count: {count}")
                            
                            if results:
                                results_found = True
                                print("\nFirst 5 results:")
                                for i, r in enumerate(results[:5]):
                                    print(f"  {i+1}. {r.get('p.name', 'Unknown')} - {r.get('p.role', 'N/A')}")
                            else:
                                print("❌ No results in response")
                                
                        elif data.get('type') == 'formatted_results':
                            if results_found:
                                print(f"\n📝 Formatted response preview:")
                                print(data.get('content', '')[:200] + "...")
                            
                except (asyncio.TimeoutError, websockets.exceptions.ConnectionClosed):
                    pass
                    
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_queries())