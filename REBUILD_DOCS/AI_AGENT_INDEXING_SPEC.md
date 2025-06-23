# AI-Agent Friendly Indexing System Specification

## Overview

This document specifies the machine-readable indexing system that enables AI agents to efficiently discover, understand, and utilize system capabilities with minimal context loading.

## Core Concepts

### 1. Hierarchical Index Structure

```
/
├── system-index.json         # Root index
├── modules/
│   ├── module-index.json    # Module registry
│   └── [module-name]/
│       ├── manifest.json    # Module metadata
│       ├── capability.json  # Capability definitions
│       └── context.json     # Context requirements
├── schemas/
│   ├── schema-index.json    # Schema registry
│   └── [domain]/
│       └── [entity].json    # Entity schemas
└── references/
    ├── reference-index.json # Reference documentation
    └── touchpoints/
        └── [topic].json     # Contextual touchpoints
```

### 2. Index Entry Format

```typescript
interface IndexEntry {
  id: string;                    // Unique identifier
  type: IndexEntryType;          // module | schema | reference | capability
  path: string;                  // Filesystem path
  metadata: {
    version: string;
    last_modified: string;
    size_bytes: number;
    load_priority: number;       // 0-100, lower = load first
  };
  discovery: {
    keywords: string[];          // For semantic search
    categories: string[];        // For classification
    relationships: string[];     // Related entries
  };
  access: {
    lazy_loadable: boolean;      // Can be loaded on-demand
    cache_ttl: number;          // Seconds, -1 for permanent
    compression: string;         // gzip | none
  };
}
```

## System Root Index

**Location**: `/system-index.json`

```json
{
  "version": "2.0.0",
  "system_id": "enterprise-knowledge-graph",
  "capabilities": {
    "natural_language_queries": true,
    "graph_database": "neo4j",
    "real_time_updates": true,
    "multi_tenant": false
  },
  "entry_points": {
    "modules": "./modules/module-index.json",
    "schemas": "./schemas/schema-index.json",
    "references": "./references/reference-index.json"
  },
  "ai_agent_hints": {
    "primary_interface": "@query-interface",
    "context_strategy": "lazy",
    "max_context_size": 100000,
    "preferred_response_format": "structured"
  }
}
```

## Module Indexing

### Module Registry

**Location**: `/modules/module-index.json`

```json
{
  "version": "2.0.0",
  "modules": [
    {
      "id": "@graph-engine",
      "path": "./graph-engine/manifest.json",
      "load_priority": 10,
      "keywords": ["query", "cypher", "natural language"],
      "categories": ["core", "query-processing"],
      "lazy_loadable": true,
      "dependencies": ["@schema-registry"]
    },
    {
      "id": "@schema-registry",
      "path": "./schema-registry/manifest.json",
      "load_priority": 0,
      "keywords": ["schema", "entities", "relationships"],
      "categories": ["core", "data-model"],
      "lazy_loadable": false,
      "dependencies": []
    }
  ],
  "discovery_hints": {
    "load_strategy": "Load @schema-registry first, then load modules based on query intent",
    "optimization": "Cache frequently used modules in agent memory"
  }
}
```

### Module Manifest

**Location**: `/modules/[module-name]/manifest.json`

```json
{
  "id": "@graph-engine",
  "version": "2.0.0",
  "description": "Converts natural language to graph queries",
  "entry_point": "./index.ts",
  "capabilities": {
    "natural_language_to_cypher": {
      "description": "Parse natural language and generate Cypher queries",
      "input_schema": "./schemas/query-request.json",
      "output_schema": "./schemas/query-response.json",
      "examples": "./examples/nl-to-cypher.json",
      "performance": {
        "avg_latency_ms": 50,
        "p95_latency_ms": 100,
        "throughput_rps": 100
      }
    }
  },
  "context_requirements": {
    "required": ["@schema-registry/entities"],
    "optional": ["@semantic-mappings/roles", "@query-patterns/common"],
    "runtime_discoverable": true
  },
  "ai_agent_interface": {
    "invocation_pattern": "function_call",
    "streaming_supported": true,
    "batch_capable": true,
    "stateless": true
  }
}
```

## Schema Indexing

### Schema Registry

**Location**: `/schemas/schema-index.json`

```json
{
  "version": "2.0.0",
  "domains": {
    "organizational": {
      "path": "./organizational",
      "entities": ["person", "team", "group", "department"],
      "relationships": ["member_of", "reports_to", "collaborates_with"]
    },
    "compliance": {
      "path": "./compliance",
      "entities": ["policy", "framework", "requirement"],
      "relationships": ["responsible_for", "complies_with"]
    }
  },
  "cross_domain_relationships": [
    {
      "from": "organizational/person",
      "to": "compliance/policy",
      "type": "responsible_for"
    }
  ]
}
```

### Entity Schema with AI Hints

**Location**: `/schemas/organizational/person.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "organizational/person",
  "type": "object",
  "description": "Represents an employee in the organization",
  "ai_hints": {
    "synonyms": ["employee", "staff", "worker", "colleague"],
    "query_patterns": ["find {name}", "who is {name}", "{name}'s manager"],
    "common_filters": ["department", "role", "location"],
    "relationships_priority": ["reports_to", "member_of"]
  },
  "properties": {
    "id": {
      "type": "string",
      "description": "Unique identifier"
    },
    "name": {
      "type": "string",
      "description": "Full name",
      "ai_hints": {
        "searchable": true,
        "fuzzy_match": true
      }
    },
    "role": {
      "type": "string",
      "description": "Job title",
      "ai_hints": {
        "semantic_groups": {
          "engineering": ["Engineer", "Developer", "Architect"],
          "management": ["Manager", "Director", "VP", "Lead"]
        }
      }
    }
  }
}
```

## Reference Touchpoint System

### Touchpoint Index

**Location**: `/references/touchpoints/query-processing.json`

```json
{
  "id": "query-processing",
  "title": "Query Processing Pipeline",
  "relevance_triggers": ["query", "search", "find", "cypher"],
  "sections": [
    {
      "id": "intent-classification",
      "title": "Classifying Query Intent",
      "content_path": "./docs/query-processing.md#intent",
      "code_references": [
        "@graph-engine/src/intent-classifier.ts"
      ],
      "related_capabilities": [
        "@graph-engine/natural_language_to_cypher"
      ],
      "load_priority": 10
    }
  ],
  "ai_navigation": {
    "entry_point": "intent-classification",
    "flow": [
      "intent-classification",
      "entity-extraction",
      "query-generation",
      "optimization"
    ]
  }
}
```

## Context Loading Strategies

### 1. Relevance Scoring

```typescript
interface ContextRelevanceScorer {
  scoreRelevance(query: string, entry: IndexEntry): number;
}

class SmartContextScorer implements ContextRelevanceScorer {
  scoreRelevance(query: string, entry: IndexEntry): number {
    let score = 0;
    
    // Keyword matching
    const queryTokens = this.tokenize(query.toLowerCase());
    const keywords = entry.discovery.keywords.map(k => k.toLowerCase());
    
    for (const token of queryTokens) {
      if (keywords.some(k => k.includes(token))) {
        score += 10;
      }
    }
    
    // Category bonus
    if (this.inferCategory(query) === entry.discovery.categories[0]) {
      score += 20;
    }
    
    // Relationship proximity
    score += this.calculateRelationshipScore(query, entry);
    
    // Penalize large contexts
    score -= Math.log(entry.metadata.size_bytes) / 10;
    
    return Math.max(0, Math.min(100, score));
  }
}
```

### 2. Progressive Loading

```typescript
interface ProgressiveLoader {
  async loadContext(query: string): Promise<Context>;
}

class LazyContextLoader implements ProgressiveLoader {
  async loadContext(query: string): Promise<Context> {
    const context = new Context();
    
    // Step 1: Load core schema (always needed)
    const schemaIndex = await this.loadIndex('/schemas/schema-index.json');
    context.add('schema', schemaIndex);
    
    // Step 2: Score all available modules
    const moduleIndex = await this.loadIndex('/modules/module-index.json');
    const scores = moduleIndex.modules.map(m => ({
      module: m,
      score: this.scorer.scoreRelevance(query, m)
    }));
    
    // Step 3: Load high-scoring modules
    const threshold = 30;
    for (const {module, score} of scores) {
      if (score >= threshold) {
        const manifest = await this.loadManifest(module.path);
        context.add(module.id, manifest);
        
        // Load required dependencies
        for (const dep of manifest.context_requirements.required) {
          if (!context.has(dep)) {
            await this.loadDependency(dep, context);
          }
        }
      }
    }
    
    return context;
  }
}
```

## AI Agent Usage Patterns

### 1. Discovery Pattern

```typescript
// AI agent discovers available capabilities
async function discoverCapabilities(): Promise<Capability[]> {
  const systemIndex = await loadIndex('/system-index.json');
  const moduleIndex = await loadIndex(systemIndex.entry_points.modules);
  
  const capabilities = [];
  for (const module of moduleIndex.modules) {
    if (module.lazy_loadable) {
      // Load just the capability definitions, not the full module
      const capabilityPath = module.path.replace('manifest.json', 'capability.json');
      const caps = await loadIndex(capabilityPath);
      capabilities.push(...caps);
    }
  }
  
  return capabilities;
}
```

### 2. Query Pattern

```typescript
// AI agent processes a user query
async function processQuery(userQuery: string): Promise<Response> {
  // Load minimal context
  const loader = new LazyContextLoader();
  const context = await loader.loadContext(userQuery);
  
  // Find relevant module
  const queryModule = context.findBestModule(userQuery);
  
  // Load module if not already loaded
  if (!queryModule.loaded) {
    await queryModule.load();
  }
  
  // Execute query
  return queryModule.execute({
    query: userQuery,
    context: context.compact()
  });
}
```

### 3. Learning Pattern

```typescript
// AI agent learns from usage
async function updateIndexRelevance(
  query: string, 
  usedModules: string[], 
  feedback: Feedback
): Promise<void> {
  const index = await loadIndex('/modules/module-index.json');
  
  for (const moduleId of usedModules) {
    const module = index.modules.find(m => m.id === moduleId);
    if (module && feedback.useful) {
      // Add query keywords to module keywords
      const queryKeywords = extractKeywords(query);
      module.keywords = [...new Set([...module.keywords, ...queryKeywords])];
    }
  }
  
  await saveIndex('/modules/module-index.json', index);
}
```

## Implementation Guidelines

### 1. Index Maintenance

```typescript
class IndexMaintainer {
  async rebuildIndex(): Promise<void> {
    const walker = new FileWalker();
    const entries: IndexEntry[] = [];
    
    // Walk module directories
    for await (const file of walker.walk('./modules')) {
      if (file.name === 'manifest.json') {
        const entry = await this.createModuleEntry(file);
        entries.push(entry);
      }
    }
    
    // Generate keyword relationships
    this.generateRelationships(entries);
    
    // Save index
    await this.saveIndex(entries);
  }
  
  private generateRelationships(entries: IndexEntry[]): void {
    // Use TF-IDF or similar to find related entries
    for (const entry of entries) {
      entry.discovery.relationships = this.findRelated(entry, entries);
    }
  }
}
```

### 2. Performance Optimization

```yaml
# Index optimization rules
optimization:
  compression:
    enabled: true
    algorithm: gzip
    threshold: 1024  # bytes
  
  caching:
    index_ttl: 3600  # 1 hour
    content_ttl: 300  # 5 minutes
    
  preloading:
    - "@schema-registry"  # Always preload
    - "@query-interface"  # Common entry point
```

## Testing AI Agent Integration

```typescript
describe('AI Agent Index Usage', () => {
  test('discovers modules with minimal loading', async () => {
    const agent = new AIAgent();
    const modules = await agent.discoverModules();
    
    expect(modules).toHaveLength(5);
    expect(agent.getLoadedBytes()).toBeLessThan(10 * 1024); // < 10KB
  });
  
  test('loads relevant context for query', async () => {
    const agent = new AIAgent();
    const context = await agent.prepareContext('find all managers');
    
    expect(context.loadedModules).toContain('@graph-engine');
    expect(context.loadedSchemas).toContain('organizational/person');
    expect(context.totalSize).toBeLessThan(50 * 1024); // < 50KB
  });
  
  test('caches frequently used modules', async () => {
    const agent = new AIAgent();
    
    // First query
    const t1 = Date.now();
    await agent.processQuery('find John');
    const firstTime = Date.now() - t1;
    
    // Second similar query
    const t2 = Date.now();
    await agent.processQuery('find Jane');
    const secondTime = Date.now() - t2;
    
    expect(secondTime).toBeLessThan(firstTime * 0.5); // 50% faster
  });
});
```

## Monitoring and Analytics

```typescript
interface IndexUsageMetrics {
  module_access_frequency: Map<string, number>;
  average_context_size: number;
  cache_hit_rate: number;
  loading_patterns: LoadPattern[];
}

class IndexAnalytics {
  async generateReport(): Promise<IndexUsageReport> {
    return {
      most_used_modules: this.getTopModules(10),
      optimal_preload_list: this.calculateOptimalPreload(),
      unused_indices: this.findUnusedIndices(),
      optimization_suggestions: this.generateSuggestions()
    };
  }
}
```