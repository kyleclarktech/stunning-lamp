#!/usr/bin/env python3
"""
Test post-processing and validation improvements directly
without waiting for AI model generation
"""

import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from query_processor import process_query
from query_validator import validate_query
from main import get_falkor_client

# Test cases with known issues that our improvements should fix
TEST_CASES = [
    {
        "name": "Function name: lower() → toLower()",
        "input": "MATCH (p:Person) WHERE lower(p.name) CONTAINS 'john' RETURN p",
        "expected_fix": "MATCH (p:Person) WHERE toLower(p.name) CONTAINS 'john' RETURN p",
        "should_execute": True
    },
    {
        "name": "Function name: LOWER() → toLower()",
        "input": "MATCH (p:Person) WHERE LOWER(p.role) = 'engineer' RETURN p",
        "expected_fix": "MATCH (p:Person) WHERE toLower(p.role) = 'engineer' RETURN p",
        "should_execute": True
    },
    {
        "name": "Multiple statements with semicolon",
        "input": "MATCH (p:Person) RETURN p LIMIT 10; MATCH (t:Team) RETURN t",
        "expected_fix": "MATCH (p:Person) RETURN p LIMIT 10",
        "should_execute": True
    },
    {
        "name": "Trailing semicolon removal",
        "input": "MATCH (p:Person) RETURN count(p) as total;",
        "expected_fix": "MATCH (p:Person) RETURN count(p) as total",
        "should_execute": True
    },
    {
        "name": "Math function: ROUND() → round()",
        "input": "MATCH (m:Metric) RETURN ROUND(avg(m.value), 2) as avg_value",
        "expected_fix": "MATCH (m:Metric) RETURN round(avg(m.value), 2) as avg_value",
        "should_execute": True
    },
    {
        "name": "Complex query with multiple issues",
        "input": "MATCH (t:Team)<-[:MEMBER_OF]-(p:Person) WHERE lower(t.name) = 'engineering' WITH t, COUNT(p) as members RETURN t.name, members;",
        "expected_fix": "MATCH (t:Team)<-[:MEMBER_OF]-(p:Person) WHERE toLower(t.name) = 'engineering' WITH t, COUNT(p) as members RETURN t.name, members",
        "should_execute": True
    },
    {
        "name": "Valid query (no changes needed)",
        "input": "MATCH (p:Person)-[:HAS_SKILL]->(s:Skill {name: 'Python'}) RETURN p.name, p.email",
        "expected_fix": "MATCH (p:Person)-[:HAS_SKILL]->(s:Skill {name: 'Python'}) RETURN p.name, p.email",
        "should_execute": True
    },
    {
        "name": "Aggregation in WHERE (validation warning)",
        "input": "MATCH (t:Team)<-[:MEMBER_OF]-(p:Person) WHERE COUNT(p) > 10 RETURN t",
        "expected_fix": "MATCH (t:Team)<-[:MEMBER_OF]-(p:Person) WHERE COUNT(p) > 10 RETURN t",
        "should_execute": False  # Should fail validation
    }
]

def test_improvements():
    """Test post-processing and validation improvements."""
    print("TESTING QUERY PROCESSING IMPROVEMENTS")
    print("=" * 60)
    
    total_tests = len(TEST_CASES)
    passed = 0
    fixed = 0
    validated = 0
    executed = 0
    
    for i, test in enumerate(TEST_CASES, 1):
        print(f"\n[{i}/{total_tests}] {test['name']}")
        print(f"Input:    {test['input']}")
        
        # Apply post-processing
        processed = process_query(test['input'])
        print(f"Output:   {processed}")
        
        # Check if fix was applied correctly
        if processed == test['expected_fix']:
            print("✓ Processing: CORRECT")
            passed += 1
        else:
            print("✗ Processing: INCORRECT")
            print(f"Expected: {test['expected_fix']}")
        
        # Track if any fix was applied
        if test['input'] != processed:
            fixed += 1
            print("🔧 Fix applied")
        
        # Validate the processed query
        is_valid, errors, warnings = validate_query(processed)
        
        if is_valid:
            print("✓ Validation: PASSED")
            validated += 1
        else:
            print("✗ Validation: FAILED")
            print(f"  Errors: {', '.join(errors[:2])}")
        
        if warnings:
            print(f"  ⚠️  Warnings: {', '.join(warnings[:2])}")
        
        # Try to execute if expected to work
        if test['should_execute'] and is_valid:
            try:
                falkor = get_falkor_client()
                db = falkor.select_graph("agent_poc")
                result = db.query(processed)
                print("✓ Execution: SUCCESS")
                executed += 1
                if result.result_set:
                    print(f"  Results: {len(result.result_set)} rows")
            except Exception as e:
                print(f"✗ Execution: FAILED - {str(e)[:100]}")
        elif not test['should_execute']:
            print("ℹ️  Execution: Skipped (expected to fail validation)")
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total tests: {total_tests}")
    print(f"Processing correct: {passed}/{total_tests} ({passed/total_tests*100:.1f}%)")
    print(f"Fixes applied: {fixed}")
    print(f"Validation passed: {validated}/{total_tests} ({validated/total_tests*100:.1f}%)")
    print(f"Execution success: {executed}/{sum(1 for t in TEST_CASES if t['should_execute'])}")
    
    # Test some real problematic queries from the failure analysis
    print("\n" + "=" * 60)
    print("TESTING REAL FAILURE PATTERNS")
    print("=" * 60)
    
    failure_patterns = [
        ("MATCH (p:Person) WHERE year(p.hire_date) = 2023 RETURN p", "year() function"),
        ("MATCH (p:Person) WHERE p.name =~ 'John.*' RETURN p; -- Find Johns", "Comment after semicolon"),
        ("MATCH p = shortestPath((a:Person)-[*]-(b:Person)) RETURN p", "shortestPath in MATCH"),
        ("MATCH (p:Policy) WHERE datetime.truncate('month', p.updated_at) = datetime() RETURN p", "datetime.truncate")
    ]
    
    for query, issue in failure_patterns:
        print(f"\nIssue: {issue}")
        print(f"Original: {query}")
        processed = process_query(query)
        print(f"Fixed:    {processed}")
        is_valid, errors, _ = validate_query(processed)
        print(f"Valid:    {'Yes' if is_valid else 'No'}")
        if errors:
            print(f"Errors:   {', '.join(errors[:2])}")

if __name__ == "__main__":
    test_improvements()