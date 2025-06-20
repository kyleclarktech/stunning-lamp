#!/usr/bin/env python3
import asyncio
import websockets
import json

async def test_query():
    uri = "ws://localhost:8000/ws"
    async with websockets.connect(uri) as websocket:
        # Send a simple test query
        query = {"message": "who works on mobile?"}
        await websocket.send(json.dumps(query))
        print(f"Sent query: {query['message']}")
        
        # Receive responses
        while True:
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=30.0)
                if not response:
                    continue
                try:
                    data = json.loads(response)
                except json.JSONDecodeError:
                    print(f"Failed to parse response: {response}")
                    continue
                print(f"Response type: {data.get('type')}")
                if data.get('type') == 'query':
                    print(f"Generated query: {data.get('query')}")
                elif data.get('type') == 'results':
                    print(f"Got {len(data.get('results', []))} results")
                elif data.get('type') == 'error':
                    print(f"Error: {data.get('message')}")
                elif data.get('type') == 'complete':
                    print("Query completed!")
                    break
            except asyncio.TimeoutError:
                print("Timeout waiting for response")
                break

asyncio.run(test_query())