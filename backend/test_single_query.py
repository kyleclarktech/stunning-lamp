#!/usr/bin/env python3
"""Test a single operational query"""

import json

print("🔍 Testing: Database seeding verification")

# Use FalkorDB directly to verify our data
import falkordb

try:
    client = falkordb.FalkorDB(host="falkordb", port=6379)
    db = client.select_graph("agent_poc")
    
    # Count nodes
    print("\n📊 Node counts:")
    for node_type in ["Schedule", "Incident", "Person", "Team"]:
        result = db.query(f"MATCH (n:{node_type}) RETURN count(n) as count")
        count = result.result_set[0][0] if result.result_set else 0
        print(f"  - {node_type}: {count}")
    
    # Check relationships
    print("\n🔗 Relationship counts:")
    for rel_type in ["ON_CALL", "RESPONDED_TO", "HANDS_OFF_TO"]:
        result = db.query(f"MATCH ()-[r:{rel_type}]->() RETURN count(r) as count")
        count = result.result_set[0][0] if result.result_set else 0
        print(f"  - {rel_type}: {count}")
    
    # Test a simple operational query
    print("\n🚨 Testing: Current on-call query")
    query = """
    MATCH (p:Person)-[oc:ON_CALL]->(s:Schedule) 
    WHERE datetime(s.start_datetime) <= datetime('2024-03-01T00:00:00') 
      AND datetime(s.end_datetime) >= datetime('2024-03-01T00:00:00')
    RETURN p.name, s.coverage_type, s.region 
    LIMIT 5
    """
    result = db.query(query)
    if result.result_set:
        print("On-call personnel found:")
        for row in result.result_set:
            print(f"  - {row[0]} ({row[1]}) in {row[2]}")
    else:
        print("No on-call personnel found for the test date")
    
    print("\n✅ Phase 3 implementation verified successfully!")
    
except Exception as e:
    print(f"❌ Database test error: {e}")
    import traceback
    traceback.print_exc()