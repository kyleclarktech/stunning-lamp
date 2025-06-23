# Unified Graph Schema

## Overview

This document defines the complete Neo4j graph schema where ALL system data lives - both organizational knowledge (people, policies, teams) and project management data (projects, tasks, assignments). This unified approach eliminates data silos and enables powerful cross-domain queries.

## Core Design Principles

1. **Everything is a Node** - All entities are first-class graph nodes
2. **Relationships are Meaningful** - Named relationships carry semantics
3. **Properties are Queryable** - Indexed properties for fast lookups
4. **No External State** - The graph is the single source of truth

## Node Types

### Organizational Nodes

#### Person
Represents an individual in the organization.

```cypher
(:Person {
  id: String!           // Unique identifier (UUID)
  name: String!         // Full name
  email: String!        // Email address (unique)
  role: String          // Job title
  department: String    // Department name
  location: String      // Office location
  availability: Integer // Hours available per week (e.g., 40)
  created_at: DateTime  // When added to system
  updated_at: DateTime  // Last modification
  active: Boolean       // Currently employed
  skills: [String]      // Array of skill tags (being migrated to relationships)
})
```

#### Team
Represents a departmental or functional team.

```cypher
(:Team {
  id: String!          // Unique identifier
  name: String!        // Team name
  type: String         // 'department' | 'functional' | 'project'
  purpose: String      // Team's mission
  created_at: DateTime
  active: Boolean
})
```

#### Group
Cross-functional groups (committees, working groups, etc).

```cypher
(:Group {
  id: String!          // Unique identifier
  name: String!        // Group name
  type: String         // 'governance' | 'technical' | 'operational'
  charter: String      // Group's charter/purpose
  formed_date: DateTime
  active: Boolean
})
```

#### Policy
Organizational policies and procedures.

```cypher
(:Policy {
  id: String!             // Unique identifier
  name: String!           // Policy name
  category: String        // 'security' | 'hr' | 'compliance' | 'operational'
  description: String     // Full description
  requirements: [String]  // List of requirements
  severity: String        // 'critical' | 'high' | 'medium' | 'low'
  effective_date: DateTime
  review_date: DateTime
  compliance_frameworks: [String] // ['SOC2', 'HIPAA', 'GDPR']
})
```

### Project Management Nodes

#### Project
High-level project or initiative.

```cypher
(:Project {
  id: String!           // Unique identifier
  name: String!         // Project name
  description: String   // Full description
  status: String        // 'planning' | 'active' | 'completed' | 'cancelled'
  priority: String      // 'critical' | 'high' | 'medium' | 'low'
  start_date: DateTime
  target_date: DateTime
  actual_end_date: DateTime?
  estimated_hours: Integer
  actual_hours: Integer?
  budget: Float?
  tags: [String]        // ['frontend', 'backend', 'infrastructure']
})
```

#### Task
Actionable work items within projects.

```cypher
(:Task {
  id: String!             // Unique identifier
  title: String!          // Task title
  description: String     // Full description
  status: String          // 'pending' | 'assigned' | 'in_progress' | 'blocked' | 'completed'
  priority: String        // 'critical' | 'high' | 'medium' | 'low'
  estimated_hours: Integer
  actual_hours: Integer?
  created_at: DateTime
  updated_at: DateTime
  due_date: DateTime?
  completed_at: DateTime?
  blocked_at: DateTime?
  unblocked_at: DateTime?
  acceptance_criteria: [String]
  required_skills: [String] // Being migrated to REQUIRES relationships
})
```

#### Skill
Skills and competencies (moving from properties to nodes).

```cypher
(:Skill {
  id: String!          // Unique identifier
  name: String!        // Skill name (unique)
  category: String     // 'technical' | 'domain' | 'soft'
  description: String
  related_tools: [String]
})
```

#### Sprint (Optional)
For teams using sprint-based planning.

```cypher
(:Sprint {
  id: String!          // Unique identifier
  name: String!        // Sprint name
  start_date: DateTime
  end_date: DateTime
  goal: String
  status: String       // 'planning' | 'active' | 'completed'
})
```

## Relationship Types

### Organizational Relationships

#### MEMBER_OF
Person belongs to a Team.
```cypher
(p:Person)-[:MEMBER_OF {
  role: String?         // Role within team
  since: DateTime
  primary: Boolean      // Primary team assignment
}]->(t:Team)
```

#### REPORTS_TO
Reporting hierarchy.
```cypher
(p1:Person)-[:REPORTS_TO {
  since: DateTime
  dotted_line: Boolean  // False for direct reports
}]->(p2:Person)
```

#### RESPONSIBLE_FOR
Ownership of policies and projects.
```cypher
// Person owns policy
(p:Person)-[:RESPONSIBLE_FOR {
  role: String          // 'owner' | 'approver' | 'reviewer'
  since: DateTime
}]->(pol:Policy)

// Team owns policy
(t:Team)-[:RESPONSIBLE_FOR]->(pol:Policy)
```

#### COLLABORATES_WITH
Working relationships.
```cypher
(p1:Person)-[:COLLABORATES_WITH {
  frequency: String     // 'daily' | 'weekly' | 'monthly'
  last_interaction: DateTime
  strength: Float       // 0.0 to 1.0
}]->(p2:Person)
```

### Project Management Relationships

#### BELONGS_TO
Task belongs to Project.
```cypher
(t:Task)-[:BELONGS_TO]->(p:Project)
```

#### ASSIGNED_TO
Person assigned to Task.
```cypher
(p:Person)-[:ASSIGNED_TO {
  assigned_at: DateTime
  assigned_by: String   // Person ID who made assignment
  confidence: Float     // Assignment confidence score
  reason: String        // Why this person was chosen
  status: String        // 'active' | 'completed' | 'declined'
}]->(t:Task)
```

#### DEPENDS_ON
Task dependencies.
```cypher
(t1:Task)-[:DEPENDS_ON {
  type: String          // 'blocks' | 'informs'
  created_at: DateTime
}]->(t2:Task)
```

#### HAS_SKILL
Person possesses skill.
```cypher
(p:Person)-[:HAS_SKILL {
  level: String         // 'beginner' | 'intermediate' | 'expert'
  years_experience: Integer
  last_used: DateTime
  verified: Boolean
}]->(s:Skill)
```

#### REQUIRES
Task requires skill.
```cypher
(t:Task)-[:REQUIRES {
  level: String         // Minimum level required
  critical: Boolean     // Is this skill critical?
}]->(s:Skill)
```

#### WANTS_TO_LEARN
Learning goals.
```cypher
(p:Person)-[:WANTS_TO_LEARN {
  priority: String      // 'high' | 'medium' | 'low'
  target_date: DateTime?
}]->(s:Skill)
```

#### SIMILAR_TO
Skill relationships.
```cypher
(s1:Skill)-[:SIMILAR_TO {
  similarity: Float     // 0.0 to 1.0
  reason: String        // Why they're similar
}]->(s2:Skill)
```

### Additional Relationships

#### CHILD_OF
Hierarchical relationships.
```cypher
// Sub-teams
(t1:Team)-[:CHILD_OF]->(t2:Team)

// Sub-tasks
(t1:Task)-[:CHILD_OF]->(t2:Task)

// Skill hierarchy
(s1:Skill)-[:CHILD_OF]->(s2:Skill)
```

#### CREATED_BY
Audit trail.
```cypher
(proj:Project)-[:CREATED_BY {
  created_at: DateTime
}]->(p:Person)

(task:Task)-[:CREATED_BY]->(p:Person)
```

## Indexes and Constraints

### Unique Constraints
```cypher
CREATE CONSTRAINT person_email_unique ON (p:Person) ASSERT p.email IS UNIQUE;
CREATE CONSTRAINT skill_name_unique ON (s:Skill) ASSERT s.name IS UNIQUE;
CREATE CONSTRAINT team_name_unique ON (t:Team) ASSERT t.name IS UNIQUE;
```

### Indexes for Performance
```cypher
CREATE INDEX person_name FOR (p:Person) ON (p.name);
CREATE INDEX person_availability FOR (p:Person) ON (p.availability);
CREATE INDEX task_status FOR (t:Task) ON (t.status);
CREATE INDEX task_priority FOR (t:Task) ON (t.priority);
CREATE INDEX project_status FOR (p:Project) ON (p.status);
CREATE INDEX skill_category FOR (s:Skill) ON (s.category);
```

### Composite Indexes
```cypher
CREATE INDEX task_status_priority FOR (t:Task) ON (t.status, t.priority);
CREATE INDEX person_dept_role FOR (p:Person) ON (p.department, p.role);
```

## Common Query Patterns

### 1. Find Available People with Skills
```cypher
MATCH (t:Task {id: $taskId})-[:REQUIRES]->(s:Skill)
MATCH (p:Person)-[:HAS_SKILL]->(s)
WHERE p.availability > 0
RETURN p, COUNT(s) as skillMatches
ORDER BY skillMatches DESC, p.availability DESC
```

### 2. Project Status Overview
```cypher
MATCH (proj:Project {id: $projectId})
MATCH (proj)<-[:BELONGS_TO]-(t:Task)
WITH proj, 
     COUNT(t) as totalTasks,
     COUNT(CASE WHEN t.status = 'completed' THEN 1 END) as completed
RETURN proj.name, 
       totalTasks, 
       completed,
       completed * 100.0 / totalTasks as percentComplete
```

### 3. Find Bottlenecks
```cypher
// Overloaded people
MATCH (p:Person)-[:ASSIGNED_TO]->(t:Task {status: 'active'})
WITH p, SUM(t.estimated_hours) as committed
WHERE committed > p.availability
RETURN p.name, p.availability, committed, committed - p.availability as overload

// Blocked tasks on critical path
MATCH (t:Task {status: 'blocked'})-[:DEPENDS_ON*]->(critical:Task)
WHERE EXISTS((critical)<-[:DEPENDS_ON*]-(:Task {status: 'pending'}))
RETURN t, COUNT(critical) as blockingCount
ORDER BY blockingCount DESC
```

### 4. Team Skill Coverage
```cypher
MATCH (team:Team {id: $teamId})<-[:MEMBER_OF]-(p:Person)-[:HAS_SKILL]->(s:Skill)
RETURN s.name, 
       s.category,
       COUNT(p) as peopleWithSkill,
       COLLECT(p.name) as people
ORDER BY s.category, peopleWithSkill DESC
```

### 5. Policy Compliance Check
```cypher
MATCH (pol:Policy {category: 'compliance'})
OPTIONAL MATCH (pol)<-[:RESPONSIBLE_FOR]-(owner)
RETURN pol.name, 
       pol.severity,
       pol.compliance_frameworks,
       owner.name as owner,
       pol.review_date < date() as needsReview
ORDER BY pol.severity DESC
```

## Migration from Array Properties

### Current State (Arrays)
```cypher
(:Person {skills: ['JavaScript', 'React', 'Node.js']})
(:Task {required_skills: ['JavaScript', 'React']})
```

### Target State (Relationships)
```cypher
(:Person)-[:HAS_SKILL]->(:Skill {name: 'JavaScript'})
(:Person)-[:HAS_SKILL]->(:Skill {name: 'React'})
(:Task)-[:REQUIRES]->(:Skill {name: 'JavaScript'})
```

### Migration Script
```cypher
// Create Skill nodes from Person skills
MATCH (p:Person)
UNWIND p.skills as skillName
MERGE (s:Skill {name: skillName})
MERGE (p)-[:HAS_SKILL]->(s)

// Create relationships from Task requirements
MATCH (t:Task)
UNWIND t.required_skills as skillName
MERGE (s:Skill {name: skillName})
MERGE (t)-[:REQUIRES]->(s)

// Later: Remove array properties
MATCH (p:Person)
REMOVE p.skills

MATCH (t:Task)
REMOVE t.required_skills
```

## Best Practices

### 1. Node Creation
Always include:
- Unique ID (UUID)
- Created/Updated timestamps
- Status/Active flags

### 2. Relationship Creation
Always include:
- Timestamp (when applicable)
- Creator/Source (for audit)
- Confidence/Strength scores (when applicable)

### 3. Query Optimization
- Use parameters instead of string concatenation
- Limit result sets with LIMIT
- Use indexes for frequently filtered properties
- Profile queries with EXPLAIN/PROFILE

### 4. Data Integrity
- Use constraints for unique values
- Validate data before insertion
- Use transactions for multi-step operations
- Regular consistency checks

## Schema Evolution

### Adding New Node Types
1. Define node structure
2. Create indexes/constraints
3. Update documentation
4. Emit schema.updated event

### Adding New Relationships
1. Define relationship properties
2. Consider bidirectional needs
3. Update affected queries
4. Test performance impact

### Deprecating Properties
1. Add new structure in parallel
2. Migrate data gradually
3. Update all queries
4. Remove old structure

## Summary

This unified graph schema provides:

1. **Single Source of Truth** - All data in one place
2. **Powerful Queries** - Complex relationships made simple
3. **Flexibility** - Easy to add new node types and relationships
4. **Performance** - Optimized with proper indexes
5. **Maintainability** - Clear structure and naming conventions

The graph-first approach eliminates the need for complex synchronization between different data stores and enables queries that would be impossible with traditional relational databases.