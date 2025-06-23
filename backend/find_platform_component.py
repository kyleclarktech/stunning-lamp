#!/usr/bin/env python3
"""Find all occurrences of PlatformComponent in the file"""

with open("prompts/generate_query.txt", "r") as f:
    content = f.read()

lines = content.split("\n")
for i, line in enumerate(lines):
    if "PlatformComponent" in line or "CloudRegion" in line:
        print(f"Line {i+1}: {line}")
        
# Also check if it's in the content at all
if "PlatformComponent" in content:
    print("\nFOUND PlatformComponent in file!")
    # Find first occurrence
    idx = content.find("PlatformComponent")
    print(f"First occurrence at character {idx}")
    print(f"Context: ...{content[max(0,idx-50):idx+50]}...")
else:
    print("\nNO PlatformComponent found in file")