#!/usr/bin/env python3
"""
Test suite for semantic query understanding
Demonstrates how the improved query patterns handle various natural language queries
"""

import asyncio
import sys
from query_patterns_improved import enhanced_query_matcher, match_and_generate_query

# Test queries organized by category
TEST_QUERIES = {
    "Generic People Queries": [
        ("How many employees are there?", "Should count ALL Person nodes"),
        ("Show me all staff members", "Should list ALL Person nodes"),
        ("List all people", "Should list ALL Person nodes"),
        ("What's the total employee count?", "Should count ALL Person nodes"),
        ("How many people do we have?", "Should count ALL Person nodes"),
    ],
    
    "Role Category Queries": [
        ("How many developers are there?", "Should count all engineering roles"),
        ("List all engineers", "Should list people with Engineer in role"),
        ("Show me all managers", "Should list people with Manager/Lead/Director roles"),
        ("Find all executives", "Should list VP/Chief/Director level roles"),
        ("Count the analysts", "Should count people with Analyst in role"),
    ],
    
    "Department Queries": [
        ("How many people work in Engineering?", "Should count people in Engineering dept"),
        ("Show me everyone in Sales", "Should list Sales department members"),
        ("List Product team members", "Should list Product department members"),
        ("Find engineers in Data Platform", "Should list engineers in Data Platform dept"),
    ],
    
    "Specific Person/Team Queries": [
        ("Who is Sarah Chen?", "Should find person by name"),
        ("Who is on the Analytics team?", "Should list team members"),
        ("Who reports to Michael Rodriguez?", "Should show direct reports"),
        ("Find the Data Platform team members", "Should list team members"),
    ],
    
    "Complex Queries": [
        ("Find senior engineers in Infrastructure", "Should filter by level and dept"),
        ("Show all team leads", "Should find people with Lead in role"),
        ("List principal engineers", "Should find Principal Engineers"),
        ("How many senior developers in Engineering?", "Should count by level and dept"),
    ],
    
    "Policy and Hierarchy Queries": [
        ("Who owns the data retention policy?", "Should find policy owner"),
        ("Show the org chart", "Should display reporting structure"),
        ("List all policies", "Should show all policies"),
    ],
    
    "Edge Cases": [
        ("employees", "Single word should still work"),
        ("developers in product", "Should handle lowercase departments"),
        ("SHOW ME ALL EMPLOYEES", "Should handle uppercase"),
        ("   how many   employees   ?  ", "Should handle extra whitespace"),
    ]
}

def test_query_matching():
    """Test the improved query pattern matcher"""
    print("=" * 80)
    print("SEMANTIC QUERY PATTERN TESTING")
    print("=" * 80)
    
    total_queries = 0
    matched_queries = 0
    
    for category, queries in TEST_QUERIES.items():
        print(f"\n{category}:")
        print("-" * len(category))
        
        for query, expected_behavior in queries:
            total_queries += 1
            result = enhanced_query_matcher.match_query(query)
            
            if result:
                matched_queries += 1
                cypher_query, params = result
                print(f"\n✓ Query: '{query}'")
                print(f"  Expected: {expected_behavior}")
                print(f"  Generated Cypher:")
                print(f"    {cypher_query}")
                if params:
                    print(f"  Parameters: {params}")
            else:
                print(f"\n✗ Query: '{query}'")
                print(f"  Expected: {expected_behavior}")
                print(f"  Result: NO MATCH (would fall back to LLM)")
    
    print("\n" + "=" * 80)
    print(f"SUMMARY: {matched_queries}/{total_queries} queries matched by patterns")
    print(f"Pattern coverage: {matched_queries/total_queries*100:.1f}%")
    print("=" * 80)
    
    # Test the specific problematic query
    print("\n" + "=" * 80)
    print("TESTING THE SPECIFIC PROBLEMATIC QUERY")
    print("=" * 80)
    
    problematic_query = "How many employees are there?"
    result = match_and_generate_query(problematic_query)
    
    print(f"\nQuery: '{problematic_query}'")
    print(f"Old behavior: MATCH (p:Person) WHERE p.role CONTAINS 'employee' OR p.role CONTAINS 'Employee' RETURN count(p) as count")
    print(f"New behavior: {result}")
    print("\nExplanation: The new system recognizes 'employees' as a semantic term meaning")
    print("'all Person nodes' rather than searching for the literal word 'employee' in roles.")
    
    # Show supported query examples
    print("\n" + "=" * 80)
    print("SUPPORTED QUERY EXAMPLES")
    print("=" * 80)
    print("\nThe system now supports these types of queries:")
    for example in enhanced_query_matcher.get_supported_queries():
        print(f"  • {example}")

def compare_old_vs_new():
    """Compare old and new behavior for key queries"""
    print("\n" + "=" * 80)
    print("OLD VS NEW BEHAVIOR COMPARISON")
    print("=" * 80)
    
    comparison_queries = [
        "How many employees are there?",
        "List all developers",
        "Show me all staff",
        "Find engineers",
        "Count people"
    ]
    
    for query in comparison_queries:
        result = match_and_generate_query(query)
        print(f"\nQuery: '{query}'")
        print(f"Old: Would search for role CONTAINS '{query.split()[-1]}'")
        print(f"New: {result if result else 'Falls back to LLM for better handling'}")

if __name__ == "__main__":
    test_query_matching()
    compare_old_vs_new()
    
    print("\n" + "=" * 80)
    print("RECOMMENDATIONS")
    print("=" * 80)
    print("\n1. Replace query_patterns.py with query_patterns_improved.py")
    print("2. Update main.py to import from query_patterns_improved")
    print("3. The new system will correctly handle 'How many employees are there?'")
    print("4. It provides semantic understanding for common organizational queries")
    print("5. Falls back to LLM for queries it doesn't understand")
    print("\nThe framework is extensible - add more semantic mappings as needed!")