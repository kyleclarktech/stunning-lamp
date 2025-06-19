# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is an AI-powered conversational interface with FalkorDB graph database integration. The system uses Ollama for LLM inference and WebSocket connections for real-time communication. It processes natural language queries, generates Cypher queries, and formats results for task-oriented users.

## Commands

### Development Commands

```bash
# Start all services (API, Frontend, FalkorDB, Ollama)
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
# Test WebSocket connection and query processing
cd backend
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
docker exec -it stunning-lamp-api-1 python seed_data.py

# Initialize empty database
docker exec -it stunning-lamp-api-1 python init_db.py

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

2. **AI Analysis** (`analyze_message.txt` prompt)
   - Determines user intent (task-oriented vs conversational)
   - Selects appropriate tools: custom_query, search_database, pig_latin
   - Prioritizes policy discovery and organizational queries

3. **Query Generation** (`generate_query.txt` prompt)
   - Converts natural language to Cypher queries
   - Uses FalkorDB schema with Person, Team, Group, Policy nodes
   - Implements fallback queries for no-result scenarios

4. **Result Formatting** (`format_results.txt` prompt)
   - Formats query results for task completion
   - Emphasizes key contacts, policy owners, and next steps
   - Uses Markdown for structured presentation

### Key Components

- **Ollama Integration**: Local LLM inference using granite3.3:8b model
- **FalkorDB Schema**: Graph database with organizational data (People, Teams, Groups, Policies)
- **Prompt Templates**: Jinja2-based templates for AI model instructions
- **Real-time Communication**: WebSocket-based bidirectional messaging
- **Docker Composition**: Multi-service orchestration with health checks

### Data Model

- **Person**: Employees with roles, departments, managers
- **Team**: Departmental teams with specific focus areas  
- **Group**: Cross-functional groups (governance, technical, operational)
- **Policy**: Compliance and operational policies with severity levels
- **Relationships**: MEMBER_OF, REPORTS_TO, RESPONSIBLE_FOR

### Environment Configuration

```bash
# Required in backend/.env
OLLAMA_HOST=http://ollama:11434
OLLAMA_MODEL=granite3.3:8b
FALKOR_HOST=falkordb
FALKOR_PORT=6379
```

## Common Tasks

### Adding New Query Patterns

1. Update `backend/prompts/analyze_message.txt` to recognize new patterns
2. Modify `backend/prompts/generate_query.txt` for Cypher query generation
3. Adjust `backend/prompts/format_results.txt` for result presentation

### Modifying the Schema

1. Update seed data generation in `backend/seed_data.py`
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
- Async execution for database operations