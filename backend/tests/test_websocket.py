
import asyncio
import websockets
import json

async def test_query():
    """Connect to the WebSocket and test a query."""
    uri = "ws://localhost:8000/ws"
    try:
        async with websockets.connect(uri) as websocket:
            # Send a question that should trigger a database query
            question = "how many people in engineering?"
            print(f"> Sending question: {question}")
            await websocket.send(question)
            
            # Receive and print all responses
            print("< Receiving responses:")
            try:
                while True:
                    message = await websocket.recv()
                    try:
                        # Try to parse and pretty-print JSON
                        data = json.loads(message)
                        print(json.dumps(data, indent=2))
                    except json.JSONDecodeError:
                        # If it's not JSON, print as is
                        print(message)
            except websockets.exceptions.ConnectionClosed:
                print("< Connection closed.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(test_query())
