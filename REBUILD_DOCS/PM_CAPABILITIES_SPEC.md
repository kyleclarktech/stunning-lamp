# Agentic PM Assistant - Core Capabilities Specification

## Overview

This document details the PM-specific capabilities that make the system an effective autonomous project manager for teams without dedicated human PMs. The PM Assistant operates entirely through graph queries against Neo4j, where ALL data (projects, tasks, people, skills) is stored as nodes and relationships. This graph-first approach eliminates data silos and enables powerful cross-functional queries.

## Graph-First PM Design

All PM entities are graph nodes:
```cypher
// Projects, tasks, people - all in the same graph
(project:Project {id, name, status, deadline})
(task:Task {id, title, estimated_hours, status})
(person:Person {id, name, skills: [], availability: 40})

// Relationships connect everything
(task)-[:BELONGS_TO]->(project)
(person)-[:ASSIGNED_TO]->(task)
(task)-[:DEPENDS_ON]->(otherTask)
(person)-[:HAS_SKILL {level: 'expert'}]->(skill:Skill)
```

## Core PM Workflows

### 1. Project Initiation & Planning

When a user describes a project in natural language, the system:

```typescript
interface GraphProjectInitiation {
  // Step 1: Create project node in graph
  async createProject(description: string): Promise<string> {
    const cypher = `
      CREATE (p:Project {
        id: randomUUID(),
        name: $name,
        description: $description,
        status: 'planning',
        created_at: datetime()
      })
      RETURN p.id as projectId
    `;
    return this.graphExecutor.execute(cypher);
  }
  
  // Step 2: Generate task nodes
  async createTasks(projectId: string, tasks: TaskDescription[]): Promise<void> {
    const cypher = `
      UNWIND $tasks as task
      CREATE (t:Task {
        id: randomUUID(),
        title: task.title,
        description: task.description,
        estimated_hours: task.hours,
        status: 'pending'
      })
      WITH t
      MATCH (p:Project {id: $projectId})
      CREATE (t)-[:BELONGS_TO]->(p)
    `;
    return this.graphExecutor.execute(cypher);
  }
}
```

**Example Interaction**:
```
User: "We need to build a customer dashboard that shows usage metrics, 
       billing info, and support tickets. Should integrate with Stripe 
       and Zendesk. Timeline is 6 weeks."

System: "I'll break this down into a project plan. Based on the requirements,
         I've identified 4 main phases with 23 tasks. Here's the breakdown:
         
         Phase 1: Backend API Development (2 weeks)
         - Set up API framework and authentication
         - Create Stripe integration service
         - Create Zendesk integration service
         - Design and implement data models
         - Build metric aggregation pipeline
         
         Phase 2: Frontend Development (2 weeks)
         ..."
```

### 2. Graph-Based Task Decomposition

Task breakdown creates connected nodes in the graph:

```typescript
class GraphTaskDecomposer {
  async decompose(projectId: string): Promise<void> {
    // Query project to understand scope
    const projectQuery = `
      MATCH (p:Project {id: $projectId})
      RETURN p.description as description, p.type as type
    `;
    
    const project = await this.graphExecutor.execute(projectQuery);
    const areas = await this.identifyFunctionalAreas(project.description);
    
    // Create task nodes for each area
    const createTasksCypher = `
      UNWIND $areas as area
      CREATE (t:Task {
        id: randomUUID(),
        title: area.title,
        type: area.type,
        estimated_hours: area.estimatedHours,
        status: 'pending'
      })
      WITH t, area
      MATCH (p:Project {id: $projectId})
      CREATE (t)-[:BELONGS_TO]->(p)
      // Create dependencies between tasks
      WITH collect(t) as tasks
      UNWIND range(0, size(tasks)-2) as i
      WITH tasks[i] as t1, tasks[i+1] as t2
      WHERE t1.type = 'backend' AND t2.type = 'frontend'
      CREATE (t2)-[:DEPENDS_ON]->(t1)
    `;
    
    await this.graphExecutor.execute(createTasksCypher);
  }
  
  private async identifyFunctionalAreas(item: Project | Task): Promise<FunctionalArea[]> {
    // Use AI to identify logical groupings
    const description = item.description;
    const areas = await this.ai.extractFunctionalAreas(description);
    
    // Common patterns
    const patterns = [
      { pattern: /API|backend|server/i, area: 'backend' },
      { pattern: /UI|frontend|dashboard/i, area: 'frontend' },
      { pattern: /database|model|schema/i, area: 'data' },
      { pattern: /test|QA|quality/i, area: 'testing' },
      { pattern: /deploy|CI|CD/i, area: 'deployment' }
    ];
    
    return this.mergeWithPatterns(areas, patterns);
  }
}
```

### 3. Graph-Powered Skill Matching

Skill matching uses graph traversal instead of complex algorithms:

```typescript
class GraphSkillMatcher {
  async findBestMatch(taskId: string): Promise<Person> {
    // Single graph query finds best match
    const cypher = `
      MATCH (t:Task {id: $taskId})
      MATCH (p:Person)-[:HAS_SKILL]->(s:Skill)<-[:REQUIRES]-(t)
      WHERE p.availability > t.estimated_hours
      WITH p, COUNT(s) as skillMatches, p.availability as avail
      ORDER BY skillMatches DESC, avail DESC
      LIMIT 1
      RETURN p
    `;
    
    const result = await this.graphExecutor.execute({
      statement: cypher,
      parameters: { taskId }
    });
    
    return result.records[0].p;
  }
  
  // Find people with growth opportunities
  async findLearningMatch(taskId: string): Promise<Person> {
    const cypher = `
      MATCH (t:Task {id: $taskId})-[:REQUIRES]->(s:Skill)
      MATCH (p:Person)
      WHERE NOT (p)-[:HAS_SKILL]->(s)
      AND (p)-[:WANTS_TO_LEARN]->(s)
      AND p.availability > t.estimated_hours * 1.5  // Extra time for learning
      RETURN p
      ORDER BY p.availability DESC
      LIMIT 1
    `;
    
    return this.graphExecutor.execute(cypher);
  }
  
  private async calculateSkillMatch(
    required: string[], 
    personSkills: SkillEntry[]
  ): Promise<number> {
    let totalScore = 0;
    let maxPossible = required.length;
    
    for (const reqSkill of required) {
      const match = await this.findSkillMatch(reqSkill, personSkills);
      
      if (match.exact) {
        // Full score for exact match
        totalScore += match.proficiency / 5; // Normalize to 0-1
      } else if (match.related) {
        // Partial score for related skills
        totalScore += (match.proficiency / 5) * match.similarity;
      }
    }
    
    return totalScore / maxPossible;
  }
}
```

### 4. Simple Availability Tracking

Availability is just a property on Person nodes:

```typescript
class GraphAvailabilityTracker {
  async getAvailability(personId: string): Promise<number> {
    const cypher = `
      MATCH (p:Person {id: $personId})
      OPTIONAL MATCH (p)-[:ASSIGNED_TO]->(t:Task {status: 'active'})
      WITH p, COALESCE(SUM(t.estimated_hours), 0) as committed
      RETURN p.availability - committed as availableHours
    `;
    
    const result = await this.graphExecutor.execute({
      statement: cypher,
      parameters: { personId }
    });
    
    return result.records[0].availableHours;
  }
  
  async updateAvailability(personId: string, taskHours: number): Promise<void> {
    // Simple decrement when task assigned
    const cypher = `
      MATCH (p:Person {id: $personId})
      SET p.availability = p.availability - $hours
    `;
    
    await this.graphExecutor.execute({
      statement: cypher,
      parameters: { personId, hours: taskHours }
    });
  }
  
  async getTeamAvailability(teamId: string): Promise<TeamAvailability> {
    const cypher = `
      MATCH (team:Team {id: $teamId})<-[:MEMBER_OF]-(p:Person)
      RETURN p.name as name, p.availability as hours
      ORDER BY p.availability DESC
    `;
    
    return this.graphExecutor.execute(cypher);
  }
}
```

### 5. Graph-Based Assignment

Assignments are just relationships in the graph:

```typescript
class GraphAssignmentEngine {
  async assignTask(taskId: string): Promise<Assignment> {
    // Find best person and create assignment relationship
    const cypher = `
      MATCH (t:Task {id: $taskId})
      MATCH (p:Person)-[:HAS_SKILL]->(s:Skill)<-[:REQUIRES]-(t)
      WHERE p.availability >= t.estimated_hours
      WITH p, t, COUNT(s) as skillMatch
      ORDER BY skillMatch DESC, p.availability DESC
      LIMIT 1
      CREATE (p)-[a:ASSIGNED_TO {
        assigned_at: datetime(),
        confidence: skillMatch * 1.0 / SIZE((t)-[:REQUIRES]->()),
        status: 'active'
      }]->(t)
      SET p.availability = p.availability - t.estimated_hours
      RETURN p, a, t
    `;
    
    const result = await this.graphExecutor.execute({
      statement: cypher,
      parameters: { taskId }
    });
    
    return this.formatAssignment(result);
  }
  
  // Bulk assignment for multiple tasks
  async assignMultipleTasks(projectId: string): Promise<void> {
    const cypher = `
      MATCH (proj:Project {id: $projectId})<-[:BELONGS_TO]-(t:Task {status: 'pending'})
      MATCH (p:Person)-[:HAS_SKILL]->(s:Skill)<-[:REQUIRES]-(t)
      WHERE p.availability > 0
      WITH t, p, COUNT(s) as skillMatch
      ORDER BY t.priority DESC, skillMatch DESC
      WITH t, COLLECT({person: p, score: skillMatch})[0] as best
      WHERE best.score > 0
      CREATE (best.person)-[:ASSIGNED_TO {assigned_at: datetime()}]->(t)
      SET t.status = 'assigned'
    `;
    
    await this.graphExecutor.execute({
      statement: cypher,
      parameters: { projectId }
    });
  }
}
```

### 6. Graph-Based Progress Monitoring

Progress is tracked through graph queries:

```typescript
class GraphProgressMonitor {
  async getProjectStatus(projectId: string): Promise<ProjectStatus> {
    const cypher = `
      MATCH (p:Project {id: $projectId})
      MATCH (p)<-[:BELONGS_TO]-(t:Task)
      WITH p, 
           COUNT(t) as totalTasks,
           COUNT(CASE WHEN t.status = 'completed' THEN 1 END) as completed,
           COUNT(CASE WHEN t.status = 'in_progress' THEN 1 END) as inProgress,
           COUNT(CASE WHEN t.status = 'blocked' THEN 1 END) as blocked
      RETURN p.name as project,
             completed * 100.0 / totalTasks as completionPercent,
             totalTasks, completed, inProgress, blocked
    `;
    
    return this.graphExecutor.execute({
      statement: cypher,
      parameters: { projectId }
    });
  }
  
  async detectBottlenecks(projectId: string): Promise<Bottleneck[]> {
    // Find blocked tasks and overloaded people
    const cypher = `
      MATCH (p:Project {id: $projectId})
      
      // Find blocked tasks on critical path
      MATCH path = (p)<-[:BELONGS_TO]-(blocked:Task {status: 'blocked'})
                   -[:DEPENDS_ON*]->(dependency:Task)
      WITH blocked, LENGTH(path) as pathLength
      ORDER BY pathLength DESC
      
      // Find overloaded people
      MATCH (person:Person)-[:ASSIGNED_TO]->(task:Task {status: 'active'})
      WHERE person.availability < 0
      WITH COLLECT(DISTINCT {type: 'blocked_task', task: blocked}) + 
           COLLECT(DISTINCT {type: 'overloaded', person: person}) as bottlenecks
      
      RETURN bottlenecks
    `;
    
    const result = await this.graphExecutor.execute({
      statement: cypher,
      parameters: { projectId }
    });
    
    return result.records[0].bottlenecks;
  }
}
```

## Natural Language PM Interactions

### Task Planning Examples

```typescript
const pmExamples = [
  {
    user: "Break down the user authentication feature",
    system: `I'll break down the user authentication feature into manageable tasks:

**Backend Tasks** (Total: ~24 hours)
1. Design authentication schema (4h)
   - User model with secure password storage
   - Session/token management
   - Required skills: Database design, Security
   
2. Implement registration endpoint (6h)
   - Input validation
   - Password hashing
   - Email verification
   - Required skills: Node.js, API development

3. Implement login endpoint (4h)
   - Credential verification
   - Token generation
   - Required skills: Node.js, JWT

[... continues with frontend tasks, testing, etc.]

Based on team availability, I recommend:
- Assign backend to Sarah (strong Node.js, available 30h/week)
- Assign frontend to Mike (React expert, available 25h/week)
- Timeline: 1.5 weeks with parallel development`
  },
  
  {
    user: "Who should work on the payment integration?",
    system: `Based on skill analysis and availability:

**Best Match: David Chen**
- Has Stripe API experience (3 projects)
- Strong Python/Node.js skills
- Available 20 hours next week
- Confidence: 92%

**Alternative: Sarah Miller**
- No direct Stripe experience but strong API skills
- Has worked with PayPal integration
- More available (35 hours)
- Confidence: 78%
- Would be a good learning opportunity

**Recommendation**: Assign to David for faster delivery, or to Sarah 
if you want to spread payment knowledge across the team.`
  },
  
  {
    user: "Show me the current bottlenecks",
    system: `I've identified 3 bottlenecks affecting project timeline:

**1. Database Migration Task (HIGH IMPACT)**
- Blocking 5 downstream tasks
- Assigned to Tom who is overloaded (45h committed this week)
- Will delay project by ~3 days if not resolved

*Suggested Action*: Reassign to Lisa (similar skills, 15h available)

**2. API Documentation (MEDIUM IMPACT)**
- No one assigned yet
- Blocking frontend team from integration
- Required skills available in team

*Suggested Action*: Assign to any backend dev for 2-3 hours

**3. Code Review Backlog (MEDIUM IMPACT)**
- 8 PRs waiting for review
- Senior devs are all at capacity

*Suggested Action*: Enable junior devs to review with senior oversight`
  }
];
```

## Simplified Implementation

### 1. Project Templates in Graph

Templates are stored as graph patterns:

```cypher
// Create a template pattern
CREATE (template:ProjectTemplate {type: 'web-feature'})
CREATE (phase1:PhaseTemplate {name: 'backend', order: 1})
CREATE (phase2:PhaseTemplate {name: 'frontend', order: 2})
CREATE (task1:TaskTemplate {title: 'API Design', hours: 8})
CREATE (task2:TaskTemplate {title: 'API Implementation', hours: 16})
CREATE (template)-[:HAS_PHASE]->(phase1)
CREATE (template)-[:HAS_PHASE]->(phase2)
CREATE (phase1)-[:CONTAINS]->(task1)
CREATE (phase1)-[:CONTAINS]->(task2)

// Apply template to new project
MATCH (template:ProjectTemplate {type: $type})-[:HAS_PHASE]->(phase)-[:CONTAINS]->(taskTemplate)
MATCH (project:Project {id: $projectId})
CREATE (task:Task {
  id: randomUUID(),
  title: taskTemplate.title,
  estimated_hours: taskTemplate.hours,
  status: 'pending'
})
CREATE (task)-[:BELONGS_TO]->(project)
```

### 2. Skills as Graph Relationships

Skills form a connected graph:

```cypher
// Skill hierarchy in the graph
CREATE (frontend:Skill {name: 'Frontend Development'})
CREATE (react:Skill {name: 'React'})
CREATE (vue:Skill {name: 'Vue'})
CREATE (js:Skill {name: 'JavaScript'})

// Relationships show hierarchy and similarity
CREATE (react)-[:CHILD_OF]->(frontend)
CREATE (vue)-[:CHILD_OF]->(frontend)
CREATE (react)-[:REQUIRES]->(js)
CREATE (vue)-[:REQUIRES]->(js)
CREATE (react)-[:SIMILAR_TO {score: 0.8}]->(vue)

// Query for related skills
MATCH (s1:Skill {name: $skill})-[:SIMILAR_TO|CHILD_OF|PARENT_OF*1..2]-(s2:Skill)
RETURN DISTINCT s2.name as relatedSkill
```

### 3. Assignment Strategies as Queries

Different Cypher queries for different strategies:

```typescript
const assignmentStrategies = {
  // Get done ASAP - prioritize availability
  minimize_time: `
    MATCH (t:Task {id: $taskId})-[:REQUIRES]->(s:Skill)
    MATCH (p:Person)-[:HAS_SKILL]->(s)
    WHERE p.availability >= t.estimated_hours
    RETURN p ORDER BY p.availability DESC LIMIT 1
  `,
  
  // Growth focus - find learning opportunities  
  develop_skills: `
    MATCH (t:Task {id: $taskId})-[:REQUIRES]->(s:Skill)
    MATCH (p:Person)
    WHERE NOT (p)-[:HAS_SKILL]->(s)
    AND (p)-[:WANTS_TO_LEARN]->(s)
    AND p.availability >= t.estimated_hours * 1.5
    RETURN p LIMIT 1
  `,
  
  // Avoid overload - spread work evenly
  sustainable_pace: `
    MATCH (t:Task {id: $taskId})
    MATCH (p:Person)
    WHERE p.availability >= t.estimated_hours + 8  // Buffer
    RETURN p ORDER BY p.availability DESC LIMIT 1
  `
};
```

## Success Metrics (Graph-Derived)

### All Metrics from Graph Queries

```cypher
// Assignment accuracy - completed without reassignment
MATCH (t:Task {status: 'completed'})
OPTIONAL MATCH (t)<-[a:ASSIGNED_TO]-()
WITH t, COUNT(a) as assignmentCount
RETURN AVG(CASE WHEN assignmentCount = 1 THEN 1.0 ELSE 0.0 END) as assignmentAccuracy

// Workload balance - check distribution
MATCH (p:Person)
OPTIONAL MATCH (p)-[:ASSIGNED_TO]->(t:Task {status: 'active'})
WITH p.name as person, COALESCE(SUM(t.estimated_hours), 0) as workload
RETURN STDEV(workload) as workloadVariance

// Estimation accuracy
MATCH (t:Task {status: 'completed'})
WHERE t.actual_hours IS NOT NULL
RETURN AVG(ABS(t.estimated_hours - t.actual_hours) / t.estimated_hours) as estimationError

// Bottleneck detection time
MATCH (t:Task)
WHERE t.status = 'blocked' AND t.unblocked_at IS NOT NULL
RETURN AVG(duration.between(t.blocked_at, t.unblocked_at).days) as avgBlockedDays
```

## Simplified Integration

### Graph Import/Export

```typescript
// Import tasks from external tools
class GraphImporter {
  async importFromJira(jiraData: JiraExport): Promise<void> {
    const cypher = `
      UNWIND $issues as issue
      CREATE (t:Task {
        id: issue.key,
        title: issue.summary,
        description: issue.description,
        status: issue.status,
        external_ref: 'jira:' + issue.key
      })
    `;
    
    await this.graphExecutor.execute({
      statement: cypher,
      parameters: { issues: jiraData.issues }
    });
  }
}

// Export for external tools
class GraphExporter {
  async exportToCSV(projectId: string): Promise<string> {
    const cypher = `
      MATCH (p:Project {id: $projectId})<-[:BELONGS_TO]-(t:Task)
      OPTIONAL MATCH (t)<-[:ASSIGNED_TO]-(person:Person)
      RETURN t.title as Task, 
             t.status as Status,
             person.name as Assignee,
             t.estimated_hours as Hours
    `;
    
    const results = await this.graphExecutor.execute(cypher);
    return this.formatAsCSV(results);
  }
}
```

## Key Simplifications from Graph-First Design

### What We Eliminated
1. **Complex scoring algorithms** - Graph queries handle matching
2. **Separate bandwidth tracking** - Simple availability property
3. **Multiple assignment strategies** - Different Cypher queries
4. **Skill ontology management** - Skills are graph nodes
5. **Progress calculation logic** - Graph aggregations

### What We Gained
1. **Unified data model** - Everything in Neo4j
2. **Powerful queries** - Complex relationships made simple
3. **Real-time updates** - No sync needed
4. **Simpler codebase** - Less business logic
5. **Better insights** - Graph algorithms available

### Example: Complete Task Assignment

```cypher
// One query does everything the old system did in hundreds of lines
MATCH (project:Project {id: $projectId})<-[:BELONGS_TO]-(task:Task {status: 'pending'})
MATCH (task)-[:REQUIRES]->(skill:Skill)<-[:HAS_SKILL]-(person:Person)
WHERE person.availability >= task.estimated_hours
WITH task, person, COUNT(skill) as skillMatch, person.availability as avail
ORDER BY task.priority DESC, skillMatch DESC, avail DESC
WITH task, FIRST(COLLECT(person)) as assignee
CREATE (assignee)-[:ASSIGNED_TO {assigned_at: datetime()}]->(task)
SET task.status = 'assigned',
    assignee.availability = assignee.availability - task.estimated_hours
RETURN task.title, assignee.name
```
