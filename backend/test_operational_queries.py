#!/usr/bin/env python3
"""Test operational queries for Phase 3 (24/7 Operations Support)"""

import asyncio
import websockets
import json
import sys

async def test_query(uri, query):
    """Send a query and print the response"""
    print(f"\n🔍 Query: {query}")
    print("-" * 60)
    
    async with websockets.connect(uri) as websocket:
        # Send the query
        await websocket.send(query)
        
        # Read responses until we get a complete result
        messages = []
        while True:
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=30)
                data = json.loads(response)
                messages.append(data)
                
                # If we get results or an error, we're done
                if data['type'] in ['results', 'error']:
                    break
                    
            except asyncio.TimeoutError:
                print("⏱️  Timeout waiting for response")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                break
        
        # Display all messages
        for msg in messages:
            if msg['type'] == 'info':
                print(f"ℹ️  {msg['data']}")
            elif msg['type'] == 'query':
                print(f"🔧 Query: {msg['data'][:100]}...")
            elif msg['type'] == 'results':
                print(f"✅ Results:")
                print(msg['data'])
            elif msg['type'] == 'error':
                print(f"❌ Error: {msg['data']}")

async def main():
    uri = "ws://localhost:8000/ws"
    
    # Test queries for Phase 3
    queries = [
        "Who's on call right now?",
        "Show P0 incidents from the last 7 days",
        "What's the on-call schedule for EMEA next week?",
        "Which services had the most incidents?",
        "Show incident response times by severity",
        "Who responded to the most incidents last month?",
        "Show team handoffs for today",
        "Find coverage gaps in the next 7 days",
        "What incidents are currently open?",
        "Show escalation path for P0 incidents in APAC"
    ]
    
    print("🚀 Testing Phase 3 Operational Queries")
    print("=" * 60)
    
    for query in queries:
        try:
            await test_query(uri, query)
        except Exception as e:
            print(f"❌ Failed to test query '{query}': {e}")
        
        # Small delay between queries
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())