# REBUILD_DOCS - System Architecture Documentation

This folder contains the complete architectural documentation for building the Enterprise Knowledge Graph & PM Assistant System.

## Core System Documents

### Architecture & Design
- **[REBUILD_PRD.md](./REBUILD_PRD.md)** - Product Requirements Document v2.0
- **[REBUILD_SUMMARY.md](./REBUILD_SUMMARY.md)** - Executive summary of the entire system
- **[MODULE_BOUNDARIES_SPEC.md](./MODULE_BOUNDARIES_SPEC.md)** - Clear module interfaces and boundaries
- **[GRAPH_SCHEMA_UNIFIED.md](./GRAPH_SCHEMA_UNIFIED.md)** - Complete Neo4j schema definition

### Implementation Guides
- **[IMPLEMENTATION_ROADMAP.md](./IMPLEMENTATION_ROADMAP.md)** - 12-week development plan
- **[INTEGRATED_USE_CASES.md](./INTEGRATED_USE_CASES.md)** - Real-world usage examples
- **[SYNCHRONIZATION_STRATEGY.md](./SYNCHRONIZATION_STRATEGY.md)** - Event-driven architecture

### Technical Specifications
- **[LAZY_LOADING_CONTEXT_SPEC.md](./LAZY_LOADING_CONTEXT_SPEC.md)** - Smart context management
- **[REFERENCE_TOUCHPOINT_SPEC.md](./REFERENCE_TOUCHPOINT_SPEC.md)** - Auto-maintained code navigation
- **[AI_AGENT_INDEXING_SPEC.md](./AI_AGENT_INDEXING_SPEC.md)** - Machine-readable module system

### PM Assistant Features
- **[PM_CAPABILITIES_SPEC.md](./PM_CAPABILITIES_SPEC.md)** - Graph-based project management
- **[PM_TOUCHPOINTS_PATTERNS.md](./PM_TOUCHPOINTS_PATTERNS.md)** - PM-specific navigation patterns

## Development Tools

The **[development_tools/](./development_tools/)** folder contains tools used during development:

- **[DEVELOPMENT_TOOLS.md](./DEVELOPMENT_TOOLS.md)** - Overview of development practices
- **Sub-Agent Orchestration** - Tools for managing context bloat during development
  - Used to delegate implementation tasks to headless Claude Code instances
  - NOT a feature of the actual system

## Key Design Decisions

1. **Neo4j Database** - Chosen for better AI training data representation
2. **6 Core Modules** - Simplified from original 10+ module design
3. **Graph-First Architecture** - All data (knowledge + PM) in one graph
4. **Event-Driven Sync** - Automatic coordination between components
5. **Auto-Maintained Touchpoints** - Claude Code maintains navigation system

## Reading Order

For developers new to the project:

1. Start with **REBUILD_SUMMARY.md** for the big picture
2. Read **REBUILD_PRD.md** for detailed requirements
3. Review **GRAPH_SCHEMA_UNIFIED.md** to understand the data model
4. Study **MODULE_BOUNDARIES_SPEC.md** for system architecture
5. Follow **IMPLEMENTATION_ROADMAP.md** for development phases

## Quick Reference

- **Database**: Neo4j (all data in one graph)
- **Core Modules**: Query Engine, Graph Executor, PM Assistant, Response Formatter, Context Manager, API Gateway
- **Languages**: TypeScript (primary), Python (tools)
- **Architecture**: Event-driven, graph-first, AI-agent friendly
- **Development Timeline**: 12 weeks for full implementation

Last updated: 2025-06-23
