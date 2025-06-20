import asyncio
import websockets
import json

async def test_single_query():
    """Test a single compliance query"""
    
    query = "Which offices are SOC2 compliant?"
    uri = "ws://localhost:8000/ws"
    
    print(f"Testing query: {query}")
    print("-" * 50)
    
    try:
        async with websockets.connect(uri) as websocket:
            # Send the query
            await websocket.send(json.dumps({"message": query}))
            print("Query sent, waiting for response...")
            
            # Receive responses with shorter timeout
            start_time = asyncio.get_event_loop().time()
            while True:
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=10.0)
                    elapsed = asyncio.get_event_loop().time() - start_time
                    print(f"\n[{elapsed:.1f}s] Received response:")
                    
                    data = json.loads(response)
                    print(f"Type: {data.get('type', 'unknown')}")
                    print(f"Content: {data.get('content', 'none')}")
                    
                    if data.get("type") == "results" or data.get("status") == "completed":
                        break
                        
                except asyncio.TimeoutError:
                    print(f"\nTimeout after {asyncio.get_event_loop().time() - start_time:.1f} seconds")
                    break
                    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_single_query())