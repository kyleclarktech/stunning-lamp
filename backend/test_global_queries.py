#!/usr/bin/env python3
"""
Test script for global operations queries
Tests current system capabilities and benchmarks performance
"""

import json
import time
import os
import sys
import falkordb
from datetime import datetime
from typing import Dict, List, Tuple

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class QueryTester:
    def __init__(self):
        self.falkor_host = os.getenv("FALKOR_HOST", "localhost") 
        self.falkor_port = int(os.getenv("FALKOR_PORT", 6379))
        self.client = None
        self.db = None
        self.results = []
        
    def connect(self):
        """Connect to FalkorDB"""
        try:
            print(f"🔌 Connecting to FalkorDB at {self.falkor_host}:{self.falkor_port}...")
            self.client = falkordb.FalkorDB(host=self.falkor_host, port=self.falkor_port)
            self.db = self.client.select_graph("agent_poc")
            print("✅ Connected successfully")
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def execute_query(self, query: str, description: str) -> Tuple[bool, float, int, str]:
        """Execute a query and return success, duration, result count, and error"""
        try:
            start_time = time.time()
            result = self.db.query(query)
            end_time = time.time()
            
            duration = (end_time - start_time) * 1000  # Convert to milliseconds
            row_count = len(result.result_set) if result.result_set else 0
            
            return True, duration, row_count, ""
        except Exception as e:
            return False, 0, 0, str(e)
    
    def test_query_category(self, category: str, queries: List[Dict]):
        """Test a category of queries"""
        print(f"\n{'='*60}")
        print(f"Testing {category}")
        print(f"{'='*60}")
        
        category_results = {
            "category": category,
            "total": len(queries),
            "successful": 0,
            "failed": 0,
            "avg_duration": 0,
            "queries": []
        }
        
        total_duration = 0
        
        for query_info in queries:
            query_name = query_info["name"]
            query = query_info["query"]
            expected_status = query_info["expected"]
            
            print(f"\n📊 {query_name}")
            print(f"Expected: {expected_status}")
            
            success, duration, count, error = self.execute_query(query, query_name)
            
            if success:
                print(f"✅ Success - {count} results in {duration:.2f}ms")
                category_results["successful"] += 1
                total_duration += duration
                status = "SUCCESS"
            else:
                print(f"❌ Failed - {error}")
                category_results["failed"] += 1
                status = "FAILED"
            
            category_results["queries"].append({
                "name": query_name,
                "status": status,
                "duration": duration if success else None,
                "result_count": count if success else None,
                "error": error if not success else None,
                "matches_expected": (success and expected_status == "supported") or 
                                  (not success and expected_status == "not_supported")
            })
        
        if category_results["successful"] > 0:
            category_results["avg_duration"] = total_duration / category_results["successful"]
        
        self.results.append(category_results)
        
        print(f"\n📈 Category Summary:")
        print(f"   Successful: {category_results['successful']}/{category_results['total']}")
        print(f"   Failed: {category_results['failed']}/{category_results['total']}")
        if category_results["successful"] > 0:
            print(f"   Avg Duration: {category_results['avg_duration']:.2f}ms")
    
    def run_all_tests(self):
        """Run all test query categories"""
        
        # Test 1: Basic Timezone Queries (Should work)
        timezone_queries = [
            {
                "name": "Q1: Find employees in Pacific timezone",
                "expected": "supported",
                "query": """
                    MATCH (p:Person)
                    WHERE p.timezone = 'US/Pacific'
                    RETURN p.name, p.role, p.department
                    ORDER BY p.department, p.name
                    LIMIT 10
                """
            },
            {
                "name": "Q2: Count employees by timezone",
                "expected": "supported",
                "query": """
                    MATCH (p:Person)
                    RETURN p.timezone, count(p) as employee_count
                    ORDER BY employee_count DESC
                """
            },
            {
                "name": "Q12: Teams distributed across timezones",
                "expected": "supported",
                "query": """
                    MATCH (t:Team)<-[:MEMBER_OF]-(p:Person)
                    WITH t, collect(DISTINCT p.timezone) as timezones, count(DISTINCT p.timezone) as tz_count
                    WHERE tz_count >= 3
                    RETURN t.name, timezones, tz_count
                    ORDER BY tz_count DESC
                """
            }
        ]
        
        # Test 2: Project Coordination Queries
        project_queries = [
            {
                "name": "Q17: Project timezone coverage",
                "expected": "supported",
                "query": """
                    MATCH (proj:Project)<-[:ALLOCATED_TO]-(p:Person)
                    WITH proj, collect(DISTINCT p.timezone) as timezones
                    RETURN proj.name, timezones, size(timezones) as timezone_coverage
                    ORDER BY timezone_coverage DESC
                    LIMIT 10
                """
            },
            {
                "name": "Q19: Available experts for projects",
                "expected": "supported", 
                "query": """
                    MATCH (p:Person)-[:HAS_SKILL]->(s:Skill)<-[:REQUIRES_SKILL]-(proj:Project)
                    WHERE p.current_utilization < 80
                      AND proj.status = 'planning'
                    WITH proj, p, count(s) as matching_skills
                    RETURN proj.name, p.name, p.timezone, p.current_utilization, matching_skills
                    ORDER BY matching_skills DESC
                    LIMIT 20
                """
            },
            {
                "name": "Q21: Cross-functional strategic groups",
                "expected": "supported",
                "query": """
                    MATCH (g:Group {type: 'strategic'})
                    MATCH (p:Person)-[:MEMBER_OF]->(g)
                    WITH g, collect(DISTINCT p.department) as departments, count(p) as member_count
                    WHERE size(departments) >= 4
                    RETURN g.name, departments, member_count
                """
            }
        ]
        
        # Test 3: Compliance Queries (Limited support)
        compliance_queries = [
            {
                "name": "Q28: Find GDPR policies",
                "expected": "supported",
                "query": """
                    MATCH (p:Policy)
                    WHERE 'GDPR' IN split(p.compliance_frameworks, ',')
                    RETURN p.name, p.category, p.severity
                    ORDER BY p.severity DESC
                    LIMIT 10
                """
            },
            {
                "name": "Q29: Map compliance to regions (will fail)",
                "expected": "not_supported",
                "query": """
                    MATCH (c:Compliance)-[:APPLIES_TO]->(o:Office)
                    WITH c, collect(o.region) as regions
                    RETURN c.framework, c.jurisdiction, regions
                    ORDER BY c.framework
                """
            }
        ]
        
        # Test 4: Resource Utilization Queries
        resource_queries = [
            {
                "name": "Q43: Team incident response capacity",
                "expected": "supported",
                "query": """
                    MATCH (t:Team)
                    WHERE t.focus CONTAINS 'reliability' OR t.focus CONTAINS 'incident'
                    MATCH (p:Person)-[:MEMBER_OF]->(t)
                    WHERE p.current_utilization < 100
                    RETURN t.name, 
                           count(p) as available_members,
                           avg(100 - p.current_utilization) as avg_available_capacity
                """
            },
            {
                "name": "Q49: Find underutilized resources",
                "expected": "supported",
                "query": """
                    MATCH (p:Person)
                    WHERE p.current_utilization < 50
                    RETURN p.name, p.department, p.timezone, p.current_utilization
                    ORDER BY p.current_utilization
                    LIMIT 20
                """
            }
        ]
        
        # Test 5: Complex Aggregation Queries
        aggregation_queries = [
            {
                "name": "Skills distribution by department",
                "expected": "supported",
                "query": """
                    MATCH (p:Person)-[:HAS_SKILL]->(s:Skill)
                    WITH p.department as dept, s.category as skill_cat, count(*) as skill_count
                    RETURN dept, skill_cat, skill_count
                    ORDER BY dept, skill_count DESC
                    LIMIT 25
                """
            },
            {
                "name": "Project allocation by timezone",
                "expected": "supported",
                "query": """
                    MATCH (p:Person)-[:ALLOCATED_TO]->(proj:Project)
                    WITH p.timezone as tz, count(DISTINCT proj) as project_count, 
                         count(DISTINCT p) as person_count
                    RETURN tz, project_count, person_count, 
                           toFloat(project_count) / person_count as projects_per_person
                    ORDER BY project_count DESC
                """
            }
        ]
        
        # Run all test categories
        self.test_query_category("Timezone Queries", timezone_queries)
        self.test_query_category("Project Coordination", project_queries)
        self.test_query_category("Compliance Tracking", compliance_queries)
        self.test_query_category("Resource Utilization", resource_queries)
        self.test_query_category("Complex Aggregations", aggregation_queries)
    
    def generate_report(self):
        """Generate final test report"""
        print(f"\n{'='*60}")
        print("FINAL TEST REPORT")
        print(f"{'='*60}")
        
        total_queries = sum(cat["total"] for cat in self.results)
        total_successful = sum(cat["successful"] for cat in self.results)
        total_failed = sum(cat["failed"] for cat in self.results)
        
        print(f"\n📊 Overall Results:")
        print(f"   Total Queries Tested: {total_queries}")
        print(f"   Successful: {total_successful} ({total_successful/total_queries*100:.1f}%)")
        print(f"   Failed: {total_failed} ({total_failed/total_queries*100:.1f}%)")
        
        print(f"\n⏱️  Performance Summary:")
        for category in self.results:
            if category["successful"] > 0:
                print(f"   {category['category']}: {category['avg_duration']:.2f}ms avg")
        
        print(f"\n🎯 Query Support Analysis:")
        supported_as_expected = 0
        unsupported_as_expected = 0
        unexpected_results = 0
        
        for category in self.results:
            for query in category["queries"]:
                if query["matches_expected"]:
                    if query["status"] == "SUCCESS":
                        supported_as_expected += 1
                    else:
                        unsupported_as_expected += 1
                else:
                    unexpected_results += 1
        
        print(f"   Supported (as expected): {supported_as_expected}")
        print(f"   Not Supported (as expected): {unsupported_as_expected}")
        print(f"   Unexpected Results: {unexpected_results}")
        
        # Save detailed results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"query_test_results_{timestamp}.json"
        
        with open(report_file, 'w') as f:
            json.dump({
                "timestamp": timestamp,
                "summary": {
                    "total_queries": total_queries,
                    "successful": total_successful,
                    "failed": total_failed,
                    "success_rate": total_successful/total_queries*100
                },
                "categories": self.results
            }, f, indent=2)
        
        print(f"\n💾 Detailed results saved to: {report_file}")
        
        return total_successful/total_queries >= 0.95  # 95% success target

def main():
    """Main test execution"""
    tester = QueryTester()
    
    if not tester.connect():
        print("Failed to connect to database. Exiting.")
        return 1
    
    print("\n🚀 Starting Global Operations Query Tests")
    print("="*60)
    
    tester.run_all_tests()
    success = tester.generate_report()
    
    if success:
        print("\n✅ TESTS PASSED - Met 95% query coverage target")
        return 0
    else:
        print("\n❌ TESTS FAILED - Did not meet 95% query coverage target")
        return 1

if __name__ == "__main__":
    sys.exit(main())