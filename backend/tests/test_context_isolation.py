#!/usr/bin/env python3
import asyncio
import websockets
import json

async def test_query_consistency():
    """Test that same queries produce consistent results with context isolation."""
    uri = "ws://localhost:8000/ws"
    
    # Test queries in different orders
    test_sequences = [
        ["list all members of engineering", "who is the CEO?", "list all members of engineering"],
        ["who is the CEO?", "list all members of engineering", "who is the CEO?"],
        ["show all policies", "list all members of engineering", "show all policies"]
    ]
    
    results = {}
    
    for seq_num, sequence in enumerate(test_sequences):
        print(f"\n{'='*60}")
        print(f"Test Sequence {seq_num + 1}: {' → '.join(sequence)}")
        print('='*60)
        
        seq_results = []
        
        for query in sequence:
            try:
                async with websockets.connect(uri) as websocket:
                    await websocket.send(query)
                    
                    # Collect the query execution message
                    query_result = None
                    message_count = 0
                    
                    try:
                        while message_count < 5:  # Limit messages to prevent hanging
                            message = await asyncio.wait_for(websocket.recv(), timeout=3.0)
                            message_count += 1
                            
                            try:
                                data = json.loads(message)
                                if data.get('type') == 'query':
                                    # Extract the actual Cypher query
                                    query_msg = data.get('message', '')
                                    if '`' in query_msg:
                                        start = query_msg.find('`') + 1
                                        end = query_msg.rfind('`')
                                        if start < end:
                                            query_result = query_msg[start:end]
                                            break
                            except json.JSONDecodeError:
                                pass
                                
                    except asyncio.TimeoutError:
                        pass
                    
                    seq_results.append({
                        'input': query,
                        'generated_query': query_result
                    })
                    
            except Exception as e:
                print(f"Error testing '{query}': {e}")
                seq_results.append({
                    'input': query,
                    'generated_query': None,
                    'error': str(e)
                })
        
        results[f"sequence_{seq_num + 1}"] = seq_results
    
    # Analyze results for consistency
    print("\n" + "="*60)
    print("CONSISTENCY ANALYSIS")
    print("="*60)
    
    # Check if identical queries produce identical results across sequences
    query_results_map = {}
    
    for seq_name, seq_results in results.items():
        for result in seq_results:
            query = result['input']
            generated = result.get('generated_query', 'ERROR')
            
            if query not in query_results_map:
                query_results_map[query] = []
            query_results_map[query].append(generated)
    
    # Report consistency
    all_consistent = True
    for query, generated_queries in query_results_map.items():
        unique_results = set(generated_queries)
        is_consistent = len(unique_results) == 1
        
        print(f"\nQuery: '{query}'")
        print(f"Consistent: {'✅ YES' if is_consistent else '❌ NO'}")
        
        if not is_consistent:
            all_consistent = False
            print("Different results generated:")
            for i, result in enumerate(unique_results):
                if result:
                    print(f"  {i+1}. {result[:100]}...")
                else:
                    print(f"  {i+1}. ERROR/None")
        else:
            result = list(unique_results)[0]
            if result:
                print(f"Always generates: {result[:100]}...")
            else:
                print("Always generates: ERROR/None")
    
    print("\n" + "="*60)
    print(f"OVERALL CONSISTENCY: {'✅ PASS' if all_consistent else '❌ FAIL'}")
    print("="*60)
    
    return all_consistent

if __name__ == "__main__":
    success = asyncio.run(test_query_consistency())
    exit(0 if success else 1)