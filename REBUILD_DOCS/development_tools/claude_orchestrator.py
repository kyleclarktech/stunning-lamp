#!/usr/bin/env python3
"""
Claude Code Orchestrator - Proof of Concept

A complete implementation for managing context bloat by delegating tasks
to headless Claude Code sub-agents with strict validation.

Usage:
    python claude_orchestrator.py --task documentation --files api.py,models.py
    python claude_orchestrator.py --task tests --module calculator --coverage 95
    python claude_orchestrator.py --task refactor --type rename --from old_var --to new_var
"""

import argparse
import asyncio
import json
import logging
import subprocess
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum

# Import our success criteria framework
from SUBAGENT_SUCCESS_CRITERIA import (
    SuccessCriterion, CriterionType, ValidationContext,
    create_test_generation_criteria, create_documentation_criteria
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TaskType(Enum):
    """Types of tasks that can be delegated"""
    DOCUMENTATION = "documentation"
    TEST_GENERATION = "test_generation"
    REFACTORING = "refactoring"
    SECURITY_AUDIT = "security_audit"
    PERFORMANCE_ANALYSIS = "performance_analysis"


@dataclass
class SubAgentTask:
    """Complete specification for a delegated task"""
    task_id: str
    task_type: TaskType
    description: str
    prompt_template: str
    context_files: List[str]
    success_criteria: List[SuccessCriterion]
    max_attempts: int = 3
    timeout_seconds: int = 300
    constraints: List[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "task_id": self.task_id,
            "task_type": self.task_type.value,
            "description": self.description,
            "context_files": self.context_files,
            "max_attempts": self.max_attempts,
            "timeout_seconds": self.timeout_seconds,
            "constraints": self.constraints or []
        }


@dataclass
class TaskResult:
    """Result from a sub-agent task"""
    task_id: str
    success: bool
    duration: float
    attempts: int
    output: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    validation_results: List[Dict[str, Any]] = None
    

class PromptGenerator:
    """Generates strict prompts for sub-agents"""
    
    DOCUMENTATION_TEMPLATE = """
STRICT DOCUMENTATION UPDATE TASK

Task ID: {task_id}
Files Changed: {changed_files}
Documentation Files: {doc_files}

ABSOLUTE REQUIREMENTS:
1. Read ALL changed files to understand modifications
2. Update ALL relevant documentation sections
3. Add "Last updated: {date}" to each modified doc
4. Include code examples for new features
5. Update table of contents if structure changes

FORBIDDEN:
- Modifying ANY non-documentation file
- Removing existing documentation
- Changing documentation style

VALIDATION: All criteria must pass. No partial updates.
"""

    TEST_GENERATION_TEMPLATE = """
STRICT TEST GENERATION TASK

Task ID: {task_id}
Module to Test: {module_path}
Test File: tests/test_{module_name}.py
Coverage Target: {coverage}%

ABSOLUTE REQUIREMENTS:
1. Create comprehensive test suite
2. Include: happy path, edge cases, error handling
3. Follow existing test patterns
4. Achieve {coverage}% coverage minimum
5. All tests must pass

FORBIDDEN:
- Modifying source code
- Creating files outside tests/
- Incomplete test coverage

VALIDATION: All tests pass with required coverage.
"""

    @classmethod
    def generate(cls, task: SubAgentTask) -> str:
        """Generate appropriate prompt for task type"""
        if task.task_type == TaskType.DOCUMENTATION:
            return cls.DOCUMENTATION_TEMPLATE.format(
                task_id=task.task_id,
                changed_files=", ".join(task.context_files),
                doc_files="README.md, docs/",
                date=datetime.now().strftime("%Y-%m-%d")
            )
        elif task.task_type == TaskType.TEST_GENERATION:
            module_path = task.context_files[0]
            module_name = Path(module_path).stem
            return cls.TEST_GENERATION_TEMPLATE.format(
                task_id=task.task_id,
                module_path=module_path,
                module_name=module_name,
                coverage=95
            )
        else:
            raise ValueError(f"No template for task type: {task.task_type}")


class ClaudeSubAgent:
    """Manages execution of a single sub-agent"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        
    def execute(self, task: SubAgentTask) -> TaskResult:
        """Execute task using headless Claude Code"""
        start_time = time.time()
        prompt = PromptGenerator.generate(task)
        
        # Write prompt to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(prompt)
            prompt_file = f.name
        
        try:
            # Build Claude command
            cmd = self._build_command(task, prompt_file)
            
            # Execute with retries
            for attempt in range(1, task.max_attempts + 1):
                logger.info(f"Executing task {task.task_id} (attempt {attempt}/{task.max_attempts})")
                
                try:
                    result = self._run_claude(cmd, task.timeout_seconds)
                    
                    # Validate results
                    validation_passed = self._validate_results(task, result)
                    
                    if validation_passed:
                        duration = time.time() - start_time
                        return TaskResult(
                            task_id=task.task_id,
                            success=True,
                            duration=duration,
                            attempts=attempt,
                            output=result
                        )
                    else:
                        logger.warning(f"Task {task.task_id} failed validation on attempt {attempt}")
                        
                except subprocess.TimeoutExpired:
                    logger.error(f"Task {task.task_id} timed out on attempt {attempt}")
                except Exception as e:
                    logger.error(f"Task {task.task_id} failed on attempt {attempt}: {e}")
                    
            # All attempts failed
            duration = time.time() - start_time
            return TaskResult(
                task_id=task.task_id,
                success=False,
                duration=duration,
                attempts=task.max_attempts,
                error="Failed all validation attempts"
            )
            
        finally:
            # Cleanup
            Path(prompt_file).unlink(missing_ok=True)
    
    def _build_command(self, task: SubAgentTask, prompt_file: str) -> List[str]:
        """Build Claude command with appropriate flags"""
        cmd = [
            'claude',
            '--print',  # Non-interactive
            '--output-format', 'json',  # Structured output
            '--dangerously-skip-permissions',  # No prompts
            '--max-turns', str(task.max_attempts * 2),
            '--file', prompt_file
        ]
        
        # Add tool restrictions based on task type
        if task.task_type == TaskType.DOCUMENTATION:
            cmd.extend(['--allowedTools', 'Read,Write,Edit,MultiEdit,Grep'])
        elif task.task_type == TaskType.TEST_GENERATION:
            cmd.extend(['--allowedTools', 'Read,Write,Edit,MultiEdit,Bash'])
            
        return cmd
    
    def _run_claude(self, cmd: List[str], timeout: int) -> Dict[str, Any]:
        """Execute Claude and parse output"""
        result = subprocess.run(
            cmd,
            cwd=self.project_root,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=True
        )
        
        # Parse JSON output
        try:
            output = json.loads(result.stdout)
            return output
        except json.JSONDecodeError:
            # Fallback for non-JSON output
            return {
                "result": result.stdout,
                "files_modified": [],
                "duration": 0
            }
    
    def _validate_results(self, task: SubAgentTask, result: Dict[str, Any]) -> bool:
        """Validate task results against success criteria"""
        context = ValidationContext(self.project_root, result)
        
        all_passed = True
        for criterion in task.success_criteria:
            validation = criterion.validate(context)
            if criterion.required and not validation.success:
                logger.error(f"Failed criterion {criterion.name}: {validation.message}")
                all_passed = False
            else:
                logger.info(f"Passed criterion {criterion.name}")
                
        return all_passed


class ClaudeOrchestrator:
    """Main orchestrator for managing multiple sub-agents"""
    
    def __init__(self, project_root: Path, max_parallel: int = 3):
        self.project_root = project_root
        self.max_parallel = max_parallel
        self.active_tasks: Dict[str, SubAgentTask] = {}
        self.completed_tasks: Dict[str, TaskResult] = {}
        self.task_queue: List[SubAgentTask] = []
        
    def add_task(self, task: SubAgentTask) -> None:
        """Add task to queue"""
        self.task_queue.append(task)
        logger.info(f"Added task {task.task_id} to queue")
        
    def execute_all(self) -> Dict[str, TaskResult]:
        """Execute all queued tasks with parallelism"""
        logger.info(f"Executing {len(self.task_queue)} tasks with max parallelism {self.max_parallel}")
        
        with ThreadPoolExecutor(max_workers=self.max_parallel) as executor:
            # Submit all tasks
            future_to_task = {}
            for task in self.task_queue:
                agent = ClaudeSubAgent(self.project_root)
                future = executor.submit(agent.execute, task)
                future_to_task[future] = task
                self.active_tasks[task.task_id] = task
            
            # Process results as they complete
            for future in as_completed(future_to_task):
                task = future_to_task[future]
                try:
                    result = future.result()
                    self.completed_tasks[task.task_id] = result
                    del self.active_tasks[task.task_id]
                    
                    if result.success:
                        logger.info(f"Task {task.task_id} completed successfully in {result.duration:.2f}s")
                    else:
                        logger.error(f"Task {task.task_id} failed: {result.error}")
                        
                except Exception as e:
                    logger.error(f"Task {task.task_id} raised exception: {e}")
                    self.completed_tasks[task.task_id] = TaskResult(
                        task_id=task.task_id,
                        success=False,
                        duration=0,
                        attempts=0,
                        error=str(e)
                    )
        
        # Clear queue
        self.task_queue.clear()
        
        return self.completed_tasks
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary of all executed tasks"""
        total = len(self.completed_tasks)
        successful = sum(1 for r in self.completed_tasks.values() if r.success)
        failed = total - successful
        
        total_duration = sum(r.duration for r in self.completed_tasks.values())
        
        return {
            "total_tasks": total,
            "successful": successful,
            "failed": failed,
            "success_rate": (successful / total * 100) if total > 0 else 0,
            "total_duration": total_duration,
            "average_duration": total_duration / total if total > 0 else 0,
            "tasks": {
                task_id: {
                    "success": result.success,
                    "duration": result.duration,
                    "attempts": result.attempts,
                    "error": result.error
                }
                for task_id, result in self.completed_tasks.items()
            }
        }


# --- Task Factory Functions ---

def create_documentation_task(changed_files: List[str]) -> SubAgentTask:
    """Create a documentation update task"""
    task_id = f"doc_{int(time.time())}"
    
    return SubAgentTask(
        task_id=task_id,
        task_type=TaskType.DOCUMENTATION,
        description="Update documentation to reflect code changes",
        prompt_template="documentation_strict",
        context_files=changed_files,
        success_criteria=create_documentation_criteria(["README.md", "docs/API.md"]),
        constraints=[
            "Only modify *.md files",
            "Preserve existing structure",
            "Add examples for new features"
        ]
    )


def create_test_task(module_path: str, coverage: int = 90) -> SubAgentTask:
    """Create a test generation task"""
    module_name = Path(module_path).stem
    task_id = f"test_{module_name}_{int(time.time())}"
    
    return SubAgentTask(
        task_id=task_id,
        task_type=TaskType.TEST_GENERATION,
        description=f"Generate tests for {module_path}",
        prompt_template="test_generation_strict",
        context_files=[module_path],
        success_criteria=create_test_generation_criteria(module_name, coverage),
        constraints=[
            f"Only create tests/test_{module_name}.py",
            "Use pytest framework",
            f"Achieve {coverage}% coverage"
        ]
    )


# --- CLI Interface ---

def main():
    parser = argparse.ArgumentParser(description="Claude Code Orchestrator")
    parser.add_argument('--task', required=True, choices=['documentation', 'tests', 'audit'])
    parser.add_argument('--files', help='Comma-separated list of files')
    parser.add_argument('--module', help='Module to test')
    parser.add_argument('--coverage', type=int, default=90, help='Test coverage target')
    parser.add_argument('--parallel', type=int, default=3, help='Max parallel sub-agents')
    
    args = parser.parse_args()
    
    # Initialize orchestrator
    orchestrator = ClaudeOrchestrator(Path.cwd(), max_parallel=args.parallel)
    
    # Create appropriate tasks
    if args.task == 'documentation':
        if not args.files:
            parser.error("--files required for documentation task")
        files = args.files.split(',')
        task = create_documentation_task(files)
        orchestrator.add_task(task)
        
    elif args.task == 'tests':
        if not args.module:
            parser.error("--module required for test task")
        task = create_test_task(args.module, args.coverage)
        orchestrator.add_task(task)
    
    # Execute tasks
    logger.info("Starting task execution...")
    results = orchestrator.execute_all()
    
    # Print summary
    summary = orchestrator.get_summary()
    print("\n" + "="*60)
    print("ORCHESTRATION SUMMARY")
    print("="*60)
    print(f"Total Tasks: {summary['total_tasks']}")
    print(f"Successful: {summary['successful']}")
    print(f"Failed: {summary['failed']}")
    print(f"Success Rate: {summary['success_rate']:.1f}%")
    print(f"Total Duration: {summary['total_duration']:.2f}s")
    print(f"Average Duration: {summary['average_duration']:.2f}s")
    print("\nTask Details:")
    for task_id, details in summary['tasks'].items():
        status = "✓" if details['success'] else "✗"
        print(f"  {status} {task_id}: {details['duration']:.2f}s ({details['attempts']} attempts)")
        if details['error']:
            print(f"     Error: {details['error']}")
    
    # Exit with appropriate code
    exit_code = 0 if summary['failed'] == 0 else 1
    return exit_code


if __name__ == "__main__":
    exit(main())