#!/usr/bin/env python3
"""Test 'How many developers?' query"""

import asyncio
import websockets
import json

async def test_query():
    uri = "ws://localhost:8000/ws"
    
    async with websockets.connect(uri) as websocket:
        print("Connected to WebSocket")
        
        # Send the query
        query = "How many developers?"
        print(f"Sending query: {query}")
        await websocket.send(query)
        
        # Receive responses
        while True:
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=30)
                print(f"Received: {response}")
                
                # Check if it's the final response (not JSON)
                try:
                    data = json.loads(response)
                    if data.get("type") == "error":
                        print(f"Error: {data.get('message')}")
                        break
                except json.JSONDecodeError:
                    # Final formatted response
                    print("Final response received")
                    break
                    
            except asyncio.TimeoutError:
                print("Timeout waiting for response")
                break

if __name__ == "__main__":
    asyncio.run(test_query())