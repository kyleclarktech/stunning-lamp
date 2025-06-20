#!/usr/bin/env python3
"""Test the employee query fix on the live system"""

import asyncio
import websockets
import json

async def test_employee_query():
    uri = "ws://localhost:8000/ws"
    
    test_queries = [
        "How many employees are there?",
        "Show me all staff",
        "List developers",
        "Count managers"
    ]
    
    async with websockets.connect(uri) as websocket:
        print("Connected to WebSocket")
        
        for query in test_queries:
            print(f"\n{'='*60}")
            print(f"Testing: {query}")
            print('='*60)
            
            # Send the query
            await websocket.send(query)
            
            # Receive responses
            while True:
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                    data = json.loads(response)
                    
                    if data['type'] == 'query':
                        print(f"Generated Query: {data['data']}")
                    elif data['type'] == 'results':
                        results = data['data']
                        if isinstance(results, list) and len(results) > 0:
                            if 'count' in results[0]:
                                print(f"Count Result: {results[0]['count']}")
                            else:
                                print(f"Results Found: {len(results)} items")
                                print(f"Sample: {results[0] if results else 'No results'}")
                    elif data['type'] == 'error':
                        print(f"Error: {data['data']}")
                    elif data['type'] == 'complete':
                        break
                        
                except asyncio.TimeoutError:
                    print("Timeout waiting for response")
                    break
                except Exception as e:
                    print(f"Error: {e}")
                    break

if __name__ == "__main__":
    asyncio.run(test_employee_query())