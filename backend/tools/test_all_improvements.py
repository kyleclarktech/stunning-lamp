#!/usr/bin/env python3
"""
Comprehensive test suite to validate FalkorDB query generation improvements.
Tests all 9 models with 27 queries, tracking improvements applied and success rates.
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
import statistics
from concurrent.futures import ThreadPoolExecutor
import threading

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import load_prompt, clean_ai_generated_query, get_falkor_client
from query_processor import QueryProcessor
from query_validator import QueryValidator

# Lock for console output
print_lock = threading.Lock()

# Models to evaluate - exactly as requested
MODELS_TO_EVALUATE = [
    "mistral:7b",
    "mistral-nemo:12b", 
    "qwen2.5:7b",
    "qwen2.5:14b",
    "qwq:32b",
    "granite3-dense:8b",
    "granite3.1-moe:3b",
    "granite3.3:8b-largectx",
    "phi4:14b"
]

# Comprehensive test queries from the evaluation (all 27)
TEST_QUERIES = [
    # Simple lookups (3)
    "Who is the CTO?",
    "List all teams in the engineering department",
    "Find employees in the Berlin office",
    
    # Filtered searches (3)
    "Show me senior engineers with Python and React skills",
    "Find all critical security policies updated this year",
    "Which teams have more than 10 members?",
    
    # Aggregations (3)
    "How many people work in each department?",
    "What's the average team size across all departments?",
    "Show the distribution of seniority levels by location",
    
    # Multi-hop relationships (3)
    "Find all people who report to someone in the data team",
    "Which policies affect teams working on customer projects?",
    "Show me engineers who work with clients in the financial sector",
    
    # Path finding (3)
    "What's the reporting chain from junior developers to the CEO?",
    "Find all connections between the security team and compliance policies",
    "Show how the product team collaborates with engineering",
    
    # Complex patterns (3)
    "Find circular reporting structures (people who indirectly report to themselves)",
    "Which teams have members with skills that no other team has?",
    "Identify skill gaps: skills needed by projects but not possessed by allocated team members",
    
    # Ambiguous requests (3)
    "Show me the important people",
    "Find problematic areas in the organization",
    "Who should I talk to about AI stuff?",
    
    # Organizational insights (3)
    "What's the bus factor for critical projects? (how many people would need to leave to endanger the project)",
    "Find potential compliance violations: teams without required policy training",
    "Identify knowledge silos: skills possessed by only one person in a team",
    
    # Edge cases (3)
    "Find people named John or Jon (handle name variations)",
    "What happens if everyone in the data team leaves?",
    "Find team leads"
]

class ImprovementTracker:
    """Tracks which improvements were applied to each query"""
    
    def __init__(self):
        self.improvements = {
            "function_names_fixed": False,
            "semicolons_removed": False,
            "validation_warnings": [],
            "validation_errors": [],
            "post_processing_applied": False,
            "original_query": "",
            "processed_query": "",
            "execution_time": 0,
            "generation_time": 0
        }
    
    def reset(self):
        """Reset for new query"""
        self.__init__()
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return self.improvements

async def check_model_available(model_name: str) -> bool:
    """Check if a model is available in Ollama"""
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get("http://ollama:11434/api/tags")
            if response.status_code == 200:
                data = response.json()
                models = data.get('models', [])
                return any(m.get('name') == model_name for m in models)
    except Exception:
        return False
    return False

async def generate_query_with_model(model: str, prompt: str, timeout: float = 5.0) -> Tuple[Optional[str], float, str]:
    """
    Generate a Cypher query using specified model with timeout.
    Returns: (query, generation_time, error_message)
    """
    start_time = time.time()
    
    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(timeout)) as client:
            response = await client.post(
                "http://ollama:11434/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.1,
                        "top_p": 0.9,
                        "num_predict": 300
                    }
                }
            )
            
            generation_time = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                query = clean_ai_generated_query(result.get('response', ''))
                return query, generation_time, ""
            else:
                return None, generation_time, f"HTTP {response.status_code}"
                
    except httpx.TimeoutException:
        generation_time = time.time() - start_time
        return None, generation_time, "Timeout"
    except Exception as e:
        generation_time = time.time() - start_time
        return None, generation_time, str(e)

def execute_query_direct(query: str, timeout: float = 5.0) -> Tuple[bool, Any, str]:
    """
    Execute query directly on FalkorDB.
    Returns: (success, results, error_message)
    """
    try:
        client = get_falkor_client()
        graph = client.select_graph("agent_poc")
        
        # Execute with timeout
        start_time = time.time()
        result = graph.query(query)
        execution_time = time.time() - start_time
        
        if execution_time > timeout:
            return False, None, "Execution timeout"
            
        # Check if we got results
        if hasattr(result, 'result_set') and result.result_set:
            return True, result.result_set, ""
        else:
            # Even empty results are technically successful
            return True, [], ""
            
    except Exception as e:
        error_msg = str(e)
        return False, None, error_msg

async def test_query_without_improvements(model: str, query: str, prompt_template: str) -> Dict[str, Any]:
    """Test a single query without any improvements (baseline)"""
    # Generate prompt
    prompt = prompt_template.replace("{{ message }}", query)
    
    # Generate query
    generated_query, gen_time, gen_error = await generate_query_with_model(model, prompt)
    
    if not generated_query:
        return {
            "query": query,
            "model": model,
            "baseline": True,
            "generated_query": None,
            "generation_time": gen_time,
            "generation_error": gen_error,
            "syntax_valid": False,
            "execution_success": False,
            "execution_error": "No query generated"
        }
    
    # Execute directly without improvements
    success, results, exec_error = execute_query_direct(generated_query)
    
    return {
        "query": query,
        "model": model,
        "baseline": True,
        "generated_query": generated_query,
        "generation_time": gen_time,
        "syntax_valid": not exec_error.startswith("Syntax"),
        "execution_success": success,
        "execution_error": exec_error,
        "result_count": len(results) if results else 0
    }

async def test_query_with_improvements(model: str, query: str, prompt_template: str) -> Dict[str, Any]:
    """Test a single query with all improvements applied"""
    tracker = ImprovementTracker()
    
    # Generate prompt
    prompt = prompt_template.replace("{{ message }}", query)
    
    # Generate query
    generated_query, gen_time, gen_error = await generate_query_with_model(model, prompt)
    tracker.improvements["generation_time"] = gen_time
    tracker.improvements["original_query"] = generated_query or ""
    
    if not generated_query:
        return {
            "query": query,
            "model": model,
            "baseline": False,
            "generated_query": None,
            "generation_time": gen_time,
            "generation_error": gen_error,
            "syntax_valid": False,
            "execution_success": False,
            "execution_error": "No query generated",
            "improvements": tracker.to_dict()
        }
    
    # Apply query processor
    processor = QueryProcessor()
    processed_query = processor.process(generated_query)
    
    if processed_query != generated_query:
        tracker.improvements["post_processing_applied"] = True
        tracker.improvements["processed_query"] = processed_query
        
        # Track specific fixes
        if "function_name" in str(processor.fixes_applied):
            tracker.improvements["function_names_fixed"] = True
        if "removed_trailing_semicolon" in processor.fixes_applied:
            tracker.improvements["semicolons_removed"] = True
    
    # Validate query
    validator = QueryValidator()
    is_valid, errors, warnings = validator.validate(processed_query)
    tracker.improvements["validation_errors"] = errors
    tracker.improvements["validation_warnings"] = warnings
    
    # Execute query
    start_exec = time.time()
    success, results, exec_error = execute_query_direct(processed_query)
    tracker.improvements["execution_time"] = time.time() - start_exec
    
    return {
        "query": query,
        "model": model,
        "baseline": False,
        "generated_query": generated_query,
        "processed_query": processed_query,
        "generation_time": gen_time,
        "syntax_valid": is_valid and not exec_error.startswith("Syntax"),
        "execution_success": success,
        "execution_error": exec_error,
        "result_count": len(results) if results else 0,
        "improvements": tracker.to_dict()
    }

async def test_model(model_name: str, progress_callback=None) -> Dict[str, Any]:
    """Test a single model with all queries"""
    with print_lock:
        print(f"\n{'='*60}")
        print(f"Testing model: {model_name}")
        print(f"{'='*60}")
    
    # Check if model is available
    if not await check_model_available(model_name):
        with print_lock:
            print(f"[X] Model {model_name} not available")
        return {
            "model": model_name,
            "available": False,
            "baseline_results": [],
            "improved_results": []
        }
    
    # Load prompt template
    prompt_template = load_prompt("generate_query")
    
    baseline_results = []
    improved_results = []
    
    # Test each query
    for i, query in enumerate(TEST_QUERIES, 1):
        if progress_callback:
            progress_callback(model_name, i, len(TEST_QUERIES))
        
        with print_lock:
            print(f"\n[{i}/{len(TEST_QUERIES)}] Testing: {query[:50]}...")
        
        # Test baseline (without improvements)
        with print_lock:
            print("  [B] Baseline test...", end='', flush=True)
        baseline = await test_query_without_improvements(model_name, query, prompt_template)
        baseline_results.append(baseline)
        
        baseline_symbol = "[OK]" if baseline["execution_success"] else "[FAIL]"
        with print_lock:
            print(f" {baseline_symbol}")
        
        # Test with improvements
        with print_lock:
            print("  [I] Improved test...", end='', flush=True)
        improved = await test_query_with_improvements(model_name, query, prompt_template)
        improved_results.append(improved)
        
        improved_symbol = "[OK]" if improved["execution_success"] else "[FAIL]"
        with print_lock:
            print(f" {improved_symbol}")
        
        # Show improvement if any
        if not baseline["execution_success"] and improved["execution_success"]:
            with print_lock:
                print(f"  *** IMPROVEMENT: Query now works!")
                if improved["improvements"]["function_names_fixed"]:
                    print(f"     - Fixed function names")
                if improved["improvements"]["semicolons_removed"]:
                    print(f"     - Removed semicolons")
                if improved["improvements"]["post_processing_applied"]:
                    print(f"     - Applied post-processing")
    
    # Calculate statistics
    baseline_success = sum(1 for r in baseline_results if r["execution_success"])
    improved_success = sum(1 for r in improved_results if r["execution_success"])
    
    model_stats = {
        "model": model_name,
        "available": True,
        "baseline_success_rate": baseline_success / len(TEST_QUERIES) * 100,
        "improved_success_rate": improved_success / len(TEST_QUERIES) * 100,
        "improvement_percentage": (improved_success - baseline_success) / len(TEST_QUERIES) * 100,
        "baseline_results": baseline_results,
        "improved_results": improved_results,
        "timestamp": datetime.now().isoformat()
    }
    
    with print_lock:
        print(f"\n{model_name} Summary:")
        print(f"  Baseline: {baseline_success}/{len(TEST_QUERIES)} ({model_stats['baseline_success_rate']:.1f}%)")
        print(f"  Improved: {improved_success}/{len(TEST_QUERIES)} ({model_stats['improved_success_rate']:.1f}%)")
        print(f"  Improvement: +{model_stats['improvement_percentage']:.1f}%")
    
    return model_stats

def progress_tracker(model: str, current: int, total: int):
    """Progress callback for real-time updates"""
    percentage = (current / total) * 100
    with print_lock:
        print(f"\r  Progress: [{current}/{total}] {percentage:.0f}%", end='', flush=True)

async def test_model_group(models: List[str], group_num: int) -> List[Dict[str, Any]]:
    """Test a group of models"""
    with print_lock:
        print(f"\n\n{'#'*60}")
        print(f"# GROUP {group_num}: Testing {len(models)} models")
        print(f"# Models: {', '.join(models)}")
        print(f"{'#'*60}")
    
    results = []
    for model in models:
        result = await test_model(model, progress_tracker)
        results.append(result)
        
        # Save intermediate results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"improvement_test_{model.replace(':', '_')}_{timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(result, f, indent=2)
        
        with print_lock:
            print(f"\n[SAVED] Intermediate results to {filename}")
    
    return results

async def main():
    """Main test execution"""
    start_time = time.time()
    
    print("="*80)
    print("COMPREHENSIVE FALKORDB QUERY GENERATION IMPROVEMENT VALIDATION")
    print("="*80)
    print(f"Models to test: {len(MODELS_TO_EVALUATE)}")
    print(f"Queries per model: {len(TEST_QUERIES)}")
    print(f"Total tests: {len(MODELS_TO_EVALUATE) * len(TEST_QUERIES) * 2} (baseline + improved)")
    print("="*80)
    
    # Split models into 3 groups for parallel execution
    model_groups = [
        MODELS_TO_EVALUATE[0:3],  # Group 1: mistral:7b, mistral-nemo:12b, qwen2.5:7b
        MODELS_TO_EVALUATE[3:6],  # Group 2: qwen2.5:14b, qwq:32b, granite3-dense:8b
        MODELS_TO_EVALUATE[6:9]   # Group 3: granite3.1-moe:3b, granite3.3:8b-largectx, phi4:14b
    ]
    
    all_results = []
    
    # Run groups sequentially (to avoid overloading)
    for i, group in enumerate(model_groups, 1):
        group_results = await test_model_group(group, i)
        all_results.extend(group_results)
    
    # Generate final report
    total_time = time.time() - start_time
    
    # Calculate overall statistics
    overall_baseline_success = 0
    overall_improved_success = 0
    total_tests = 0
    
    for result in all_results:
        if result["available"]:
            overall_baseline_success += len([r for r in result["baseline_results"] if r["execution_success"]])
            overall_improved_success += len([r for r in result["improved_results"] if r["execution_success"]])
            total_tests += len(result["baseline_results"])
    
    # Save complete results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    final_results = {
        "test_date": datetime.now().isoformat(),
        "total_models": len(MODELS_TO_EVALUATE),
        "total_queries": len(TEST_QUERIES),
        "total_execution_time": total_time,
        "overall_baseline_success_rate": (overall_baseline_success / total_tests * 100) if total_tests > 0 else 0,
        "overall_improved_success_rate": (overall_improved_success / total_tests * 100) if total_tests > 0 else 0,
        "overall_improvement": ((overall_improved_success - overall_baseline_success) / total_tests * 100) if total_tests > 0 else 0,
        "model_results": all_results
    }
    
    results_filename = f"comprehensive_improvement_validation_{timestamp}.json"
    with open(results_filename, 'w') as f:
        json.dump(final_results, f, indent=2)
    
    print(f"\n\n{'='*80}")
    print("FINAL RESULTS")
    print(f"{'='*80}")
    print(f"Total execution time: {total_time/60:.1f} minutes")
    print(f"Overall baseline success rate: {final_results['overall_baseline_success_rate']:.1f}%")
    print(f"Overall improved success rate: {final_results['overall_improved_success_rate']:.1f}%")
    print(f"Overall improvement: +{final_results['overall_improvement']:.1f}%")
    print(f"\nComplete results saved to: {results_filename}")
    print(f"{'='*80}")
    
    # Generate markdown report
    generate_markdown_report(final_results, f"IMPROVEMENT_VALIDATION_REPORT_{timestamp}.md")

def generate_markdown_report(results: Dict[str, Any], filename: str):
    """Generate detailed markdown report"""
    with open(filename, 'w') as f:
        f.write("# FalkorDB Query Generation Improvement Validation Report\n\n")
        f.write(f"**Test Date**: {results['test_date']}\n\n")
        f.write(f"**Total Models Tested**: {results['total_models']}\n")
        f.write(f"**Total Queries per Model**: {results['total_queries']}\n")
        f.write(f"**Total Execution Time**: {results['total_execution_time']/60:.1f} minutes\n\n")
        
        f.write("## Executive Summary\n\n")
        f.write(f"- **Baseline Success Rate**: {results['overall_baseline_success_rate']:.1f}%\n")
        f.write(f"- **Improved Success Rate**: {results['overall_improved_success_rate']:.1f}%\n")
        f.write(f"- **Overall Improvement**: +{results['overall_improvement']:.1f}%\n\n")
        
        # Target achievement
        if results['overall_improved_success_rate'] >= 85:
            f.write("### [SUCCESS] TARGET ACHIEVED! Success rate exceeds 85%\n\n")
        else:
            f.write("### [WARNING] Target of 85-90% success rate not yet achieved\n\n")
        
        f.write("## Model-by-Model Results\n\n")
        
        # Sort models by improvement
        sorted_models = sorted(
            [r for r in results['model_results'] if r['available']], 
            key=lambda x: x.get('improved_success_rate', 0), 
            reverse=True
        )
        
        f.write("| Model | Baseline | Improved | Improvement | Status |\n")
        f.write("|-------|----------|----------|-------------|--------|\n")
        
        for model in sorted_models:
            baseline = f"{model['baseline_success_rate']:.1f}%"
            improved = f"{model['improved_success_rate']:.1f}%"
            improvement = f"+{model['improvement_percentage']:.1f}%"
            
            if model['improved_success_rate'] >= 85:
                status = "[OK] Excellent"
            elif model['improved_success_rate'] >= 70:
                status = "[+] Good"
            elif model['improved_success_rate'] >= 50:
                status = "[~] Fair"
            else:
                status = "[-] Poor"
            
            f.write(f"| {model['model']} | {baseline} | {improved} | {improvement} | {status} |\n")
        
        # Unavailable models
        unavailable = [r for r in results['model_results'] if not r['available']]
        if unavailable:
            f.write(f"\n### Unavailable Models ({len(unavailable)})\n")
            for model in unavailable:
                f.write(f"- {model['model']}\n")
        
        f.write("\n## Improvement Analysis\n\n")
        
        # Analyze which improvements helped most
        improvements_applied = {
            "function_names": 0,
            "semicolons": 0,
            "post_processing": 0,
            "validation_caught": 0
        }
        
        improvement_examples = {
            "function_names": [],
            "semicolons": [],
            "post_processing": []
        }
        
        for model_result in results['model_results']:
            if not model_result['available']:
                continue
                
            for i, (baseline, improved) in enumerate(zip(model_result['baseline_results'], model_result['improved_results'])):
                if not baseline['execution_success'] and improved['execution_success']:
                    impr = improved.get('improvements', {})
                    
                    if impr.get('function_names_fixed'):
                        improvements_applied['function_names'] += 1
                        if len(improvement_examples['function_names']) < 3:
                            improvement_examples['function_names'].append({
                                'model': model_result['model'],
                                'query': baseline['query'],
                                'original': impr.get('original_query', ''),
                                'fixed': impr.get('processed_query', '')
                            })
                    
                    if impr.get('semicolons_removed'):
                        improvements_applied['semicolons'] += 1
                        if len(improvement_examples['semicolons']) < 3:
                            improvement_examples['semicolons'].append({
                                'model': model_result['model'],
                                'query': baseline['query']
                            })
                    
                    if impr.get('post_processing_applied'):
                        improvements_applied['post_processing'] += 1
                    
                    if impr.get('validation_errors'):
                        improvements_applied['validation_caught'] += 1
        
        f.write("### Most Effective Improvements\n\n")
        f.write("| Improvement Type | Queries Fixed | Impact |\n")
        f.write("|-----------------|---------------|--------|\n")
        
        total_improvements = sum(improvements_applied.values())
        for improvement, count in sorted(improvements_applied.items(), key=lambda x: x[1], reverse=True):
            if count > 0:
                impact = f"{count/total_improvements*100:.1f}%" if total_improvements > 0 else "0%"
                f.write(f"| {improvement.replace('_', ' ').title()} | {count} | {impact} |\n")
        
        f.write("\n### Example Improvements\n\n")
        
        if improvement_examples['function_names']:
            f.write("#### Function Name Fixes\n\n")
            for ex in improvement_examples['function_names'][:2]:
                f.write(f"**Model**: {ex['model']}\n")
                f.write(f"**Query**: {ex['query']}\n")
                f.write(f"**Original**: `{ex['original'][:100]}...`\n")
                f.write(f"**Fixed**: `{ex['fixed'][:100]}...`\n\n")
        
        f.write("\n## Remaining Challenges\n\n")
        
        # Analyze persistent failures
        persistent_failures = {}
        
        for model_result in results['model_results']:
            if not model_result['available']:
                continue
                
            for improved in model_result['improved_results']:
                if not improved['execution_success']:
                    error = improved.get('execution_error', 'Unknown')
                    if error not in persistent_failures:
                        persistent_failures[error] = []
                    persistent_failures[error].append({
                        'model': model_result['model'],
                        'query': improved['query']
                    })
        
        f.write("### Common Failure Patterns\n\n")
        for error, examples in sorted(persistent_failures.items(), key=lambda x: len(x[1]), reverse=True)[:5]:
            f.write(f"**{error}** ({len(examples)} occurrences)\n")
            for ex in examples[:2]:
                f.write(f"- {ex['model']}: \"{ex['query'][:50]}...\"\n")
            f.write("\n")
        
        f.write("\n## Recommendations\n\n")
        
        if results['overall_improved_success_rate'] >= 85:
            f.write("1. [SUCCESS] **Success!** The improvements have achieved the target success rate.\n")
            f.write("2. Consider deploying these improvements to production.\n")
            f.write("3. Focus on the few remaining edge cases for even better performance.\n")
        else:
            f.write("1. [WARNING] **Additional improvements needed** to reach 85-90% target.\n")
            f.write("2. Focus on the most common failure patterns identified above.\n")
            f.write("3. Consider model-specific optimizations for poor performers.\n")
            f.write("4. May need to enhance prompt templates further.\n")
        
        f.write("\n## Next Steps\n\n")
        f.write("1. Review persistent failure patterns\n")
        f.write("2. Enhance query processor for specific error types\n")
        f.write("3. Consider fallback strategies for complex queries\n")
        f.write("4. Test with additional edge cases\n")
        
    print(f"\nMarkdown report generated: {filename}")

if __name__ == "__main__":
    asyncio.run(main())