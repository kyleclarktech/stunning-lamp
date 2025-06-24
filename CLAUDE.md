# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is an AI-powered conversational interface with FalkorDB graph database integration. The system uses Ollama for LLM inference and WebSocket connections for real-time communication. It processes natural language queries, generates Cypher queries, and formats results for task-oriented users.

## Commands

### Development Commands

```bash
# Start all services (API, Frontend, FalkorDB, Ollama, Redis)
docker-compose up -d

# Start services with live reload
docker-compose up

# View logs
docker-compose logs -f api
docker-compose logs -f ollama

# Stop all services  
docker-compose down

# Rebuild after code changes
docker-compose up -d --build
```

### Testing

```bash
# Run backend tests
cd backend
pytest tests/

# Run specific test file
pytest tests/test_websocket.py -v

# Test WebSocket connection and query processing
python test_websocket.py

# Access services
# Frontend: http://localhost:5173
# API: http://localhost:8000
# FalkorDB UI: http://localhost:3000
# Ollama: http://localhost:11434
```

### Database Management

```bash
# Seed database with test data
docker exec -it stunning-lamp-api-1 python scripts/seed_data.py

# Initialize empty database
docker exec -it stunning-lamp-api-1 python scripts/init_db.py

# Access FalkorDB CLI
docker exec -it stunning-lamp-falkordb-1 redis-cli
> GRAPH.QUERY agent_poc "MATCH (n) RETURN n LIMIT 10"
```

## Architecture

### Query Processing Pipeline

1. **WebSocket Handler** (`main.py:748-966`)
   - Receives user messages via WebSocket
   - Manages timeout handling and error recovery
   - Sends structured responses (info, query, results, error)
   - Implements heartbeat mechanism (30s interval) to keep connections alive
   - WebSocket connection manager tracks active connections

2. **AI Analysis** (`analyze_message.txt` prompt)
   - Determines user intent (task-oriented vs conversational)
   - Selects appropriate tools: custom_query, search_database, pig_latin, store_message
   - Prioritizes policy discovery and organizational queries
   - Analyzes query reasoning and applicable policies

3. **Query Generation** (`generate_query.txt` prompt)
   - Converts natural language to Cypher queries
   - Uses FalkorDB schema with Person, Team, Group, Policy nodes
   - Implements fallback queries for no-result scenarios
   - Supports query pattern matching for optimized performance

4. **Result Formatting** (`format_results.txt` prompt)
   - Formats query results for task completion
   - Emphasizes key contacts, policy owners, and next steps
   - Uses Markdown for structured presentation
   - Supports streaming responses for better UX

### Key Components

- **Ollama Integration**: Local LLM inference using granite3.3:8b model (8192 context window)
- **FalkorDB Schema**: Graph database with organizational data (People, Teams, Groups, Policies)
- **Prompt Templates**: Jinja2-based templates for AI model instructions
- **Real-time Communication**: WebSocket-based bidirectional messaging
- **Dashboard API**: Analytics endpoints with real-time metrics (`api/dashboard.py`)
- **Docker Composition**: Multi-service orchestration with health checks
- **Query Pattern Matcher** (`query_patterns.py`): Pre-compiled query patterns with semantic understanding
- **Error Handler** (`error_handler.py`): User-friendly error messages with suggestions and "did you mean?" functionality
- **Query Processor** (`query_processor.py`): Post-processes Cypher queries to fix FalkorDB-specific issues
- **Streaming Utils** (`streaming_utils.py`): Progressive result streaming for improved UX

### Data Model

#### Core Nodes
- **Person**: Employees with roles, departments, managers, visa status, hire date
- **Team**: Departmental teams with specific focus areas  
- **Group**: Cross-functional groups (governance, technical, operational)
- **Policy**: Compliance and operational policies with severity levels
- **Office**: Physical office locations with timezone, location details
- **Skill**: Technical and professional skills
- **Project**: Active projects with status tracking
- **Repository**: Code repositories
- **PullRequest**: Pull request tracking
- **Issue**: Issue tracking
- **Document**: Document management
- **CalendarEvent**: Calendar event tracking
- **Message**: Stored pig latin translations and original messages

#### Relationships
- **MEMBER_OF**: Person → Team/Group membership
- **REPORTS_TO**: Person → Person reporting structure
- **RESPONSIBLE_FOR**: Person/Team/Group → Policy ownership
- **WORKS_IN**: Person → Office location
- **HAS_SKILL**: Person → Skill associations

### Environment Configuration

```bash
# Required in backend/.env
OLLAMA_HOST=http://ollama:11434
OLLAMA_MODEL=granite3.3:8b
FALKOR_HOST=falkordb
FALKOR_PORT=6379
REDIS_HOST=redis
REDIS_PORT=6379
```

## Common Tasks

### Adding New Query Patterns

#### Method 1: Prompt-based (AI-generated queries)
1. Update `backend/prompts/analyze_message.txt` to recognize new patterns
2. Modify `backend/prompts/generate_query.txt` for Cypher query generation
3. Adjust `backend/prompts/format_results.txt` for result presentation

#### Method 2: Pattern-based (Pre-compiled queries)
1. Add new patterns to `query_patterns.py` in the `EnhancedQueryPatternMatcher` class
2. Define regex patterns, Cypher templates, and parameter extractors
3. Set appropriate priority (higher = matched first)
4. Add semantic mappings if needed for generic terms

### Modifying the Schema

1. Update seed data generation in `backend/scripts/seed_data.py`
2. Modify query prompts to reflect new node types/relationships
3. Update the schema documentation in prompt files

### Debugging Queries

1. Enable debug logging: `logging.basicConfig(level=logging.DEBUG)`
2. Check WebSocket test output: `python test_websocket.py`
3. Monitor query execution in logs: `docker-compose logs -f api`
4. Use FalkorDB UI at http://localhost:3000 for direct query testing

### Performance Optimization

- Query timeout: 15 seconds (configurable in `execute_custom_query`)
- WebSocket timeout: 60 seconds for AI processing
- Connection pooling via FalkorDB client
- Redis caching layer for frequently accessed data
- Async execution for database operations

### Frontend Development

```bash
# Start frontend development server with hot reload
cd frontend
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Key Frontend Routes

- `/`: Chat interface for conversational queries
- `/dashboard`: Analytics dashboard with organizational metrics
- Components use Vue 3 Composition API with reactive state management

## Enhanced Features

### Query Pattern System (`query_patterns.py`)

The system includes an advanced pattern matching engine with semantic understanding:

- **Semantic Mappings**: Understands generic terms like "employees", "developers", "managers"
- **Role Categories**: Maps job titles to query conditions (e.g., "executives" → VP, Chief, Director roles)
- **Department Categories**: Groups related departments (e.g., "engineering team" → Engineering, Data Platform, Infrastructure)
- **Pattern Priority**: Patterns are prioritized for optimal matching
- **Fallback Support**: Gracefully handles unmatched queries

Example semantic queries:
- "How many employees are there?" → Counts all Person nodes
- "List all developers" → Finds people with Engineer/Developer roles excluding managers
- "Show me executives in Engineering" → Combines role and department filters

### Dashboard API Endpoints (`api/dashboard.py`)

Real-time analytics endpoints with Redis caching:

- **`/api/dashboard/overview`**: Global metrics (employees, teams, policies, system health)
- **`/api/dashboard/offices`**: Office status with timezone-aware online/offline status
- **`/api/dashboard/incidents`**: Active incidents grouped by severity (simulated with policies)
- **`/api/dashboard/metrics`**: Performance metrics timeseries (query response time, active users, API requests)
- **`/api/dashboard/teams`**: Team distribution across departments with skill analytics
- **`/api/dashboard/visas`**: Visa expiry timeline for immigration tracking

Features:
- 60-second Redis cache for performance
- Concurrent query execution with thread pools
- Timezone-aware office status calculation
- Real-time metric generation

### Error Handling System (`error_handler.py`)

Intelligent error handling with user-friendly messages:

- **Error Pattern Recognition**: Maps FalkorDB errors to helpful messages
- **Fuzzy Matching**: Suggests similar entity names using difflib
- **Alternative Queries**: Provides 5 alternative query suggestions
- **"Did You Mean?"**: Detects potential typos and suggests corrections
- **Common Entity Database**: Pre-loaded with common teams, roles, departments, policies

### Query Processing (`query_processor.py`)

Post-processes generated Cypher queries to fix common issues:

- **Function Name Mapping**: Converts SQL-style functions to FalkorDB equivalents
  - `LOWER()` → `toLower()`
  - `UPPER()` → `toUpper()`
- **Statement Cleanup**: Removes multiple statements and trailing semicolons
- **Validation**: Checks for undefined variables and aggregations in WHERE clauses
- **Warning System**: Logs issues that need manual intervention

### Streaming Support (`streaming_utils.py`)

Progressive response streaming for better perceived performance:

- **Chunk Types**: query_progress, result_chunk, formatted_chunk, stream_complete
- **Result Streaming**: Sends results in configurable chunks (default: 5)
- **Progress Indicators**: Visual feedback during query generation
- **Formatted Streaming**: Progressive display of formatted responses
- **Metadata Support**: Includes chunk numbers and total counts

### WebSocket Enhancements

- **Connection Manager**: Tracks all active WebSocket connections
- **Heartbeat Mechanism**: 30-second ping/pong to prevent timeouts
- **Broadcast Support**: Dashboard updates to all connected clients
- **Graceful Disconnection**: Proper cleanup of resources
- **Structured Messages**: Type-based message routing (info, query, results, error, stream)

### Full-Text Search

The system supports full-text search across all indexed fields:
```cypher
CALL db.idx.fulltext.queryNodes('all_text_search', 'search_term') YIELD node, score
```

### Query Timeout Management

- AI Processing: 120 seconds (increased for complex queries)
- Database Queries: 15 seconds with graceful timeout handling
- Fallback Queries: Automatic retry with broader search on empty results
- Connection Timeouts: 10 seconds for initial FalkorDB connection

## Testing & Monitoring

### Available Test Scripts

```bash
# Test query patterns and semantic understanding
python backend/test_complete_flow.py

# Test dashboard API endpoints
python backend/test_dashboard_manual.py

# Test specific compliance queries
python backend/test_compliance_queries.py

# Test query processing and fixes
python backend/test_fixes.py

# Performance testing at scale
python backend/test_scale_performance.py

# Test Ollama direct integration
python backend/test_ollama_direct.py
```

### Monitoring & Debugging

1. **WebSocket Messages**: All WebSocket messages include type field for easy filtering
2. **Query Logging**: Cypher queries logged with execution time and results
3. **Error Tracking**: Detailed error messages with stack traces in debug mode
4. **Pattern Matching**: Logs show which pattern matched for each query
5. **Cache Hits**: Redis cache hits/misses logged for dashboard endpoints

### Health Endpoints

- **`/health`**: Basic health check
- **Dashboard metrics**: Real-time system performance at `/api/dashboard/metrics`