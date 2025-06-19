#!/usr/bin/env python3
import asyncio
import websockets
import json
import time

TEST_QUERIES = [
    # Basic queries
    "who works on mobile?",
    "find Sarah's manager",
    "show me people in engineering",
    
    # Role-based queries
    "who reports to the Chief Operating Officer?",
    "who are the team leads?",
    
    # Complex queries
    "which team has the most members?",
    "which teams are responsible for compliance policies?",
    "who is on the Mobile Apps team and also in the security group?",
]

async def test_query(query_text):
    uri = "ws://localhost:8000/ws"
    start_time = time.time()
    results = {
        "query": query_text,
        "generated_cypher": None,
        "result_count": 0,
        "error": None,
        "response_time": 0,
        "formatted_response": None
    }
    
    try:
        async with websockets.connect(uri) as websocket:
            # Send query
            await websocket.send(json.dumps({"message": query_text}))
            
            # Receive responses
            while True:
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=30.0)
                    if not response:
                        continue
                    
                    # Try to parse as JSON
                    try:
                        data = json.loads(response)
                        if data.get('type') == 'query':
                            results['generated_cypher'] = data.get('query')
                        elif data.get('type') == 'results':
                            results['result_count'] = len(data.get('results', []))
                        elif data.get('type') == 'error':
                            results['error'] = data.get('message')
                        elif data.get('type') == 'complete':
                            break
                    except json.JSONDecodeError:
                        # This is the formatted response
                        results['formatted_response'] = response[:200] + "..." if len(response) > 200 else response
                        
                except asyncio.TimeoutError:
                    break
                    
    except Exception as e:
        results['error'] = str(e)
    
    results['response_time'] = time.time() - start_time
    return results

async def run_all_tests():
    print("=" * 80)
    print("FalkorDB Chat Interface Test Report")
    print("=" * 80)
    print()
    
    all_results = []
    
    for i, query in enumerate(TEST_QUERIES, 1):
        print(f"\n[{i}/{len(TEST_QUERIES)}] Testing: {query}")
        print("-" * 60)
        
        result = await test_query(query)
        all_results.append(result)
        
        print(f"✓ Response Time: {result['response_time']:.2f}s")
        print(f"✓ Results Found: {result['result_count']}")
        if result['generated_cypher']:
            print(f"✓ Generated Cypher: {result['generated_cypher'][:100]}...")
        if result['error']:
            print(f"✗ Error: {result['error']}")
        if result['formatted_response']:
            print(f"✓ Formatted Response Preview: {result['formatted_response']}")
            
        # Brief pause between queries
        await asyncio.sleep(1)
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    successful = sum(1 for r in all_results if r['result_count'] > 0 or r['formatted_response'])
    failed = sum(1 for r in all_results if r['error'] and not r['formatted_response'])
    avg_time = sum(r['response_time'] for r in all_results) / len(all_results)
    
    print(f"\nTotal Queries: {len(TEST_QUERIES)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Average Response Time: {avg_time:.2f}s")
    
    print("\nDetailed Results:")
    for i, result in enumerate(all_results, 1):
        status = "✓" if (result['result_count'] > 0 or result['formatted_response']) else "✗"
        print(f"{status} Query {i}: {result['query']}")
        print(f"  - Results: {result['result_count']}, Time: {result['response_time']:.2f}s")
        if result['error']:
            print(f"  - Error: {result['error']}")

if __name__ == "__main__":
    asyncio.run(run_all_tests())