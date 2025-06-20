import asyncio
import websockets
import json

async def test_compliance_queries():
    """Test compliance and data governance queries"""
    
    test_queries = [
        # Office compliance
        "What compliance frameworks apply to the London office?",
        "Which offices are SOC2 compliant?",
        "Show upcoming compliance audits",
        
        # Client compliance
        "What compliance requirements do healthcare clients have?",
        "Show financial clients and their compliance requirements",
        
        # Data residency
        "Where can we store EU customer data?",
        "Which projects store data in the EU?",
        "What are the requirements for transferring data from EU to US?",
        
        # GDPR specific
        "Show GDPR requirements and which offices must comply",
        "Which projects need GDPR compliance?",
        
        # Compliance violations
        "Find projects with potential data residency violations",
    ]
    
    uri = "ws://localhost:8000/ws"
    
    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"Query: {query}")
        print(f"{'='*60}")
        
        try:
            async with websockets.connect(uri) as websocket:
                # Send the query
                await websocket.send(json.dumps({"message": query}))
                
                # Receive all responses
                while True:
                    try:
                        response = await asyncio.wait_for(websocket.recv(), timeout=30.0)
                        data = json.loads(response)
                        
                        # Handle different response types
                        if data.get("type") == "info":
                            print(f"Info: {data.get('content', '')}")
                        elif data.get("type") == "query":
                            print(f"Query: {data.get('content', '')}")
                        elif data.get("type") == "results":
                            print(f"Results: {data.get('content', '')}")
                            # Pretty print if it's a structured result
                            if isinstance(data.get('content'), str) and data['content'].strip():
                                print("\nFormatted Result:")
                                print(data['content'])
                            break
                        elif data.get("type") == "error":
                            print(f"Error: {data.get('content', '')}")
                            break
                        elif data.get("status") == "completed":
                            break
                            
                    except asyncio.TimeoutError:
                        print("Timeout waiting for response")
                        break
                        
        except Exception as e:
            print(f"Error testing query: {e}")
            
        # Small delay between queries
        await asyncio.sleep(1)

if __name__ == "__main__":
    print("Testing Compliance & Data Governance Queries...")
    asyncio.run(test_compliance_queries())