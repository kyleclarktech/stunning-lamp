#!/usr/bin/env python3
"""Phase 1: Test baseline performance of all LLM models."""

import asyncio
import json
import time
import os
import sys
import subprocess
import statistics
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import httpx
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import load_prompt, clean_ai_generated_query, get_falkor_client

# Core test queries (keep it focused)
BASELINE_QUERIES = [
    # Simple queries (3)
    "Who manages the data team?",
    "List all compliance policies",
    "Find people with Python skills",
    
    # Medium complexity (3)
    "What are the critical security policies and who's responsible?",
    "Find senior engineers in Europe with React skills",
    "Which teams are working on customer projects?",
    
    # Complex queries (2)
    "Show the complete org structure with reporting lines",
    "Find all paths between the CTO and data team members",
    
    # Edge cases (2)
    "xyz123 nonexistent query",
    "Find people in the quantum department"
]

# Model configurations
MODELS_TO_TEST = [
    # Priority 1
    {"name": "phi4:14b", "priority": 1, "type": "general"},
    {"name": "granite3.3:8b", "priority": 1, "type": "general"},
    {"name": "granite3.3:8b-largectx", "priority": 1, "type": "general"},
    
    # Priority 2
    {"name": "qwen2.5-coder:7b", "priority": 2, "type": "coding"},
    {"name": "granite-code:8b", "priority": 2, "type": "coding"},
    {"name": "deepseek-coder:1.3b", "priority": 2, "type": "coding"},
    {"name": "codeqwen:7b", "priority": 2, "type": "coding"},
    
    # Priority 3
    {"name": "mistral:7b", "priority": 3, "type": "general"},
    {"name": "llama3.2:3b", "priority": 3, "type": "general"},
    {"name": "phi3-mini:3.8b", "priority": 3, "type": "general"},
]

async def check_model_available(model_name: str) -> bool:
    """Check if a model is available in Ollama."""
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get("http://localhost:11434/api/tags")
            if response.status_code == 200:
                data = response.json()
                models = data.get('models', [])
                return any(m.get('name') == model_name for m in models)
    except Exception as e:
        print(f"Error checking model availability: {e}")
    return False

async def pull_model(model_name: str) -> bool:
    """Pull a model if not available."""
    print(f"Pulling model {model_name}...")
    try:
        async with httpx.AsyncClient(timeout=1800) as client:  # 30 min timeout for large models
            # Start the pull
            response = await client.post(
                "http://localhost:11434/api/pull",
                json={"name": model_name},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                # The response is a stream of JSON objects
                async for line in response.aiter_lines():
                    if line:
                        try:
                            data = json.loads(line)
                            status = data.get('status', '')
                            
                            if 'total' in data and 'completed' in data:
                                # Progress update
                                total = data['total']
                                completed = data['completed']
                                percent = (completed / total * 100) if total > 0 else 0
                                print(f"\rPulling {model_name}: {percent:.1f}%", end='', flush=True)
                            elif status:
                                print(f"\r{status}", end='', flush=True)
                                
                        except json.JSONDecodeError:
                            pass
                
                print(f"\nSuccessfully pulled {model_name}")
                return True
            else:
                print(f"Failed to pull {model_name}: {response.status_code}")
                return False
    except Exception as e:
        print(f"Error pulling {model_name}: {e}")
        return False

async def get_vram_usage() -> Dict[str, Any]:
    """Get current VRAM usage."""
    try:
        # Try to run nvidia-smi from the host
        proc = await asyncio.create_subprocess_exec(
            'nvidia-smi',
            '--query-gpu=memory.used,memory.total',
            '--format=csv,noheader,nounits',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        
        if proc.returncode == 0:
            output = stdout.decode().strip()
            lines = output.split('\n')
            if lines:
                # Use first GPU
                used, total = map(int, lines[0].split(', '))
                return {
                    'used_mb': used,
                    'total_mb': total,
                    'percentage': (used / total) * 100 if total > 0 else 0
                }
    except FileNotFoundError:
        # nvidia-smi not available, try from host via docker
        try:
            result = subprocess.run(
                ['docker', 'exec', 'stunning-lamp-api-1', 'nvidia-smi', 
                 '--query-gpu=memory.used,memory.total', '--format=csv,noheader,nounits'],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                output = result.stdout.strip()
                lines = output.split('\n')
                if lines:
                    used, total = map(int, lines[0].split(', '))
                    return {
                        'used_mb': used,
                        'total_mb': total,
                        'percentage': (used / total) * 100 if total > 0 else 0
                    }
        except:
            pass
    
    return {
        'used_mb': 0,
        'total_mb': 0,
        'percentage': 0,
        'note': 'nvidia-smi not available'
    }

async def execute_query(cypher_query: str) -> Tuple[bool, Optional[List], Optional[str]]:
    """Execute a Cypher query against FalkorDB and return success status, results, and error."""
    try:
        def run_query():
            falkor = get_falkor_client()
            db = falkor.select_graph("agent_poc")
            result = db.query(cypher_query)
            return result
        
        # Execute with timeout
        result = await asyncio.wait_for(
            asyncio.get_event_loop().run_in_executor(None, run_query),
            timeout=15
        )
        
        # Check if we got results
        has_results = result and result.result_set and len(result.result_set) > 0
        return True, result.result_set if has_results else [], None
        
    except asyncio.TimeoutError:
        return False, None, "Query timeout (15s)"
    except Exception as e:
        return False, None, str(e)

async def call_model(prompt_text: str, model_name: str, timeout: int = 60) -> str:
    """Call a specific model."""
    url = "http://localhost:11434/api/generate"
    
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

async def test_single_query(model_name: str, query: str, is_cold_start: bool = False) -> Dict[str, Any]:
    """Test a single query with a model."""
    start_time = time.time()
    
    try:
        # Generate prompt using simple template
        prompt = load_prompt("generate_query_simple", user_message=query)
        prompt += f"\n\nQuestion: \"{query}\"\nQuery:"
        
        # Call model
        raw_response = await call_model(prompt, model_name, timeout=30)
        
        # Clean up the query
        cypher_query = clean_ai_generated_query(raw_response)
        
        elapsed_time = time.time() - start_time
        
        # Check if query looks valid
        syntax_valid = (
            cypher_query and 
            'MATCH' in cypher_query and 
            len(cypher_query) > 10 and
            not cypher_query.startswith("I ") and
            not "I can" in cypher_query and
            not "To " in cypher_query
        )
        
        # Execute the query
        execution_success = False
        has_results = False
        execution_error = None
        
        if syntax_valid:
            execution_success, results, execution_error = await execute_query(cypher_query)
            has_results = results is not None and len(results) > 0
        
        return {
            'query': query,
            'cypher': cypher_query,
            'time': elapsed_time,
            'syntax_valid': syntax_valid,
            'execution_success': execution_success,
            'has_results': has_results,
            'is_cold_start': is_cold_start,
            'execution_error': execution_error
        }
        
    except Exception as e:
        return {
            'query': query,
            'cypher': None,
            'time': time.time() - start_time,
            'syntax_valid': False,
            'execution_success': False,
            'has_results': False,
            'is_cold_start': is_cold_start,
            'error': str(e)
        }

async def test_concurrent_queries(model_name: str, queries: List[str]) -> List[Dict[str, Any]]:
    """Test multiple queries concurrently."""
    tasks = [test_single_query(model_name, query) for query in queries]
    results = await asyncio.gather(*tasks)
    return results

async def get_model_info(model_name: str) -> Dict[str, Any]:
    """Get model information."""
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                "http://localhost:11434/api/show",
                json={"name": model_name}
            )
            if response.status_code == 200:
                data = response.json()
                details = data.get('details', {})
                return {
                    "parameter_size": details.get('parameter_size', 'unknown'),
                    "quantization": details.get('quantization_level', 'unknown'),
                    "family": details.get('family', 'unknown'),
                    "format": details.get('format', 'unknown')
                }
    except:
        pass
    return {}

async def test_model_baseline(model_config: Dict) -> Dict[str, Any]:
    """Test a single model with baseline queries."""
    model_name = model_config['name']
    print(f"\n{'='*60}")
    print(f"Testing model: {model_name}")
    print(f"Priority: {model_config['priority']}, Type: {model_config['type']}")
    print(f"{'='*60}")
    
    # Check if model is available
    available = await check_model_available(model_name)
    if not available:
        print(f"Model {model_name} not available. Attempting to pull...")
        success = await pull_model(model_name)
        if not success:
            print(f"Failed to pull {model_name}. Skipping...")
            return {
                'model': model_name,
                'config': model_config,
                'available': False,
                'skipped': True,
                'error': 'Failed to pull model'
            }
    
    # Get model info
    model_info = await get_model_info(model_name)
    print(f"Model info: {model_info}")
    
    # Record initial VRAM usage
    vram_before = await get_vram_usage()
    print(f"VRAM before: {vram_before['used_mb']}MB / {vram_before['total_mb']}MB ({vram_before['percentage']:.1f}%)")
    
    # Test cold start (first query after load)
    print("\nTesting cold start...")
    cold_start_result = await test_single_query(model_name, BASELINE_QUERIES[0], is_cold_start=True)
    print(f"Cold start time: {cold_start_result['time']:.2f}s")
    
    # Small delay to let model fully load
    await asyncio.sleep(2)
    
    # Test all baseline queries
    print("\nTesting baseline queries...")
    all_results = [cold_start_result]  # Include cold start in results
    
    for i, query in enumerate(BASELINE_QUERIES[1:], 1):  # Skip first query (already tested)
        print(f"\n[{i+1}/{len(BASELINE_QUERIES)}] {query}")
        result = await test_single_query(model_name, query)
        all_results.append(result)
        
        print(f"  Time: {result['time']:.2f}s")
        print(f"  Syntax Valid: {'✓' if result['syntax_valid'] else '✗'}")
        print(f"  Execution: {'✓' if result['execution_success'] else '✗'}")
        print(f"  Has Results: {'✓' if result['has_results'] else '✗'}")
        
        if result.get('execution_error'):
            print(f"  Error: {result['execution_error']}")
        
        # Small delay between queries
        await asyncio.sleep(0.5)
    
    # Record VRAM during operation
    vram_during = await get_vram_usage()
    
    # Test concurrent queries
    print("\nTesting concurrent queries (3 simultaneous)...")
    concurrent_queries = BASELINE_QUERIES[1:4]  # Use 3 simple/medium queries
    concurrent_start = time.time()
    concurrent_results = await test_concurrent_queries(model_name, concurrent_queries)
    concurrent_time = time.time() - concurrent_start
    
    print(f"Concurrent execution time: {concurrent_time:.2f}s")
    print(f"Throughput: {len(concurrent_queries) / concurrent_time:.2f} queries/second")
    
    # Record peak VRAM usage
    vram_peak = await get_vram_usage()
    
    # Calculate metrics
    response_times = [r['time'] for r in all_results]
    syntax_valid_count = sum(1 for r in all_results if r['syntax_valid'])
    execution_success_count = sum(1 for r in all_results if r['execution_success'])
    has_results_count = sum(1 for r in all_results if r['has_results'])
    
    # Calculate P95
    sorted_times = sorted(response_times)
    p95_index = int(len(sorted_times) * 0.95)
    p95_time = sorted_times[p95_index] if p95_index < len(sorted_times) else sorted_times[-1]
    
    return {
        'model': model_name,
        'config': model_config,
        'available': True,
        'model_info': model_info,
        'metrics': {
            'cold_start_time': cold_start_result['time'],
            'average_time': statistics.mean(response_times),
            'median_time': statistics.median(response_times),
            'p95_time': p95_time,
            'min_time': min(response_times),
            'max_time': max(response_times),
            'throughput_qps': len(concurrent_queries) / concurrent_time,
            'syntax_validity_rate': syntax_valid_count / len(all_results),
            'execution_success_rate': execution_success_count / len(all_results),
            'has_results_rate': has_results_count / len(all_results)
        },
        'resource_usage': {
            'vram_before_mb': vram_before['used_mb'],
            'vram_during_mb': vram_during['used_mb'],
            'vram_peak_mb': vram_peak['used_mb'],
            'vram_delta_mb': vram_peak['used_mb'] - vram_before['used_mb']
        },
        'detailed_results': all_results,
        'concurrent_results': concurrent_results,
        'timestamp': datetime.now().isoformat()
    }

def generate_summary_report(results: Dict[str, Any]) -> str:
    """Generate markdown summary report."""
    tested_models = [r for r in results['models_tested'] if not r.get('skipped', False)]
    
    report = f"""# Phase 1: LLM Model Baseline Performance Results

**Generated:** {results['timestamp']}

## Executive Summary

- **Models Tested:** {len(tested_models)} of {len(results['models_tested'])} attempted
- **Test Queries:** {len(BASELINE_QUERIES)} queries across simple, medium, complex, and edge cases
- **Test Duration:** {results.get('test_duration', 'N/A')}

## Model Performance Rankings

### By Speed (Average Response Time)
"""
    
    # Sort by average time
    tested_models.sort(key=lambda x: x['metrics']['average_time'])
    
    for i, model in enumerate(tested_models[:5], 1):  # Top 5
        metrics = model['metrics']
        report += f"\n{i}. **{model['model']}**"
        report += f"\n   - Average: {metrics['average_time']:.2f}s"
        report += f"\n   - P95: {metrics['p95_time']:.2f}s"
        report += f"\n   - Throughput: {metrics['throughput_qps']:.2f} queries/sec"
    
    report += "\n\n### By Accuracy (Execution Success Rate)\n"
    
    # Sort by execution success rate
    tested_models.sort(key=lambda x: x['metrics']['execution_success_rate'], reverse=True)
    
    for i, model in enumerate(tested_models[:5], 1):  # Top 5
        metrics = model['metrics']
        report += f"\n{i}. **{model['model']}**"
        report += f"\n   - Syntax Valid: {metrics['syntax_validity_rate']:.1%}"
        report += f"\n   - Execution Success: {metrics['execution_success_rate']:.1%}"
        report += f"\n   - Has Results: {metrics['has_results_rate']:.1%}"
    
    report += "\n\n### By Resource Efficiency (VRAM Usage)\n"
    
    # Sort by VRAM delta
    tested_models.sort(key=lambda x: x['resource_usage']['vram_delta_mb'])
    
    for i, model in enumerate(tested_models[:5], 1):  # Top 5
        resources = model['resource_usage']
        report += f"\n{i}. **{model['model']}**"
        report += f"\n   - VRAM Usage: +{resources['vram_delta_mb']}MB"
        report += f"\n   - Peak VRAM: {resources['vram_peak_mb']}MB"
        if model.get('model_info'):
            report += f"\n   - Parameters: {model['model_info'].get('parameter_size', 'unknown')}"
    
    # Overall recommendations
    report += "\n\n## Top 3 Recommended Models for Phase 2\n"
    
    # Score models based on balanced criteria
    for model in tested_models:
        metrics = model['metrics']
        # Normalize scores (lower is better for time, higher is better for accuracy)
        speed_score = 1 / (1 + metrics['average_time'])  # Inverse for speed
        accuracy_score = metrics['execution_success_rate']
        efficiency_score = 1 / (1 + model['resource_usage']['vram_delta_mb'] / 1000)  # Normalize MB to GB
        
        # Weighted score: 40% speed, 40% accuracy, 20% efficiency
        model['overall_score'] = (0.4 * speed_score + 0.4 * accuracy_score + 0.2 * efficiency_score) * 100
    
    tested_models.sort(key=lambda x: x['overall_score'], reverse=True)
    
    for i, model in enumerate(tested_models[:3], 1):
        report += f"\n### {i}. {model['model']} (Score: {model['overall_score']:.1f}/100)"
        report += f"\n- **Strengths:** "
        
        strengths = []
        if model['metrics']['average_time'] < 4:
            strengths.append("Fast response time")
        if model['metrics']['execution_success_rate'] > 0.8:
            strengths.append("High accuracy")
        if model['resource_usage']['vram_delta_mb'] < 10000:
            strengths.append("Efficient VRAM usage")
        
        report += ", ".join(strengths) if strengths else "Balanced performance"
        
        report += f"\n- **Performance:** {model['metrics']['average_time']:.2f}s avg, {model['metrics']['execution_success_rate']:.1%} success"
        report += f"\n- **Resources:** {model['resource_usage']['vram_delta_mb']}MB VRAM"
        report += f"\n- **Recommendation:** "
        
        if i == 1:
            report += "Primary model for Phase 2 testing"
        elif i == 2:
            report += "Strong alternative for comparison"
        else:
            report += "Good backup option"
    
    # Add detailed metrics table
    report += "\n\n## Detailed Metrics Comparison\n\n"
    report += "| Model | Avg Time | P95 Time | Success Rate | VRAM Delta | Overall Score |\n"
    report += "|-------|----------|----------|--------------|------------|---------------|\n"
    
    for model in tested_models[:10]:  # Top 10
        metrics = model['metrics']
        resources = model['resource_usage']
        report += f"| {model['model']} "
        report += f"| {metrics['average_time']:.2f}s "
        report += f"| {metrics['p95_time']:.2f}s "
        report += f"| {metrics['execution_success_rate']:.1%} "
        report += f"| {resources['vram_delta_mb']}MB "
        report += f"| {model['overall_score']:.1f} |\n"
    
    return report

def generate_csv_report(results: Dict[str, Any]) -> str:
    """Generate CSV quick reference."""
    tested_models = [r for r in results['models_tested'] if not r.get('skipped', False)]
    
    # Calculate overall scores if not already done
    for model in tested_models:
        if 'overall_score' not in model:
            metrics = model['metrics']
            speed_score = 1 / (1 + metrics['average_time'])
            accuracy_score = metrics['execution_success_rate']
            efficiency_score = 1 / (1 + model['resource_usage']['vram_delta_mb'] / 1000)
            model['overall_score'] = (0.4 * speed_score + 0.4 * accuracy_score + 0.2 * efficiency_score) * 100
    
    csv_content = "Model,Avg_Time,Success_Rate,VRAM_Usage,Overall_Score\n"
    
    for model in tested_models:
        metrics = model['metrics']
        resources = model['resource_usage']
        csv_content += f"{model['model']},"
        csv_content += f"{metrics['average_time']:.2f}s,"
        csv_content += f"{metrics['execution_success_rate']:.0%},"
        csv_content += f"{resources['vram_delta_mb']}MB,"
        csv_content += f"{model['overall_score']:.0f}\n"
    
    return csv_content

async def main():
    """Run Phase 1 baseline tests."""
    print("PHASE 1: LLM Model Baseline Performance Testing")
    print("=" * 60)
    
    start_time = time.time()
    
    results = {
        "phase": 1,
        "timestamp": datetime.now().isoformat(),
        "models_tested": [],
        "summary": {}
    }
    
    # Test each model
    for model in MODELS_TO_TEST:
        try:
            result = await test_model_baseline(model)
            results["models_tested"].append(result)
            
            # Save intermediate results
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            with open(f"phase1_baseline_{timestamp}.json", 'w') as f:
                json.dump(results, f, indent=2)
                
        except Exception as e:
            print(f"\nError testing {model['name']}: {e}")
            results["models_tested"].append({
                'model': model['name'],
                'config': model,
                'available': False,
                'skipped': True,
                'error': str(e)
            })
        
        # Small delay between models
        await asyncio.sleep(5)
    
    # Calculate test duration
    results['test_duration'] = f"{(time.time() - start_time) / 60:.1f} minutes"
    
    # Generate reports
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Save final JSON results
    with open(f"phase1_baseline_{timestamp}.json", 'w') as f:
        json.dump(results, f, indent=2)
    
    # Generate and save summary report
    summary_report = generate_summary_report(results)
    with open("phase1_summary.md", 'w') as f:
        f.write(summary_report)
    
    # Generate and save CSV quick reference
    csv_report = generate_csv_report(results)
    with open("phase1_quick_ref.csv", 'w') as f:
        f.write(csv_report)
    
    print("\n" + "=" * 60)
    print("PHASE 1 TESTING COMPLETE")
    print("=" * 60)
    print(f"\nTest Duration: {results['test_duration']}")
    print(f"\nReports generated:")
    print(f"  - JSON Results: phase1_baseline_{timestamp}.json")
    print(f"  - Summary Report: phase1_summary.md")
    print(f"  - Quick Reference: phase1_quick_ref.csv")
    print("\nReview phase1_summary.md for recommendations on models to use in Phase 2.")

if __name__ == "__main__":
    asyncio.run(main())