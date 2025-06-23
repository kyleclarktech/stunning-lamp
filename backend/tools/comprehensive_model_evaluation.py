#!/usr/bin/env python3
"""
Comprehensive evaluation of top 3 models for complex organizational query translation.
Designed to run inside Docker container for direct FalkorDB access.
"""

import asyncio
import json
import time
import sys
import os
from datetime import datetime
from typing import Dict, List, Any, Tuple, Optional
import httpx
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import load_prompt, clean_ai_generated_query, get_falkor_client
from query_processor import process_query
from query_validator import validate_query

# Models to evaluate - remaining models not tested in first run
MODELS_TO_EVALUATE = [
    "mistral:7b",
    "codeqwen:7b", 
    "granite-code:8b",
    "phi4:14b",
    "granite3.3:8b",
    "granite3.3:8b-largectx"
]

# Comprehensive test queries organized by category and complexity
EVALUATION_QUERIES = {
    "simple_lookups": [
        {
            "query": "Who is the CTO?",
            "expected_pattern": "role.*CTO|chief.*technology",
            "complexity": 1
        },
        {
            "query": "List all teams in the engineering department",
            "expected_pattern": "Team.*department.*engineering",
            "complexity": 1
        },
        {
            "query": "Find employees in the Berlin office",
            "expected_pattern": "Person.*location.*Berlin|office.*Berlin",
            "complexity": 1
        }
    ],
    
    "filtered_searches": [
        {
            "query": "Show me senior engineers with Python and React skills",
            "expected_pattern": "HAS_SKILL.*Python.*React.*seniority.*senior",
            "complexity": 2
        },
        {
            "query": "Find all critical security policies updated this year",
            "expected_pattern": "Policy.*security.*critical|severity.*updated",
            "complexity": 2
        },
        {
            "query": "Which teams have more than 10 members?",
            "expected_pattern": "Team.*MEMBER_OF.*COUNT.*>.*10",
            "complexity": 2
        }
    ],
    
    "aggregations": [
        {
            "query": "How many people work in each department?",
            "expected_pattern": "COUNT.*Person.*department.*GROUP BY",
            "complexity": 3
        },
        {
            "query": "What's the average team size across all departments?",
            "expected_pattern": "AVG.*COUNT.*Team.*MEMBER_OF",
            "complexity": 3
        },
        {
            "query": "Show the distribution of seniority levels by location",
            "expected_pattern": "seniority.*location.*COUNT.*GROUP BY",
            "complexity": 3
        }
    ],
    
    "multi_hop_relationships": [
        {
            "query": "Find all people who report to someone in the data team",
            "expected_pattern": "REPORTS_TO.*MEMBER_OF.*Team.*data",
            "complexity": 4
        },
        {
            "query": "Which policies affect teams working on customer projects?",
            "expected_pattern": "Policy.*AFFECTS|RESPONSIBLE_FOR.*Team.*Project.*customer",
            "complexity": 4
        },
        {
            "query": "Show me engineers who work with clients in the financial sector",
            "expected_pattern": "Person.*engineer.*WORKS_WITH.*Client.*financial|sector",
            "complexity": 4
        }
    ],
    
    "path_finding": [
        {
            "query": "What's the reporting chain from junior developers to the CEO?",
            "expected_pattern": "path.*REPORTS_TO.*junior.*CEO|shortestPath",
            "complexity": 5
        },
        {
            "query": "Find all connections between the security team and compliance policies",
            "expected_pattern": "path.*Team.*security.*Policy.*compliance|allShortestPaths",
            "complexity": 5
        },
        {
            "query": "Show how the product team collaborates with engineering",
            "expected_pattern": "Team.*product.*engineering.*WORKS_WITH|COLLABORATES|path",
            "complexity": 5
        }
    ],
    
    "complex_patterns": [
        {
            "query": "Find circular reporting structures (people who indirectly report to themselves)",
            "expected_pattern": "REPORTS_TO.*cycle|circular.*path.*=",
            "complexity": 6
        },
        {
            "query": "Which teams have members with skills that no other team has?",
            "expected_pattern": "UNIQUE.*skills.*Team.*NOT.*EXISTS|DISTINCT",
            "complexity": 6
        },
        {
            "query": "Identify skill gaps: skills needed by projects but not possessed by allocated team members",
            "expected_pattern": "Project.*REQUIRES.*Skill.*NOT.*HAS_SKILL.*ALLOCATED_TO",
            "complexity": 6
        }
    ],
    
    "ambiguous_requests": [
        {
            "query": "Show me the important people",
            "expected_pattern": "Person.*(manager|lead|senior|director|chief)",
            "complexity": 2,
            "ambiguous": True
        },
        {
            "query": "Find problematic areas in the organization",
            "expected_pattern": "Policy.*violation|risk|Team.*understaffed|issue",
            "complexity": 3,
            "ambiguous": True
        },
        {
            "query": "Who should I talk to about AI stuff?",
            "expected_pattern": "Person.*AI|artificial intelligence|machine learning|HAS_SKILL",
            "complexity": 2,
            "ambiguous": True
        }
    ],
    
    "organizational_insights": [
        {
            "query": "What's the bus factor for critical projects? (how many people would need to leave to endanger the project)",
            "expected_pattern": "Project.*critical.*COUNT.*DISTINCT.*Person.*ALLOCATED_TO",
            "complexity": 5
        },
        {
            "query": "Find potential compliance violations: teams without required policy training",
            "expected_pattern": "Team.*NOT.*TRAINED_ON|COMPLIANCE.*Policy.*required",
            "complexity": 5
        },
        {
            "query": "Identify knowledge silos: skills possessed by only one person in a team",
            "expected_pattern": "Skill.*COUNT.*=.*1.*Team.*MEMBER_OF",
            "complexity": 5
        }
    ],
    
    "edge_cases": [
        {
            "query": "Find people named John or Jon (handle name variations)",
            "expected_pattern": "name.*John|Jon|CONTAINS|~",
            "complexity": 2
        },
        {
            "query": "What happens if everyone in the data team leaves?",
            "expected_pattern": "Team.*data.*MEMBER_OF|DEPENDS_ON|impact",
            "complexity": 4
        },
        {
            "query": "πŸ'₯ Find team leads πŸ'₯",  # Test emoji handling
            "expected_pattern": "Team.*lead|is_lead.*true",
            "complexity": 1
        }
    ]
}

async def call_model(prompt_text: str, model_name: str, timeout: int = 30) -> str:
    """Call a specific model with the prompt."""
    # Use localhost when running inside Docker container
    # Use Docker service name when running in container
    url = os.getenv("OLLAMA_HOST", "http://ollama:11434") + "/api/generate"
    if "ollama" not in url:
        url = "http://ollama:11434/api/generate"  # Force Docker hostname
    
    async with httpx.AsyncClient(timeout=timeout) as client:
        payload = {
            "model": model_name,
            "prompt": prompt_text,
            "stream": False,
            "context": []
        }
        
        resp = await client.post(url, json=payload)
        
        if resp.status_code != 200:
            raise Exception(f"Model returned status {resp.status_code}")
        
        data = resp.json()
        return data.get('response', '')

async def execute_query(cypher_query: str) -> Tuple[bool, Optional[List], Optional[str], float]:
    """Execute query and return (success, results, error, execution_time)."""
    start_time = time.time()
    
    try:
        def run_query():
            falkor = get_falkor_client()
            db = falkor.select_graph("agent_poc")
            result = db.query(cypher_query)
            return result
        
        result = await asyncio.wait_for(
            asyncio.get_event_loop().run_in_executor(None, run_query),
            timeout=15
        )
        
        execution_time = time.time() - start_time
        has_results = result and result.result_set and len(result.result_set) > 0
        
        return True, result.result_set if has_results else [], None, execution_time
        
    except asyncio.TimeoutError:
        return False, None, "Query timeout (15s)", time.time() - start_time
    except Exception as e:
        return False, None, str(e), time.time() - start_time

def evaluate_query_quality(query: str, test_case: Dict) -> Dict[str, Any]:
    """Evaluate the quality of a generated query."""
    scores = {
        "syntax_valid": False,
        "pattern_match": False,
        "complexity_appropriate": False,
        "handles_ambiguity": False
    }
    
    # Check syntax validity
    if query and 'MATCH' in query and 'RETURN' in query:
        scores["syntax_valid"] = True
    
    # Check if query matches expected pattern
    import re
    if test_case.get("expected_pattern"):
        pattern = test_case["expected_pattern"]
        if re.search(pattern, query, re.IGNORECASE):
            scores["pattern_match"] = True
    
    # Check complexity appropriateness
    query_complexity = 0
    if 'WHERE' in query: query_complexity += 1
    if 'GROUP BY' in query: query_complexity += 1
    if 'COUNT' in query or 'AVG' in query: query_complexity += 1
    if 'path' in query.lower(): query_complexity += 2
    if 'NOT EXISTS' in query: query_complexity += 1
    
    expected_complexity = test_case.get("complexity", 1)
    scores["complexity_appropriate"] = abs(query_complexity - expected_complexity) <= 1
    
    # Check ambiguity handling
    if test_case.get("ambiguous", False):
        # For ambiguous queries, check if the model made reasonable assumptions
        scores["handles_ambiguity"] = scores["syntax_valid"] and len(query) > 50
    else:
        scores["handles_ambiguity"] = True
    
    return scores

async def evaluate_model(model_name: str, test_queries: Dict) -> Dict[str, Any]:
    """Comprehensively evaluate a single model."""
    print(f"\n{'='*80}")
    print(f"Evaluating: {model_name}")
    print(f"{'='*80}")
    
    results = {
        "model": model_name,
        "timestamp": datetime.now().isoformat(),
        "categories": {},
        "overall_metrics": {
            "total_queries": 0,
            "syntax_valid": 0,
            "execution_success": 0,
            "has_results": 0,
            "pattern_matches": 0,
            "avg_generation_time": 0,
            "avg_execution_time": 0,
            "category_scores": {}
        }
    }
    
    all_generation_times = []
    all_execution_times = []
    
    for category, queries in test_queries.items():
        print(f"\n[{category.upper()}]")
        category_results = []
        
        for i, test_case in enumerate(queries, 1):
            query_text = test_case["query"]
            print(f"\n{i}. {query_text}")
            
            # Generate query
            start_time = time.time()
            try:
                prompt = load_prompt("generate_query_simple", user_message=query_text)
                prompt += f"\n\nQuestion: \"{query_text}\"\nQuery:"
                
                raw_response = await call_model(prompt, model_name)
                cypher_query = clean_ai_generated_query(raw_response)
                
                # Apply post-processing to fix common FalkorDB issues
                original_query = cypher_query
                cypher_query = process_query(cypher_query)
                
                # Validate the query
                is_valid, validation_errors, validation_warnings = validate_query(cypher_query)
                
                generation_time = time.time() - start_time
                all_generation_times.append(generation_time)
                
                print(f"   Generated: {cypher_query[:100]}...")
                print(f"   Generation time: {generation_time:.2f}s")
                
                if original_query != cypher_query:
                    print(f"   Post-processing applied: Yes")
                
                if not is_valid:
                    print(f"   Validation errors: {', '.join(validation_errors[:2])}")
                
                # Evaluate query quality
                quality_scores = evaluate_query_quality(cypher_query, test_case)
                
                # Execute query
                success, results_data, error, exec_time = await execute_query(cypher_query)
                all_execution_times.append(exec_time)
                
                result_entry = {
                    "query": query_text,
                    "generated_cypher": cypher_query,
                    "generation_time": generation_time,
                    "execution_time": exec_time,
                    "syntax_valid": quality_scores["syntax_valid"],
                    "execution_success": success,
                    "has_results": results_data is not None and len(results_data) > 0,
                    "pattern_match": quality_scores["pattern_match"],
                    "complexity_appropriate": quality_scores["complexity_appropriate"],
                    "handles_ambiguity": quality_scores["handles_ambiguity"],
                    "error": error,
                    "result_count": len(results_data) if results_data else 0
                }
                
                category_results.append(result_entry)
                
                # Update overall metrics
                results["overall_metrics"]["total_queries"] += 1
                if quality_scores["syntax_valid"]:
                    results["overall_metrics"]["syntax_valid"] += 1
                if success:
                    results["overall_metrics"]["execution_success"] += 1
                if result_entry["has_results"]:
                    results["overall_metrics"]["has_results"] += 1
                if quality_scores["pattern_match"]:
                    results["overall_metrics"]["pattern_matches"] += 1
                
                # Print summary
                status = "OK" if success else "FAIL"
                print(f"   Execution: {status} ({exec_time:.2f}s)")
                if results_data:
                    print(f"   Results: {len(results_data)} rows")
                if error:
                    print(f"   Error: {error}")
                
            except Exception as e:
                print(f"   ERROR: {str(e)}")
                category_results.append({
                    "query": query_text,
                    "error": str(e),
                    "generation_time": time.time() - start_time
                })
        
        results["categories"][category] = category_results
        
        # Calculate category score
        if category_results:
            category_score = sum(
                r.get("syntax_valid", False) and 
                r.get("execution_success", False) and
                r.get("pattern_match", False)
                for r in category_results
            ) / len(category_results)
            results["overall_metrics"]["category_scores"][category] = category_score
    
    # Calculate averages
    if all_generation_times:
        results["overall_metrics"]["avg_generation_time"] = sum(all_generation_times) / len(all_generation_times)
    if all_execution_times:
        results["overall_metrics"]["avg_execution_time"] = sum(all_execution_times) / len(all_execution_times)
    
    # Calculate overall score
    metrics = results["overall_metrics"]
    results["overall_score"] = (
        (metrics["syntax_valid"] / metrics["total_queries"]) * 0.25 +
        (metrics["execution_success"] / metrics["total_queries"]) * 0.25 +
        (metrics["pattern_matches"] / metrics["total_queries"]) * 0.25 +
        (metrics["has_results"] / metrics["total_queries"]) * 0.25
    ) * 100
    
    return results

async def main():
    """Run comprehensive evaluation of top 3 models."""
    print("COMPREHENSIVE MODEL EVALUATION")
    print("Testing complex organizational query translation capabilities")
    print("=" * 80)
    
    # Check if running inside Docker
    if os.getenv('FALKOR_HOST') != 'falkordb':
        print("\nWARNING: Not running inside Docker container!")
        print("Run this script inside Docker for proper FalkorDB access:")
        print("docker exec -it stunning-lamp-api-1 python tools/comprehensive_model_evaluation.py")
        print("\nContinuing with current configuration...")
    
    all_results = []
    
    # Evaluate each model
    for model in MODELS_TO_EVALUATE:
        try:
            result = await evaluate_model(model, EVALUATION_QUERIES)
            all_results.append(result)
            
            # Save intermediate results
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            with open(f"comprehensive_eval_{model.replace(':', '_')}_{timestamp}.json", 'w') as f:
                json.dump(result, f, indent=2)
                
        except Exception as e:
            print(f"\nError evaluating {model}: {e}")
            all_results.append({"model": model, "error": str(e)})
    
    # Generate comparative report
    print("\n" + "="*80)
    print("COMPARATIVE ANALYSIS")
    print("="*80)
    
    # Sort by overall score
    valid_results = [r for r in all_results if "overall_score" in r]
    valid_results.sort(key=lambda x: x["overall_score"], reverse=True)
    
    print("\n## Overall Rankings")
    for i, result in enumerate(valid_results, 1):
        metrics = result["overall_metrics"]
        print(f"\n{i}. {result['model']} - Score: {result['overall_score']:.1f}/100")
        print(f"   Syntax Valid: {metrics['syntax_valid']}/{metrics['total_queries']} ({metrics['syntax_valid']/metrics['total_queries']*100:.0f}%)")
        print(f"   Execution Success: {metrics['execution_success']}/{metrics['total_queries']} ({metrics['execution_success']/metrics['total_queries']*100:.0f}%)")
        print(f"   Pattern Matches: {metrics['pattern_matches']}/{metrics['total_queries']} ({metrics['pattern_matches']/metrics['total_queries']*100:.0f}%)")
        print(f"   Avg Generation Time: {metrics['avg_generation_time']:.2f}s")
        print(f"   Avg Execution Time: {metrics['avg_execution_time']:.2f}s")
    
    print("\n## Category Performance")
    categories = list(EVALUATION_QUERIES.keys())
    
    print("\n| Category | " + " | ".join(f"{m['model'][:10]}" for m in valid_results) + " |")
    print("|----------|" + "|".join("-"*12 for _ in valid_results) + "|")
    
    for category in categories:
        row = f"| {category[:20]:<20} |"
        for result in valid_results:
            score = result["overall_metrics"]["category_scores"].get(category, 0)
            row += f" {score*100:>10.0f}% |"
        print(row)
    
    # Save final comprehensive report
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    final_report = {
        "evaluation_date": datetime.now().isoformat(),
        "models_evaluated": MODELS_TO_EVALUATE,
        "total_test_queries": sum(len(queries) for queries in EVALUATION_QUERIES.values()),
        "results": all_results,
        "rankings": [{"model": r["model"], "score": r["overall_score"]} for r in valid_results]
    }
    
    with open(f"comprehensive_evaluation_final_{timestamp}.json", 'w') as f:
        json.dump(final_report, f, indent=2)
    
    # Generate markdown report
    with open(f"comprehensive_evaluation_report_{timestamp}.md", 'w') as f:
        f.write("# Comprehensive Model Evaluation Report\n\n")
        f.write(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**Models**: {', '.join(MODELS_TO_EVALUATE)}\n\n")
        f.write(f"**Total Queries**: {final_report['total_test_queries']}\n\n")
        
        f.write("## Rankings\n\n")
        for i, r in enumerate(valid_results, 1):
            f.write(f"{i}. **{r['model']}** - {r['overall_score']:.1f}/100\n")
        
        f.write("\n## Detailed Results\n\n")
        for result in valid_results:
            f.write(f"### {result['model']}\n\n")
            metrics = result['overall_metrics']
            f.write(f"- Syntax Validity: {metrics['syntax_valid']/metrics['total_queries']*100:.0f}%\n")
            f.write(f"- Execution Success: {metrics['execution_success']/metrics['total_queries']*100:.0f}%\n")
            f.write(f"- Average Generation Time: {metrics['avg_generation_time']:.2f}s\n")
            f.write(f"- Category Scores: {', '.join(f'{k}: {v*100:.0f}%' for k, v in metrics['category_scores'].items())}\n\n")
    
    print(f"\n\nEvaluation complete! Results saved to:")
    print(f"  - comprehensive_evaluation_final_{timestamp}.json")
    print(f"  - comprehensive_evaluation_report_{timestamp}.md")

if __name__ == "__main__":
    asyncio.run(main())