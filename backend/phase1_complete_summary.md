# Phase 1: LLM Model Baseline Performance Results

**Generated:** 2025-06-22T14:59:05.389968

## Executive Summary

- **Models Tested:** 9 of 9 attempted
- **Test Queries:** 10 queries across simple, medium, complex, and edge cases
- **Test Duration:** 17.4 minutes

## Model Performance Rankings

### By Speed (Average Response Time)

1. **phi3-mini:3.8b**
   - Average: 0.02s
   - P95: 0.02s
   - Throughput: 74.59 queries/sec
2. **deepseek-coder:1.3b**
   - Average: 0.85s
   - P95: 1.81s
   - Throughput: 0.26 queries/sec
3. **llama3.2:3b**
   - Average: 1.10s
   - P95: 2.20s
   - Throughput: 0.25 queries/sec
4. **granite-code:8b**
   - Average: 1.87s
   - P95: 3.71s
   - Throughput: 0.24 queries/sec
5. **mistral:7b**
   - Average: 2.03s
   - P95: 3.46s
   - Throughput: 0.24 queries/sec

### By Accuracy (Execution Success Rate)

1. **phi3-mini:3.8b**
   - Syntax Valid: 0.0%
   - Execution Success: 0.0%
   - Has Results: 0.0%
2. **deepseek-coder:1.3b**
   - Syntax Valid: 100.0%
   - Execution Success: 0.0%
   - Has Results: 0.0%
3. **llama3.2:3b**
   - Syntax Valid: 100.0%
   - Execution Success: 0.0%
   - Has Results: 0.0%
4. **granite-code:8b**
   - Syntax Valid: 90.0%
   - Execution Success: 0.0%
   - Has Results: 0.0%
5. **mistral:7b**
   - Syntax Valid: 90.0%
   - Execution Success: 0.0%
   - Has Results: 0.0%

### By Resource Efficiency (VRAM Usage)

1. **granite3.3:8b**
   - VRAM Usage: +-4078MB
   - Peak VRAM: 8871MB
   - Parameters: 8.2B
2. **llama3.2:3b**
   - VRAM Usage: +-1810MB
   - Peak VRAM: 10693MB
   - Parameters: 3.2B
3. **codeqwen:7b**
   - VRAM Usage: +-1648MB
   - Peak VRAM: 9576MB
   - Parameters: 7.3B
4. **phi3-mini:3.8b**
   - VRAM Usage: +10MB
   - Peak VRAM: 10703MB
5. **granite3.3:8b-largectx**
   - VRAM Usage: +1942MB
   - Peak VRAM: 10806MB
   - Parameters: 8.2B

## Top 3 Recommended Models for Phase 2

### 1. phi3-mini:3.8b (Score: 59.2/100)
- **Strengths:** Fast response time, Efficient VRAM usage
- **Performance:** 0.02s avg, 0.0% success
- **Resources:** 10MB VRAM
- **Recommendation:** Primary model for Phase 2 testing
### 2. deepseek-coder:1.3b (Score: 27.2/100)
- **Strengths:** Fast response time, Efficient VRAM usage
- **Performance:** 0.85s avg, 0.0% success
- **Resources:** 2616MB VRAM
- **Recommendation:** Strong alternative for comparison
### 3. granite-code:8b (Score: 16.7/100)
- **Strengths:** Fast response time, Efficient VRAM usage
- **Performance:** 1.87s avg, 0.0% success
- **Resources:** 6312MB VRAM
- **Recommendation:** Good backup option

## Detailed Metrics Comparison

| Model | Avg Time | P95 Time | Success Rate | VRAM Delta | Overall Score |
|-------|----------|----------|--------------|------------|---------------|
| phi3-mini:3.8b | 0.02s | 0.02s | 0.0% | 10MB | 59.2 |
| deepseek-coder:1.3b | 0.85s | 1.81s | 0.0% | 2616MB | 27.2 |
| granite-code:8b | 1.87s | 3.71s | 0.0% | 6312MB | 16.7 |
| mistral:7b | 2.03s | 3.46s | 0.0% | 5625MB | 16.2 |
| granite3.3:8b-largectx | 3.31s | 8.57s | 0.0% | 1942MB | 16.1 |
| phi4:14b | 3.85s | 6.46s | 0.0% | 10875MB | 9.9 |
| granite3.3:8b | 3.29s | 8.68s | 0.0% | -4078MB | 2.8 |
| llama3.2:3b | 1.10s | 2.20s | 0.0% | -1810MB | -5.6 |
| codeqwen:7b | 2.95s | 4.69s | 0.0% | -1648MB | -20.7 |
