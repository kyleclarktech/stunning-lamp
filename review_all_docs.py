#!/usr/bin/env python3
import os
import sys
import time
from pathlib import Path

# Add REBUILD_DOCS to Python path for imports
sys.path.insert(0, str(Path(__file__).parent / "REBUILD_DOCS" / "development_tools"))

from claude_orchestrator import ClaudeOrchestrator, SubAgentTask, TaskType
from SUBAGENT_SUCCESS_CRITERIA import SuccessCriterion, CriterionType

# Get all documents to review
docs_path = Path("REBUILD_DOCS")
documents = [
    f for f in docs_path.glob("*.md")
    if f.name not in ["README.md"] and f.is_file()
]

print(f"Found {len(documents)} documents to review:")
for doc in documents:
    print(f"  - {doc.name}")

# Create orchestrator
orchestrator = ClaudeOrchestrator(Path.cwd(), max_parallel=3)

# Create review task for each document
for doc in documents:
    task_id = f"review_{doc.stem}_{int(time.time())}"
    
    # Get all other docs for context
    context_docs = [str(d) for d in documents if d != doc]
    
    # Create the review prompt
    prompt = f'''STRICT DOCUMENT REVIEW TASK

You are a documentation review sub-agent. Your ONLY job is to review one document comprehensively.

DOCUMENT TO REVIEW: {doc}
CONTEXT DOCUMENTS: {', '.join(context_docs)}

ABSOLUTE REQUIREMENTS:
1. Read the target document completely
2. Read ALL context documents to understand the system
3. Analyze for these specific issues:
   - Internal contradictions within the document
   - Inconsistencies with other documents
   - Missing sections or incomplete explanations
   - Technical errors in code examples
   - Ambiguous or unclear language
   - Broken cross-references
4. Create a findings report at REBUILD_DOCS/Findings/{doc.stem}_review.md

FORBIDDEN ACTIONS:
- Modifying any documents except the findings report
- Providing opinions or suggestions beyond objective findings
- Skipping any section of the document
- Making assumptions about missing information

ANALYSIS CHECKLIST:
[ ] Every section of the document reviewed
[ ] All code examples validated for syntax
[ ] All cross-references to other docs verified
[ ] Technical accuracy checked against system design
[ ] Terminology consistency verified
[ ] Completeness of explanations assessed

OUTPUT FORMAT:
```markdown
# Review Findings: {doc.name}

Date: {time.strftime("%Y-%m-%d %H:%M:%S")}
Reviewer: Sub-Agent {task_id}

## Summary
- Document Purpose: [Brief description]
- Overall Status: [COMPLETE|INCOMPLETE|INCONSISTENT]
- Critical Issues: [count]
- Total Findings: [count]

## Findings

### Finding #1: [Descriptive Title]
**Severity**: CRITICAL|HIGH|MEDIUM|LOW
**Type**: Inconsistency|Missing Content|Technical Error|Clarity Issue|Broken Reference
**Location**: [Section name, line number if applicable]
**Description**: [Detailed explanation of the issue]
**Evidence**: 
[Quote the specific problematic text]
**Impact**: [How this affects system understanding or implementation]
**Cross-Reference**: [If this contradicts another document, specify which and where]

[Repeat for each finding]

## Cross-Document Consistency Check
- References to this document from others: [List with validation status]
- References from this document to others: [List with validation status]
- Terminology alignment: [CONSISTENT|INCONSISTENT - list issues]
- Technical alignment: [CONSISTENT|INCONSISTENT - list issues]

## Code Example Validation
[List each code example with validation status]

## Completeness Assessment
- Required sections present: [YES|NO - list missing]
- Concepts fully explained: [YES|NO - list incomplete]
- Examples adequate: [YES|NO - specify needs]

VALIDATION: Task succeeds ONLY if findings file is created with ALL sections completed.
```'''
    
    # Create success criteria
    criteria = [
        SuccessCriterion(
            name="findings_file_created",
            type=CriterionType.FILE_EXISTS,
            config={"path": f"REBUILD_DOCS/Findings/{doc.stem}_review.md"},
            required=True
        ),
        SuccessCriterion(
            name="findings_file_valid",
            type=CriterionType.FILE_CONTAINS,
            config={
                "path": f"REBUILD_DOCS/Findings/{doc.stem}_review.md",
                "text": "## Summary"
            },
            required=True
        ),
        SuccessCriterion(
            name="no_source_modifications",
            type=CriterionType.NO_CHANGES_TO,
            config={"patterns": ["REBUILD_DOCS/*.md", "!REBUILD_DOCS/Findings/*"]},
            required=True
        )
    ]
    
    # Create task
    task = SubAgentTask(
        task_id=task_id,
        task_type=TaskType.DOCUMENTATION,  # Reuse existing type
        description=f"Comprehensive review of {doc.name}",
        prompt_template=prompt,
        context_files=[str(doc)] + context_docs,
        success_criteria=criteria,
        max_attempts=2,
        timeout_seconds=600  # 10 minutes per document
    )
    
    orchestrator.add_task(task)

# Execute all review tasks
print(f"\nExecuting review of {len(documents)} documents...")
results = orchestrator.execute_all()

# Generate summary report
summary = orchestrator.get_summary()
print(f"\nReview complete. Success rate: {summary['success_rate']:.1f}%")

# Create comprehensive summary
if summary['success_rate'] > 80:
    print("\nGenerating comprehensive summary...")
    # Create a final task to synthesize all findings
    synthesis_task = SubAgentTask(
        task_id=f"synthesis_{int(time.time())}",
        task_type=TaskType.DOCUMENTATION,
        description="Synthesize all review findings",
        prompt_template="""Create REBUILD_DOCS/Findings/COMPREHENSIVE_REVIEW_SUMMARY.md that:
1. Aggregates all findings from individual reviews
2. Identifies systemic issues across documents
3. Prioritizes fixes by severity and impact
4. Groups related issues together
5. Provides a clear action plan

Read all individual review files in REBUILD_DOCS/Findings/ and create a comprehensive summary.""",
        context_files=[f"REBUILD_DOCS/Findings/{doc.stem}_review.md" for doc in documents],
        success_criteria=[
            SuccessCriterion(
                name="summary_created",
                type=CriterionType.FILE_EXISTS,
                config={"path": "REBUILD_DOCS/Findings/COMPREHENSIVE_REVIEW_SUMMARY.md"},
                required=True
            )
        ],
        timeout_seconds=900
    )
    
    synthesis_orchestrator = ClaudeOrchestrator(Path.cwd(), max_parallel=1)
    synthesis_orchestrator.add_task(synthesis_task)
    synthesis_orchestrator.execute_all()

print("\nReview process complete. Check REBUILD_DOCS/Findings/ for results.")