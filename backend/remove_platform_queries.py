#!/usr/bin/env python3
"""Remove remaining PlatformComponent queries"""

with open("prompts/generate_query.txt", "r") as f:
    lines = f.readlines()

# Find lines with PlatformComponent or CloudRegion
new_lines = []
skip_next = False
i = 0

while i < len(lines):
    line = lines[i]
    
    # Check if this line contains problematic content
    if "PlatformComponent" in line or "CloudRegion" in line:
        # Skip this line and possibly the next if it's part of a query pattern
        if i > 0 and "Question:" in lines[i-1]:
            # Remove the previous line (question) too
            new_lines.pop()
        i += 1
        continue
    
    new_lines.append(line)
    i += 1

# Write back
with open("prompts/generate_query.txt", "w") as f:
    f.writelines(new_lines)

print(f"Removed {len(lines) - len(new_lines)} lines containing PlatformComponent/CloudRegion")