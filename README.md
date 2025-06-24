# Stunning Lamp - AI-Powered Organizational Knowledge Graph

An intelligent conversational interface that leverages graph database technology and AI to help users navigate organizational information, policies, and relationships. Built with FalkorDB, Ollama, and modern web technologies.

## Features

- **Natural Language Queries**: Ask questions in plain English about your organization
- **Graph-Based Knowledge**: Navigate complex organizational relationships and policies
- **Real-Time Analytics**: Interactive dashboard with organizational metrics
- **AI-Powered Understanding**: Semantic query interpretation using local LLMs
- **WebSocket Communication**: Real-time bidirectional messaging
- **Extensible Architecture**: Easy to add new data types and query patterns

## Quick Start

```bash
# Clone the repository
git clone <repository-url>
cd stunning-lamp

# Start all services
docker-compose up -d

# Seed the database with sample data
docker exec -it stunning-lamp-api-1 python scripts/seed_data.py

# Access the application
# Frontend: http://localhost:5173
# API: http://localhost:8000
# FalkorDB UI: http://localhost:3000
```

## Architecture Overview

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Vue Frontend  │────▶│  FastAPI Backend │────▶│    FalkorDB     │
│   (Port 5173)   │◀────│   (Port 8000)    │◀────│   (Port 6379)   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                               │                          │
                               ▼                          ▼
                        ┌─────────────┐          ┌─────────────────┐
                        │   Ollama    │          │     Redis       │
                        │ (Port 11434)│          │  (Port 6380)    │
                        └─────────────┘          └─────────────────┘
```

## Key Components

### Frontend (Vue 3)
- **Chat Interface**: Natural language query interface
- **Dashboard**: Real-time organizational analytics
- **Technologies**: Vue 3, Vue Router, Chart.js, Leaflet, Axios

### Backend (FastAPI)
- **WebSocket Handler**: Real-time message processing
- **Query Processor**: Converts natural language to Cypher queries
- **Pattern Matcher**: Optimized handling of common queries
- **Dashboard API**: REST endpoints for analytics
- **Technologies**: FastAPI, Ollama, FalkorDB, Redis, Jinja2

### Database (FalkorDB)
- **Graph Structure**: Nodes for Person, Team, Group, Policy, Office, Skill, Project
- **Relationships**: MEMBER_OF, REPORTS_TO, RESPONSIBLE_FOR, WORKS_IN, HAS_SKILL
- **Performance**: Indexed properties, connection pooling, query optimization

### AI Model (Ollama)
- **Model**: granite3.3:8b-largectx (8192 context window)
- **Local Inference**: Privacy-preserving, no external API calls
- **Prompt Engineering**: Specialized templates for analysis, generation, and formatting

## Development

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for frontend development)
- Python 3.11+ (for backend development)
- NVIDIA GPU (optional, for accelerated inference)

### Local Development

```bash
# Backend development
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend development
cd frontend
npm install
npm run dev

# Run tests
cd backend
pytest tests/
```

### Environment Variables

Create `backend/.env`:
```env
OLLAMA_HOST=http://ollama:11434
OLLAMA_MODEL=granite3.3:8b-largectx
FALKOR_HOST=falkordb
FALKOR_PORT=6379
REDIS_HOST=redis
REDIS_PORT=6380
```

## Testing

```bash
# Run all backend tests
cd backend
pytest tests/

# Test specific functionality
pytest tests/test_websocket.py -v
pytest tests/test_semantic_queries.py -v

# Test query processing
python test_websocket.py
```

## Common Queries

The system understands natural language queries like:

- "Who works in engineering?"
- "Show me all compliance policies"
- "Find data protection policies and their owners"
- "Who reports to the CTO?"
- "What teams are in the technology department?"
- "Find experts in machine learning"

## Extending the System

### Adding New Query Patterns

1. Update `backend/prompts/analyze_message.txt` for intent recognition
2. Modify `backend/prompts/generate_query.txt` for query generation
3. Adjust `backend/prompts/format_results.txt` for result formatting
4. Optionally add patterns to `backend/query_patterns.py`

### Adding New Node Types

1. Update the schema in `backend/scripts/seed_data.py`
2. Modify prompt templates to recognize new entities
3. Add appropriate relationships and properties
4. Regenerate the database

## Performance Considerations

- **Query Timeout**: 15 seconds (configurable)
- **WebSocket Timeout**: 60 seconds for AI processing
- **Caching**: Redis with 60s TTL for dashboard queries
- **Connection Pooling**: Min 10, Max 50 connections
- **GPU Acceleration**: Automatic when NVIDIA GPU available

## Monitoring

- **Health Check**: `GET /health`
- **Metrics**: Available via dashboard API
- **Logs**: `docker-compose logs -f api`
- **Query Monitoring**: FalkorDB UI at http://localhost:3000

## Security

- CORS configuration for API access
- No external API calls (all processing local)
- Prepared statements for query safety
- Environment-based configuration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

[License information here]

## Acknowledgments

- FalkorDB for the graph database
- Ollama for local LLM inference
- Granite model by IBM Research