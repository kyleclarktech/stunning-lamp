# Prompt for FalkorDB Chat Interface Performance Optimization

## Context
You are tasked with implementing performance improvements for a FalkorDB chat interface that converts natural language queries to Cypher queries using Ollama LLM. The system is functional but needs optimization.

## Current System Architecture
- **Backend**: FastAPI with WebSocket support (`/home/kyle/projects/stunning-lamp/backend/main.py`)
- **LLM**: Ollama API using granite3.3:8b model for query generation
- **Database**: FalkorDB graph database with 625 nodes
- **Frontend**: React/Vite application with WebSocket client
- **Current Response Time**: 15-20 seconds (first query), 10-15 seconds (subsequent)

## Key Files to Review
1. `/home/kyle/projects/stunning-lamp/backend/main.py` - WebSocket handler and Ollama integration
2. `/home/kyle/projects/stunning-lamp/backend/prompts/generate_query.txt` - Query generation prompt
3. `/home/kyle/projects/stunning-lamp/backend/prompts/analyze_message.txt` - Message analysis prompt
4. `/home/kyle/projects/stunning-lamp/docker-compose.yml` - Service configuration
5. `/home/kyle/projects/stunning-lamp/QUERY_TESTING_REPORT.md` - Current test results

## Identified Improvements Needed

### 1. Query Pattern Pre-compilation
**Goal**: Pre-compile and optimize common Cypher query patterns
**Requirements**:
- Identify top 20 most common query patterns from prompts
- Create template Cypher queries with parameter placeholders
- Build a pattern matcher to detect and use templates
- Bypass LLM for matched patterns
**Success Metric**: 50% of queries use pre-compiled patterns

### 2. Enhanced Error Messages
**Goal**: Provide user-friendly, actionable error messages
**Requirements**:
- Map FalkorDB error codes to user-friendly messages
- Add query suggestions when no results found
- Include "did you mean?" functionality for typos
- Provide examples of similar working queries
**Success Metric**: Users can self-correct 75% of failed queries

### 3. Response Streaming Implementation
**Goal**: Stream results as they're generated for better UX
**Requirements**:
- Modify WebSocket protocol to support chunked responses
- Stream Cypher query generation progress
- Stream database results in batches
- Update frontend to display partial results
**Success Metric**: First result visible in <3 seconds

## Technical Constraints
- Must maintain backward compatibility with existing WebSocket protocol
- Cannot modify FalkorDB or Ollama configurations
- Must work within Docker container resource limits
- Should not increase memory usage by more than 20%

## Deliverables
1. Updated `main.py` with caching and streaming
2. New `query_patterns.py` for pre-compiled patterns
3. Updated WebSocket protocol documentation
4. Performance benchmark comparing before/after

## Testing Requirements
- All existing queries must continue to work
- New unit tests for each improvement
- Load testing with 100 concurrent users
- Measure and document performance improvements

## Additional Context
- The system uses fuzzy matching with CONTAINS for better results
- Role vs name detection is already implemented
- Current bottleneck is Ollama inference time (10-15s)
- FalkorDB query execution is fast (<100ms)

## Questions to Address
1. Should pre-compiled patterns be configurable or hardcoded?
2. What streaming chunk size provides the best UX?

Please analyze the codebase and implement these improvements, focusing first on query caching as it will provide the most immediate benefit. Document your design decisions and provide benchmarks for each optimization.