# Reference Touchpoint System Specification

## Overview

The Reference Touchpoint System provides a semantic layer that connects code, documentation, examples, and context in a way that AI agents (especially Claude Code) can efficiently navigate and understand. The system is designed for automatic maintenance - touchpoints are extracted and updated by Claude Code as files change, eliminating manual maintenance burden.

## Core Concepts

### 1. Touchpoint Definition

A touchpoint is a semantically-rich reference point that connects related information across the codebase:

```typescript
interface Touchpoint {
  id: string;                      // Unique identifier
  type: TouchpointType;            // code | doc | example | pattern | concept
  location: TouchpointLocation;    // Where to find this
  metadata: TouchpointMetadata;    // Semantic information
  connections: Connection[];       // Related touchpoints
  triggers: TriggerCondition[];    // When this is relevant
}

enum TouchpointType {
  CODE_IMPLEMENTATION = 'code',
  DOCUMENTATION = 'doc',
  EXAMPLE_USAGE = 'example',
  DESIGN_PATTERN = 'pattern',
  CONCEPT_EXPLANATION = 'concept',
  ERROR_REFERENCE = 'error',
  PERFORMANCE_HINT = 'performance'
}
```

## Auto-Maintenance by Claude Code

### CLAUDE.md Integration

Add to your CLAUDE.md file:
```markdown
## Touchpoint Maintenance

When modifying code:
1. Update @touchpoint comments in changed functions
2. Run `npm run update-touchpoints` after changes
3. Touchpoints are extracted from:
   - @touchpoint comments in code
   - ## headers in markdown files  
   - Error class definitions
   - Exported interfaces

Example:
```typescript
// @touchpoint task-assignment
// @concepts [assignment, skills, availability]
async assignTask(task: Task): Promise<Assignment>
```

Git pre-commit hook validates touchpoint references.
```

### Automatic Extraction

```typescript
// Claude Code watches for these patterns
const TOUCHPOINT_PATTERNS = [
  /@touchpoint\s+([\w-]+)/,          // Code comments
  /##\s+(.+)/,                       // Markdown headers
  /class\s+(\w+Error)/,              // Error definitions
  /export\s+interface\s+(\w+)/,     // Interface definitions
];
```

## Touchpoint Categories

### 1. Code Implementation Touchpoints

Simple annotations that Claude Code can maintain:

```typescript
// @touchpoint query-parser
// @concepts [natural-language, parsing]
export class QueryParser {
  // @touchpoint parse-method
  async parse(query: string): Promise<QueryIntent> {
    // Implementation
  }
}
```

### 2. Documentation Touchpoints

Claude Code extracts from markdown headers automatically:

```markdown
## Query Processing Pipeline

The query processing pipeline consists of several stages...

### Intent Classification

How we classify user intent...
```

No manual annotations needed - headers become touchpoints.

### 3. Example Touchpoints

Simplified example format:

```typescript
// @touchpoint find-person-example
// @example person-search
const findPersonExample = {
  query: "Find John Smith",
  cypher: "MATCH (p:Person {name: $name}) RETURN p",
  params: { name: "John Smith" }
};
```

### 4. Pattern Touchpoints

Patterns in code comments:

```typescript
// @touchpoint pagination-pattern
// @pattern graph-pagination
// Problem: Paginate large result sets
// Solution: Use SKIP and LIMIT
export function paginateQuery(query: string, page: number, size: number) {
  return `${query} SKIP ${page * size} LIMIT ${size}`;
}
```

## Touchpoint Discovery System

### 1. Semantic Search

```typescript
class TouchpointSearchEngine {
  async search(query: string): Promise<RankedTouchpoint[]> {
    // Extract concepts from query
    const concepts = await this.extractConcepts(query);
    
    // Find touchpoints by triggers
    const triggered = await this.findByTriggers(query);
    
    // Find by concept similarity
    const similar = await this.findByConcepts(concepts);
    
    // Rank by relevance
    return this.rankResults([...triggered, ...similar], query);
  }
  
  private async extractConcepts(query: string): Promise<Concept[]> {
    // Use NLP to extract key concepts
    const tokens = this.tokenize(query);
    const concepts = await this.conceptExtractor.extract(tokens);
    
    // Expand with synonyms and related concepts
    return this.expandConcepts(concepts);
  }
}
```

### 2. Contextual Navigation

```typescript
class TouchpointNavigator {
  async getRelatedTouchpoints(
    current: Touchpoint,
    intent: NavigationIntent
  ): Promise<TouchpointPath[]> {
    const paths: TouchpointPath[] = [];
    
    // Direct connections
    const direct = current.connections
      .filter(c => this.matchesIntent(c, intent))
      .map(c => ({ steps: [current, c.target], score: c.strength }));
    
    paths.push(...direct);
    
    // Multi-hop paths for deeper connections
    if (intent.depth > 1) {
      const multiHop = await this.findMultiHopPaths(current, intent);
      paths.push(...multiHop);
    }
    
    return this.optimizePaths(paths);
  }
}
```

## Touchpoint Annotations

### 1. Code Annotations

```typescript
// Inline touchpoint markers
class DatabaseConnector {
  /**
   * @touchpoint db-connection-setup
   * @critical-path
   * @error-prone timeout-errors, connection-refused
   * @performance-impact high
   * @monitoring connection-pool-metrics
   */
  async connect(config: DBConfig): Promise<Connection> {
    // <TOUCHPOINT:connection-retry-logic>
    for (let attempt = 0; attempt < config.maxRetries; attempt++) {
      try {
        return await this.attemptConnection(config);
      } catch (error) {
        // <RELATED:error-handling-pattern>
        if (attempt === config.maxRetries - 1) throw error;
        await this.delay(this.backoffTime(attempt));
      }
    }
    // </TOUCHPOINT:connection-retry-logic>
  }
}
```

### 2. Documentation Annotations

```markdown
<!-- TOUCHPOINT-REGION: api-authentication -->
## API Authentication

Our API uses JWT tokens for authentication...

<!-- TRIGGER: ["auth", "authentication", "jwt", "token"] -->
<!-- IMPLEMENTS: oauth2-pattern, jwt-pattern -->
<!-- SEE-ALSO: auth-middleware, token-validation -->

### Token Structure
<!-- SUBTOUCHPOINT: jwt-structure -->
```json
{
  "sub": "user-id",
  "iat": 1234567890,
  "exp": 1234571490,
  "roles": ["user", "admin"]
}
```
<!-- /SUBTOUCHPOINT -->
<!-- /TOUCHPOINT-REGION -->
```

### 3. Error Reference Touchpoints

```typescript
// @touchpoint-error validation-error-invalid-query
export class InvalidQueryError extends Error {
  static code = 'INVALID_QUERY';
  
  constructor(query: string, reason: string) {
    super(`Invalid query: ${reason}`);
    
    // @debugging-hints
    // 1. Check query syntax
    // 2. Verify entity names match schema
    // 3. Ensure relationships are valid
    
    // @common-causes
    // - Typos in entity/relationship names  
    // - Missing required parameters
    // - Invalid filter syntax
    
    // @resolution-touchpoints
    // - query-syntax-guide
    // - schema-validator
    // - query-examples
  }
}
```

## Claude Code Auto-Generation

### Event-Driven Updates

```typescript
// In CLAUDE.md - Claude Code handles these events
interface TouchpointEvents {
  'file.saved': (file: string) => void;
  'file.deleted': (file: string) => void;
  'refactor.complete': (files: string[]) => void;
}

// Claude Code runs this on file changes
async function updateTouchpoints(file: string) {
  if (file.endsWith('.ts') || file.endsWith('.js')) {
    const touchpoints = await extractCodeTouchpoints(file);
    await updateTouchpointIndex(touchpoints);
  } else if (file.endsWith('.md')) {
    const touchpoints = await extractDocTouchpoints(file);
    await updateTouchpointIndex(touchpoints);
  }
}
```

### Git Integration

```bash
# .git/hooks/pre-commit
#!/bin/bash
# Validate touchpoint references before commit
npm run validate-touchpoints || exit 1
```

### Simplified Touchpoint Storage

```json
// .touchpoints/index.json - Auto-generated
{
  "version": "1.0.0",
  "lastUpdated": "2024-01-15T10:30:00Z",
  "touchpoints": [
    {
      "id": "query-parser",
      "file": "src/modules/query-engine/parser.ts",
      "line": 45,
      "type": "code",
      "concepts": ["parsing", "natural-language"]
    },
    {
      "id": "query-processing-pipeline",
      "file": "docs/architecture.md",
      "line": 23,
      "type": "documentation",
      "concepts": ["pipeline", "architecture"]
    }
  ],
  "connections": [
    {
      "from": "query-parser",
      "to": "query-processing-pipeline",
      "type": "implements"
    }
  ]
}
```

## Touchpoint Index Structure

### 1. Hierarchical Index

```json
{
  "version": "1.0.0",
  "touchpoints": {
    "modules": {
      "@query-interface": {
        "concepts": ["query-processing", "natural-language"],
        "implementations": ["query-parser-entry", "intent-classifier"],
        "examples": ["simple-query-example", "complex-query-example"],
        "patterns": ["command-pattern", "pipeline-pattern"]
      }
    },
    "domains": {
      "query-processing": {
        "overview": "query-processing-overview",
        "components": ["parser", "engine", "executor"],
        "flow": ["receive", "parse", "generate", "execute", "format"]
      }
    },
    "cross-references": {
      "error-handling": ["validation-errors", "timeout-errors", "recovery-patterns"],
      "performance": ["optimization-hints", "caching-strategies", "indexing"]
    }
  }
}
```

### 2. Semantic Graph

```typescript
interface TouchpointGraph {
  nodes: Map<string, TouchpointNode>;
  edges: TouchpointEdge[];
  
  // Semantic relationships
  conceptClusters: Map<string, string[]>;
  implementationMap: Map<string, string[]>;
  exampleMap: Map<string, string[]>;
}

interface TouchpointNode {
  id: string;
  touchpoint: Touchpoint;
  embeddings?: number[]; // For semantic similarity
  importance: number;     // PageRank-style importance
}

interface TouchpointEdge {
  source: string;
  target: string;
  type: EdgeType;
  weight: number;
  metadata?: any;
}
```

## AI Agent Integration

### 1. Touchpoint-Aware Context Loading

```typescript
class TouchpointContextLoader {
  async loadContextForQuery(query: string): Promise<EnrichedContext> {
    // Find relevant touchpoints
    const touchpoints = await this.searchEngine.search(query);
    
    // Build context graph
    const contextGraph = this.buildContextGraph(touchpoints);
    
    // Load in priority order
    const context = new EnrichedContext();
    
    for (const tp of this.prioritize(contextGraph)) {
      // Load touchpoint content
      const content = await this.loadTouchpointContent(tp);
      context.add(tp.id, content);
      
      // Load related code if needed
      if (tp.type === TouchpointType.CODE_IMPLEMENTATION) {
        const code = await this.loadCodeContext(tp);
        context.addCode(tp.id, code);
      }
      
      // Stop if context is large enough
      if (context.size > this.maxContextSize * 0.8) break;
    }
    
    return context;
  }
}
```

### 2. Intelligent Navigation

```typescript
class AIAgentNavigator {
  async navigateToSolution(problem: string): Promise<NavigationPath> {
    // Start with problem touchpoints
    const start = await this.findProblemTouchpoints(problem);
    
    // Find solution touchpoints
    const solutions = await this.findSolutionTouchpoints(problem);
    
    // Build navigation path
    const path = new NavigationPath();
    
    // Add conceptual understanding first
    path.addStep('understand', await this.findConcepts(problem));
    
    // Add relevant patterns
    path.addStep('patterns', await this.findPatterns(problem));
    
    // Add implementation references
    path.addStep('implement', await this.findImplementations(solutions));
    
    // Add examples
    path.addStep('examples', await this.findExamples(solutions));
    
    return path;
  }
}
```

## Maintenance-Free Design

### Why It's Maintenance-Free

1. **Simple Format**: Just comments, no complex schemas
2. **Auto-Discovery**: Claude Code finds touchpoints automatically
3. **Git Integration**: Pre-commit hooks ensure consistency
4. **No Manual Links**: Connections inferred from code structure

### Validation Script

```bash
# package.json scripts
{
  "scripts": {
    "update-touchpoints": "node scripts/update-touchpoints.js",
    "validate-touchpoints": "node scripts/validate-touchpoints.js"
  }
}
```

```typescript
// scripts/validate-touchpoints.js
import { readFileSync } from 'fs';

const index = JSON.parse(readFileSync('.touchpoints/index.json'));
const errors = [];

// Check all referenced files exist
for (const tp of index.touchpoints) {
  if (!existsSync(tp.file)) {
    errors.push(`Missing file: ${tp.file} (touchpoint: ${tp.id})`);
  }
}

if (errors.length > 0) {
  console.error('Touchpoint validation failed:');
  errors.forEach(e => console.error(`  - ${e}`));
  process.exit(1);
}
```

### Benefits for AI Agents

```typescript
// How Claude Code uses touchpoints
class ClaudeCodeIntegration {
  async findRelevantCode(query: string): Promise<CodeLocation[]> {
    // Load lightweight index
    const index = await this.loadTouchpointIndex();
    
    // Find matching touchpoints
    const matches = index.touchpoints.filter(tp => 
      tp.concepts.some(c => query.toLowerCase().includes(c))
    );
    
    // Return file locations
    return matches.map(tp => ({
      file: tp.file,
      line: tp.line,
      relevance: this.scoreRelevance(query, tp.concepts)
    }));
  }
  
  async updateAfterEdit(file: string, changes: Change[]): Promise<void> {
    // Re-extract touchpoints from edited file
    const newTouchpoints = await this.extractTouchpoints(file);
    
    // Update index
    await this.updateIndex(file, newTouchpoints);
    
    // No manual intervention needed!
  }
}
```

## Real-World Usage

### 1. Claude Code Finding Relevant Code

```bash
User: "How do I handle pagination in graph queries?"

# Claude Code automatically:
1. Searches touchpoint index for "pagination"
2. Finds @touchpoint pagination-pattern
3. Shows the code with context
4. Suggests related examples
```

### 2. Automatic Updates During Development

```bash
# Developer modifies task assignment logic
$ vim src/pm-assistant/assign.ts

# Claude Code detects the change and:
1. Extracts new/modified @touchpoint comments
2. Updates .touchpoints/index.json
3. Validates references still valid
4. Commits updated index with code changes
```

### 3. Zero-Maintenance Example

```typescript
// Before: Complex manual touchpoint
/**
 * @touchpoint query-parser-main-entry-point
 * @type code-implementation
 * @concepts [natural-language, parsing, query-analysis]
 * @related [nlp-processor, intent-classifier, cypher-generator]
 * @triggers ["parse query", "natural language", "NLP"]
 * @performance O(n) where n is query length
 * @see-also ../docs/query-processing.md#parsing
 */

// After: Simple auto-maintained
// @touchpoint query-parser
// @concepts [parsing, natural-language]
export class QueryParser {
  // Claude Code handles the rest!
}
```

## Summary: Maintenance-Free by Design

### Key Simplifications

1. **No Manual Linking** - Connections inferred from code structure
2. **Simple Comments** - Just @touchpoint and @concepts
3. **Auto-Updates** - Claude Code maintains the index
4. **Git Integration** - Pre-commit validation
5. **Lightweight Index** - Single JSON file, fast to load

### What This Enables

- Claude Code can find relevant code instantly
- Developers write normal comments, system does the rest
- No drift between code and documentation
- AI agents get semantic navigation for free
- Zero maintenance overhead

### Getting Started

```bash
# Add to package.json
{
  "scripts": {
    "postinstall": "npm run update-touchpoints",
    "update-touchpoints": "node scripts/update-touchpoints.js"
  }
}

# Add to .gitignore
.touchpoints/cache/

# Add to CLAUDE.md
## Touchpoints
This project uses auto-maintained touchpoints.
Update @touchpoint comments when changing code.
```
