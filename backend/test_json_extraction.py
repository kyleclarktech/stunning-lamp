#!/usr/bin/env python3
"""
Test the JSON extraction logic from main.py
"""

import json

# Test the actual response we got from Ollama
ai_response = '''```json
{
  "reasoning": "The user's query is a task-oriented request to identify who manages or leads the data team. This involves organizational structure and leadership, fitting into the 'Team Leadership' category under organizational analysis. The specific nature of this query requires accessing relational data between people and teams within the organization. Therefore, it necessitates using a custom Cypher query to accurately retrieve this information from the database.",
  "tools": ["custom_query", "store_message"],
  "response_type": "custom"
}
```'''

print("Original AI response:")
print(ai_response)
print("\n" + "="*80 + "\n")

# Apply the extraction logic from main.py
response_text = ai_response.strip()

# Look for JSON in markdown code blocks
if "```json" in response_text:
    start = response_text.find("```json") + 7
    end = response_text.find("```", start)
    if end > start:
        response_text = response_text[start:end].strip()
elif "```" in response_text:
    start = response_text.find("```") + 3
    end = response_text.find("```", start)
    if end > start:
        response_text = response_text[start:end].strip()

print("Extracted text:")
print(response_text)
print("\n" + "="*80 + "\n")

# Try to parse
try:
    analysis = json.loads(response_text)
    print("✅ Successfully parsed JSON!")
    print(json.dumps(analysis, indent=2))
    
    tools_to_execute = analysis.get("tools", [])
    response_type = analysis.get("response_type", "pig_latin")
    reasoning = analysis.get("reasoning", "No reasoning provided")
    
    print(f"\nExtracted values:")
    print(f"- Tools: {tools_to_execute}")
    print(f"- Response type: {response_type}")
    print(f"- Reasoning: {reasoning[:50]}...")
    
except json.JSONDecodeError as e:
    print(f"❌ Failed to parse JSON: {e}")