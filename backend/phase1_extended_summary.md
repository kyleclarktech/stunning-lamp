# Phase 1: LLM Model Baseline Performance Results

**Generated:** 2025-06-22T14:20:28.390036

## Executive Summary

- **Models Tested:** 4 of 4 attempted
- **Test Queries:** 10 queries across simple, medium, complex, and edge cases
- **Test Duration:** N/A

## Model Performance Rankings

### By Speed (Average Response Time)

1. **qwen2.5-coder:7b**
   - Average: 1.67s
   - P95: 2.97s
   - Throughput: 0.23 queries/sec
2. **granite3.3:8b**
   - Average: 3.29s
   - P95: 8.68s
   - Throughput: 0.21 queries/sec
3. **granite3.3:8b-largectx**
   - Average: 3.31s
   - P95: 8.57s
   - Throughput: 0.21 queries/sec
4. **phi4:14b**
   - Average: 3.85s
   - P95: 6.46s
   - Throughput: 0.18 queries/sec

### By Accuracy (Execution Success Rate)

1. **qwen2.5-coder:7b**
   - Syntax Valid: 100.0%
   - Execution Success: 0.0%
   - Has Results: 0.0%
2. **granite3.3:8b**
   - Syntax Valid: 90.0%
   - Execution Success: 0.0%
   - Has Results: 0.0%
3. **granite3.3:8b-largectx**
   - Syntax Valid: 100.0%
   - Execution Success: 0.0%
   - Has Results: 0.0%
4. **phi4:14b**
   - Syntax Valid: 90.0%
   - Execution Success: 0.0%
   - Has Results: 0.0%

### By Resource Efficiency (VRAM Usage)

1. **granite3.3:8b**
   - VRAM Usage: +-4078MB
   - Peak VRAM: 8871MB
   - Parameters: 8.2B
2. **granite3.3:8b-largectx**
   - VRAM Usage: +1942MB
   - Peak VRAM: 10806MB
   - Parameters: 8.2B
3. **qwen2.5-coder:7b**
   - VRAM Usage: +5576MB
   - Peak VRAM: 7421MB
   - Parameters: 7.6B
4. **phi4:14b**
   - VRAM Usage: +10875MB
   - Peak VRAM: 12934MB
   - Parameters: 14.7B

## Top 3 Recommended Models for Phase 2

### 1. qwen2.5-coder:7b (Score: 18.0/100)
- **Strengths:** Fast response time, Efficient VRAM usage
- **Performance:** 1.67s avg, 0.0% success
- **Resources:** 5576MB VRAM
- **Recommendation:** Primary model for Phase 2 testing
### 2. granite3.3:8b-largectx (Score: 16.1/100)
- **Strengths:** Fast response time, Efficient VRAM usage
- **Performance:** 3.31s avg, 0.0% success
- **Resources:** 1942MB VRAM
- **Recommendation:** Strong alternative for comparison
### 3. phi4:14b (Score: 9.9/100)
- **Strengths:** Fast response time
- **Performance:** 3.85s avg, 0.0% success
- **Resources:** 10875MB VRAM
- **Recommendation:** Good backup option

## Detailed Metrics Comparison

| Model | Avg Time | P95 Time | Success Rate | VRAM Delta | Overall Score |
|-------|----------|----------|--------------|------------|---------------|
| qwen2.5-coder:7b | 1.67s | 2.97s | 0.0% | 5576MB | 18.0 |
| granite3.3:8b-largectx | 3.31s | 8.57s | 0.0% | 1942MB | 16.1 |
| phi4:14b | 3.85s | 6.46s | 0.0% | 10875MB | 9.9 |
| granite3.3:8b | 3.29s | 8.68s | 0.0% | -4078MB | 2.8 |
