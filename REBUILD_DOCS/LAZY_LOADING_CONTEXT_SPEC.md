# Lazy Loading Context Management Specification

## Overview

This specification defines a context management system that intelligently loads only the necessary information for processing queries, optimizing for both performance and relevance. The system uses predictive loading, smart caching, and progressive enhancement to minimize memory usage while maintaining fast response times.

## Core Principles

1. **Load What's Needed**: Only load context directly relevant to the current operation
2. **Progressive Enhancement**: Start with minimal context, add more if needed
3. **Predictive Caching**: Anticipate likely next contexts based on patterns
4. **Model-Aware Sizing**: Adapt context size to the AI model's capabilities

## Architecture

### Context Hierarchy

```
Context Tree
├── Core Context (Always Loaded)
│   ├── System Capabilities
│   ├── Basic Schema
│   └── Entry Points
├── Domain Context (Lazy Loaded)
│   ├── Entity Definitions
│   ├── Relationship Maps
│   └── Business Rules
├── Module Context (On-Demand)
│   ├── Module Capabilities
│   ├── Implementation Details
│   └── Examples
└── Reference Context (As-Needed)
    ├── Documentation
    ├── Code Samples
    └── Historical Patterns
```

### Context Manager Architecture

```typescript
interface ContextManager {
  // Core operations
  initialize(): Promise<void>;
  loadContext(request: ContextRequest, model: string): Promise<Context>;
  unloadContext(contextId: string): void;
  
  // Model-aware sizing
  getMaxContextSize(model: string): number;
  
  // Optimization
  preloadPredicted(query: string): Promise<void>;
  optimizeMemory(): void;
  
  // Analytics
  getMetrics(): ContextMetrics;
}

// Dynamic limits based on model
const MODEL_CONTEXT_LIMITS = {
  'gpt-4': 128_000,
  'gpt-3.5-turbo': 16_000,
  'claude-3-opus': 200_000,
  'claude-3-sonnet': 200_000,
  'claude-2': 100_000,
  'llama-2': 4_000,
  'local-small': 2_000
};
```

## Context Loading Strategies

### 1. Query-Driven Loading

```typescript
class QueryContextLoader {
  async loadForQuery(query: string, model: string): Promise<QueryContext> {
    // Step 1: Get model's context limit
    const maxSize = this.getMaxContextSize(model) * 0.5; // 50% safety margin
    
    // Step 2: Analyze query intent
    const intent = await this.analyzeIntent(query);
    
    // Step 3: Determine required context within limit
    const requirements = this.determineRequirements(intent, maxSize);
    
    // Step 4: Load in priority order
    const context = new QueryContext(maxSize);
    
    // Always load core
    await context.loadCore();
    
    // Load based on intent
    switch (intent.type) {
      case 'FIND_PERSON':
        await context.loadDomain('organizational');
        await context.loadSchema('person', 'team');
        break;
        
      case 'POLICY_QUERY':
        await context.loadDomain('compliance');
        await context.loadSchema('policy', 'requirement');
        await context.loadRelationships('responsible_for');
        break;
        
      case 'COMPLEX_ANALYSIS':
        await context.loadModule('@graph-engine');
        await context.loadModule('@analytics-engine');
        break;
    }
    
    return context;
  }
  
  private determineRequirements(intent: QueryIntent): ContextRequirements {
    return {
      domains: this.getRequiredDomains(intent),
      schemas: this.getRequiredSchemas(intent),
      modules: this.getRequiredModules(intent),
      relationships: this.getRequiredRelationships(intent),
      maxSize: this.calculateMaxSize(intent),
      timeout: this.calculateTimeout(intent)
    };
  }
}
```

### 2. Progressive Loading Pattern

```typescript
class ProgressiveContextLoader {
  async loadProgressive(query: string): Promise<Context> {
    const stages = [
      this.loadStage1, // Minimal viable context
      this.loadStage2, // Enhanced context
      this.loadStage3  // Full context
    ];
    
    let context = new Context();
    let confidence = 0;
    
    for (const loadStage of stages) {
      context = await loadStage.call(this, query, context);
      confidence = await this.evaluateConfidence(query, context);
      
      // Stop loading if we have enough context
      if (confidence >= 0.9) {
        break;
      }
      
      // Check model-specific constraints
      const modelLimit = this.getMaxContextSize(model);
      if (context.size > modelLimit * 0.8) {
        context = await this.optimizeContext(context, modelLimit);
        break;
      }
    }
    
    return context;
  }
  
  private async loadStage1(query: string, context: Context, model: string): Promise<Context> {
    // Load only essential schemas and basic patterns
    const stageLimit = Math.min(10 * 1024, this.getMaxContextSize(model) * 0.1);
    await context.load({
      schemas: ['person', 'team', 'policy', 'project', 'task'],
      patterns: ['basic-queries'],
      maxSize: stageLimit
    });
    return context;
  }
  
  private async loadStage2(query: string, context: Context): Promise<Context> {
    // Add relationships and semantic mappings
    await context.load({
      relationships: await this.inferRelationships(query),
      semantics: await this.loadSemanticMappings(query),
      examples: await this.findSimilarExamples(query, 5),
      maxSize: 50 * 1024 // 50KB
    });
    return context;
  }
  
  private async loadStage3(query: string, context: Context): Promise<Context> {
    // Load full module capabilities and documentation
    const modules = await this.identifyRequiredModules(query);
    await context.load({
      modules: modules,
      documentation: await this.findRelevantDocs(query),
      historicalPatterns: await this.loadHistoricalPatterns(query),
      maxSize: 200 * 1024 // 200KB
    });
    return context;
  }
}
```

### 3. Predictive Loading

```typescript
class PredictiveContextLoader {
  private patternCache = new Map<string, PatternStats>();
  
  async predictNextContext(currentContext: Context, query: string): Promise<PredictedContext[]> {
    const predictions: PredictedContext[] = [];
    
    // Analyze current query pattern
    const pattern = this.extractPattern(query);
    
    // Look up historical patterns
    const history = this.patternCache.get(pattern.type) || { transitions: [] };
    
    // Calculate probabilities
    for (const transition of history.transitions) {
      if (transition.probability > 0.3) {
        predictions.push({
          contextType: transition.nextContext,
          probability: transition.probability,
          estimatedSize: transition.avgSize,
          preloadPriority: this.calculatePriority(transition)
        });
      }
    }
    
    // Sort by priority
    predictions.sort((a, b) => b.preloadPriority - a.preloadPriority);
    
    return predictions.slice(0, 3); // Top 3 predictions
  }
  
  async preloadPredicted(predictions: PredictedContext[]): Promise<void> {
    // Preload in background without blocking
    for (const prediction of predictions) {
      if (prediction.probability > 0.5) {
        // High probability - preload immediately
        this.backgroundLoad(prediction.contextType, 'high');
      } else {
        // Lower probability - preload when idle
        this.idleLoad(prediction.contextType, 'low');
      }
    }
  }
}
```

## Memory Management

### 1. Context Lifecycle

```typescript
class ContextLifecycleManager {
  private contexts = new Map<string, ManagedContext>();
  private memoryLimit = this.calculateMemoryLimit(); // Dynamic based on environment
  
  async manageLifecycle(contextId: string): Promise<void> {
    const context = this.contexts.get(contextId);
    if (!context) return;
    
    // Update last access time
    context.lastAccessed = Date.now();
    
    // Check memory pressure
    const totalMemory = this.calculateTotalMemory();
    if (totalMemory > this.memoryLimit * 0.9) {
      await this.evictLRU();
    }
    
    // Schedule for eviction if not used
    setTimeout(() => {
      if (Date.now() - context.lastAccessed > context.ttl) {
        this.evict(contextId);
      }
    }, context.ttl);
  }
  
  private async evictLRU(): Promise<void> {
    const contexts = Array.from(this.contexts.entries());
    contexts.sort((a, b) => a[1].lastAccessed - b[1].lastAccessed);
    
    // Evict oldest contexts until we're under 70% memory
    let currentMemory = this.calculateTotalMemory();
    for (const [id, context] of contexts) {
      if (currentMemory < this.memoryLimit * 0.7) break;
      if (!context.isPinned) {
        this.evict(id);
        currentMemory -= context.size;
      }
    }
  }
}
```

### 2. Context Compression

```typescript
class ContextCompressor {
  compress(context: Context): CompressedContext {
    // Remove redundant data
    const deduplicated = this.deduplicateContext(context);
    
    // Compress strings
    const compressed = this.compressStrings(deduplicated);
    
    // Create indices for fast access
    const indexed = this.createIndices(compressed);
    
    return {
      data: indexed,
      originalSize: context.size,
      compressedSize: indexed.size,
      compressionRatio: indexed.size / context.size,
      decompressionTime: this.estimateDecompressionTime(indexed)
    };
  }
  
  private deduplicateContext(context: Context): Context {
    const seen = new Set<string>();
    const dedup = new Context();
    
    // Remove duplicate schemas
    for (const schema of context.schemas) {
      const key = this.schemaKey(schema);
      if (!seen.has(key)) {
        seen.add(key);
        dedup.addSchema(schema);
      }
    }
    
    // Merge overlapping relationships
    dedup.relationships = this.mergeRelationships(context.relationships);
    
    return dedup;
  }
}
```

## Context Resolution

### 1. Smart Context Resolution

```typescript
class SmartContextResolver {
  async resolve(request: ContextRequest): Promise<ResolvedContext> {
    // Check cache first
    const cached = await this.checkCache(request);
    if (cached && cached.isValid()) {
      return cached;
    }
    
    // Build context graph
    const graph = await this.buildContextGraph(request);
    
    // Find optimal loading path
    const loadingPath = this.findOptimalPath(graph, request);
    
    // Load contexts in parallel where possible
    const contexts = await this.loadParallel(loadingPath);
    
    // Merge and validate
    const merged = this.mergeContexts(contexts);
    const validated = await this.validate(merged, request);
    
    // Cache for future use
    await this.cache(request, validated);
    
    return validated;
  }
  
  private buildContextGraph(request: ContextRequest): ContextGraph {
    const graph = new ContextGraph();
    
    // Add required contexts as nodes
    for (const req of request.requirements) {
      graph.addNode(req);
    }
    
    // Add dependencies as edges
    for (const req of request.requirements) {
      const deps = this.getDependencies(req);
      for (const dep of deps) {
        graph.addEdge(req, dep);
      }
    }
    
    return graph;
  }
}
```

### 2. Fallback Strategies

```typescript
class ContextFallbackHandler {
  async handleMissingContext(
    request: ContextRequest, 
    missing: MissingContext[]
  ): Promise<FallbackContext> {
    const strategies = [
      this.useDefaultContext,
      this.usePartialContext,
      this.useCachedContext,
      this.generateMinimalContext
    ];
    
    for (const strategy of strategies) {
      try {
        const fallback = await strategy.call(this, request, missing);
        if (fallback.isUsable()) {
          return fallback;
        }
      } catch (error) {
        continue;
      }
    }
    
    // Last resort - return error context
    return this.createErrorContext(missing);
  }
  
  private async usePartialContext(
    request: ContextRequest, 
    missing: MissingContext[]
  ): Promise<FallbackContext> {
    // Load what we can
    const available = request.requirements.filter(
      req => !missing.some(m => m.id === req.id)
    );
    
    const partial = await this.loadContexts(available);
    
    // Add placeholders for missing
    for (const m of missing) {
      partial.addPlaceholder(m.id, this.createPlaceholder(m));
    }
    
    return {
      context: partial,
      isPartial: true,
      missingFeatures: missing.map(m => m.feature),
      confidence: this.calculateConfidence(partial, request)
    };
  }
}
```

## Performance Optimization

### 1. Context Warming

```typescript
class ContextWarmer {
  private warmupQueue = new PriorityQueue<WarmupTask>();
  
  async warmupForUser(userId: string, preferredModel: string): Promise<void> {
    // Get user's query history
    const history = await this.getUserHistory(userId);
    
    // Identify common patterns
    const patterns = this.extractPatterns(history);
    
    // Schedule warmup tasks
    for (const pattern of patterns) {
      this.warmupQueue.enqueue({
        pattern: pattern,
        priority: pattern.frequency * pattern.recency,
        contexts: this.predictContextsForPattern(pattern)
      });
    }
    
    // Process warmup queue in background
    this.processWarmupQueue();
  }
  
  private async processWarmupQueue(): Promise<void> {
    while (!this.warmupQueue.isEmpty()) {
      const task = this.warmupQueue.dequeue();
      
      // Check if still relevant
      if (this.isStillRelevant(task)) {
        await this.warmupContexts(task.contexts);
      }
      
      // Yield to prevent blocking
      await this.sleep(10);
    }
  }
}
```

### 2. Context Streaming

```typescript
class ContextStreamer {
  async *streamContext(request: ContextRequest): AsyncGenerator<ContextChunk> {
    const plan = await this.createStreamingPlan(request);
    
    for (const stage of plan.stages) {
      // Load stage data
      const data = await this.loadStageData(stage);
      
      // Yield chunk
      yield {
        stageId: stage.id,
        data: data,
        isComplete: false,
        nextStageHint: stage.next
      };
      
      // Check if we have enough context
      if (await this.hasSufficientContext(data, request)) {
        yield {
          stageId: 'final',
          data: null,
          isComplete: true,
          nextStageHint: null
        };
        break;
      }
    }
  }
  
  private createStreamingPlan(request: ContextRequest): StreamingPlan {
    return {
      stages: [
        { id: 'core', priority: 1, size: 5000, next: 'schema' },
        { id: 'schema', priority: 2, size: 15000, next: 'relationships' },
        { id: 'relationships', priority: 3, size: 10000, next: 'examples' },
        { id: 'examples', priority: 4, size: 30000, next: 'full' },
        { id: 'full', priority: 5, size: 100000, next: null }
      ],
      strategy: 'progressive',
      timeout: 5000
    };
  }
}
```

## Monitoring and Analytics

### 1. Context Usage Analytics

```typescript
interface ContextAnalytics {
  // Usage patterns
  contextAccessPatterns: Map<string, AccessPattern>;
  averageContextSize: number;
  cacheHitRate: number;
  
  // Performance metrics
  averageLoadTime: number;
  p95LoadTime: number;
  memoryEfficiency: number;
  
  // Optimization suggestions
  unusedContexts: string[];
  oversizedContexts: string[];
  frequentlyEvicted: string[];
}

class ContextAnalyzer {
  async analyze(timeRange: TimeRange): Promise<ContextAnalytics> {
    const events = await this.getContextEvents(timeRange);
    
    return {
      contextAccessPatterns: this.analyzeAccessPatterns(events),
      averageContextSize: this.calculateAverageSize(events),
      cacheHitRate: this.calculateCacheHitRate(events),
      averageLoadTime: this.calculateAverageLoadTime(events),
      p95LoadTime: this.calculateP95LoadTime(events),
      memoryEfficiency: this.calculateMemoryEfficiency(events),
      unusedContexts: this.findUnusedContexts(events),
      oversizedContexts: this.findOversizedContexts(events),
      frequentlyEvicted: this.findFrequentlyEvicted(events)
    };
  }
}
```

### 2. Real-time Monitoring

```typescript
class ContextMonitor {
  private metrics = new MetricsCollector();
  
  monitorContextOperation(operation: ContextOperation): void {
    const timer = this.metrics.startTimer();
    
    operation.on('start', () => {
      this.metrics.increment('context.operations.started');
    });
    
    operation.on('loaded', (size: number) => {
      this.metrics.histogram('context.size', size);
      this.metrics.gauge('context.memory.used', this.getMemoryUsage());
    });
    
    operation.on('complete', () => {
      const duration = timer.end();
      this.metrics.histogram('context.load.duration', duration);
      this.metrics.increment('context.operations.completed');
    });
    
    operation.on('error', (error: Error) => {
      this.metrics.increment('context.operations.failed');
      this.logError(error);
    });
  }
  
  getHealthStatus(): ContextHealthStatus {
    return {
      memoryUsage: this.getMemoryUsage(),
      cacheHitRate: this.metrics.getRate('cache.hits', 'cache.total'),
      avgLoadTime: this.metrics.getAverage('context.load.duration'),
      errorRate: this.metrics.getRate('context.operations.failed', 'context.operations.started'),
      status: this.calculateOverallHealth()
    };
  }
}
```

## Testing Strategy

### 1. Context Loading Tests

```typescript
describe('Context Loading', () => {
  test('loads context within model limits', async () => {
    const loader = new QueryContextLoader();
    const context = await loader.loadForQuery('find John Smith', 'gpt-3.5-turbo');
    
    expect(context.size).toBeLessThan(16_000 * 0.5); // Within 50% of model limit
    expect(context.hasSchema('person')).toBe(true);
    expect(context.hasModule('@query-engine')).toBe(false); // Not needed for simple query
  });
  
  test('progressively loads context for complex query', async () => {
    const loader = new ProgressiveContextLoader();
    const contexts: Context[] = [];
    
    loader.on('stage-complete', (context) => {
      contexts.push(context.clone());
    });
    
    await loader.loadProgressive('analyze team structure and compliance');
    
    expect(contexts.length).toBeGreaterThan(1);
    expect(contexts[0].size).toBeLessThan(contexts[contexts.length - 1].size);
  });
  
  test('handles missing context gracefully', async () => {
    const resolver = new SmartContextResolver();
    const request = {
      requirements: ['@missing-module', '@schema-registry'],
      query: 'test query'
    };
    
    const context = await resolver.resolve(request);
    
    expect(context.isPartial).toBe(true);
    expect(context.hasPlaceholder('@missing-module')).toBe(true);
    expect(context.confidence).toBeGreaterThan(0.5);
  });
});
```

### 2. Performance Tests

```typescript
describe('Context Performance', () => {
  test('meets latency requirements', async () => {
    const loader = new QueryContextLoader();
    const queries = generateTestQueries(100);
    
    const latencies: number[] = [];
    for (const query of queries) {
      const start = Date.now();
      await loader.loadForQuery(query);
      latencies.push(Date.now() - start);
    }
    
    const p95 = percentile(latencies, 95);
    expect(p95).toBeLessThan(100); // < 100ms
  });
  
  test('memory usage stays within limits', async () => {
    const manager = new ContextLifecycleManager();
    const initialMemory = process.memoryUsage().heapUsed;
    
    // Load many contexts
    for (let i = 0; i < 1000; i++) {
      await manager.loadContext(`context-${i}`, { size: 100 * 1024 });
    }
    
    const finalMemory = process.memoryUsage().heapUsed;
    const memoryGrowth = finalMemory - initialMemory;
    
    expect(memoryGrowth).toBeLessThan(100 * 1024 * 1024); // < 100MB
  });
});
```
