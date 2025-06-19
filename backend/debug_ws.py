#!/usr/bin/env python3
import asyncio
import websockets

async def debug_websocket():
    """Debug WebSocket messages."""
    uri = "ws://localhost:8000/ws"
    query = "list all members of engineering"
    
    try:
        async with websockets.connect(uri) as websocket:
            print(f"Connected! Sending: {query}")
            await websocket.send(query)
            
            message_count = 0
            try:
                while True:
                    message = await asyncio.wait_for(websocket.recv(), timeout=8.0)
                    message_count += 1
                    print(f"\n--- Message #{message_count} (length: {len(message)}) ---")
                    print(f"Raw: {message[:200]}..." if len(message) > 200 else f"Raw: {message}")
                    
            except asyncio.TimeoutError:
                print(f"\nTimeout reached. Total messages received: {message_count}")
            except websockets.exceptions.ConnectionClosed:
                print(f"\nConnection closed. Total messages received: {message_count}")
                
    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}")

if __name__ == "__main__":
    asyncio.run(debug_websocket())