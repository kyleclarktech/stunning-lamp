# Claude Code Orchestrator - Sub-Agent Task Management

## Overview

This system enables Claude Code to programmatically offload tasks to headless sub-agents, managing context window bloat while maintaining strict quality control through explicit prompting and testable success criteria.

## Core Architecture

### 1. Orchestrator Pattern

The main Claude Code session acts as an orchestrator that:
- Identifies tasks suitable for delegation
- Creates explicit task specifications
- Spawns sub-agents with focused contexts
- Validates results against success criteria
- Integrates results back into main context

### 2. Task Types Suitable for Offloading

1. **Documentation Updates**
   - Update README files to reflect code changes
   - Generate API documentation
   - Create migration guides

2. **Code Generation**
   - Generate test suites for specific modules
   - Create boilerplate code from templates
   - Implement well-defined interfaces

3. **Analysis Tasks**
   - Security audits of specific files
   - Performance analysis of algorithms
   - Dependency analysis

4. **Refactoring**
   - Apply consistent code style
   - Update imports across files
   - Rename variables/functions

## Implementation

### Task Specification Format

```python
@dataclass
class SubAgentTask:
    """Specification for a delegated task"""
    task_id: str
    task_type: str  # 'documentation', 'code_gen', 'analysis', 'refactor'
    description: str
    context_files: List[str]  # Minimal context needed
    constraints: List[str]  # Explicit requirements
    success_criteria: List[SuccessCriterion]
    max_attempts: int = 3
    timeout_seconds: int = 300
    
@dataclass
class SuccessCriterion:
    """Testable success criterion"""
    name: str
    test_type: str  # 'file_exists', 'test_passes', 'pattern_match', 'validator'
    test_spec: Dict[str, Any]
    required: bool = True
```

### Explicit Prompt Templates

```python
TASK_PROMPT_TEMPLATE = """
You are a specialized sub-agent with ONE specific task. You MUST complete this task
exactly as specified with NO deviations or compromises.

TASK: {task_description}

CONTEXT FILES:
{context_files}

STRICT CONSTRAINTS:
{constraints}

SUCCESS CRITERIA (ALL must be met):
{success_criteria}

FAILURE CONDITIONS:
- Any deviation from the specified task
- Any changes outside the allowed scope
- Any compromise on quality or completeness
- Failure to meet ANY success criterion

You have {max_attempts} attempts to complete this task successfully.
If you cannot meet ALL criteria, you MUST report failure rather than
delivering a partial solution.

BEGIN TASK EXECUTION NOW.
"""
```

### Orchestrator Script

```python
#!/usr/bin/env python3
"""
Claude Code Orchestrator - Manages sub-agent task delegation
"""

import json
import subprocess
import tempfile
import time
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ClaudeOrchestrator:
    """Orchestrates sub-agent tasks to manage context bloat"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.active_tasks: Dict[str, SubAgentTask] = {}
        self.task_results: Dict[str, TaskResult] = {}
        
    def delegate_task(self, task: SubAgentTask) -> TaskResult:
        """Delegate a task to a headless sub-agent"""
        logger.info(f"Delegating task {task.task_id}: {task.description}")
        
        # Prepare minimal context
        context = self._prepare_context(task)
        
        # Generate explicit prompt
        prompt = self._generate_prompt(task, context)
        
        # Save prompt to temporary file (for complex prompts)
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(prompt)
            prompt_file = f.name
        
        try:
            # Execute sub-agent
            result = self._execute_subagent(task, prompt_file)
            
            # Validate results
            validation = self._validate_results(task, result)
            
            if validation.success:
                logger.info(f"Task {task.task_id} completed successfully")
                return TaskResult(
                    task_id=task.task_id,
                    success=True,
                    output=result,
                    validation=validation
                )
            else:
                logger.warning(f"Task {task.task_id} failed validation")
                return self._handle_failure(task, validation)
                
        finally:
            # Clean up
            Path(prompt_file).unlink(missing_ok=True)
    
    def _execute_subagent(self, task: SubAgentTask, prompt_file: str) -> Dict[str, Any]:
        """Execute Claude Code in headless mode"""
        cmd = [
            'claude',
            '--print',  # Non-interactive mode
            '--output-format', 'json',  # Structured output
            '--dangerously-skip-permissions',  # Fully automated
            '--max-turns', str(task.max_attempts),
            '--file', prompt_file  # Read prompt from file
        ]
        
        # Add tool restrictions if needed
        if task.task_type == 'documentation':
            cmd.extend(['--allowedTools', 'Read,Write,Edit,MultiEdit'])
        elif task.task_type == 'analysis':
            cmd.extend(['--allowedTools', 'Read,Grep,Glob'])
        
        # Execute with timeout
        try:
            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=task.timeout_seconds,
                check=True
            )
            
            return json.loads(result.stdout)
            
        except subprocess.TimeoutExpired:
            raise TaskTimeoutError(f"Task {task.task_id} timed out")
        except subprocess.CalledProcessError as e:
            raise SubAgentError(f"Sub-agent failed: {e.stderr}")
    
    def _validate_results(self, task: SubAgentTask, result: Dict[str, Any]) -> ValidationResult:
        """Validate task results against success criteria"""
        validations = []
        
        for criterion in task.success_criteria:
            passed = self._check_criterion(criterion, result)
            validations.append({
                'criterion': criterion.name,
                'passed': passed,
                'required': criterion.required
            })
            
            if criterion.required and not passed:
                return ValidationResult(
                    success=False,
                    validations=validations,
                    reason=f"Failed required criterion: {criterion.name}"
                )
        
        return ValidationResult(success=True, validations=validations)
    
    def _check_criterion(self, criterion: SuccessCriterion, result: Dict[str, Any]) -> bool:
        """Check a single success criterion"""
        if criterion.test_type == 'file_exists':
            path = self.project_root / criterion.test_spec['path']
            return path.exists()
            
        elif criterion.test_type == 'test_passes':
            # Run specified test
            test_cmd = criterion.test_spec['command']
            try:
                subprocess.run(test_cmd, shell=True, check=True, cwd=self.project_root)
                return True
            except subprocess.CalledProcessError:
                return False
                
        elif criterion.test_type == 'pattern_match':
            # Check if output contains pattern
            pattern = criterion.test_spec['pattern']
            text = result.get('result', '')
            return pattern in text
            
        elif criterion.test_type == 'validator':
            # Run custom validator
            validator_func = criterion.test_spec['function']
            return validator_func(result)
            
        return False

# Example task definitions
def create_documentation_task(files_changed: List[str]) -> SubAgentTask:
    """Create a documentation update task"""
    return SubAgentTask(
        task_id=f"doc_update_{int(time.time())}",
        task_type="documentation",
        description="Update documentation to reflect recent code changes",
        context_files=files_changed + ['README.md', 'docs/API.md'],
        constraints=[
            "Only modify documentation files (*.md)",
            "Preserve existing documentation structure",
            "Include code examples for new features",
            "Update table of contents if needed"
        ],
        success_criteria=[
            SuccessCriterion(
                name="readme_updated",
                test_type="pattern_match",
                test_spec={"pattern": "Last updated:"},
                required=True
            ),
            SuccessCriterion(
                name="no_code_changes",
                test_type="validator",
                test_spec={"function": lambda r: not any('.py' in f for f in r.get('files_modified', []))},
                required=True
            )
        ]
    )

def create_test_generation_task(module_path: str) -> SubAgentTask:
    """Create a test generation task"""
    return SubAgentTask(
        task_id=f"test_gen_{Path(module_path).stem}_{int(time.time())}",
        task_type="code_gen",
        description=f"Generate comprehensive unit tests for {module_path}",
        context_files=[module_path, "tests/conftest.py"],
        constraints=[
            f"Only create/modify test files in tests/ directory",
            "Follow existing test patterns and naming conventions",
            "Achieve 100% code coverage for public methods",
            "Include edge cases and error handling tests",
            "Use pytest framework exclusively"
        ],
        success_criteria=[
            SuccessCriterion(
                name="test_file_created",
                test_type="file_exists",
                test_spec={"path": f"tests/test_{Path(module_path).stem}.py"},
                required=True
            ),
            SuccessCriterion(
                name="tests_pass",
                test_type="test_passes",
                test_spec={"command": f"pytest tests/test_{Path(module_path).stem}.py"},
                required=True
            ),
            SuccessCriterion(
                name="coverage_target",
                test_type="test_passes",
                test_spec={"command": f"pytest --cov={module_path} --cov-fail-under=95"},
                required=True
            )
        ]
    )

# Integration with main Claude Code session
class ContextManager:
    """Manages context window by offloading tasks"""
    
    def __init__(self, max_context_tokens: int = 50000):
        self.max_context_tokens = max_context_tokens
        self.current_context_size = 0
        self.orchestrator = ClaudeOrchestrator(Path.cwd())
        
    def should_offload(self, task_description: str) -> bool:
        """Determine if a task should be offloaded"""
        # Offload if context is getting large
        if self.current_context_size > self.max_context_tokens * 0.7:
            return True
            
        # Offload well-defined, isolated tasks
        offloadable_patterns = [
            "update documentation",
            "generate tests",
            "refactor",
            "analyze",
            "create boilerplate"
        ]
        
        return any(pattern in task_description.lower() for pattern in offloadable_patterns)
    
    def offload_task(self, task: SubAgentTask) -> Dict[str, Any]:
        """Offload task and return results"""
        result = self.orchestrator.delegate_task(task)
        
        if result.success:
            # Summarize results instead of full inclusion
            return {
                'status': 'completed',
                'task_id': task.task_id,
                'summary': f"Successfully completed: {task.description}",
                'files_modified': result.output.get('files_modified', [])
            }
        else:
            return {
                'status': 'failed',
                'task_id': task.task_id,
                'reason': result.validation.reason,
                'action_required': 'Manual intervention needed'
            }
```

### Usage Examples

```python
# In main Claude Code session
context_manager = ContextManager()

# When receiving a task
task_description = "Update the README to document the new API endpoints we just added"

if context_manager.should_offload(task_description):
    # Create specific task
    task = create_documentation_task(
        files_changed=['api/endpoints.py', 'api/routes.py']
    )
    
    # Offload to sub-agent
    result = context_manager.offload_task(task)
    
    # Continue with main flow using summary
    print(f"Documentation task result: {result['summary']}")
else:
    # Handle in main session
    # ... regular processing
```

## Benefits

1. **Context Preservation**: Main session maintains focus on high-level orchestration
2. **Parallel Execution**: Multiple sub-agents can run simultaneously
3. **Quality Assurance**: Explicit criteria ensure no compromises
4. **Failure Isolation**: Sub-agent failures don't corrupt main context
5. **Auditability**: Each task has clear specifications and results

## Best Practices

1. **Task Granularity**: Keep sub-agent tasks focused and atomic
2. **Minimal Context**: Only provide files absolutely necessary
3. **Explicit Constraints**: Leave no room for interpretation
4. **Testable Criteria**: All success criteria must be programmatically verifiable
5. **Timeout Management**: Set appropriate timeouts for each task type
6. **Error Recovery**: Plan for sub-agent failures with retry strategies

## Future Enhancements

1. **Task Queue**: Implement priority queue for task scheduling
2. **Resource Management**: Track Claude API usage across sub-agents
3. **Result Caching**: Cache successful results for similar tasks
4. **Learning System**: Track which prompts work best for different task types
5. **Visual Dashboard**: Monitor all active sub-agents in real-time
