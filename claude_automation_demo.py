#!/usr/bin/env python3
"""
Claude Code Automation Demo
This script demonstrates how to use Claude Code in automation workflows
"""

import subprocess
import json
import sys

def claude_query(prompt, output_format="json", skip_permissions=True):
    """Execute a Claude Code query and return the result"""
    cmd = ["claude", "--print", f"--output-format={output_format}"]
    
    if skip_permissions:
        cmd.append("--dangerously-skip-permissions")
    
    cmd.append(prompt)
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        if output_format == "json":
            return json.loads(result.stdout)
        else:
            return result.stdout
            
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}", file=sys.stderr)
        return None

def batch_code_analysis(files):
    """Analyze multiple files using Claude Code"""
    results = {}
    
    for file in files:
        print(f"Analyzing {file}...")
        prompt = f"Count the number of functions in the file {file} and list their names"
        response = claude_query(prompt)
        
        if response:
            results[file] = {
                "success": True,
                "result": response.get("result", ""),
                "cost": response.get("total_cost_usd", 0),
                "duration_ms": response.get("duration_ms", 0)
            }
        else:
            results[file] = {"success": False, "error": "Query failed"}
    
    return results

def generate_documentation(file_path):
    """Use Claude to generate documentation for a file"""
    prompt = f"Generate a brief documentation summary for {file_path} including its main purpose and key functions"
    response = claude_query(prompt)
    
    if response:
        return response.get("result", "")
    return None

def find_patterns(pattern, directory="."):
    """Use Claude to find code patterns"""
    prompt = f"Find all occurrences of the pattern '{pattern}' in Python files in {directory}"
    response = claude_query(prompt)
    
    if response:
        return response.get("result", "")
    return None

# Example usage
if __name__ == "__main__":
    print("Claude Code Automation Demo")
    print("=" * 50)
    
    # Example 1: Analyze multiple files
    print("\n1. Batch File Analysis:")
    files_to_analyze = [
        "backend/main.py",
        "backend/query_processor.py"
    ]
    
    analysis_results = batch_code_analysis(files_to_analyze)
    for file, result in analysis_results.items():
        print(f"\n{file}:")
        if result["success"]:
            print(f"  Result: {result['result'][:200]}...")
            print(f"  Duration: {result['duration_ms']}ms")
            print(f"  Cost: ${result['cost']:.6f}")
        else:
            print(f"  Error: {result['error']}")
    
    # Example 2: Generate documentation
    print("\n\n2. Documentation Generation:")
    doc = generate_documentation("backend/api/dashboard.py")
    if doc:
        print(f"Documentation:\n{doc[:300]}...")
    
    # Example 3: Find patterns
    print("\n\n3. Pattern Search:")
    patterns = find_patterns("WebSocket", "backend")
    if patterns:
        print(f"Pattern occurrences:\n{patterns[:300]}...")
    
    # Summary
    print("\n\nSummary of Claude Code Automation Capabilities:")
    print("- Non-interactive mode with --print flag")
    print("- JSON output for structured data parsing")
    print("- Stream JSON for real-time processing")
    print("- Permission bypass for fully automated workflows")
    print("- Can be integrated into CI/CD pipelines")
    print("- Supports complex tasks like code analysis, documentation, and refactoring")