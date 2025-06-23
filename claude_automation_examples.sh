#!/bin/bash
# Claude Code Automation Examples
# Demonstrates various automation patterns and use cases

echo "Claude Code Automation Examples"
echo "==============================="

# 1. Simple query with text output
echo -e "\n1. Simple text query:"
claude --print "What is the capital of France?"

# 2. JSON output for parsing
echo -e "\n\n2. JSON output (parsed with jq):"
claude --print --output-format json "What is 10 * 20?" | jq -r '.result'

# 3. Code generation
echo -e "\n\n3. Code generation:"
claude --print --dangerously-skip-permissions "Write a Python function that calculates factorial"

# 4. File analysis with specific tool allowlist
echo -e "\n\n4. File analysis with restricted tools:"
claude --print --allowedTools "Read,Grep" "How many Python files are in the backend directory?"

# 5. Batch processing multiple queries
echo -e "\n\n5. Batch processing:"
queries=(
    "Count lines in backend/main.py"
    "Find all TODO comments in backend/"
    "List all Python files in backend/scripts/"
)

for query in "${queries[@]}"; do
    echo -e "\nQuery: $query"
    result=$(claude --print --output-format json --dangerously-skip-permissions "$query" | jq -r '.result' | head -3)
    echo "Result: $result"
done

# 6. Pipeline integration
echo -e "\n\n6. Pipeline integration:"
echo "def add(a, b): return a + b" | claude --print "Explain this Python code"

# 7. Error handling
echo -e "\n\n7. Error handling example:"
if claude --print --output-format json "Analyze nonexistent_file.py" 2>/dev/null | jq -e '.is_error' > /dev/null; then
    echo "Error detected and handled"
else
    echo "No error or query succeeded"
fi

# 8. Session management
echo -e "\n\n8. Session management:"
# Get session ID from first query
session_id=$(claude --print --output-format json "Remember the number 42" | jq -r '.session_id')
echo "Session ID: $session_id"

# Note: --resume flag can be used to continue a session
# claude --resume $session_id --print "What number did I ask you to remember?"

# 9. Cost tracking
echo -e "\n\n9. Cost tracking:"
total_cost=0
for i in {1..3}; do
    cost=$(claude --print --output-format json "What is $i + $i?" | jq -r '.total_cost_usd // 0')
    total_cost=$(echo "$total_cost + $cost" | bc -l)
done
echo "Total cost for 3 queries: \$$total_cost"

# 10. Model selection
echo -e "\n\n10. Model selection:"
claude --print --model sonnet "Briefly explain quantum computing in one sentence"

# 11. Fallback model handling
echo -e "\n\n11. Fallback model (for when primary is overloaded):"
claude --print --model opus --fallback-model sonnet "What is machine learning?"

echo -e "\n\nKey Automation Features:"
echo "- --print: Non-interactive mode"
echo "- --output-format json: Structured output"
echo "- --dangerously-skip-permissions: No permission prompts"
echo "- --allowedTools/--disallowedTools: Control tool access"
echo "- --model: Select specific models"
echo "- --fallback-model: Automatic fallback on overload"
echo "- Piping and streaming support"
echo "- Session persistence with --resume"