#!/usr/bin/env python3
"""Test if the query generation is now fixed"""

import json
import httpx
from jinja2 import Template
import os
import asyncio

async def test_query_generation(query: str):
    """Test query generation for a specific query"""
    
    # Load the template
    template_path = "/app/prompts/generate_query.txt"
    with open(template_path, 'r') as f:
        template_content = f.read()
    
    template = Template(template_content)
    
    # Mock context
    db_context = {
        "people_count": 100,
        "sample_departments": ["Engineering", "Sales", "Data"],
        "teams_count": 20,
        "sample_teams": [
            {"name": "Data Analytics", "department": "Data"},
            {"name": "Backend", "department": "Engineering"}
        ],
        "groups_count": 10,
        "sample_groups": [{"name": "Tech Council", "type": "technical"}],
        "policies_count": 50
    }
    
    intent_context = {
        "primary_intent": "information_gathering",
        "actual_goal": f"answer the question: {query}",
        "information_depth": "specific",
        "urgency": "normal",
        "complexity": "simple",
        "domain": "organizational",
        "confidence": 0.9,
        "suggested_approach": "Use appropriate Cypher query"
    }
    
    # Render prompt
    prompt = template.render(
        user_message=query,
        database_context=db_context,
        intent_context=intent_context
    )
    
    # Call Ollama
    ollama_host = os.getenv("OLLAMA_HOST", "http://ollama:11434")
    ollama_model = os.getenv("OLLAMA_MODEL", "phi4:14b")
    
    payload = {
        "model": ollama_model,
        "prompt": prompt,
        "stream": False,
        "temperature": 0.1,
        "options": {"num_predict": 300}
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(f"{ollama_host}/api/generate", json=payload)
        response.raise_for_status()
        result = response.json()
        
        generated_query = result.get("response", "").strip()
        return generated_query

async def main():
    test_queries = [
        "Who manages the data team?",
        "Find all GDPR compliance policies",
        "Show me the engineering team leads",
        "What are the security policies?"
    ]
    
    print("Testing query generation after fix...")
    print("=" * 80)
    
    for query in test_queries:
        print(f"\nQuery: '{query}'")
        generated = await test_query_generation(query)
        print(f"Generated Cypher: {generated}")
        
        # Check if it contains problematic nodes
        if "PlatformComponent" in generated or "CloudRegion" in generated:
            print("❌ STILL GENERATING WRONG SCHEMA!")
        elif "MATCH" in generated:
            print("✅ Generated valid Cypher query")
        else:
            print("⚠️  Response doesn't look like Cypher")
        
        print("-" * 40)

if __name__ == "__main__":
    asyncio.run(main())