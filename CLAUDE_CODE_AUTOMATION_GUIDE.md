# Claude Code Automation & API Capabilities Guide

## Overview

Claude Code provides powerful automation capabilities through its command-line interface, enabling programmatic control, batch processing, and integration into various workflows. While it doesn't have a traditional REST API, its CLI features enable API-like functionality.

## Key Automation Features

### 1. Non-Interactive Mode (`--print`)

The `--print` flag enables non-interactive execution, making Claude Code scriptable:

```bash
claude --print "Your prompt here"
```

This returns the result and exits immediately, perfect for automation scripts.

### 2. Structured Output Formats

Claude Code supports multiple output formats for easy parsing:

- **Text** (default): Plain text response
- **JSON**: Structured data with metadata
- **Stream-JSON**: Real-time streaming with detailed events

```bash
# JSON output with metadata
claude --print --output-format json "Count files in current directory"

# Returns:
{
  "type": "result",
  "subtype": "success",
  "is_error": false,
  "duration_ms": 3029,
  "result": "42 files found",
  "session_id": "uuid-here",
  "total_cost_usd": 0.0265,
  "usage": { ... }
}
```

### 3. Permission Management

For fully automated workflows:

```bash
# Skip all permission prompts (use with caution)
claude --print --dangerously-skip-permissions "Create a file"

# Or restrict/allow specific tools
claude --print --allowedTools "Read,Grep" "Analyze code"
claude --print --disallowedTools "Bash,Write" "Review this file"
```

### 4. Session Management

Maintain context across multiple queries:

```bash
# First query
SESSION_ID=$(claude --print --output-format json "Remember X=42" | jq -r '.session_id')

# Continue session
claude --resume $SESSION_ID --print "What is X?"
```

## Practical Automation Patterns

### Sub-Agent Pattern

Use multiple Claude instances as specialized agents:

```python
class ClaudeAgent:
    def __init__(self, agent_id, allowed_tools=None):
        self.agent_id = agent_id
        self.allowed_tools = allowed_tools
    
    def query(self, prompt):
        cmd = ["claude", "--print", "--output-format=json"]
        if self.allowed_tools:
            cmd.extend(["--allowedTools", ",".join(self.allowed_tools)])
        cmd.append(prompt)
        # Execute and return parsed JSON
```

### Pipeline Processing

Chain Claude Code operations:

```bash
# Extract -> Analyze -> Generate
claude --print "Extract functions from main.py" | \
claude --print "Analyze these functions: $(cat -)" | \
claude --print "Generate tests for: $(cat -)"
```

### Batch Processing

Process multiple items efficiently:

```bash
for file in *.py; do
    claude --print --output-format json \
      "Review $file for code quality" \
      > "reviews/${file%.py}_review.json"
done
```

### CI/CD Integration

Example GitHub Actions workflow:

```yaml
- name: Code Review
  run: |
    claude --print --output-format json \
      --dangerously-skip-permissions \
      "Review changed files for issues" \
      > code_review.json
```

## Advanced Use Cases

### 1. Automated Code Review

```bash
# Pre-commit hook
claude --print --allowedTools "Read,Grep" \
  "Check for code smells and security issues in staged files"
```

### 2. Documentation Generation

```bash
# Generate docs for all Python files
find . -name "*.py" -exec claude --print \
  --dangerously-skip-permissions \
  "Generate docstring for {}" \; > documentation.md
```

### 3. Test Generation

```bash
claude --print --allowedTools "Read,Write" \
  "Generate pytest tests for functions without test coverage"
```

### 4. Performance Analysis

```bash
claude --print --output-format json \
  "Analyze backend/ for performance bottlenecks" | \
  jq -r '.result' > performance_report.md
```

### 5. Multi-Model Consensus

```bash
# Get opinions from different models
for model in opus sonnet; do
    claude --print --model $model "$QUESTION" > "${model}_response.txt"
done
```

## Integration Examples

### Python Integration

```python
import subprocess
import json

def claude_query(prompt, output_format="json"):
    result = subprocess.run(
        ["claude", "--print", f"--output-format={output_format}", prompt],
        capture_output=True,
        text=True
    )
    return json.loads(result.stdout) if output_format == "json" else result.stdout
```

### Shell Script Integration

```bash
#!/bin/bash
claude_analyze() {
    local file=$1
    claude --print --output-format json \
      --dangerously-skip-permissions \
      "Analyze $file" | jq -r '.result'
}
```

### Node.js Integration

```javascript
const { execSync } = require('child_process');

function claudeQuery(prompt) {
    const result = execSync(
        `claude --print --output-format json "${prompt}"`,
        { encoding: 'utf8' }
    );
    return JSON.parse(result);
}
```

## Best Practices

1. **Use JSON output** for structured data parsing
2. **Handle errors** by checking the `is_error` field
3. **Track costs** using the `total_cost_usd` field
4. **Implement timeouts** for long-running operations
5. **Use `--allowedTools`** to restrict capabilities for safety
6. **Cache responses** when appropriate to reduce costs
7. **Log session IDs** for debugging and continuity

## Limitations & Considerations

- No traditional REST API (CLI-based only)
- Requires local Claude Code installation
- Permission prompts unless using `--dangerously-skip-permissions`
- Rate limits may apply to the underlying API
- Cost accumulates with each query

## Example Applications

1. **Code Quality Bot**: Automated PR reviews
2. **Documentation Generator**: Auto-generate missing docs
3. **Test Suite Builder**: Create tests for untested code
4. **Security Scanner**: Check for vulnerabilities
5. **Performance Analyzer**: Identify bottlenecks
6. **Refactoring Assistant**: Suggest code improvements
7. **Learning Tool**: Generate examples and explanations
8. **Migration Helper**: Convert code between frameworks

## Conclusion

While Claude Code doesn't offer a traditional API, its CLI provides powerful automation capabilities that can be integrated into virtually any workflow. The combination of non-interactive mode, structured output, and flexible tool permissions makes it suitable for everything from simple scripts to complex CI/CD pipelines.