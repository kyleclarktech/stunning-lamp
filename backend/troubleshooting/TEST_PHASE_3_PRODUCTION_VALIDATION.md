# Test Phase 3: Production Validation & Stress Testing

ultrathink use sequential thinking mcp, use memory mcp
## Objective
Validate the winning model-strategy combination from Phase 2 under production-like conditions, including stress testing, error recovery, and long-term stability.

## Prerequisites
- Completed Phase 2 testing
- Identified optimal model-strategy combination
- System resources available for stress testing

## Input from Phase 2
```python
# Example winning configuration from Phase 2
WINNING_CONFIG = {
    "model": "granite3.3:8b-largectx",
    "strategy": "enhanced_few_shot",
    "avg_response_time": 3.2,
    "success_rate": 0.96,
    "vram_usage": 8192
}

# Fallback configuration
FALLBACK_CONFIG = {
    "model": "phi4:14b",
    "strategy": "simple_current",
    "avg_response_time": 4.1,
    "success_rate": 0.94,
    "vram_usage": 14336
}
```

## Production Tests

### 1. Load Testing
- Concurrent users: 1, 5, 10, 20
- Query patterns: Real-world distribution
- Duration: 30 minutes per level
- Measure: Response time degradation, error rates

### 2. Stress Testing  
- Burst traffic: 50 queries in 10 seconds
- Sustained load: 5 queries/second for 1 hour
- Complex queries: Multi-hop graph traversals
- Memory pressure: Near VRAM limit operation

### 3. Reliability Testing
- Long-running test: 24-hour operation
- Connection failures: WebSocket disconnects
- Model crashes: Recovery behavior
- Database timeouts: Fallback mechanisms

### 4. Edge Case Validation
- Malformed queries
- Injection attempts
- Context overflow
- Concurrent model switching

## Test Implementation

Create `tools/test_phase3_production_validation.py`:

```python
#!/usr/bin/env python3
"""Phase 3: Production validation and stress testing."""

import asyncio
import json
import time
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any
import concurrent.futures

# Production-like query distribution
PRODUCTION_QUERY_MIX = {
    "simple_lookups": {
        "weight": 0.40,
        "queries": [
            "Who is on the {team} team?",
            "Find {role} in {department}",
            "Show me {name}'s details"
        ]
    },
    "policy_compliance": {
        "weight": 0.25,
        "queries": [
            "What are our {category} policies?",
            "Who owns {policy_area} compliance?",
            "Show {severity} severity policies"
        ]
    },
    "complex_analysis": {
        "weight": 0.20,
        "queries": [
            "Find all {skill} experts under {executive}",
            "Show cross-team dependencies for {project}",
            "Trace approval chain for {policy}"
        ]
    },
    "exploration": {
        "weight": 0.15,
        "queries": [
            "Show me the org structure",
            "Find similar people to {person}",
            "What teams work together most?"
        ]
    }
}

class ProductionSimulator:
    """Simulate production usage patterns."""
    
    async def generate_realistic_load(self, duration_minutes: int, qps: float):
        """Generate realistic query load."""
        # Implementation:
        # 1. Mix queries according to distribution
        # 2. Add random delays (human typing)
        # 3. Simulate session patterns
        # 4. Include think time between queries
        pass
    
    async def stress_test_bursts(self, burst_size: int, burst_duration: float):
        """Test burst traffic handling."""
        # Implementation:
        # 1. Generate burst_size queries
        # 2. Fire them within burst_duration
        # 3. Measure system response
        # 4. Check for failures/timeouts
        pass
    
    async def test_failure_recovery(self):
        """Test various failure scenarios."""
        # Scenarios:
        # 1. WebSocket disconnect mid-query
        # 2. Model OOM and restart
        # 3. Database connection timeout
        # 4. Corrupt query generation
        pass

async def run_load_test(config: Dict, concurrent_users: int, duration: int):
    """Run load test with specified concurrency."""
    results = {
        "config": config,
        "concurrent_users": concurrent_users,
        "duration_minutes": duration,
        "metrics": {
            "total_queries": 0,
            "successful_queries": 0,
            "failed_queries": 0,
            "response_times": [],
            "errors": []
        }
    }
    
    # Run concurrent user sessions
    # Collect metrics
    # Return comprehensive results
    return results

async def run_stress_test(config: Dict):
    """Run stress tests to find breaking points."""
    stress_results = {
        "burst_test": {},
        "sustained_load": {},
        "memory_pressure": {},
        "recovery_time": {}
    }
    
    # Test various stress scenarios
    # Find system limits
    # Document failure modes
    return stress_results

async def run_24h_stability_test(config: Dict):
    """Run 24-hour stability test."""
    # Run abbreviated version (2 hours) for testing
    # Monitor for memory leaks
    # Check performance degradation
    # Verify consistent behavior
    pass

async def main():
    """Run Phase 3 production validation."""
    print("PHASE 3: Production Validation & Stress Testing")
    print("=" * 60)
    
    # Load winning config from Phase 2
    with open("phase2_optimization_report.json", 'r') as f:
        phase2_results = json.load(f)
        winning_config = phase2_results["optimal_configuration"]
    
    results = {
        "phase": 3,
        "timestamp": datetime.now().isoformat(),
        "configuration": winning_config,
        "tests": {}
    }
    
    # 1. Load Testing
    print("\n1. LOAD TESTING")
    for users in [1, 5, 10, 20]:
        print(f"Testing with {users} concurrent users...")
        load_results = await run_load_test(winning_config, users, duration=30)
        results["tests"][f"load_{users}_users"] = load_results
    
    # 2. Stress Testing
    print("\n2. STRESS TESTING")
    stress_results = await run_stress_test(winning_config)
    results["tests"]["stress"] = stress_results
    
    # 3. Stability Testing (abbreviated)
    print("\n3. STABILITY TESTING (2-hour version)")
    stability_results = await run_24h_stability_test(winning_config)
    results["tests"]["stability"] = stability_results
    
    # Generate final report
    generate_production_readiness_report(results)
```

## Metrics to Monitor

### Performance Metrics
- **Response Time**: P50, P95, P99 percentiles
- **Throughput**: Successful queries per second
- **Error Rate**: Failures per 1000 queries
- **Recovery Time**: Time to recover from failures

### Resource Metrics
- **VRAM Usage**: Peak, average, trend over time
- **CPU Utilization**: Model inference vs system
- **Memory Leaks**: RSS growth over time
- **Connection Pool**: Active connections

### Quality Metrics
- **Query Accuracy**: Under load vs baseline
- **Timeout Rate**: Queries exceeding 15s
- **Fallback Usage**: How often fallback needed
- **Context Overflow**: Frequency of context clears

## Test Scenarios

### 1. Normal Load (Baseline)
```
Users: 5 concurrent
Rate: 1 query per user per 30s
Duration: 30 minutes
Expected: All queries < 5s
```

### 2. Peak Load
```
Users: 20 concurrent
Rate: 1 query per user per 15s  
Duration: 30 minutes
Expected: P95 < 10s, <5% errors
```

### 3. Burst Traffic
```
Burst: 50 queries in 10 seconds
Recovery: Measure time to normal
Expected: No crashes, <10% timeouts
```

### 4. Sustained Stress
```
Rate: 5 queries/second
Duration: 1 hour
Expected: Stable performance, no degradation
```

## Expected Output

### 1. Production Readiness Report
`phase3_production_ready.md` containing:
- Go/No-Go recommendation
- Performance under load graphs
- Failure mode documentation
- Scaling recommendations
- Monitoring requirements

### 2. Stress Test Results
`phase3_stress_results.json` with:
- Breaking points identified
- Resource limits discovered
- Recovery behavior documented
- Error patterns analyzed

### 3. Configuration Guide
`production_configuration.md` with:
```yaml
# Recommended Production Config
model: granite3.3:8b-largectx
prompting_strategy: enhanced_few_shot
max_concurrent_users: 15
timeout_seconds: 15
fallback_model: phi4:14b
monitoring:
  - response_time_p95
  - vram_usage_percent
  - error_rate
alerts:
  - response_time_p95 > 10s
  - vram_usage > 85%
  - error_rate > 5%
```

## Execution Instructions

1. **Prepare Environment**
   ```bash
   # Ensure clean state
   docker-compose down
   docker-compose up -d
   
   # Pre-load winning model
   docker exec stunning-lamp-ollama-1 ollama pull granite3.3:8b-largectx
   ```

2. **Run Production Tests**
   ```bash
   python tools/test_phase3_production_validation.py \
     --load-test \
     --stress-test \
     --stability-hours 2
   ```

3. **Monitor During Tests**
   ```bash
   # Terminal 1: Watch logs
   docker-compose logs -f api | grep -E "(ERROR|TIMEOUT|SUCCESS)"
   
   # Terminal 2: Monitor resources  
   watch -n 5 'nvidia-smi --query-gpu=memory.used,utilization.gpu --format=csv'
   
   # Terminal 3: Check Docker stats
   docker stats
   ```

## Success Criteria

Phase 3 validates production readiness if:

1. **Performance Requirements Met**
   - P95 response time < 10s under normal load
   - P99 response time < 15s under peak load
   - Zero crashes during stress tests

2. **Resource Usage Acceptable**
   - VRAM usage stays below 85%
   - No memory leaks detected
   - CPU usage sustainable

3. **Reliability Proven**
   - 99.5% uptime during tests
   - Graceful degradation under stress
   - Fast recovery from failures

4. **Quality Maintained**
   - Query accuracy > 95% under load
   - Fallback activation < 5%
   - User experience consistent

## Go/No-Go Decision

After Phase 3, make production deployment decision:

### GO Criteria
- All success criteria met
- No critical issues discovered
- Performance meets SLAs
- Resource usage sustainable

### NO-GO Triggers
- Crashes under normal load
- Memory leaks detected
- Performance degradation > 50%
- Recovery time > 5 minutes

## Next Steps

If GO:
1. Deploy winning configuration
2. Set up monitoring per recommendations
3. Configure alerts and runbooks
4. Plan capacity for growth

If NO-GO:
1. Analyze failure points
2. Try fallback configuration
3. Consider infrastructure upgrades
4. Re-run affected tests

## Final Deliverable

Complete production deployment package:
1. Tested configuration files
2. Deployment instructions
3. Monitoring setup guide
4. Troubleshooting runbook
5. Capacity planning data