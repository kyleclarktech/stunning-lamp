"""
Performance Benchmark Script for FalkorDB Chat Interface

This script measures the performance improvements from the optimization features.
"""

import asyncio
import time
import statistics
from typing import List, Dict, Tuple
import json
from query_patterns import match_and_generate_query
from main import call_ai_model, load_prompt, get_falkor_client
import logging

# Disable debug logging for benchmarks
logging.basicConfig(level=logging.WARNING)

class PerformanceBenchmark:
    """Benchmark performance of query generation and execution"""
    
    def __init__(self):
        self.test_queries = [
            # Pattern-matchable queries
            "who's on the mobile team?",
            "find Sarah's manager",
            "show me all engineers",
            "who are the team leads?",
            "who owns security policy?",
            "members of the engineering team",
            "who reports to the CTO?",
            "find people in engineering department",
            
            # Non-pattern queries (require AI)
            "what teams work on mobile apps and have more than 5 members?",
            "find all policies related to data security with high severity",
            "show me people who joined in the last 6 months",
            "which department has the most team leads?"
        ]
        
        self.results = {
            "pattern_matched": [],
            "ai_generated": [],
            "query_execution": [],
            "overall": []
        }
    
    async def benchmark_pattern_matching(self, query: str) -> Tuple[float, bool]:
        """Benchmark pattern matching performance"""
        start_time = time.time()
        result = match_and_generate_query(query)
        end_time = time.time()
        
        elapsed = end_time - start_time
        matched = result is not None
        
        return elapsed, matched
    
    async def benchmark_ai_generation(self, query: str) -> Tuple[float, str]:
        """Benchmark AI query generation"""
        start_time = time.time()
        
        prompt = load_prompt("generate_query", user_message=query)
        prompt += f"\n\nQuestion: \"{query}\"\nQuery:"
        
        cypher_query = await call_ai_model(prompt, websocket=None, timeout=60)
        
        # Clean up the query
        cypher_query = cypher_query.strip()
        if "```" in cypher_query:
            start = cypher_query.find("```")
            if start >= 0:
                start = cypher_query.find("\n", start) + 1
                end = cypher_query.find("```", start)
                if end > start:
                    cypher_query = cypher_query[start:end].strip()
        
        end_time = time.time()
        elapsed = end_time - start_time
        
        return elapsed, cypher_query
    
    def benchmark_query_execution(self, cypher_query: str) -> float:
        """Benchmark query execution time"""
        start_time = time.time()
        
        try:
            falkor = get_falkor_client()
            db = falkor.select_graph("agent_poc")
            result = db.query(cypher_query)
            success = True
        except Exception as e:
            print(f"Query execution error: {e}")
            success = False
        
        end_time = time.time()
        return end_time - start_time if success else -1
    
    async def run_benchmark(self):
        """Run the complete benchmark suite"""
        print("🚀 Starting Performance Benchmark")
        print("=" * 60)
        
        for i, query in enumerate(self.test_queries, 1):
            print(f"\n[{i}/{len(self.test_queries)}] Testing: {query}")
            
            # Measure overall time
            overall_start = time.time()
            
            # 1. Try pattern matching first
            pattern_time, matched = await self.benchmark_pattern_matching(query)
            
            if matched:
                cypher_query = match_and_generate_query(query)
                print(f"   ✅ Pattern matched in {pattern_time*1000:.2f}ms")
                self.results["pattern_matched"].append(pattern_time)
                
                # Skip AI generation for pattern-matched queries
                ai_time = 0
            else:
                print(f"   ❌ No pattern match ({pattern_time*1000:.2f}ms)")
                
                # 2. Fall back to AI generation
                ai_time, cypher_query = await self.benchmark_ai_generation(query)
                print(f"   🤖 AI generation took {ai_time:.2f}s")
                self.results["ai_generated"].append(ai_time)
            
            # 3. Execute the query
            if cypher_query:
                exec_time = self.benchmark_query_execution(cypher_query)
                if exec_time > 0:
                    print(f"   ⚡ Query execution took {exec_time*1000:.2f}ms")
                    self.results["query_execution"].append(exec_time)
                else:
                    print(f"   ❌ Query execution failed")
            
            overall_time = time.time() - overall_start
            self.results["overall"].append({
                "query": query,
                "pattern_matched": matched,
                "total_time": overall_time,
                "breakdown": {
                    "pattern_check": pattern_time,
                    "ai_generation": ai_time,
                    "execution": exec_time if cypher_query else 0
                }
            })
        
        self._print_summary()
    
    def _print_summary(self):
        """Print benchmark summary"""
        print("\n" + "=" * 60)
        print("📊 BENCHMARK SUMMARY")
        print("=" * 60)
        
        # Pattern matching stats
        pattern_queries = [r for r in self.results["overall"] if r["pattern_matched"]]
        ai_queries = [r for r in self.results["overall"] if not r["pattern_matched"]]
        
        print(f"\n✅ Pattern-matched queries: {len(pattern_queries)}/{len(self.test_queries)}")
        if pattern_queries:
            avg_time = statistics.mean([r["total_time"] for r in pattern_queries])
            print(f"   Average total time: {avg_time*1000:.2f}ms")
            print(f"   Pattern match time: {statistics.mean(self.results['pattern_matched'])*1000:.2f}ms avg")
        
        print(f"\n🤖 AI-generated queries: {len(ai_queries)}/{len(self.test_queries)}")
        if ai_queries:
            avg_time = statistics.mean([r["total_time"] for r in ai_queries])
            print(f"   Average total time: {avg_time:.2f}s")
            print(f"   AI generation time: {statistics.mean(self.results['ai_generated']):.2f}s avg")
        
        print(f"\n⚡ Query execution times:")
        if self.results["query_execution"]:
            print(f"   Average: {statistics.mean(self.results['query_execution'])*1000:.2f}ms")
            print(f"   Min: {min(self.results['query_execution'])*1000:.2f}ms")
            print(f"   Max: {max(self.results['query_execution'])*1000:.2f}ms")
        
        # Performance improvement calculation
        if pattern_queries and ai_queries:
            pattern_avg = statistics.mean([r["total_time"] for r in pattern_queries])
            ai_avg = statistics.mean([r["total_time"] for r in ai_queries])
            improvement = (ai_avg - pattern_avg) / ai_avg * 100
            speedup = ai_avg / pattern_avg
            
            print(f"\n🚀 PERFORMANCE IMPROVEMENT:")
            print(f"   Pattern matching is {speedup:.1f}x faster than AI generation")
            print(f"   Time saved: {improvement:.1f}% ({ai_avg - pattern_avg:.2f}s per query)")
        
        # Save detailed results
        with open("benchmark_results.json", "w") as f:
            json.dump(self.results, f, indent=2)
        print(f"\n📁 Detailed results saved to benchmark_results.json")

async def main():
    """Run the benchmark"""
    benchmark = PerformanceBenchmark()
    await benchmark.run_benchmark()

if __name__ == "__main__":
    print("Starting FalkorDB Chat Interface Performance Benchmark...")
    print("Note: First AI query may take longer due to model loading")
    asyncio.run(main())