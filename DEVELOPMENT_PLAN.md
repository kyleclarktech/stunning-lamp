# Development Plan: Rich Dashboard, Import/Export, and API Gateway

## Executive Summary

This plan outlines the implementation of three major features for the FalkorDB-based B2B analytics platform:
1. **Rich Dashboard** - Real-time visualization of global operations
2. **Import/Export System** - Bulk data management capabilities
3. **API Gateway** - REST API with rate limiting and authentication

## Architecture Overview

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Vue.js SPA    │     │  FastAPI Backend │     │    FalkorDB     │
│  + Dashboard    │────▶│  + REST API      │────▶│  Graph Database │
│  + Import UI    │     │  + Rate Limiter  │     └─────────────────┘
└─────────────────┘     │  + Import/Export │
                        └──────────────────┘
```

## Phase 1: Rich Dashboard (Week 1-2)

### 1.1 Backend API Endpoints

Create new REST endpoints in `backend/api/` directory:

```python
# backend/api/dashboard.py
GET /api/dashboard/overview  # Global metrics summary
GET /api/dashboard/offices   # Office status with on-call data
GET /api/dashboard/incidents # Active incidents by severity
GET /api/dashboard/metrics   # Performance metrics timeseries
GET /api/dashboard/teams     # Team distribution data
GET /api/dashboard/visas     # Visa expiry timeline
```

### 1.2 Frontend Components

Create Vue components in `frontend/src/components/dashboard/`:

```
dashboard/
├── DashboardLayout.vue      # Main dashboard container
├── GlobalMap.vue            # Interactive world map (using Leaflet)
├── MetricsChart.vue         # Performance charts (using Chart.js)
├── IncidentBoard.vue        # Incident status cards
├── TeamDistribution.vue     # Team breakdown by office
├── VisaTimeline.vue         # Visa expiry gantt chart
└── KeyStats.vue             # Summary statistics cards
```

### 1.3 Real-time Updates

Extend WebSocket to broadcast dashboard updates:
- New message type: `dashboard_update`
- Push updates when incidents change or metrics update
- Client-side state management with Pinia store

### 1.4 Technical Stack
- **Maps**: Leaflet.js with OpenStreetMap
- **Charts**: Chart.js for metrics visualization
- **State**: Pinia for dashboard state management
- **Styling**: Tailwind CSS maintaining current theme

## Phase 2: Import/Export System (Week 2-3)

### 2.1 Import Functionality

```python
# backend/api/import_export.py
POST /api/import/employees   # Bulk employee import (CSV/JSON)
POST /api/import/validate    # Validate import data
GET  /api/import/template    # Download import templates
GET  /api/import/status/{id} # Check import job status
```

### 2.2 Export Functionality

```python
GET  /api/export/query       # Export query results
POST /api/export/schedule    # Create scheduled export
GET  /api/export/schedules   # List scheduled exports
GET  /api/export/download/{id} # Download export file
```

### 2.3 Data Processing Pipeline

```python
# backend/services/data_pipeline.py
class DataImporter:
    - validate_schema()
    - detect_changes()    # Incremental updates
    - apply_updates()     # Batch FalkorDB operations
    - rollback()          # Transaction safety

class DataExporter:
    - execute_query()
    - format_results()    # CSV, Excel, JSON
    - compress_large_files()
```

### 2.4 Scheduled Jobs

Using APScheduler for automated exports:
```python
# backend/services/scheduler.py
- Daily team rosters export
- Weekly performance metrics
- Monthly compliance reports
- Custom schedules via API
```

### 2.5 Frontend Import/Export UI

```
import-export/
├── ImportWizard.vue         # Multi-step import process
├── ExportBuilder.vue        # Query builder for exports
├── ScheduleManager.vue      # Manage scheduled exports
└── JobMonitor.vue          # Track import/export jobs
```

## Phase 3: API Gateway with Rate Limiting (Week 3-4)

### 3.1 Authentication & API Keys

```python
# backend/models/api_key.py
class APIKey:
    key: str
    name: str
    created_at: datetime
    rate_limit: int
    usage_quota: int
    scopes: List[str]

# backend/api/auth.py
POST /api/auth/keys          # Create API key
GET  /api/auth/keys          # List API keys
DELETE /api/auth/keys/{id}   # Revoke API key
```

### 3.2 Rate Limiting Implementation

```python
# backend/middleware/rate_limiter.py
class RateLimiter:
    - Redis-based rate limiting
    - Sliding window algorithm
    - Per-key limits
    - Global limits
    - Burst allowance
```

### 3.3 REST API Wrapper

Convert WebSocket functionality to REST:

```python
# backend/api/v1/
POST /api/v1/query           # Execute natural language query
POST /api/v1/cypher          # Execute raw Cypher query
GET  /api/v1/employees       # List employees with filters
GET  /api/v1/teams           # List teams
GET  /api/v1/incidents       # List incidents
GET  /api/v1/policies        # List policies
```

### 3.4 API Documentation

Auto-generated OpenAPI documentation:
```python
# backend/api/docs.py
- Swagger UI at /api/docs
- ReDoc at /api/redoc
- OpenAPI schema at /api/openapi.json
- Code examples for each endpoint
```

### 3.5 Usage Analytics

```python
# backend/services/analytics.py
class APIAnalytics:
    - Track requests per key
    - Response time metrics
    - Error rates
    - Popular endpoints
    - Usage patterns

# backend/api/analytics.py
GET /api/analytics/usage     # API usage statistics
GET /api/analytics/performance # Performance metrics
```

## Implementation Timeline

### Week 1: Dashboard Backend
- [ ] Create dashboard API endpoints
- [ ] Implement data aggregation queries
- [ ] Add WebSocket dashboard updates
- [ ] Write API tests

### Week 2: Dashboard Frontend
- [ ] Setup Pinia store
- [ ] Implement dashboard components
- [ ] Integrate Leaflet for maps
- [ ] Add Chart.js visualizations
- [ ] Connect to backend APIs

### Week 3: Import/Export Core
- [ ] Build data validation pipeline
- [ ] Implement CSV/JSON parsers
- [ ] Create export formatters
- [ ] Add scheduled job system
- [ ] Build import/export UI

### Week 4: API Gateway
- [ ] Implement API key management
- [ ] Add Redis rate limiting
- [ ] Create REST endpoints
- [ ] Generate API documentation
- [ ] Build usage analytics

## Technical Considerations

### Performance
- Cache dashboard queries in Redis
- Paginate large exports
- Stream large import files
- Use connection pooling for FalkorDB

### Security
- API key encryption
- Input validation for imports
- Rate limiting per IP and key
- Audit logging for all operations

### Scalability
- Horizontal scaling for API servers
- Redis cluster for rate limiting
- Background workers for import/export
- CDN for static dashboard assets

### Monitoring
- Prometheus metrics
- Grafana dashboards
- Error tracking with Sentry
- API performance monitoring

## Testing Strategy

### Unit Tests
- Dashboard query logic
- Import/export processors
- Rate limiting algorithms
- API key validation

### Integration Tests
- End-to-end import flows
- Export generation
- API authentication
- WebSocket updates

### Load Tests
- Dashboard with 1000+ concurrent users
- Bulk imports of 100k+ records
- API rate limiting under load
- Export generation performance

## Deployment Plan

1. **Development Environment**
   - Feature branches for each component
   - Docker Compose for local testing
   - Automated tests in CI/CD

2. **Staging Deployment**
   - Deploy features incrementally
   - Load testing
   - Security scanning
   - User acceptance testing

3. **Production Rollout**
   - Blue-green deployment
   - Feature flags for gradual rollout
   - Monitoring and alerting
   - Rollback procedures

## Success Metrics

- Dashboard load time < 2 seconds
- Import processing: 10k records/minute
- API response time < 200ms (p95)
- 99.9% uptime for API gateway
- Zero data loss during imports

## Next Steps

1. Review and approve development plan
2. Set up development branches
3. Begin Phase 1 implementation
4. Weekly progress reviews
5. Iterative testing and refinement