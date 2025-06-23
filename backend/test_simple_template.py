#!/usr/bin/env python3
"""Test with simpler template"""

import json
import httpx
from jinja2 import Template
import os
import asyncio

async def test_simple_template(query: str):
    """Test query generation with simple template"""
    
    # Load the simple template
    template_path = "/app/prompts/generate_query_simple.txt"
    with open(template_path, 'r') as f:
        template_content = f.read()
    
    template = Template(template_content)
    prompt = template.render(user_message=query)
    
    # Call Ollama
    ollama_host = os.getenv("OLLAMA_HOST", "http://ollama:11434")
    ollama_model = os.getenv("OLLAMA_MODEL", "phi4:14b")
    
    payload = {
        "model": ollama_model,
        "prompt": prompt,
        "stream": False,
        "temperature": 0.1,
        "options": {"num_predict": 200}
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
    
    print("Testing with simplified template...")
    print("=" * 80)
    
    for query in test_queries:
        print(f"\nQuery: '{query}'")
        generated = await test_simple_template(query)
        print(f"Generated: {generated}")
        
        # Basic validation
        if "MATCH" in generated:
            # Check if it's querying the right things
            if "manages the data team" in query.lower() and ("Team" in generated or "MEMBER_OF" in generated):
                print("✅ Correctly queries teams/members")
            elif "gdpr" in query.lower() and "Policy" in generated:
                print("✅ Correctly queries policies")
            elif "engineering team leads" in query.lower() and ("Team" in generated or "MEMBER_OF" in generated):
                print("✅ Correctly queries teams/members")
            elif "security policies" in query.lower() and "Policy" in generated:
                print("✅ Correctly queries policies")
            else:
                print("⚠️  Query might not match intent")
        else:
            print("❌ Doesn't look like valid Cypher")
        
        print("-" * 40)

if __name__ == "__main__":
    asyncio.run(main())