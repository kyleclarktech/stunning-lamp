import asyncio
import websockets
import json
import sys

async def test_query():
    """Connect to the WebSocket and test a query."""
    uri = "ws://localhost:8000/ws"
    question = "list all members of engineering"
    
    try:
        print(f"Connecting to {uri}...")
        async with websockets.connect(uri) as websocket:
            print(f"Connected! Sending: {question}")
            await websocket.send(question)
            
            # Set a timeout for receiving messages
            try:
                while True:
                    # Wait for message with timeout
                    message = await asyncio.wait_for(websocket.recv(), timeout=10.0)
                    
                    try:
                        data = json.loads(message)
                        print(f"\nReceived {data.get('type', 'unknown')} message:")
                        
                        if data.get('type') == 'query':
                            print(f"Query: {data.get('query', 'N/A')}")
                        elif data.get('type') == 'results':
                            print(f"Count: {data.get('count', 0)}")
                            if data.get('results'):
                                print("Results found!")
                                for r in data.get('results', [])[:3]:  # Show first 3
                                    print(f"  - {r.get('name', 'Unknown')} ({r.get('department', 'N/A')})")
                            else:
                                print("No results returned")
                        elif data.get('type') == 'error':
                            print(f"Error: {data.get('error', 'Unknown error')}")
                        else:
                            print(json.dumps(data, indent=2))
                            
                    except json.JSONDecodeError:
                        print(f"Non-JSON message: {message}")
                        
            except asyncio.TimeoutError:
                print("\nNo more messages received (timeout)")
            except websockets.exceptions.ConnectionClosed:
                print("\nConnection closed by server")
                
    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(test_query())