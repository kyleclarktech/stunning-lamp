# Module Boundaries and Interface Specification

## Overview

This document defines clear boundaries between the 5 core modules, their interfaces, and communication patterns. The system has been simplified from the original design to reduce complexity while maintaining all functionality through a graph-first approach where ALL data (knowledge and PM) lives in Neo4j.

## Module Design Principles

### 1. Single Responsibility
Each module has one clear purpose and owns its domain completely.

### 2. Explicit Dependencies
All dependencies are declared in module manifests with version constraints.

### 3. Interface Stability
Public interfaces are versioned and backward compatible within major versions.

### 4. Data Encapsulation
Modules own their data and expose it only through defined interfaces.

### 5. Async-First
All module interfaces are asynchronous to support streaming and lazy loading.

## Core Module Definitions (5 Total)

### 1. Query Engine Module (`@query-engine`)

**Purpose**: Convert natural language to Cypher queries for both knowledge and PM operations

**Boundaries**:
- Owns: NL parsing, intent classification, Cypher generation, query optimization
- Does NOT own: Query execution, data storage, result formatting

**Public Interface**:
```typescript
// @query-engine/types.ts
export interface QueryEngineModule extends BaseModule {
  // Convert natural language to Cypher
  generateCypher(query: string, intent?: QueryIntent): Promise<CypherQuery>;
  
  // Classify query intent (knowledge vs PM)
  classifyIntent(query: string): Promise<QueryIntent>;
  
  // Optimize generated queries
  optimizeQuery(cypher: CypherQuery): Promise<CypherQuery>;
  
  // Validate Cypher syntax
  validateCypher(cypher: string): ValidationResult;
}

export interface QueryRequest {
  id: string;
  query: string;
  user?: UserContext;
  options?: QueryOptions;
}

export interface QueryResponse {
  id: string;
  status: 'success' | 'partial' | 'error';
  results?: any[];
  error?: ErrorInfo;
  metadata: QueryMetadata;
}
```

**Module Contract**:
```yaml
module: "@query-engine"
version: "2.0.0"
stability: "stable"

provides:
  - capability: "natural-language-to-cypher"
    interface: "QueryEngineModule"
    sla:
      latency_p95: 50ms
      availability: 99.9%

requires:
  - "@context-manager": "^2.0.0"  # For touchpoint context

events:
  emits:
    - "query.parsed"
    - "cypher.generated"
    - "intent.classified"
  
  subscribes:
    - "schema.updated"  # Graph schema changes
    - "touchpoint.added"
```

### 2. Graph Executor Module (`@graph-executor`)

**Purpose**: Execute Cypher queries against Neo4j and manage connections

**Boundaries**:
- Owns: Database connections, query execution, transactions, result streaming
- Does NOT own: Query generation, natural language parsing, result formatting

**Public Interface**:
```typescript
// @graph-executor/types.ts
export interface GraphExecutorModule extends BaseModule {
  // Execute single query
  execute(query: CypherQuery): Promise<QueryResult>;
  
  // Execute transaction
  executeTransaction(queries: CypherQuery[]): Promise<TransactionResult>;
  
  // Stream large results
  stream(query: CypherQuery): AsyncIterator<ResultChunk>;
  
  // Get query execution plan
  explain(query: CypherQuery): Promise<ExecutionPlan>;
}

export interface CypherQuery {
  statement: string;
  parameters: Record<string, any>;
  timeout?: number;
  database?: string;
}

export interface QueryResult {
  records: any[];
  summary: QuerySummary;
  metadata: QueryMetadata;
}
```

**Module Contract**:
```yaml
module: "@graph-executor"
version: "2.0.0"

provides:
  - capability: "neo4j-execution"
    interface: "GraphExecutorModule"
    sla:
      query_timeout: 30s
      connection_pool: 50

requires:
  - "neo4j-driver": "^5.0.0"

events:
  emits:
    - "query.executed"
    - "connection.created"
    - "transaction.completed"
```

### 3. PM Assistant Module (`@pm-assistant`)

**Purpose**: All project management logic using graph queries

**Boundaries**:
- Owns: Project planning, task assignment, progress tracking, bottleneck detection
- Does NOT own: Direct database access, query generation, UI formatting

**Public Interface**:
```typescript
// @pm-assistant/types.ts
export interface PMAssistantModule extends BaseModule {
  // Project management operations
  createProject(description: string): Promise<Project>;
  breakdownProject(projectId: string): Promise<Task[]>;
  assignTask(taskId: string, criteria?: AssignmentCriteria): Promise<Assignment>;
  
  // Progress tracking
  getProjectStatus(projectId: string): Promise<ProjectStatus>;
  detectBottlenecks(projectId: string): Promise<Bottleneck[]>;
  
  // Team insights
  findAvailableResources(skills: string[], timeframe: DateRange): Promise<Person[]>;
  suggestTeamFormation(projectRequirements: Requirements): Promise<Team>;
}

// All PM operations work through graph queries
export interface PMOperation {
  description: string;
  cypherQueries: CypherQuery[];  // Queries to execute
  resultProcessor: (results: QueryResult[]) => any;
}
```

**Module Contract**:
```yaml
module: "@pm-assistant"
version: "2.0.0"

provides:
  - capability: "project-management"
    interface: "PMAssistantModule"

requires:
  - "@query-engine": "^2.0.0"  # Generate queries
  - "@graph-executor": "^2.0.0"  # Execute queries

events:
  emits:
    - "project.created"
    - "task.assigned"
    - "bottleneck.detected"
```

### 4. Response Formatter Module (`@response-formatter`)

**Purpose**: Format query results for different consumers

**Boundaries**:
- Owns: Output formatting, template rendering, localization, pagination
- Does NOT own: Query execution, data transformation logic, caching

**Public Interface**:
```typescript
// @response-formatter/types.ts
export interface ResponseFormatterModule extends BaseModule {
  // Format results based on options
  format(results: QueryResult, options: FormatOptions): Promise<FormattedResponse>;
  
  // Register custom formatter
  registerFormatter(type: string, formatter: Formatter): void;
  
  // Stream formatted results
  streamFormat(results: AsyncIterator<any>, options: FormatOptions): AsyncIterator<string>;
  
  // Get available formats
  getAvailableFormats(): string[];
}

export interface FormatOptions {
  format: 'json' | 'table' | 'markdown' | 'csv' | 'html';
  locale?: string;
  template?: string;
  pagination?: PaginationOptions;
  includeMetadata?: boolean;
}
```

**Module Contract**:
```yaml
module: "@response-formatter"
version: "2.0.0"

provides:
  - capability: "result-formatting"
    interface: "ResponseFormatterModule"

requires: []  # No dependencies, pure formatting

events:
  emits:
    - "format.completed"
    - "format.failed"
```

### 5. Context Manager Module (`@context-manager`)

**Purpose**: Smart context loading with touchpoints and model awareness

**Boundaries**:
- Owns: Context loading, touchpoint management, caching, model-specific sizing
- Does NOT own: Query processing, database access, result formatting

**Public Interface**:
```typescript
// @context-manager/types.ts
export interface ContextManagerModule extends BaseModule {
  // Load context for query with model awareness
  loadContext(query: string, model: string): Promise<Context>;
  
  // Manage touchpoints
  addTouchpoint(touchpoint: Touchpoint): Promise<void>;
  updateTouchpoints(file: string): Promise<Touchpoint[]>;
  
  // Get model-specific limits
  getMaxContextSize(model: string): number;
  
  // Search touchpoints
  searchTouchpoints(query: string): Promise<Touchpoint[]>;
}

export interface Context {
  touchpoints: Touchpoint[];
  size: number;
  relevanceScore: number;
  model: string;
}
```

**Module Contract**:
```yaml
module: "@context-manager"
version: "2.0.0"

provides:
  - capability: "context-management"
    interface: "ContextManagerModule"

requires: []  # Self-contained

events:
  emits:
    - "context.loaded"
    - "touchpoint.updated"
  subscribes:
    - "code.modified"  # Auto-update touchpoints
```

## Simplified Communication Patterns

### 1. Query Pipeline Flow

Main flow through the 5 modules:

```typescript
// User Query → Query Engine → Graph Executor → Response Formatter
class QueryPipeline {
  constructor(
    private queryEngine: QueryEngineModule,
    private graphExecutor: GraphExecutorModule,
    private pmAssistant: PMAssistantModule,
    private formatter: ResponseFormatterModule,
    private contextManager: ContextManagerModule
  ) {}
  
  async processQuery(userQuery: string, model: string): Promise<FormattedResponse> {
    // Load context based on model
    const context = await this.contextManager.loadContext(userQuery, model);
    
    // Generate Cypher
    const intent = await this.queryEngine.classifyIntent(userQuery);
    const cypher = await this.queryEngine.generateCypher(userQuery, intent);
    
    // Route PM queries through PM Assistant
    if (intent.type.startsWith('pm.')) {
      return this.pmAssistant.handleQuery(userQuery, cypher);
    }
    
    // Execute query
    const results = await this.graphExecutor.execute(cypher);
    
    // Format response
    return this.formatter.format(results, { format: 'json' });
  }
}
```

### 2. Event-Based Synchronization

All modules emit events for system-wide coordination:

```typescript
// Event bus for touchpoint and schema synchronization
class SystemEventBus {
  async emit(event: SystemEvent): Promise<void> {
    // All interested modules receive the event
    switch (event.type) {
      case 'code.modified':
        await this.contextManager.updateTouchpoints(event.payload.file);
        break;
      case 'schema.updated':
        await this.queryEngine.refreshSchema();
        break;
      case 'task.assigned':
        await this.notifyRelevantModules(event);
        break;
    }
  }
}
```

### 3. Graph-First Data Access

All data operations go through the graph:

```typescript
// PM Assistant uses graph queries, not separate data store
class PMAssistant implements PMAssistantModule {
  async assignTask(taskId: string): Promise<Assignment> {
    // Generate Cypher to find best assignee
    const cypher = `
      MATCH (t:Task {id: $taskId})
      MATCH (p:Person)-[:HAS_SKILL]->(s:Skill)
      WHERE s.name IN t.required_skills
      AND NOT EXISTS((p)-[:ASSIGNED_TO]->(:Task {status: 'active'}))
      RETURN p ORDER BY p.availability DESC LIMIT 1
    `;
    
    const result = await this.graphExecutor.execute({
      statement: cypher,
      parameters: { taskId }
    });
    
    // Create assignment in graph
    return this.createAssignment(taskId, result.records[0].p.id);
  }
}
```

## Simplified Dependency Graph

```mermaid
graph TD
    QE[Query Engine] --> CM[Context Manager]
    PA[PM Assistant] --> QE
    PA --> GE[Graph Executor]
    GE --> Neo4j[(Neo4j Database)]
    RF[Response Formatter] --> None
    CM --> None
```

### Module Dependencies

```yaml
# Minimal dependencies between modules
@query-engine:
  requires: [@context-manager]
  
@graph-executor:
  requires: [neo4j-driver]
  
@pm-assistant:
  requires: [@query-engine, @graph-executor]
  
@response-formatter:
  requires: []  # No dependencies
  
@context-manager:
  requires: []  # Self-contained
```

### 2. Dependency Injection

```typescript
// Module container handles dependency injection
class ModuleContainer {
  private modules = new Map<string, Module>();
  
  async loadModule(moduleId: string): Promise<Module> {
    const manifest = await this.loadManifest(moduleId);
    const dependencies = await this.loadDependencies(manifest);
    
    const ModuleClass = await this.importModule(moduleId);
    return new ModuleClass(dependencies);
  }
  
  private async loadDependencies(manifest: Manifest): Promise<Dependencies> {
    const deps: Dependencies = {};
    
    for (const [name, version] of Object.entries(manifest.dependencies.required)) {
      deps[name] = await this.loadModule(name);
    }
    
    return deps;
  }
}
```

### 3. Version Compatibility

```typescript
interface VersionPolicy {
  // Semantic versioning rules
  major: 'breaking-changes';
  minor: 'backward-compatible-features';
  patch: 'backward-compatible-fixes';
  
  // Deprecation policy
  deprecation: {
    warningPeriod: '6-months';
    removalPolicy: 'next-major-version';
  };
}
```

## Error Handling Across Boundaries

### 1. Error Types

```typescript
// Base error class for all modules
export class ModuleError extends Error {
  constructor(
    public module: string,
    public code: string,
    message: string,
    public cause?: Error
  ) {
    super(message);
  }
}

// Specific error types
export class ValidationError extends ModuleError {}
export class TimeoutError extends ModuleError {}
export class DependencyError extends ModuleError {}
```

### 2. Error Propagation

```typescript
// Modules wrap and propagate errors with context
class GraphEngine {
  async generateQuery(intent: QueryIntent): Promise<CypherQuery> {
    try {
      return await this.generate(intent);
    } catch (error) {
      throw new ModuleError(
        '@graph-engine',
        'QUERY_GENERATION_FAILED',
        `Failed to generate query for intent type: ${intent.type}`,
        error
      );
    }
  }
}
```

### 3. Error Recovery

```typescript
interface ErrorRecoveryStrategy {
  retry?: {
    attempts: number;
    backoff: 'linear' | 'exponential';
    maxDelay: number;
  };
  
  fallback?: {
    handler: (error: Error) => Promise<any>;
  };
  
  circuitBreaker?: {
    threshold: number;
    timeout: number;
  };
}
```

## Testing Module Boundaries

### 1. Contract Testing

```typescript
describe('Module Contract: @graph-engine', () => {
  let graphEngine: GraphEngineModule;
  
  beforeEach(() => {
    graphEngine = new GraphEngine();
  });
  
  describe('generateQuery', () => {
    it('returns valid CypherQuery for valid intent', async () => {
      const intent: QueryIntent = {
        type: 'FIND_ENTITY',
        entities: [{ type: 'Person', filters: [] }],
        filters: [],
        relationships: [],
        aggregations: []
      };
      
      const query = await graphEngine.generateQuery(intent);
      
      expect(query).toMatchObject({
        statement: expect.any(String),
        parameters: expect.any(Object),
        timeout: expect.any(Number)
      });
    });
    
    it('throws ValidationError for invalid intent', async () => {
      const invalidIntent = {} as QueryIntent;
      
      await expect(graphEngine.generateQuery(invalidIntent))
        .rejects.toThrow(ValidationError);
    });
  });
});
```

### 2. Integration Testing

```typescript
describe('Module Integration: Query Pipeline', () => {
  let container: ModuleContainer;
  let queryInterface: QueryInterfaceModule;
  
  beforeEach(async () => {
    container = new ModuleContainer();
    await container.loadModules([
      '@query-interface',
      '@graph-engine',
      '@query-executor',
      '@response-formatter'
    ]);
    
    queryInterface = container.get('@query-interface');
  });
  
  it('processes query through full pipeline', async () => {
    const request: QueryRequest = {
      id: 'test-1',
      query: 'Find all engineers in London',
      options: { format: 'json' }
    };
    
    const response = await queryInterface.processQuery(request);
    
    expect(response.status).toBe('success');
    expect(response.results).toBeDefined();
    expect(response.metadata.modules).toContain('@graph-engine');
  });
});
```

### 3. Mock Boundaries

```typescript
// Mock module for testing
class MockGraphEngine implements GraphEngineModule {
  async generateQuery(intent: QueryIntent): Promise<CypherQuery> {
    return {
      statement: 'MATCH (n) RETURN n',
      parameters: {},
      timeout: 1000,
      options: {}
    };
  }
}

// Use in tests
const queryInterface = new QueryInterface(
  new MockGraphEngine(),
  new MockResponseFormatter()
);
```

## Module Lifecycle Management

### 1. Initialization

```typescript
interface ModuleLifecycle {
  // Called when module is loaded
  async initialize(config: ModuleConfig): Promise<void>;
  
  // Called when dependencies are ready
  async start(): Promise<void>;
  
  // Health check
  async healthCheck(): Promise<HealthStatus>;
  
  // Graceful shutdown
  async shutdown(): Promise<void>;
}
```

### 2. Hot Reloading

```typescript
class ModuleReloader {
  async reloadModule(moduleId: string): Promise<void> {
    // Save current state
    const state = await this.saveModuleState(moduleId);
    
    // Unload old version
    await this.unloadModule(moduleId);
    
    // Load new version
    const newModule = await this.loadModule(moduleId);
    
    // Restore state
    await this.restoreModuleState(newModule, state);
    
    // Update dependencies
    await this.updateDependentModules(moduleId);
  }
}
```

## Performance Boundaries

### 1. Resource Allocation

```typescript
interface ModuleResources {
  memory: {
    min: number;
    max: number;
    alert: number;
  };
  
  cpu: {
    cores: number;
    priority: 'high' | 'normal' | 'low';
  };
  
  io: {
    maxConcurrentOps: number;
    queueSize: number;
  };
}
```

### 2. Performance Monitoring

```typescript
interface ModuleMetrics {
  // Operation metrics
  operations: {
    count: number;
    successRate: number;
    errorRate: number;
    avgDuration: number;
    p95Duration: number;
  };
  
  // Resource metrics  
  resources: {
    memoryUsed: number;
    cpuPercent: number;
    activeConnections: number;
  };
  
  // Business metrics
  business: {
    [key: string]: number;
  };
}
```

## Security Boundaries

### 1. Access Control

```typescript
interface ModulePermissions {
  // Who can call this module
  callers: string[] | '*';
  
  // What operations are allowed
  operations: {
    [operation: string]: {
      roles: string[];
      rateLimit?: number;
    };
  };
  
  // Data access restrictions
  dataAccess: {
    read: string[];
    write: string[];
  };
}
```

### 2. Data Sanitization

```typescript
// Modules sanitize data at boundaries
class QueryInterface {
  async processQuery(request: QueryRequest): Promise<QueryResponse> {
    // Sanitize input
    const sanitized = this.sanitizeInput(request);
    
    // Validate against schema
    this.validateRequest(sanitized);
    
    // Process with sanitized data
    return this.process(sanitized);
  }
  
  private sanitizeInput(request: QueryRequest): QueryRequest {
    return {
      ...request,
      query: this.sanitizeString(request.query),
      user: request.user ? this.sanitizeUser(request.user) : undefined
    };
  }
}
```