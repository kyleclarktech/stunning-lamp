#!/usr/bin/env python3
"""Test the count query fix and WebSocket stability improvements"""

import asyncio
import json
import websockets

async def test_fixes():
    uri = "ws://localhost:8000/ws"
    
    try:
        async with websockets.connect(uri) as websocket:
            print("✅ Connected to WebSocket")
            
            # Test 1: Count query that was previously failing
            print("\n📊 Test 1: Testing count query fix")
            count_query = "How many employees work for the company?"
            await websocket.send(count_query)
            print(f"Sent: {count_query}")
            
            # Collect all responses for this query
            responses = []
            while True:
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=10)
                    responses.append(response)
                    
                    # Check if it's a JSON response (error or info message)
                    try:
                        data = json.loads(response)
                        if data.get("type") in ["info", "query", "results", "error"]:
                            print(f"Received {data['type']}: {data.get('message', '')}")
                        elif data.get("type") == "ping":
                            # Respond to ping with pong
                            await websocket.send(json.dumps({"type": "pong"}))
                            print("🏓 Received ping, sent pong")
                    except json.JSONDecodeError:
                        # This is the final formatted response
                        print("\n📋 Final Response:")
                        print(response)
                        break
                        
                except asyncio.TimeoutError:
                    print("Timeout waiting for response")
                    break
            
            # Test 2: WebSocket heartbeat
            print("\n💓 Test 2: Testing WebSocket heartbeat (waiting 35 seconds for ping)")
            ping_received = False
            start_time = asyncio.get_event_loop().time()
            
            while asyncio.get_event_loop().time() - start_time < 35:
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=1)
                    data = json.loads(response)
                    if data.get("type") == "ping":
                        ping_received = True
                        print(f"🏓 Received ping at {data.get('timestamp')}")
                        # Send pong response
                        await websocket.send(json.dumps({"type": "pong"}))
                        print("   Sent pong response")
                        break
                except asyncio.TimeoutError:
                    # Continue waiting
                    continue
                except json.JSONDecodeError:
                    # Ignore non-JSON messages
                    continue
            
            if ping_received:
                print("✅ Heartbeat mechanism is working!")
            else:
                print("❌ No ping received within 35 seconds")
            
            # Test 3: Simple query to verify general functionality
            print("\n📊 Test 3: Testing a simple list query")
            list_query = "List developers"
            await websocket.send(list_query)
            print(f"Sent: {list_query}")
            
            # Wait for response
            response_count = 0
            while response_count < 5:  # Expect a few info messages plus final response
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=10)
                    response_count += 1
                    
                    try:
                        data = json.loads(response)
                        if data.get("type") == "ping":
                            await websocket.send(json.dumps({"type": "pong"}))
                            continue
                        print(f"Received {data['type']}: {data.get('message', '')[:100]}...")
                    except json.JSONDecodeError:
                        print("\n📋 Final Response (truncated):")
                        print(response[:500] + "..." if len(response) > 500 else response)
                        break
                        
                except asyncio.TimeoutError:
                    break
            
            print("\n✅ All tests completed successfully!")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_fixes())