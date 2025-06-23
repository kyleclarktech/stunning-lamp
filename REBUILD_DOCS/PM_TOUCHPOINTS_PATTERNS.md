# PM-Specific Touchpoints & Patterns

## Overview

This document defines touchpoints and patterns specific to project management workflows, enabling AI agents to efficiently navigate PM concepts, best practices, and common scenarios.

## PM Touchpoint Categories

### 1. Project Planning Touchpoints

```yaml
# touchpoint: project-initiation-pattern
type: pattern
name: "Project Initiation Pattern"
triggers:
  - "start new project"
  - "kick off"
  - "project planning"
  - "initial breakdown"
concepts:
  - project-scoping
  - requirement-gathering
  - stakeholder-identification
  - success-criteria
implementation_refs:
  - "@project-planner/initiation.ts"
  - "@project-planner/templates/"
examples:
  - "web-app-project-example"
  - "api-integration-example"
  - "bug-fix-sprint-example"
related_patterns:
  - "task-decomposition-pattern"
  - "milestone-planning-pattern"
  - "risk-assessment-pattern"
```

```typescript
// @touchpoint project-breakdown-algorithm
// @type implementation
// @concepts [decomposition, work-breakdown-structure, task-hierarchy]
export class ProjectBreakdownService {
  /**
   * @touchpoint recursive-decomposition
   * @pattern divide-and-conquer
   * @complexity O(n log n) where n is number of requirements
   */
  async breakdownProject(project: Project): Promise<TaskHierarchy> {
    // <TOUCHPOINT:complexity-assessment>
    const complexity = await this.assessComplexity(project);
    
    if (complexity.score < this.SIMPLE_THRESHOLD) {
      return this.simpleBreakdown(project);
    }
    // </TOUCHPOINT:complexity-assessment>
    
    // <TOUCHPOINT:functional-decomposition>
    const functionalAreas = await this.identifyFunctionalAreas(project);
    const tasks = await this.createTasksForAreas(functionalAreas);
    // </TOUCHPOINT:functional-decomposition>
    
    return this.buildHierarchy(tasks);
  }
}
```

### 2. Task Assignment Touchpoints

```markdown
<!-- TOUCHPOINT: skill-matching-overview -->
<!-- TYPE: concept -->
<!-- TRIGGERS: ["assign task", "find best person", "skill match"] -->

# Skill-Based Task Assignment

The skill matching system uses a multi-factor scoring algorithm...

<!-- SUBTOUCHPOINT: exact-skill-matching -->
## Exact Skill Matching
When a task requires specific skills, the system first looks for exact matches...

<!-- RELATED: skill-ontology, proficiency-levels -->
<!-- EXAMPLES: frontend-task-assignment, database-expert-matching -->

<!-- SUBTOUCHPOINT: related-skill-inference -->
## Related Skill Inference
The system can infer related skills using the skill ontology...
<!-- /TOUCHPOINT -->
```

### 3. Common PM Patterns

#### Task Decomposition Pattern

```typescript
// @touchpoint-pattern task-decomposition
interface TaskDecompositionPattern {
  name: "Task Decomposition";
  problem: "Large, complex task needs to be broken down";
  context: "Task estimated > 8 hours or has multiple concerns";
  
  solution: {
    steps: [
      "Identify functional boundaries",
      "Extract sub-tasks",
      "Define interfaces/handoffs",
      "Estimate each sub-task",
      "Map dependencies"
    ];
    
    heuristics: [
      "No task larger than 8 hours",
      "Single responsibility per task",
      "Clear acceptance criteria",
      "Identifiable deliverable"
    ];
  };
  
  examples: [
    {
      before: "Implement user authentication",
      after: [
        "Design auth database schema",
        "Create user registration API",
        "Implement password hashing",
        "Create login endpoint",
        "Add session management",
        "Create auth middleware",
        "Write auth tests"
      ]
    }
  ];
  
  anti_patterns: [
    "Over-decomposition (< 1 hour tasks)",
    "Technical-only breakdown (missing user value)",
    "Dependency cycles"
  ];
}
```

#### Workload Balancing Pattern

```typescript
// @touchpoint-pattern workload-balancing
interface WorkloadBalancingPattern {
  name: "Workload Balancing";
  problem: "Team members have uneven work distribution";
  context: "Some overloaded, others underutilized";
  
  solution: {
    steps: [
      "Calculate current utilization",
      "Identify moveable tasks",
      "Find skill matches in underutilized members",
      "Rebalance assignments",
      "Monitor and adjust"
    ];
    
    strategies: {
      peak_shaving: "Move tasks from overloaded members",
      valley_filling: "Assign new work to underutilized",
      cross_training: "Pair for knowledge transfer",
      time_shifting: "Delay non-critical tasks"
    };
  };
  
  metrics: [
    "utilization_variance < 20%",
    "no_member > 90% utilized",
    "maintain_skill_match > 70%"
  ];
}
```

#### Bottleneck Resolution Pattern

```typescript
// @touchpoint-pattern bottleneck-resolution
interface BottleneckResolutionPattern {
  name: "Bottleneck Resolution";
  problem: "Critical path task is blocking progress";
  
  detection: {
    signals: [
      "Multiple tasks waiting on single task",
      "Person assigned to critical task overloaded",
      "External dependency not responding",
      "Technical blocker discovered"
    ];
  };
  
  resolution_strategies: {
    resource_addition: {
      when: "Skill available in team",
      action: "Add additional person to task"
    },
    
    scope_reduction: {
      when: "Timeline critical",
      action: "Reduce scope to unblock dependents"
    },
    
    parallel_work: {
      when: "Interface defined",
      action: "Start dependent work with mocks"
    },
    
    fast_track: {
      when: "Other work can be delayed",
      action: "Prioritize blocker above all else"
    }
  };
}
```

### 4. Progress Monitoring Touchpoints

```typescript
// @touchpoint progress-health-check
// @type implementation
// @triggers ["check progress", "project status", "are we on track"]
export class ProgressHealthCheck {
  /**
   * @touchpoint velocity-calculation
   * @formula story_points_completed / time_period
   * @see-also burndown-charts, sprint-metrics
   */
  calculateVelocity(period: DateRange): number {
    // Implementation
  }
  
  /**
   * @touchpoint risk-identification
   * @patterns slipping-timeline, scope-creep, resource-constraint
   */
  identifyRisks(): Risk[] {
    // Check for common risk patterns
  }
}
```

### 5. Communication Pattern Touchpoints

```markdown
<!-- TOUCHPOINT: status-update-templates -->
<!-- TYPE: templates -->
<!-- TRIGGERS: ["weekly update", "status report", "project summary"] -->

## Status Update Templates

### Weekly Team Update
**Format**: Slack/Email
**When**: Every Monday

```
📊 Weekly Status: [Project Name]

✅ Completed Last Week:
- [Task 1] by [Person] 
- [Task 2] by [Person]

🚀 In Progress:
- [Task 3] (60% complete) - [Person]
- [Task 4] (just started) - [Person]

⚠️ Blockers:
- [Blocker description] - Need [resolution]

📅 This Week's Goals:
- Complete [Task 3, 4]
- Start [Task 5, 6]

💬 Notes:
- [Any important context]
```

<!-- VARIATIONS: executive-summary, technical-deep-dive, client-update -->
```

### 6. Decision Making Touchpoints

```typescript
// @touchpoint-pattern assignment-decision-tree
interface AssignmentDecisionTree {
  name: "Task Assignment Decision Tree";
  
  decision_flow: {
    start: "New task to assign",
    
    questions: [
      {
        question: "Does task require specific expertise?",
        yes: "Find people with required skills",
        no: "Consider learning opportunity"
      },
      {
        question: "Are skilled people available?",
        yes: "Check workload balance",
        no: "Consider training or outsourcing"
      },
      {
        question: "Is timeline critical?",
        yes: "Assign to most experienced",
        no: "Balance experience with growth"
      }
    ],
    
    outcomes: {
      assign_expert: "Best skilled person with capacity",
      train_junior: "Junior with senior oversight",
      defer_task: "Wait for availability",
      scope_change: "Modify requirements"
    }
  };
}
```

## Touchpoint Navigation Examples

### 1. PM Query Navigation

```typescript
// User: "How do I handle a team member who's overloaded?"

const navigation = await touchpointNavigator.findPath({
  query: "team member overloaded",
  context: "project management"
});

// Returns navigation path:
{
  touchpoints: [
    {
      id: "workload-balancing-pattern",
      type: "pattern",
      relevance: 0.95
    },
    {
      id: "bandwidth-tracker-usage",
      type: "implementation",
      relevance: 0.87
    },
    {
      id: "rebalancing-example",
      type: "example",
      relevance: 0.82
    }
  ],
  
  suggested_flow: [
    "Understand the pattern",
    "Use bandwidth tracker to quantify",
    "Apply rebalancing strategies",
    "Monitor results"
  ]
}
```

### 2. Error Recovery Navigation

```typescript
// System: "Failed to assign task: No available team members"

const errorGuidance = await touchpointNavigator.handleError({
  error: "NO_AVAILABLE_MEMBERS",
  context: { task, team }
});

// Returns:
{
  explanation: "All team members with required skills are at capacity",
  
  touchpoints: [
    "capacity-planning-pattern",
    "cross-training-strategy",
    "outsourcing-decision-tree"
  ],
  
  immediate_actions: [
    "Review task priority",
    "Check if task can be delayed",
    "Consider scope reduction"
  ],
  
  preventive_measures: [
    "Implement capacity forecasting",
    "Build skill redundancy",
    "Maintain resource buffer"
  ]
}
```

## PM-Specific Learning Patterns

### 1. Pattern Recognition

```typescript
class PMPatternLearning {
  async learnFromOutcome(
    decision: AssignmentDecision,
    outcome: TaskOutcome
  ): Promise<void> {
    // Record decision factors
    await this.recordDecision({
      factors: decision.factors,
      weights: decision.weights,
      result: decision.assignment
    });
    
    // Record outcome
    await this.recordOutcome({
      completed_on_time: outcome.on_time,
      quality_score: outcome.quality,
      assignee_feedback: outcome.feedback
    });
    
    // Update pattern weights
    if (outcome.success) {
      await this.reinforcePattern(decision.pattern_id);
    } else {
      await this.adjustPattern(decision.pattern_id, outcome.failure_reason);
    }
    
    // Update touchpoint relevance
    await this.updateTouchpointScores(decision, outcome);
  }
}
```

### 2. Adaptive Improvement

```typescript
class AdaptivePMImprovement {
  async improveEstimation(
    task: Task,
    actual: ActualEffort
  ): Promise<void> {
    const variance = actual.hours / task.estimated_hours;
    
    // Update estimation patterns
    if (variance > 1.5 || variance < 0.5) {
      // Significant estimation error
      await this.analyzeEstimationError({
        task_type: task.type,
        complexity_factors: task.complexity,
        skill_requirements: task.required_skills,
        variance: variance
      });
      
      // Update relevant touchpoints
      await this.updateTouchpoint('estimation-patterns', {
        add_factor: this.identifyMissingFactor(task, actual)
      });
    }
    
    // Learn from success
    if (Math.abs(variance - 1) < 0.1) {
      await this.reinforceEstimationPattern(task);
    }
  }
}
```

## Integration with AI Agents

### 1. Contextual PM Assistance

```typescript
class PMAssistantAgent {
  async handleQuery(query: string): Promise<PMResponse> {
    // Identify PM intent
    const intent = await this.classifyPMIntent(query);
    
    // Load relevant touchpoints
    const touchpoints = await this.loadPMTouchpoints(intent);
    
    // Build context
    const context = await this.buildContext({
      intent,
      touchpoints,
      current_projects: await this.getActiveProjects(),
      team_state: await this.getTeamState()
    });
    
    // Generate response
    return this.generateResponse(query, context);
  }
  
  private async loadPMTouchpoints(
    intent: PMIntent
  ): Promise<Touchpoint[]> {
    const relevant = await this.touchpointIndex.search({
      intent: intent.type,
      concepts: intent.concepts,
      triggers: intent.keywords
    });
    
    // Prioritize based on intent
    return this.prioritizeTouchpoints(relevant, intent);
  }
}
```

### 2. Proactive PM Suggestions

```typescript
class ProactivePMMonitor {
  async checkForIssues(): Promise<Suggestion[]> {
    const suggestions: Suggestion[] = [];
    
    // Check each touchpoint trigger
    for (const trigger of this.activeTriggers) {
      const condition = await trigger.evaluate();
      
      if (condition.triggered) {
        const touchpoint = await this.loadTouchpoint(trigger.touchpoint_id);
        
        suggestions.push({
          type: trigger.type,
          severity: condition.severity,
          message: this.generateMessage(touchpoint, condition),
          actions: touchpoint.recommended_actions,
          learn_more: touchpoint.id
        });
      }
    }
    
    return this.prioritizeSuggestions(suggestions);
  }
}
```

## Touchpoint Maintenance

### PM Pattern Validation

```typescript
class PMPatternValidator {
  async validatePatterns(): Promise<ValidationReport> {
    const report = new ValidationReport();
    
    // Check each PM pattern
    for (const pattern of await this.getPMPatterns()) {
      // Validate against recent outcomes
      const outcomes = await this.getPatternOutcomes(pattern.id);
      
      if (outcomes.success_rate < 0.6) {
        report.addWarning(
          `Pattern ${pattern.id} has low success rate`,
          { success_rate: outcomes.success_rate }
        );
      }
      
      // Check if pattern is still used
      if (outcomes.last_used > 30) { // days
        report.addInfo(
          `Pattern ${pattern.id} hasn't been used recently`,
          { last_used_days: outcomes.last_used }
        );
      }
    }
    
    return report;
  }
}
```