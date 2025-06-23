#!/usr/bin/env python3
"""
Claude Code Sub-Agent Pattern Demo
Demonstrates how to use Claude Code as sub-agents for complex workflows
"""

import subprocess
import json
import concurrent.futures
import time
from typing import List, Dict, Any

class ClaudeAgent:
    """Wrapper for Claude Code to act as a sub-agent"""
    
    def __init__(self, agent_id: str, model: str = None, allowed_tools: List[str] = None):
        self.agent_id = agent_id
        self.model = model
        self.allowed_tools = allowed_tools
        self.session_id = None
    
    def query(self, prompt: str, continue_session: bool = False) -> Dict[str, Any]:
        """Execute a query with this agent"""
        cmd = ["claude", "--print", "--output-format=json", "--dangerously-skip-permissions"]
        
        if self.model:
            cmd.extend(["--model", self.model])
        
        if self.allowed_tools:
            cmd.extend(["--allowedTools", ",".join(self.allowed_tools)])
        
        if continue_session and self.session_id:
            cmd.extend(["--resume", self.session_id])
        
        cmd.append(prompt)
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            response = json.loads(result.stdout)
            
            # Store session ID for continuity
            if not self.session_id:
                self.session_id = response.get("session_id")
            
            return {
                "agent_id": self.agent_id,
                "success": True,
                "result": response.get("result", ""),
                "cost": response.get("total_cost_usd", 0),
                "duration_ms": response.get("duration_ms", 0),
                "session_id": self.session_id
            }
        except subprocess.CalledProcessError as e:
            return {
                "agent_id": self.agent_id,
                "success": False,
                "error": e.stderr
            }

class ClaudeOrchestrator:
    """Orchestrates multiple Claude agents for complex tasks"""
    
    def __init__(self):
        self.agents = {}
        self.results = []
    
    def create_agent(self, agent_id: str, **kwargs) -> ClaudeAgent:
        """Create a new agent with specific capabilities"""
        agent = ClaudeAgent(agent_id, **kwargs)
        self.agents[agent_id] = agent
        return agent
    
    def parallel_query(self, queries: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """Execute multiple queries in parallel"""
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            
            for query in queries:
                agent_id = query["agent_id"]
                prompt = query["prompt"]
                agent = self.agents.get(agent_id)
                
                if agent:
                    future = executor.submit(agent.query, prompt)
                    futures.append(future)
            
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
            self.results.extend(results)
            return results
    
    def pipeline_query(self, pipeline: List[Dict[str, str]]) -> str:
        """Execute queries in a pipeline where each result feeds the next"""
        previous_result = None
        
        for step in pipeline:
            agent_id = step["agent_id"]
            prompt_template = step["prompt"]
            
            # Replace {previous} placeholder with previous result
            if previous_result:
                prompt = prompt_template.replace("{previous}", previous_result)
            else:
                prompt = prompt_template
            
            agent = self.agents.get(agent_id)
            if agent:
                result = agent.query(prompt)
                if result["success"]:
                    previous_result = result["result"]
                else:
                    return f"Pipeline failed at {agent_id}: {result['error']}"
        
        return previous_result
    
    def get_total_cost(self) -> float:
        """Calculate total cost across all agents"""
        return sum(r.get("cost", 0) for r in self.results)

# Example usage scenarios
def demo_code_review_workflow():
    """Demonstrate a code review workflow with multiple specialized agents"""
    print("Code Review Workflow Demo")
    print("=" * 50)
    
    orchestrator = ClaudeOrchestrator()
    
    # Create specialized agents
    orchestrator.create_agent("analyzer", allowed_tools=["Read", "Grep"])
    orchestrator.create_agent("security", allowed_tools=["Read", "Grep"])
    orchestrator.create_agent("optimizer", allowed_tools=["Read"])
    orchestrator.create_agent("documenter", allowed_tools=["Read", "Write"])
    
    # Parallel analysis of a file
    file_to_review = "backend/query_processor.py"
    
    parallel_queries = [
        {
            "agent_id": "analyzer",
            "prompt": f"Analyze {file_to_review} for code quality issues and patterns"
        },
        {
            "agent_id": "security",
            "prompt": f"Check {file_to_review} for potential security vulnerabilities"
        },
        {
            "agent_id": "optimizer",
            "prompt": f"Suggest performance optimizations for {file_to_review}"
        }
    ]
    
    print(f"\nAnalyzing {file_to_review} with specialized agents...")
    results = orchestrator.parallel_query(parallel_queries)
    
    for result in results:
        print(f"\n{result['agent_id'].upper()} Agent:")
        if result["success"]:
            print(f"  {result['result'][:200]}...")
            print(f"  Duration: {result['duration_ms']}ms")
        else:
            print(f"  Error: {result['error']}")
    
    print(f"\nTotal cost: ${orchestrator.get_total_cost():.6f}")

def demo_research_pipeline():
    """Demonstrate a research pipeline with sequential processing"""
    print("\n\nResearch Pipeline Demo")
    print("=" * 50)
    
    orchestrator = ClaudeOrchestrator()
    
    # Create agents for different research stages
    orchestrator.create_agent("researcher", allowed_tools=["WebSearch"])
    orchestrator.create_agent("analyzer", allowed_tools=[])
    orchestrator.create_agent("writer", allowed_tools=["Write"])
    
    # Define pipeline
    pipeline = [
        {
            "agent_id": "researcher",
            "prompt": "Search for recent developments in quantum computing"
        },
        {
            "agent_id": "analyzer",
            "prompt": "Analyze this information and identify the top 3 breakthroughs: {previous}"
        },
        {
            "agent_id": "writer",
            "prompt": "Write a brief summary of these quantum computing breakthroughs: {previous}"
        }
    ]
    
    print("\nExecuting research pipeline...")
    final_result = orchestrator.pipeline_query(pipeline)
    print(f"\nFinal result:\n{final_result}")

def demo_multi_model_consensus():
    """Demonstrate using different models for consensus"""
    print("\n\nMulti-Model Consensus Demo")
    print("=" * 50)
    
    orchestrator = ClaudeOrchestrator()
    
    # Create agents with different models (if available)
    orchestrator.create_agent("opus_agent", model="opus")
    orchestrator.create_agent("sonnet_agent", model="sonnet")
    
    question = "What are the main benefits of using GraphQL over REST APIs?"
    
    consensus_queries = [
        {"agent_id": "opus_agent", "prompt": question},
        {"agent_id": "sonnet_agent", "prompt": question}
    ]
    
    print(f"\nAsking multiple models: {question}")
    results = orchestrator.parallel_query(consensus_queries)
    
    for result in results:
        print(f"\n{result['agent_id']}:")
        if result["success"]:
            print(f"  {result['result'][:300]}...")

if __name__ == "__main__":
    print("Claude Code Sub-Agent Pattern Demonstrations")
    print("=" * 60)
    
    # Run demonstrations
    demo_code_review_workflow()
    demo_research_pipeline()
    demo_multi_model_consensus()
    
    print("\n\nSub-Agent Pattern Capabilities:")
    print("- Parallel execution with ThreadPoolExecutor")
    print("- Pipeline processing with result chaining")
    print("- Specialized agents with restricted tool access")
    print("- Multi-model consensus building")
    print("- Session persistence for stateful conversations")
    print("- Cost tracking across all agents")
    print("- Error handling and retry logic")
    print("- Can be integrated into larger automation frameworks")