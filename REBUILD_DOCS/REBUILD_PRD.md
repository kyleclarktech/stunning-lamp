# Enterprise Knowledge Graph & PM Assistant System - Build PRD
## Product Requirements Document v2.2

### Executive Summary

This PRD outlines the build of a comprehensive system that combines an Enterprise Knowledge Graph with an interactive, state-aware Project Management Assistant. The system is designed as a Proof of Concept (PoC) to validate the architecture and core functionality. It enables natural language queries against organizational data and assists Project Managers by allowing them to "chat with their projects" to create new, non-redundant tasks. It leverages Neo4j as the core graph database.

### Core Value Proposition

**Dual Purpose System**:
1. **Knowledge Graph**: Enable employees to quickly find the right people, policies, and processes through natural language queries.
2. **Interactive PM Assistant**: Provide a state-aware tool for Project Managers to interact with project data, understand the current state of work, and create new tasks without introducing redundancy.

**Key Differentiators**:
- Unified organizational intelligence platform.
- **Agent-First Architecture**: Designed primarily for agentic coding assistants, with a secondary human-friendly API.
- **State-Aware Task Creation**: Reads from the graph to ensure new tasks are relevant to the project's current state.
- Self-documenting codebase via agent-maintained touchpoints.

---

## Architecture Principles

### 1. Modular Design
Each module is a self-contained unit with clear API boundaries, its own documentation, and independent tests.

### 2. Agent-First Development
The primary interface is designed for programmatic use by AI agents, with machine-readable manifests and context-aware loading. A human-friendly gateway serves as a secondary interface.

### 3. Proof of Concept Focus
This build prioritizes functional correctness and architectural validation over production-grade performance and scalability. The schema and components are designed to prove the concept.

### 4. Graph-First Design
All data is stored in the Neo4j graph database, making it the single source of truth and enabling unified queries.

---

## System Architecture

### Database Choice: Neo4j

**Why Neo4j over FalkorDB:**
- Better representation in AI training data and more mature tooling.
- Standard Cypher query language and strong community support.
- Native graph database, ideal for the PoC's focus on relationships.

### Core Modules (Expanded to 6)

#### 1. Query Engine (`@query-engine`)
**Purpose**: Convert natural language to graph queries.
**Components**: NL Parser, Intent Classifier, Cypher Generator.

#### 2. Graph Executor (`@graph-executor`)
**Purpose**: Execute Cypher queries against Neo4j.
**Components**: Connection Pool, Query Executor, Transaction Handler.

#### 3. PM Assistant (`@pm-assistant`)
**Purpose**: Interactive, state-aware project management assistance.
**Key Features**:
- Reads existing project data from the graph to understand context.
- Interacts with a PM to define and create new tasks.
- **Analyzes new task requests to prevent duplication and suggests modifications or consolidation with existing work items.**
- **Is not an autonomous agent.**

#### 4. Response Formatter (`@response-formatter`)
**Purpose**: Format query results for different consumers (JSON, Markdown, etc.).

#### 5. Context Manager (`@context-manager`)
**Purpose**: Smart context loading with touchpoints and model-aware sizing.

#### 6. API Gateway (`@api-gateway`)
**Purpose**: Provide a stable, human-friendly REST API.
**Key Features**:
- Exposes core functionalities of other modules.
- Provides endpoints for UI clients and external integrations.
- Handles authentication and rate limiting (future).

The following modules have been merged or redefined:

- **Schema Registry** → Part of Graph Executor for the PoC.
- **Response Orchestrator** → Merged with Response Formatter.

---

## Unified Graph Schema

All entities stored in Neo4j:

```cypher
// Knowledge Graph Entities
(p:Person {id, name, email, role, department, skills: []})
(t:Team {id, name, purpose})
(g:Group {id, name, type})
(pol:Policy {id, name, category, severity})

// PM Entities (in same graph)
(proj:Project {id, name, status, deadline})
(task:Task {id, title, estimated_hours, status})
(s:Sprint {id, start_date, end_date})

// Relationships connect everything
(p)-[:MEMBER_OF]->(t)
(p)-[:ASSIGNED_TO]->(task)
(task)-[:BELONGS_TO]->(proj)
(task)-[:DEPENDS_ON]->(task2)
(p)-[:HAS_SKILL]->(skill)
```

## AI-Agent Friendly Features

### 1. Machine-Readable Indexing

**Module Index** (`/modules/index.json`):
```json
{
  "modules": {
    "@graph-engine": {
      "path": "./graph-engine",
      "load_priority": 1,
      "context_keywords": ["query", "search", "find"]
    },
    "@schema-registry": {
      "path": "./schema-registry",
      "load_priority": 0,
      "always_loaded": true
    }
  }
}
```

**Capability Discovery**:
```typescript
interface ModuleCapability {
  id: string;
  description: string;
  input_schema: JSONSchema;
  output_schema: JSONSchema;
  examples: Example[];
  performance_hints: PerformanceHint[];
}
```

### 2. Dynamic Context Loading

**Model-Aware Sizing**:
```typescript
interface ContextManager {
  getMaxContext(model: string): number {
    const limits = {
      'gpt-4': 128_000,
      'gpt-3.5': 16_000,
      'claude-3': 200_000,
      'claude-2': 100_000,
      'local-llm': 32_000
    };
    return limits[model] * 0.5; // Use 50% for safety margin
  }
  
  async loadContext(query: string, model: string): Promise<Context> {
    const maxSize = this.getMaxContext(model);
    return this.progressiveLoad(query, maxSize);
  }
}
```

### 3. Auto-Maintained Touchpoints

**Claude Code Integration**:
```typescript
// @touchpoint query-parser
// @concepts [natural-language, parsing]
// Auto-extracted by Claude Code when files change
export class QueryParser {
  parse(query: string): QueryIntent {
    // Implementation
  }
}
```

**CLAUDE.md Rules**:
- Update touchpoint comments when modifying functions
- Run `npm run update-touchpoints` after changes
- Git pre-commit hook validates references

**Code Annotations**:
```typescript
/**
 * @module @graph-engine
 * @capability natural-language-to-cypher
 * @performance O(n) where n is query length
 * @context-required @schema-registry/entities
 */
export class QueryParser {
  // ...
}
```

---

## Event-Driven Synchronization

```typescript
// All changes emit events for synchronization
interface SystemEvent {
  type: 'entity.created' | 'task.assigned' | 'touchpoint.updated';
  timestamp: Date;
  payload: any;
  source: string;
}

// Claude Code listens and updates
on('code.modified', async (file) => {
  await extractAndUpdateTouchpoints(file);
  await updateGraphSchema(file);
});
```

## Data Model (Stored in Graph)

```typescript
// @schema-registry/entities/person.ts
interface Person {
  id: string;
  name: string;
  email: string;
  role: string;
  department: string;
  skills: string[];
  location: Location;
  reports_to?: string; // Person.id
}

// @schema-registry/entities/policy.ts
interface Policy {
  id: string;
  name: string;
  category: PolicyCategory;
  description: string;
  requirements: Requirement[];
  owner: EntityReference; // Person | Team | Group
  compliance_frameworks: string[];
}

// @schema-registry/entities/project.ts
interface Project {
  id: string;
  name: string;
  description: string;
  status: ProjectStatus;
  priority: Priority;
  start_date: Date;
  target_date: Date;
  actual_end_date?: Date;
  created_by: string; // Person.id
  project_lead?: string; // Person.id
  stakeholders: string[]; // Person.id[]
  tags: string[];
  estimated_effort: number; // hours
  actual_effort?: number;
}

// @schema-registry/entities/task.ts
interface Task {
  id: string;
  project_id: string;
  parent_task_id?: string; // For subtasks
  title: string;
  description: string;
  status: TaskStatus;
  priority: Priority;
  estimated_hours: number;
  actual_hours?: number;
  assigned_to?: string; // Person.id
  created_by: string; // Person.id
  created_at: Date;
  updated_at: Date;
  due_date?: Date;
  completed_at?: Date;
  required_skills: string[];
  difficulty_level: DifficultyLevel;
  dependencies: string[]; // Task.id[]
  acceptance_criteria: string[];
  comments: Comment[];
}

// @schema-registry/entities/assignment.ts
interface Assignment {
  id: string;
  task_id: string;
  person_id: string;
  assigned_at: Date;
  assigned_by: string; // Person.id
  status: AssignmentStatus;
  confidence_score: number; // 0-1, skill match confidence
  availability_score: number; // 0-1, bandwidth availability
  reason: string; // Why this person was assigned
  alternatives: AlternativeAssignment[]; // Other considered options
}

// @schema-registry/entities/skill-profile.ts
interface SkillProfile {
  person_id: string;
  skills: SkillEntry[];
  learning_goals: string[];
  certifications: Certification[];
  experience_summary: string;
  availability: AvailabilityWindow[];
  preferences: WorkPreferences;
}

interface SkillEntry {
  skill_id: string;
  proficiency: ProficiencyLevel;
  years_experience: number;
  last_used: Date;
  projects_count: number;
  peer_endorsements: number;
}

// @schema-registry/entities/bandwidth.ts
interface BandwidthRecord {
  person_id: string;
  week_starting: Date;
  allocated_hours: number;
  available_hours: number;
  planned_pto: number;
  task_commitments: TaskCommitment[];
  utilization_rate: number; // allocated/available
}

interface TaskCommitment {
  task_id: string;
  hours_per_week: number;
  confidence: number; // How certain we are about this estimate
}
```

### Semantic Mappings

```typescript
// @schema-registry/mappings/role-categories.ts
export const RoleMappings = {
  "developers": {
    includes: ["Engineer", "Developer", "Programmer"],
    excludes: ["Manager", "Director"],
    context: "technical-roles"
  },
  "managers": {
    includes: ["Manager", "Lead", "Director", "VP"],
    context: "leadership-roles"
  }
};
```

---

## Query Processing Pipeline

### 1. Query Reception
```typescript
interface QueryRequest {
  id: string;
  query: string;
  context?: QueryContext;
  user?: UserContext;
  options?: QueryOptions;
}
```

### 2. Intent Classification
```typescript
enum QueryIntent {
  // Original intents
  FIND_PERSON = "find_person",
  FIND_POLICY = "find_policy",
  COUNT_ENTITIES = "count_entities",
  ANALYZE_STRUCTURE = "analyze_structure",
  TASK_ASSISTANCE = "task_assistance",
  
  // PM-specific intents
  CREATE_PROJECT_PLAN = "create_project_plan",
  BREAK_DOWN_TASK = "break_down_task",
  FIND_AVAILABLE_PERSON = "find_available_person",
  ASSIGN_TASK = "assign_task",
  CHECK_PROGRESS = "check_progress",
  IDENTIFY_BOTTLENECK = "identify_bottleneck",
  ESTIMATE_TIMELINE = "estimate_timeline",
  BALANCE_WORKLOAD = "balance_workload",
  FIND_SKILL_MATCH = "find_skill_match",
  SCHEDULE_REVIEW = "schedule_review"
}
```

### 3. Query Generation
```typescript
interface QueryPlan {
  intent: QueryIntent;
  primary_query: CypherQuery;
  fallback_queries?: CypherQuery[];
  required_context: string[];
  estimated_cost: number;
}
```

### 4. Execution & Response
```typescript
interface QueryResponse {
  id: string;
  request_id: string;
  results: any[];
  metadata: {
    execution_time: number;
    modules_used: string[];
    context_loaded: string[];
  };
  suggestions?: QuerySuggestion[];
}
```

---

## Module Development Guidelines

### 1. Module Structure
```
/modules/[module-name]/
  ├── manifest.json          # Module metadata
  ├── index.ts              # Main entry point
  ├── README.md             # Human documentation
  ├── schema/               # Input/output schemas
  ├── tests/                # Module tests
  ├── examples/             # Usage examples
  └── benchmarks/           # Performance tests
```

### 2. Module Interface
```typescript
export interface Module {
  id: string;
  version: string;
  
  // Lifecycle
  initialize(config: ModuleConfig): Promise<void>;
  shutdown(): Promise<void>;
  
  // Capabilities
  getCapabilities(): Capability[];
  canHandle(request: Request): boolean;
  
  // Execution
  execute(request: Request): Promise<Response>;
  
  // Introspection
  getMetrics(): Metrics;
  getHealth(): HealthStatus;
}
```

### 3. Context Awareness
```typescript
export interface ContextAwareModule extends Module {
  // Declare what context this module needs
  getRequiredContext(): ContextRequirement[];
  
  // Declare what context this module provides
  getProvidedContext(): ContextProvision[];
  
  // Handle partial context gracefully
  executeWithContext(
    request: Request, 
    context: PartialContext
  ): Promise<Response>;
}
```

---

## Testing Strategy

### 1. Module Testing
Standard unit and integration tests will be applied to all modules to ensure functional correctness.

```typescript
// Each module includes test manifests
{
  "test_suites": {
    "unit": {
      "pattern": "**/*.test.ts",
      "required_coverage": 80
    },
    "integration": {
      "pattern": "**/*.integration.ts",
      "requires": ["@test-database"]
    }
  }
}
```

### 2. LLM Component Validation
For non-deterministic components like the `@pm-assistant`, a specific validation strategy will be used during development.

- **Schema Adherence**: The primary check is to ensure the LLM's JSON output strictly conforms to the defined response schemas (e.g., `TaskDraft`).
- **Agent-Assisted Semantic Review**: During development, the engineer will use their agentic pair programmer as a "semantic judge." The engineer will prompt the agent with the user request and the module's output and ask it to validate if the output logically and contextually satisfies the request. This formalizes the human-in-the-loop validation process.

---

## User Interaction Model & Configuration

### 1. Primary Client: Command-Line Interface (CLI)
For the PoC, the primary user interface will be a CLI. This client will be responsible for:
- Taking user input.
- Calling the `@api-gateway`.
- Displaying the formatted results.
- **Managing Conversational State**: The CLI will be responsible for managing conversation history. To accommodate local models with smaller context windows, the CLI will provide a mechanism for the user to control how much history is sent with each request (e.g., the last 3 turns, the last 5 turns, etc.).

### 2. Configuration Management
All module and system configuration will be managed via a single `.env` file at the project root. This file will contain database credentials, API ports, and other environment-specific variables. It will be excluded from version control.

---

## Implementation Phases

### Phase 1: Core Infrastructure (Weeks 1-2)
- [ ] Module system architecture
- [ ] Context manager foundation
- [ ] Basic schema registry
- [ ] Testing framework

### Phase 2: Query Engine (Weeks 3-4)
- [ ] Natural language parser
- [ ] Cypher generator (single database support)
- [ ] Basic query executor
- [ ] Result formatter

### Phase 3: Smart Features (Weeks 5-6)
- [ ] Semantic mappings
- [ ] Query optimization
- [ ] Fallback strategies
- [ ] Performance monitoring

### Phase 4: AI Integration (Weeks 7-8)
- [ ] AI-agent testing suite
- [ ] Context optimization
- [ ] Self-documentation generation
- [ ] Module discovery API

---

## Success Metrics

### Technical Metrics
- Query response time: p95 < 2s
- Context load time: < 100ms (dynamic per model)
- Neo4j query performance: < 500ms p95
- Test coverage: > 90%

### Business Metrics
- Query success rate: > 95%
- Task assignment accuracy: > 90%
- Time to find information: 80% reduction
- PM automation satisfaction: > 4.5/5

---

## Appendix: Lessons Learned

### From Development Phase
- **Database Choice**: FalkorDB syntax differences caused friction
- **Complexity Growth**: System expanded beyond initial scope
- **Module Proliferation**: Too many small modules increased complexity
- **Fixed Context Sizes**: Not adaptable to different models

### Applied to This Build
1. Neo4j chosen for better AI training representation
2. Simplified to 5 core modules with clear boundaries
3. Graph-first design stores everything in one place
4. Dynamic context sizing based on model capabilities
5. Auto-maintained touchpoints via Claude Code integration

---

## Document Metadata

```json
{
  "document_type": "product_requirements",
  "version": "2.0.0",
  "status": "draft",
  "ai_agent_compatible": true,
  "indexable_sections": [
    "system-architecture",
    "module-specifications",
    "data-model",
    "query-pipeline"
  ],
  "context_keywords": [
    "knowledge-graph",
    "natural-language",
    "modular-architecture",
    "ai-agent-friendly"
  ]
}
```