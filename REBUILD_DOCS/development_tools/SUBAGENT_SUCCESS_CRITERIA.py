#!/usr/bin/env python3
"""
Sub-Agent Success Criteria Framework

A comprehensive framework for defining and validating testable success criteria
for delegated sub-agent tasks. Ensures strict quality control and no compromises.
"""

import json
import subprocess
import re
import ast
from pathlib import Path
from typing import Dict, Any, List, Callable, Optional, Union
from dataclasses import dataclass, field
from enum import Enum
import hashlib
import difflib
from datetime import datetime


class CriterionType(Enum):
    """Types of success criteria that can be validated"""
    FILE_EXISTS = "file_exists"
    FILE_CONTAINS = "file_contains"
    FILE_MATCHES_PATTERN = "file_matches_pattern"
    FILE_HASH = "file_hash"
    COMMAND_SUCCEEDS = "command_succeeds"
    COMMAND_OUTPUT = "command_output"
    PYTHON_ASSERTION = "python_assertion"
    JSON_SCHEMA = "json_schema"
    DIFF_CHECK = "diff_check"
    AST_CHECK = "ast_check"
    PERFORMANCE_CHECK = "performance_check"
    SECURITY_CHECK = "security_check"
    NO_CHANGES_TO = "no_changes_to"
    ALL_OF = "all_of"
    ANY_OF = "any_of"


@dataclass
class ValidationResult:
    """Result of validating a success criterion"""
    success: bool
    criterion_name: str
    message: str
    details: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class SuccessCriterion:
    """A testable success criterion for sub-agent tasks"""
    name: str
    type: CriterionType
    config: Dict[str, Any]
    required: bool = True
    description: str = ""
    
    def validate(self, context: 'ValidationContext') -> ValidationResult:
        """Validate this criterion against the context"""
        validator = VALIDATORS.get(self.type)
        if not validator:
            return ValidationResult(
                success=False,
                criterion_name=self.name,
                message=f"Unknown criterion type: {self.type}"
            )
        
        try:
            return validator(self, context)
        except Exception as e:
            return ValidationResult(
                success=False,
                criterion_name=self.name,
                message=f"Validation error: {str(e)}",
                details={"exception": str(e), "type": type(e).__name__}
            )


class ValidationContext:
    """Context for running validations"""
    
    def __init__(self, project_root: Path, task_result: Dict[str, Any]):
        self.project_root = project_root
        self.task_result = task_result
        self.file_cache: Dict[str, str] = {}
        self.command_cache: Dict[str, Any] = {}
        
    def read_file(self, path: Union[str, Path]) -> str:
        """Read file with caching"""
        path_str = str(path)
        if path_str not in self.file_cache:
            full_path = self.project_root / path
            self.file_cache[path_str] = full_path.read_text()
        return self.file_cache[path_str]
    
    def run_command(self, cmd: Union[str, List[str]], **kwargs) -> subprocess.CompletedProcess:
        """Run command with caching"""
        cmd_key = str(cmd)
        if cmd_key not in self.command_cache:
            if isinstance(cmd, str):
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, 
                                      cwd=self.project_root, **kwargs)
            else:
                result = subprocess.run(cmd, capture_output=True, text=True,
                                      cwd=self.project_root, **kwargs)
            self.command_cache[cmd_key] = result
        return self.command_cache[cmd_key]


# --- Validator Functions ---

def validate_file_exists(criterion: SuccessCriterion, context: ValidationContext) -> ValidationResult:
    """Validate that a file exists"""
    path = Path(context.project_root) / criterion.config['path']
    exists = path.exists()
    
    return ValidationResult(
        success=exists,
        criterion_name=criterion.name,
        message=f"File {'exists' if exists else 'does not exist'}: {path}",
        details={"path": str(path), "exists": exists}
    )


def validate_file_contains(criterion: SuccessCriterion, context: ValidationContext) -> ValidationResult:
    """Validate that a file contains specific text"""
    path = criterion.config['path']
    text = criterion.config['text']
    case_sensitive = criterion.config.get('case_sensitive', True)
    
    try:
        content = context.read_file(path)
        if not case_sensitive:
            content = content.lower()
            text = text.lower()
        
        contains = text in content
        
        return ValidationResult(
            success=contains,
            criterion_name=criterion.name,
            message=f"File {'contains' if contains else 'does not contain'} required text",
            details={"path": path, "text": text[:100], "found": contains}
        )
    except FileNotFoundError:
        return ValidationResult(
            success=False,
            criterion_name=criterion.name,
            message=f"File not found: {path}",
            details={"path": path}
        )


def validate_file_matches_pattern(criterion: SuccessCriterion, context: ValidationContext) -> ValidationResult:
    """Validate that a file matches a regex pattern"""
    path = criterion.config['path']
    pattern = criterion.config['pattern']
    flags = criterion.config.get('flags', 0)
    
    try:
        content = context.read_file(path)
        regex = re.compile(pattern, flags)
        matches = regex.findall(content)
        
        success = len(matches) > 0
        
        return ValidationResult(
            success=success,
            criterion_name=criterion.name,
            message=f"Found {len(matches)} matches for pattern",
            details={"path": path, "pattern": pattern, "matches": matches[:5]}
        )
    except FileNotFoundError:
        return ValidationResult(
            success=False,
            criterion_name=criterion.name,
            message=f"File not found: {path}",
            details={"path": path}
        )


def validate_file_hash(criterion: SuccessCriterion, context: ValidationContext) -> ValidationResult:
    """Validate that a file has a specific hash"""
    path = criterion.config['path']
    expected_hash = criterion.config['hash']
    algorithm = criterion.config.get('algorithm', 'sha256')
    
    try:
        content = context.read_file(path).encode()
        hasher = hashlib.new(algorithm)
        hasher.update(content)
        actual_hash = hasher.hexdigest()
        
        matches = actual_hash == expected_hash
        
        return ValidationResult(
            success=matches,
            criterion_name=criterion.name,
            message=f"File hash {'matches' if matches else 'does not match'}",
            details={
                "path": path,
                "expected": expected_hash,
                "actual": actual_hash,
                "algorithm": algorithm
            }
        )
    except FileNotFoundError:
        return ValidationResult(
            success=False,
            criterion_name=criterion.name,
            message=f"File not found: {path}",
            details={"path": path}
        )


def validate_command_succeeds(criterion: SuccessCriterion, context: ValidationContext) -> ValidationResult:
    """Validate that a command runs successfully"""
    command = criterion.config['command']
    timeout = criterion.config.get('timeout', 30)
    
    try:
        result = context.run_command(command, timeout=timeout)
        success = result.returncode == 0
        
        return ValidationResult(
            success=success,
            criterion_name=criterion.name,
            message=f"Command {'succeeded' if success else 'failed'} with code {result.returncode}",
            details={
                "command": command,
                "returncode": result.returncode,
                "stdout": result.stdout[:500],
                "stderr": result.stderr[:500]
            }
        )
    except subprocess.TimeoutExpired:
        return ValidationResult(
            success=False,
            criterion_name=criterion.name,
            message=f"Command timed out after {timeout} seconds",
            details={"command": command, "timeout": timeout}
        )


def validate_command_output(criterion: SuccessCriterion, context: ValidationContext) -> ValidationResult:
    """Validate command output matches expectations"""
    command = criterion.config['command']
    expected = criterion.config.get('expected_output')
    expected_pattern = criterion.config.get('expected_pattern')
    contains = criterion.config.get('contains')
    
    result = context.run_command(command)
    output = result.stdout
    
    if expected is not None:
        success = output.strip() == expected.strip()
        message = f"Output {'matches' if success else 'does not match'} expected"
    elif expected_pattern is not None:
        success = bool(re.search(expected_pattern, output))
        message = f"Output {'matches' if success else 'does not match'} pattern"
    elif contains is not None:
        success = contains in output
        message = f"Output {'contains' if success else 'does not contain'} required text"
    else:
        return ValidationResult(
            success=False,
            criterion_name=criterion.name,
            message="No expected output specified"
        )
    
    return ValidationResult(
        success=success,
        criterion_name=criterion.name,
        message=message,
        details={
            "command": command,
            "output": output[:500],
            "expected": expected or expected_pattern or contains
        }
    )


def validate_python_assertion(criterion: SuccessCriterion, context: ValidationContext) -> ValidationResult:
    """Validate using a Python assertion"""
    code = criterion.config['code']
    setup = criterion.config.get('setup', '')
    
    # Create evaluation namespace
    namespace = {
        'context': context,
        'project_root': context.project_root,
        'task_result': context.task_result,
        'Path': Path,
        're': re,
        'json': json
    }
    
    try:
        # Run setup code
        if setup:
            exec(setup, namespace)
        
        # Run assertion
        exec(f"__result__ = bool({code})", namespace)
        success = namespace['__result__']
        
        return ValidationResult(
            success=success,
            criterion_name=criterion.name,
            message=f"Assertion {'passed' if success else 'failed'}",
            details={"code": code, "result": success}
        )
    except Exception as e:
        return ValidationResult(
            success=False,
            criterion_name=criterion.name,
            message=f"Assertion error: {str(e)}",
            details={"code": code, "error": str(e)}
        )


def validate_json_schema(criterion: SuccessCriterion, context: ValidationContext) -> ValidationResult:
    """Validate JSON against a schema"""
    try:
        import jsonschema
    except ImportError:
        return ValidationResult(
            success=False,
            criterion_name=criterion.name,
            message="jsonschema module not installed"
        )
    
    data_source = criterion.config['data_source']
    schema = criterion.config['schema']
    
    # Get data to validate
    if data_source == 'task_result':
        data = context.task_result
    elif data_source.startswith('file:'):
        path = data_source[5:]
        data = json.loads(context.read_file(path))
    else:
        data = json.loads(data_source)
    
    try:
        jsonschema.validate(data, schema)
        return ValidationResult(
            success=True,
            criterion_name=criterion.name,
            message="JSON validates against schema"
        )
    except jsonschema.ValidationError as e:
        return ValidationResult(
            success=False,
            criterion_name=criterion.name,
            message=f"JSON validation failed: {e.message}",
            details={"error": str(e), "path": list(e.path)}
        )


def validate_diff_check(criterion: SuccessCriterion, context: ValidationContext) -> ValidationResult:
    """Validate file differences"""
    file1 = criterion.config['file1']
    file2 = criterion.config['file2']
    max_diff_lines = criterion.config.get('max_diff_lines', 0)
    
    try:
        content1 = context.read_file(file1).splitlines(keepends=True)
        content2 = context.read_file(file2).splitlines(keepends=True)
        
        diff = list(difflib.unified_diff(content1, content2, fromfile=file1, tofile=file2))
        diff_lines = len([line for line in diff if line.startswith('+') or line.startswith('-')])
        
        success = diff_lines <= max_diff_lines
        
        return ValidationResult(
            success=success,
            criterion_name=criterion.name,
            message=f"Files have {diff_lines} different lines (max allowed: {max_diff_lines})",
            details={
                "file1": file1,
                "file2": file2,
                "diff_lines": diff_lines,
                "sample_diff": ''.join(diff[:20])
            }
        )
    except FileNotFoundError as e:
        return ValidationResult(
            success=False,
            criterion_name=criterion.name,
            message=f"File not found: {e.filename}"
        )


def validate_ast_check(criterion: SuccessCriterion, context: ValidationContext) -> ValidationResult:
    """Validate Python AST structure"""
    file_path = criterion.config['file']
    expected_classes = criterion.config.get('expected_classes', [])
    expected_functions = criterion.config.get('expected_functions', [])
    forbidden_imports = criterion.config.get('forbidden_imports', [])
    
    try:
        content = context.read_file(file_path)
        tree = ast.parse(content)
        
        # Extract information
        classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                imports.append(node.module)
        
        # Check expectations
        issues = []
        
        for expected in expected_classes:
            if expected not in classes:
                issues.append(f"Missing class: {expected}")
        
        for expected in expected_functions:
            if expected not in functions:
                issues.append(f"Missing function: {expected}")
        
        for forbidden in forbidden_imports:
            if forbidden in imports:
                issues.append(f"Forbidden import: {forbidden}")
        
        success = len(issues) == 0
        
        return ValidationResult(
            success=success,
            criterion_name=criterion.name,
            message="AST check passed" if success else f"AST check failed: {'; '.join(issues)}",
            details={
                "classes": classes,
                "functions": functions,
                "imports": imports,
                "issues": issues
            }
        )
    except SyntaxError as e:
        return ValidationResult(
            success=False,
            criterion_name=criterion.name,
            message=f"Syntax error in file: {e}",
            details={"file": file_path, "error": str(e)}
        )


def validate_no_changes_to(criterion: SuccessCriterion, context: ValidationContext) -> ValidationResult:
    """Validate that specific files/patterns were not changed"""
    patterns = criterion.config['patterns']
    if isinstance(patterns, str):
        patterns = [patterns]
    
    # Get list of modified files from task result
    modified_files = context.task_result.get('files_modified', [])
    
    violations = []
    for pattern in patterns:
        for file in modified_files:
            if Path(file).match(pattern):
                violations.append(f"{file} matches protected pattern {pattern}")
    
    success = len(violations) == 0
    
    return ValidationResult(
        success=success,
        criterion_name=criterion.name,
        message="No protected files changed" if success else f"Protected files were modified",
        details={
            "patterns": patterns,
            "violations": violations,
            "modified_files": modified_files
        }
    )


def validate_all_of(criterion: SuccessCriterion, context: ValidationContext) -> ValidationResult:
    """Validate that all sub-criteria pass"""
    sub_criteria = [SuccessCriterion(**c) for c in criterion.config['criteria']]
    results = [c.validate(context) for c in sub_criteria]
    
    all_passed = all(r.success for r in results)
    failed = [r for r in results if not r.success]
    
    return ValidationResult(
        success=all_passed,
        criterion_name=criterion.name,
        message=f"All criteria passed" if all_passed else f"{len(failed)} criteria failed",
        details={
            "total": len(sub_criteria),
            "passed": len([r for r in results if r.success]),
            "failed": len(failed),
            "failures": [{"name": r.criterion_name, "message": r.message} for r in failed]
        }
    )


def validate_any_of(criterion: SuccessCriterion, context: ValidationContext) -> ValidationResult:
    """Validate that at least one sub-criterion passes"""
    sub_criteria = [SuccessCriterion(**c) for c in criterion.config['criteria']]
    results = [c.validate(context) for c in sub_criteria]
    
    any_passed = any(r.success for r in results)
    passed = [r for r in results if r.success]
    
    return ValidationResult(
        success=any_passed,
        criterion_name=criterion.name,
        message=f"{len(passed)} criteria passed" if any_passed else "No criteria passed",
        details={
            "total": len(sub_criteria),
            "passed": len(passed),
            "passed_criteria": [r.criterion_name for r in passed]
        }
    )


# Register all validators
VALIDATORS: Dict[CriterionType, Callable] = {
    CriterionType.FILE_EXISTS: validate_file_exists,
    CriterionType.FILE_CONTAINS: validate_file_contains,
    CriterionType.FILE_MATCHES_PATTERN: validate_file_matches_pattern,
    CriterionType.FILE_HASH: validate_file_hash,
    CriterionType.COMMAND_SUCCEEDS: validate_command_succeeds,
    CriterionType.COMMAND_OUTPUT: validate_command_output,
    CriterionType.PYTHON_ASSERTION: validate_python_assertion,
    CriterionType.JSON_SCHEMA: validate_json_schema,
    CriterionType.DIFF_CHECK: validate_diff_check,
    CriterionType.AST_CHECK: validate_ast_check,
    CriterionType.NO_CHANGES_TO: validate_no_changes_to,
    CriterionType.ALL_OF: validate_all_of,
    CriterionType.ANY_OF: validate_any_of,
}


# --- Example Usage ---

def create_test_generation_criteria(module_name: str, coverage_target: int = 90) -> List[SuccessCriterion]:
    """Create criteria for test generation task"""
    return [
        SuccessCriterion(
            name="test_file_exists",
            type=CriterionType.FILE_EXISTS,
            config={"path": f"tests/test_{module_name}.py"},
            required=True,
            description="Test file must be created"
        ),
        SuccessCriterion(
            name="test_file_valid_python",
            type=CriterionType.AST_CHECK,
            config={
                "file": f"tests/test_{module_name}.py",
                "expected_functions": [],  # At least parseable
                "forbidden_imports": []
            },
            required=True,
            description="Test file must be valid Python"
        ),
        SuccessCriterion(
            name="tests_pass",
            type=CriterionType.COMMAND_SUCCEEDS,
            config={
                "command": f"pytest tests/test_{module_name}.py -v"
            },
            required=True,
            description="All tests must pass"
        ),
        SuccessCriterion(
            name="coverage_met",
            type=CriterionType.COMMAND_OUTPUT,
            config={
                "command": f"pytest tests/test_{module_name}.py --cov={module_name} --cov-report=json",
                "expected_pattern": f'"totals".*"percent_covered": *([{coverage_target}-9]\\d|100)'
            },
            required=True,
            description=f"Code coverage must be at least {coverage_target}%"
        ),
        SuccessCriterion(
            name="no_source_modifications",
            type=CriterionType.NO_CHANGES_TO,
            config={
                "patterns": [f"src/{module_name}.py", f"{module_name}.py"]
            },
            required=True,
            description="Source code must not be modified"
        )
    ]


def create_documentation_criteria(doc_files: List[str]) -> List[SuccessCriterion]:
    """Create criteria for documentation tasks"""
    return [
        SuccessCriterion(
            name="all_docs_updated",
            type=CriterionType.ALL_OF,
            config={
                "criteria": [
                    {
                        "name": f"{Path(doc).stem}_updated",
                        "type": "file_contains",
                        "config": {
                            "path": doc,
                            "text": f"Last updated: {datetime.now().strftime('%Y-%m-%d')}"
                        }
                    }
                    for doc in doc_files
                ]
            },
            required=True,
            description="All documentation files must be updated with current date"
        ),
        SuccessCriterion(
            name="valid_markdown",
            type=CriterionType.ALL_OF,
            config={
                "criteria": [
                    {
                        "name": f"{Path(doc).stem}_valid_md",
                        "type": "command_succeeds",
                        "config": {
                            "command": f"python -m markdown {doc} > /dev/null"
                        }
                    }
                    for doc in doc_files
                ]
            },
            required=True,
            description="All documentation must be valid Markdown"
        ),
        SuccessCriterion(
            name="no_code_changes",
            type=CriterionType.NO_CHANGES_TO,
            config={
                "patterns": ["*.py", "*.js", "*.ts", "*.java", "*.go"]
            },
            required=True,
            description="No source code files should be modified"
        )
    ]


if __name__ == "__main__":
    # Example validation
    task_result = {
        "files_modified": ["tests/test_example.py", "README.md"],
        "task_id": "test_gen_123",
        "duration": 45.2
    }
    
    context = ValidationContext(Path.cwd(), task_result)
    criteria = create_test_generation_criteria("example", coverage_target=95)
    
    print("Validating test generation criteria...")
    for criterion in criteria:
        result = criterion.validate(context)
        status = "✓" if result.success else "✗"
        print(f"{status} {criterion.name}: {result.message}")
        if not result.success and result.details:
            print(f"   Details: {result.details}")
