#!/usr/bin/env python3
"""Fix the generate_query.txt template by removing all PlatformComponent references"""

import re

# Read the file
with open("prompts/generate_query.txt", "r") as f:
    content = f.read()

# Count occurrences before
count_before = content.count("PlatformComponent") + content.count("CloudRegion")
print(f"Found {count_before} occurrences of PlatformComponent/CloudRegion")

# Replace wrong examples with correct ones
replacements = [
    # Replace PlatformComponent expertise queries with Skill-based queries
    (
        r"MATCH \(p:Person\)-\[e:EXPERT_IN\]->\(pc:PlatformComponent.*?\).*?labels\(p\) as labels.*?(?=\n|$)",
        "MATCH (p:Person)-[hs:HAS_SKILL]->(s:Skill) WHERE s.category = 'Data' AND hs.proficiency_level IN ['advanced', 'expert'] RETURN p.id, p.name, p.email, s.name as skill, hs.proficiency_level, labels(p) as labels"
    ),
    # Replace CloudRegion queries with Office-based queries
    (
        r"MATCH.*?CloudRegion.*?(?=\n|$)",
        "MATCH (o:Office) RETURN o.id, o.name, o.city, o.country, o.region, labels(o) as labels"
    ),
    # Replace USES_COMPONENT queries with project-based queries
    (
        r"MATCH \(c:Client\).*?USES_COMPONENT.*?PlatformComponent.*?(?=\n|$)",
        "MATCH (pr:Project)-[:FOR_CLIENT]->(c:Client) WITH c, count(pr) as project_count RETURN c.id, c.name, c.industry, project_count, labels(c) as labels"
    ),
    # Replace component ownership with policy ownership
    (
        r"MATCH \(pc:PlatformComponent.*?\)<-\[:DELIVERS\]-\(t:Team\).*?(?=\n|$)",
        "MATCH (t:Team)-[:RESPONSIBLE_FOR]->(p:Policy) RETURN t.name as team, collect(p.name) as policies, count(p) as policy_count ORDER BY count(p) DESC"
    ),
    # Remove DEPLOYED_IN relationships
    (
        r".*?DEPLOYED_IN.*?CloudRegion.*?\n",
        ""
    ),
    # Remove remaining PlatformComponent references
    (
        r".*?PlatformComponent.*?\n",
        ""
    )
]

# Apply replacements
for pattern, replacement in replacements:
    content = re.sub(pattern, replacement, content, flags=re.MULTILINE | re.DOTALL)

# Clean up extra blank lines
content = re.sub(r'\n\n\n+', '\n\n', content)

# Count occurrences after
count_after = content.count("PlatformComponent") + content.count("CloudRegion")
print(f"After cleanup: {count_after} occurrences remain")

# Write back
with open("prompts/generate_query.txt", "w") as f:
    f.write(content)

print("File has been cleaned!")

# Verify by checking specific sections
lines = content.split("\n")
for i, line in enumerate(lines):
    if "PlatformComponent" in line or "CloudRegion" in line:
        print(f"WARNING: Still found at line {i+1}: {line[:100]}...")