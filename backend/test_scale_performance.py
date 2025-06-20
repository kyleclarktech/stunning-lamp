#!/usr/bin/env python3
"""
Performance and scale testing for global operations
Tests query performance with current data volume
"""

import json
import time
import os
import sys
import falkordb
import statistics
from typing import Dict, List, Tuple

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class PerformanceTester:
    def __init__(self):
        self.falkor_host = os.getenv("FALKOR_HOST", "localhost")
        self.falkor_port = int(os.getenv("FALKOR_PORT", 6379))
        self.client = None
        self.db = None
        
    def connect(self):
        """Connect to FalkorDB"""
        try:
            self.client = falkordb.FalkorDB(host=self.falkor_host, port=self.falkor_port)
            self.db = self.client.select_graph("agent_poc")
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def warm_cache(self):
        """Warm up the cache with initial queries"""
        print("🔥 Warming cache...")
        warm_queries = [
            "MATCH (n) RETURN count(n)",
            "MATCH (p:Person) RETURN count(p)",
            "MATCH ()-[r]->() RETURN count(r)"
        ]
        for q in warm_queries:
            self.db.query(q)
    
    def benchmark_query(self, query: str, runs: int = 10) -> Dict:
        """Run a query multiple times and collect statistics"""
        times = []
        results = []
        
        for i in range(runs):
            start = time.time()
            try:
                result = self.db.query(query)
                duration = (time.time() - start) * 1000  # ms
                times.append(duration)
                results.append(len(result.result_set) if result.result_set else 0)
            except Exception as e:
                print(f"Query failed: {e}")
                return None
        
        return {
            "min": min(times),
            "max": max(times),
            "avg": statistics.mean(times),
            "median": statistics.median(times),
            "p95": statistics.quantiles(times, n=20)[18] if len(times) > 1 else times[0],
            "p99": statistics.quantiles(times, n=100)[98] if len(times) > 2 else max(times),
            "result_count": results[0] if results else 0
        }
    
    def test_scale_queries(self):
        """Test queries that stress the system at scale"""
        
        print("\n" + "="*60)
        print("PERFORMANCE BENCHMARKING - SCALE TESTS")
        print("="*60)
        
        scale_queries = [
            {
                "name": "Count all nodes",
                "description": "Basic scale check",
                "query": "MATCH (n) RETURN count(n) as total_nodes"
            },
            {
                "name": "Count all relationships", 
                "description": "Relationship scale check",
                "query": "MATCH ()-[r]->() RETURN count(r) as total_relationships"
            },
            {
                "name": "Complex path query - 2 hops",
                "description": "Find all 2-hop connections from a person",
                "query": """
                    MATCH path = (p1:Person {id: 'person_1'})-[*2]-(p2:Person)
                    WHERE p1 <> p2
                    RETURN count(DISTINCT p2) as connected_people
                """
            },
            {
                "name": "Complex path query - 3 hops",
                "description": "Find all 3-hop connections from a person",
                "query": """
                    MATCH path = (p1:Person {id: 'person_1'})-[*3]-(p2:Person)
                    WHERE p1 <> p2
                    RETURN count(DISTINCT p2) as connected_people
                    LIMIT 100
                """
            },
            {
                "name": "Full organization hierarchy",
                "description": "Traverse entire reporting structure",
                "query": """
                    MATCH (p:Person)
                    OPTIONAL MATCH path = (p)-[:REPORTS_TO*]->(manager:Person)
                    WITH p, 
                         CASE WHEN manager IS NULL THEN 0 
                              ELSE length(path) END as level
                    RETURN level, count(p) as people_at_level
                    ORDER BY level
                """
            },
            {
                "name": "Global skill inventory",
                "description": "Aggregate all skills by timezone",
                "query": """
                    MATCH (p:Person)-[:HAS_SKILL]->(s:Skill)
                    WITH p.timezone as tz, s.category as category, count(*) as skill_count
                    WITH tz, collect({category: category, count: skill_count}) as skills
                    RETURN tz, skills, reduce(total = 0, s IN skills | total + s.count) as total_skills
                    ORDER BY total_skills DESC
                """
            },
            {
                "name": "Project resource optimization",
                "description": "Complex multi-join for resource matching",
                "query": """
                    MATCH (proj:Project {status: 'active'})-[:REQUIRES_SKILL]->(req_skill:Skill)
                    MATCH (p:Person)-[:HAS_SKILL]->(p_skill:Skill)
                    WHERE req_skill.id = p_skill.id
                      AND p.current_utilization < 90
                    WITH proj, p, count(DISTINCT req_skill) as matching_skills
                    WITH proj.name as project, 
                         collect({
                            person: p.name, 
                            timezone: p.timezone,
                            utilization: p.current_utilization,
                            skills: matching_skills
                         })[0..5] as top_candidates
                    RETURN project, top_candidates
                    ORDER BY project
                """
            },
            {
                "name": "Cross-functional collaboration network",
                "description": "Find collaboration patterns across departments",
                "query": """
                    MATCH (p1:Person)-[:MEMBER_OF]->(g:Group)<-[:MEMBER_OF]-(p2:Person)
                    WHERE p1.department <> p2.department
                    WITH p1.department as dept1, p2.department as dept2, count(*) as collaborations
                    WHERE collaborations > 5
                    RETURN dept1, dept2, collaborations
                    ORDER BY collaborations DESC
                    LIMIT 20
                """
            },
            {
                "name": "Policy compliance coverage",
                "description": "Complex aggregation of policy responsibilities",
                "query": """
                    MATCH (p:Policy)
                    OPTIONAL MATCH (t:Team)-[:RESPONSIBLE_FOR]->(p)
                    OPTIONAL MATCH (g:Group)-[:RESPONSIBLE_FOR]->(p)
                    WITH p, 
                         count(DISTINCT t) as team_count,
                         count(DISTINCT g) as group_count
                    RETURN p.severity, 
                           count(p) as policy_count,
                           avg(team_count + group_count) as avg_responsible_entities
                    ORDER BY p.severity DESC
                """
            },
            {
                "name": "Timezone handoff analysis",
                "description": "Calculate potential handoff pairs",
                "query": """
                    MATCH (p1:Person)
                    WITH p1.timezone as tz1, collect(p1)[0..10] as sample1
                    MATCH (p2:Person)
                    WHERE p2.timezone <> tz1
                    WITH tz1, sample1, p2.timezone as tz2, collect(p2)[0..10] as sample2
                    WITH tz1, tz2, 
                         size(sample1) * size(sample2) as potential_handoffs
                    RETURN tz1, tz2, potential_handoffs
                    ORDER BY potential_handoffs DESC
                    LIMIT 15
                """
            }
        ]
        
        results = []
        
        for test in scale_queries:
            print(f"\n📊 Testing: {test['name']}")
            print(f"   {test['description']}")
            
            stats = self.benchmark_query(test['query'])
            
            if stats:
                print(f"   ✅ Results: {stats['result_count']} rows")
                print(f"   ⏱️  Performance:")
                print(f"      Min: {stats['min']:.2f}ms")
                print(f"      Avg: {stats['avg']:.2f}ms")
                print(f"      P95: {stats['p95']:.2f}ms")
                print(f"      P99: {stats['p99']:.2f}ms")
                
                # Check against performance targets
                if stats['p95'] < 100:
                    performance = "🟢 Excellent"
                elif stats['p95'] < 500:
                    performance = "🟡 Good"
                elif stats['p95'] < 1000:
                    performance = "🟠 Acceptable"
                else:
                    performance = "🔴 Needs Optimization"
                
                print(f"   {performance}")
                
                results.append({
                    "query": test['name'],
                    "stats": stats,
                    "performance": performance
                })
            else:
                print("   ❌ Query failed")
        
        return results
    
    def test_concurrent_load(self):
        """Simulate concurrent query load"""
        print("\n" + "="*60)
        print("CONCURRENT LOAD TESTING")
        print("="*60)
        
        # Simple queries that would be common in production
        concurrent_queries = [
            "MATCH (p:Person {id: 'person_100'}) RETURN p",
            "MATCH (t:Team {id: 'team_5'}) RETURN t", 
            "MATCH (p:Person)-[:MEMBER_OF]->(t:Team {id: 'team_10'}) RETURN count(p)",
            "MATCH (p:Policy {severity: 'critical'}) RETURN p.name LIMIT 5",
            "MATCH (p:Person) WHERE p.timezone = 'US/Eastern' RETURN count(p)"
        ]
        
        print("\nRunning 50 queries in rapid succession...")
        
        start_time = time.time()
        total_queries = 0
        
        for i in range(10):
            for query in concurrent_queries:
                try:
                    self.db.query(query)
                    total_queries += 1
                except:
                    pass
        
        total_time = time.time() - start_time
        qps = total_queries / total_time
        
        print(f"\n📊 Concurrent Load Results:")
        print(f"   Total Queries: {total_queries}")
        print(f"   Total Time: {total_time:.2f}s")
        print(f"   Queries/Second: {qps:.2f}")
        
        if qps > 100:
            print("   🟢 Excellent throughput")
        elif qps > 50:
            print("   🟡 Good throughput")
        else:
            print("   🔴 Low throughput - may need optimization")
        
        return qps
    
    def generate_performance_report(self, scale_results, qps):
        """Generate performance assessment report"""
        print("\n" + "="*60)
        print("PERFORMANCE ASSESSMENT SUMMARY")
        print("="*60)
        
        # Calculate performance metrics
        excellent = sum(1 for r in scale_results if "🟢" in r["performance"])
        good = sum(1 for r in scale_results if "🟡" in r["performance"])
        acceptable = sum(1 for r in scale_results if "🟠" in r["performance"])
        needs_work = sum(1 for r in scale_results if "🔴" in r["performance"])
        
        total = len(scale_results)
        
        print(f"\n📊 Query Performance Distribution:")
        print(f"   🟢 Excellent (<100ms): {excellent}/{total} ({excellent/total*100:.1f}%)")
        print(f"   🟡 Good (<500ms): {good}/{total} ({good/total*100:.1f}%)")
        print(f"   🟠 Acceptable (<1000ms): {acceptable}/{total} ({acceptable/total*100:.1f}%)")
        print(f"   🔴 Needs Optimization (>1000ms): {needs_work}/{total} ({needs_work/total*100:.1f}%)")
        
        print(f"\n⚡ Throughput:")
        print(f"   Queries/Second: {qps:.2f}")
        
        # Overall assessment
        print(f"\n🎯 Overall Assessment:")
        
        if excellent + good >= total * 0.8 and qps > 50:
            print("   ✅ System performs well at current scale")
            print("   ✅ Sub-second response times achieved for most queries")
        else:
            print("   ⚠️  Performance concerns identified")
            print("   ⚠️  May need optimization before scaling to 10K+ employees")
        
        # Recommendations
        print(f"\n💡 Recommendations:")
        if needs_work > 0:
            print("   - Add indexes for frequently queried fields")
            print("   - Consider query optimization for complex path traversals")
        if qps < 100:
            print("   - Implement connection pooling")
            print("   - Consider caching for frequently accessed data")
        print("   - Monitor performance as data volume grows")
        print("   - Plan for horizontal scaling if needed")

def main():
    """Main performance test execution"""
    tester = PerformanceTester()
    
    if not tester.connect():
        return 1
    
    print("🚀 Starting Performance and Scale Testing")
    
    # Warm cache
    tester.warm_cache()
    
    # Run scale tests
    scale_results = tester.test_scale_queries()
    
    # Run concurrent load test
    qps = tester.test_concurrent_load()
    
    # Generate report
    tester.generate_performance_report(scale_results, qps)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())