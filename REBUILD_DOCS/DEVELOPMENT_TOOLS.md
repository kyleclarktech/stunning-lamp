# Development Tools and Practices

## Overview

This document describes the tools and practices used during the development of the Enterprise Knowledge Graph & PM Assistant System. These are NOT features of the system itself, but rather tools that help manage the complexity of building it.

## Sub-Agent Orchestration for Development

### Purpose

When developing a complex system with Claude Code, context window limitations can become a bottleneck. The Sub-Agent Orchestration system allows developers to:

- Delegate well-defined tasks to headless Claude Code instances
- Run multiple development tasks in parallel
- Maintain strict quality control through validation
- Preserve the main conversation's context for architectural decisions

### How It Works

1. **Task Identification**: During development, identify tasks that are:
   - Well-bounded (clear inputs/outputs)
   - Testable (success can be verified programmatically)
   - Independent (don't require back-and-forth discussion)

2. **Delegation**: Use the orchestrator to spawn sub-agents:
   ```bash
   # Generate tests for a module
   python claude_orchestrator.py --task tests --module src/query_engine.py --coverage 95
   
   # Update documentation after changes
   python claude_orchestrator.py --task documentation --files src/api.py,src/models.py
   ```

3. **Validation**: Each task has strict success criteria that must be met

### Common Development Tasks for Delegation

1. **Test Generation**
   - Generate comprehensive test suites
   - Achieve specific coverage targets
   - Follow existing test patterns

2. **Documentation Updates**
   - Update README and API docs after code changes
   - Ensure examples match current implementation
   - Add "Last updated" timestamps

3. **Code Refactoring**
   - Rename variables/functions consistently
   - Apply formatting standards
   - Update import statements

4. **Analysis Tasks**
   - Security audits of specific modules
   - Performance profiling
   - Dependency analysis

### Files in development_tools/

- `SUB_AGENT_ORCHESTRATION_SPEC.md` - Detailed specification
- `CLAUDE_ORCHESTRATOR.md` - Architecture and usage guide
- `SUBAGENT_PROMPT_TEMPLATES.md` - Strict prompt templates
- `SUBAGENT_SUCCESS_CRITERIA.py` - Validation framework
- `claude_orchestrator.py` - Implementation

## Development Workflow with Claude Code

### 1. Planning Phase

When starting a new feature:
1. Create a high-level plan in the main Claude session
2. Identify components that can be developed in parallel
3. Define clear interfaces between components
4. Use the orchestrator for implementation tasks

### 2. Implementation Phase

```bash
# Main Claude session handles architecture
# Sub-agents handle specific implementations

# Example workflow:
# 1. Main session designs the Query Engine interface
# 2. Delegate implementation tasks:
python claude_orchestrator.py --task implement --module query_parser --spec specs/parser.md
python claude_orchestrator.py --task implement --module cypher_generator --spec specs/generator.md
python claude_orchestrator.py --task tests --module query_engine --coverage 90
```

### 3. Integration Phase

After sub-agents complete tasks:
1. Review results in main session
2. Integrate components
3. Run system-level tests
4. Update documentation

## Best Practices

### 1. Task Granularity

**Good Tasks for Sub-Agents:**
- "Generate tests for the user authentication module"
- "Update API documentation to reflect new endpoints"
- "Refactor all print statements to use logger"

**Keep in Main Session:**
- Architectural decisions
- API design discussions
- Complex problem solving
- User requirement clarification

### 2. Context Management

- Monitor context usage with Claude Code's built-in tools
- Offload when approaching 70% of context limit
- Keep architectural context in main session
- Use summaries instead of full sub-agent outputs

### 3. Quality Control

- Define explicit success criteria for every task
- Use the validation framework to ensure quality
- Review sub-agent outputs before integration
- Maintain a consistent code style across agents

## Other Development Tools

### 1. Auto-Maintained Touchpoints

The system uses Claude Code to maintain touchpoints automatically:

```typescript
// @touchpoint query-parser
// @concepts [parsing, natural-language]
export class QueryParser {
  // Claude Code updates these when files change
}
```

### 2. Event-Driven Updates

File changes trigger automatic updates:
- Touchpoint extraction
- Documentation synchronization
- Schema updates

### 3. Git Integration

Pre-commit hooks ensure:
- Touchpoint references are valid
- Documentation is updated
- Tests pass

## Environment Setup

### Prerequisites

1. Claude Code CLI installed
2. Python 3.8+ for orchestrator
3. Node.js for the main project
4. Neo4j database for development

### Configuration

```bash
# .env file for development
CLAUDE_API_KEY=your_key_here
MAX_PARALLEL_AGENTS=3
DEFAULT_TIMEOUT=300
VALIDATION_STRICT=true
```

## Troubleshooting

### Common Issues

1. **Context Overflow**
   - Symptom: Claude Code becomes slow or unresponsive
   - Solution: Use orchestrator to offload tasks

2. **Sub-Agent Failures**
   - Symptom: Tasks fail validation
   - Solution: Check prompt templates, make requirements more explicit

3. **Integration Conflicts**
   - Symptom: Sub-agent code doesn't integrate cleanly
   - Solution: Define clearer interfaces, use stricter templates

## Summary

The development tools, especially the Sub-Agent Orchestration system, are designed to make building complex systems with Claude Code more efficient. They are development-time tools only and are not part of the deployed system. By delegating well-defined tasks to sub-agents, developers can maintain focus on architecture and design while still achieving comprehensive implementation coverage.