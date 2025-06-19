#!/usr/bin/env python3
import asyncio
import websockets
import json
import re

async def test_engineering_query():
    """Test the engineering query and parse results properly."""
    uri = "ws://localhost:8000/ws"
    query = "list all members of engineering"
    
    try:
        async with websockets.connect(uri) as websocket:
            print(f"Testing: {query}")
            await websocket.send(query)
            
            messages_received = []
            
            try:
                while True:
                    message = await asyncio.wait_for(websocket.recv(), timeout=10.0)
                    
                    # Try to parse as JSON first
                    try:
                        data = json.loads(message)
                        messages_received.append(data)
                        
                        if data.get('type') == 'info':
                            print(f"✓ Info: {data.get('message', '')}")
                            
                        elif data.get('type') == 'query':
                            query_msg = data.get('message', '')
                            # Extract the actual query from the markdown
                            match = re.search(r'`([^`]+)`', query_msg)
                            if match:
                                print(f"✓ Query executed: {match.group(1)[:80]}...")
                            
                        elif data.get('type') == 'results':
                            results_msg = data.get('message', '')
                            # Extract row count from the message
                            count_match = re.search(r'\((\d+) rows\)', results_msg)
                            if count_match:
                                count = int(count_match.group(1))
                                print(f"\n✅ Found {count} engineering team members!")
                                
                                # Extract first few names from the table
                                lines = results_msg.split('\n')
                                data_lines = [l for l in lines if l.startswith('| person_')]
                                if data_lines:
                                    print("\nFirst 5 members:")
                                    for i, line in enumerate(data_lines[:5]):
                                        # Parse the table row
                                        parts = [p.strip() for p in line.split('|') if p.strip()]
                                        if len(parts) >= 4:
                                            name = parts[1]
                                            role = parts[3]
                                            print(f"  {i+1}. {name} - {role}")
                            else:
                                print("❌ Could not parse result count")
                                
                    except json.JSONDecodeError:
                        # It's the final formatted response (not JSON)
                        print(f"\n📝 Final formatted response received ({len(message)} chars)")
                        # Show first few lines
                        lines = message.split('\n')
                        for line in lines[:5]:
                            if line.strip():
                                print(f"   {line[:80]}...")
                        
            except asyncio.TimeoutError:
                print(f"\n✓ Test complete. Received {len(messages_received)} JSON messages.")
                
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("Engineering Query Test - Verifying the Fix")
    print("=" * 60)
    asyncio.run(test_engineering_query())