# Global Operations Test Query Suite

## Overview
This document contains 50+ test queries organized by operational requirement. Each query includes:
- Current system support status (✅ Supported, ⚠️ Partial, ❌ Not Supported)
- Required schema enhancements
- Expected results format
- Performance targets

---

## 1. Cross-Timezone Resource Management Queries (15 queries)

### 1.1 Basic Timezone Queries

#### Q1: Find all employees in a specific timezone
**Status:** ✅ Supported
```cypher
MATCH (p:Person)
WHERE p.timezone = 'US/Pacific'
RETURN p.name, p.role, p.department
ORDER BY p.department, p.name
```

#### Q2: Count employees by timezone
**Status:** ✅ Supported
```cypher
MATCH (p:Person)
RETURN p.timezone, count(p) as employee_count
ORDER BY employee_count DESC
```

#### Q3: Find employees available during specific hours across timezones
**Status:** ❌ Not Supported (Requires Office entity with business hours)
```cypher
// Proposed query after enhancement
MATCH (p:Person)-[:WORKS_AT]->(o:Office)
WHERE time() >= o.business_hours_start 
  AND time() <= o.business_hours_end
RETURN p.name, p.timezone, o.business_hours_start, o.business_hours_end
```

### 1.2 Language-Based Resource Queries

#### Q4: Find employees who speak specific languages
**Status:** ❌ Not Supported (Requires Language entity)
```cypher
// Proposed query after enhancement
MATCH (p:Person)-[:SPEAKS {proficiency: 'fluent'}]->(l:Language)
WHERE l.code IN ['en', 'de', 'fr']
RETURN p.name, collect(l.name) as languages
```

#### Q5: Find multilingual support teams
**Status:** ❌ Not Supported
```cypher
// Proposed query after enhancement
MATCH (t:Team)<-[:MEMBER_OF]-(p:Person)-[:SPEAKS]->(l:Language)
WITH t, count(DISTINCT l.code) as language_count, collect(DISTINCT l.name) as languages
WHERE language_count >= 3
RETURN t.name, languages, language_count
```

#### Q6: Find native speakers for customer support
**Status:** ❌ Not Supported
```cypher
// Proposed query after enhancement
MATCH (c:Client)-[:REQUIRES_LANGUAGE]->(l:Language)
MATCH (p:Person)-[:SPEAKS {proficiency: 'native'}]->(l)
WHERE p.department = 'Customer Success'
RETURN c.name, l.name, collect(p.name) as native_speakers
```

### 1.3 Holiday and Availability Queries

#### Q7: Find employees working today (considering holidays)
**Status:** ❌ Not Supported (Requires Holiday entity)
```cypher
// Proposed query after enhancement
MATCH (p:Person)-[:WORKS_AT]->(o:Office)
WHERE NOT EXISTS {
    MATCH (h:Holiday)
    WHERE o.id IN h.offices AND h.date = date()
}
RETURN p.name, o.name, o.country
```

#### Q8: Calculate team availability for next week
**Status:** ❌ Not Supported
```cypher
// Proposed query after enhancement
MATCH (t:Team)<-[:MEMBER_OF]-(p:Person)-[:WORKS_AT]->(o:Office)
WITH t, p, o
MATCH (h:Holiday)
WHERE o.id IN h.offices 
  AND h.date >= date() 
  AND h.date <= date() + duration('P7D')
WITH t, count(DISTINCT h.date) as holiday_days, count(DISTINCT p) as team_size
RETURN t.name, team_size * 5 - (team_size * holiday_days) as available_person_days
```

### 1.4 Visa and Work Authorization Queries

#### Q9: Find employees with work authorization for specific countries
**Status:** ❌ Not Supported (Requires visa tracking)
```cypher
// Proposed query after enhancement
MATCH (p:Person)-[:HAS_VISA {status: 'valid'}]->(country:Country)
WHERE country.code = 'DE' 
  AND p.visa_expiry > date() + duration('P30D')
RETURN p.name, p.visa_type, p.visa_expiry
```

#### Q10: Alert on expiring work visas
**Status:** ❌ Not Supported
```cypher
// Proposed query after enhancement
MATCH (p:Person)-[v:HAS_VISA]->(c:Country)
WHERE v.expires <= date() + duration('P90D')
  AND v.expires > date()
RETURN p.name, c.name, v.type, v.expires, 
       duration.between(date(), v.expires).days as days_until_expiry
ORDER BY days_until_expiry
```

### 1.5 Cross-Office Collaboration Queries

#### Q11: Find overlapping work hours between offices
**Status:** ❌ Not Supported (Requires Office entity)
```cypher
// Proposed query after enhancement
MATCH (o1:Office), (o2:Office)
WHERE o1.id <> o2.id
WITH o1, o2, 
     CASE 
       WHEN o1.business_hours_end_utc > o2.business_hours_start_utc 
        AND o1.business_hours_start_utc < o2.business_hours_end_utc
       THEN true 
       ELSE false 
     END as has_overlap
WHERE has_overlap
RETURN o1.name, o2.name, 
       o1.timezone, o2.timezone,
       o1.business_hours_start, o2.business_hours_start
```

#### Q12: Find teams distributed across multiple timezones
**Status:** ⚠️ Partial
```cypher
MATCH (t:Team)<-[:MEMBER_OF]-(p:Person)
WITH t, collect(DISTINCT p.timezone) as timezones, count(DISTINCT p.timezone) as tz_count
WHERE tz_count >= 3
RETURN t.name, timezones, tz_count
ORDER BY tz_count DESC
```

#### Q13: Identify follow-the-sun capable teams
**Status:** ❌ Not Supported
```cypher
// Proposed query after enhancement
MATCH (t:Team)<-[:MEMBER_OF]-(p:Person)-[:WORKS_AT]->(o:Office)
WITH t, 
     sum(CASE WHEN o.region = 'AMERICAS' THEN 1 ELSE 0 END) as americas_count,
     sum(CASE WHEN o.region = 'EMEA' THEN 1 ELSE 0 END) as emea_count,
     sum(CASE WHEN o.region = 'APAC' THEN 1 ELSE 0 END) as apac_count
WHERE americas_count >= 2 AND emea_count >= 2 AND apac_count >= 2
RETURN t.name, americas_count, emea_count, apac_count
```

#### Q14: Find closest timezone colleagues for handoffs
**Status:** ❌ Not Supported
```cypher
// Proposed query after enhancement
MATCH (p1:Person {id: $person_id})-[:WORKS_AT]->(o1:Office)
MATCH (p2:Person)-[:WORKS_AT]->(o2:Office)
WHERE p1 <> p2
  AND abs(o1.timezone_offset - o2.timezone_offset) <= 3
  AND (p1)-[:WORKS_WITH]-(p2)
RETURN p2.name, o2.timezone, abs(o1.timezone_offset - o2.timezone_offset) as hour_difference
ORDER BY hour_difference
LIMIT 10
```

#### Q15: Calculate global meeting time optimization
**Status:** ❌ Not Supported
```cypher
// Proposed query after enhancement
MATCH (p:Person)-[:WORKS_AT]->(o:Office)
WHERE p.id IN $participant_ids
WITH collect({
  person: p.name, 
  timezone: o.timezone,
  business_start: o.business_hours_start,
  business_end: o.business_hours_end
}) as participants
RETURN findOptimalMeetingTime(participants) as optimal_time_utc
```

---

## 2. Global Project Coordination Queries (12 queries)

### 2.1 Multi-Region Project Queries

#### Q16: Find projects spanning multiple regions
**Status:** ❌ Not Supported (Projects lack regional assignment)
```cypher
// Proposed query after enhancement
MATCH (proj:Project)-[:DEPLOYED_IN]->(o:Office)
WITH proj, collect(DISTINCT o.region) as regions
WHERE size(regions) > 1
RETURN proj.name, regions, size(regions) as region_count
```

#### Q17: Identify project teams by timezone coverage
**Status:** ⚠️ Partial
```cypher
MATCH (proj:Project)<-[:ALLOCATED_TO]-(p:Person)
WITH proj, collect(DISTINCT p.timezone) as timezones
RETURN proj.name, timezones, size(timezones) as timezone_coverage
ORDER BY timezone_coverage DESC
```

#### Q18: Find projects needing regional expertise
**Status:** ❌ Not Supported
```cypher
// Proposed query after enhancement
MATCH (proj:Project)-[:DEPLOYED_IN]->(o:Office {region: 'APAC'})
WHERE NOT EXISTS {
    MATCH (proj)<-[:ALLOCATED_TO]-(p:Person)-[:WORKS_AT]->(o2:Office {region: 'APAC'})
}
RETURN proj.name, 'APAC' as missing_regional_expertise
```

### 2.2 Resource Allocation Queries

#### Q19: Find available experts for global project staffing
**Status:** ⚠️ Partial
```cypher
MATCH (p:Person)-[:HAS_SKILL]->(s:Skill)<-[:REQUIRES_SKILL]-(proj:Project)
WHERE p.current_utilization < 80
  AND proj.status = 'planning'
WITH proj, p, count(s) as matching_skills
RETURN proj.name, p.name, p.timezone, p.current_utilization, matching_skills
ORDER BY matching_skills DESC
```

#### Q20: Balance project allocation across timezones
**Status:** ❌ Not Supported
```cypher
// Proposed query after enhancement
MATCH (proj:Project {status: 'planning'})
MATCH (p:Person)-[:HAS_SKILL]->(s:Skill)<-[:REQUIRES_SKILL]-(proj)
WITH proj, p.timezone as tz, count(p) as available_people
WITH proj, collect({timezone: tz, count: available_people}) as tz_distribution
RETURN proj.name, tz_distribution, 
       calculateTimezoneBalance(tz_distribution) as balance_score
```

#### Q21: Find cross-functional teams for global initiatives
**Status:** ✅ Supported
```cypher
MATCH (g:Group {type: 'strategic'})
MATCH (p:Person)-[:MEMBER_OF]->(g)
WITH g, collect(DISTINCT p.department) as departments, count(p) as member_count
WHERE size(departments) >= 4
RETURN g.name, departments, member_count
```

### 2.3 Handoff and Collaboration Queries

#### Q22: Identify handoff gaps in project coverage
**Status:** ❌ Not Supported
```cypher
// Proposed query after enhancement
MATCH (proj:Project)<-[:ALLOCATED_TO]-(p:Person)-[:WORKS_AT]->(o:Office)
WITH proj, o.timezone_offset as tz_offset, count(p) as people_count
ORDER BY proj.name, tz_offset
WITH proj, collect(tz_offset) as covered_offsets
WHERE NOT all(i in range(0, 23) WHERE 
    any(offset in covered_offsets WHERE abs(offset - i) <= 4))
RETURN proj.name, covered_offsets, 'Coverage gap detected' as issue
```

#### Q23: Find optimal project meeting times
**Status:** ❌ Not Supported
```cypher
// Proposed query after enhancement
MATCH (proj:Project)<-[:ALLOCATED_TO]-(p:Person)-[:WORKS_AT]->(o:Office)
WITH proj, collect({
    person: p.name,
    timezone: o.timezone,
    start: o.business_hours_start,
    end: o.business_hours_end
}) as team_members
RETURN proj.name, 
       calculateOptimalMeetingWindow(team_members) as meeting_window_utc
```

### 2.4 Deployment and Rollout Queries

#### Q24: Plan phased global rollout by timezone
**Status:** ❌ Not Supported
```cypher
// Proposed query after enhancement
MATCH (proj:Project {type: 'platform'})
MATCH (o:Office)
WITH proj, o
ORDER BY o.timezone_offset
RETURN proj.name, 
       o.name, 
       o.timezone,
       o.timezone_offset,
       CASE 
         WHEN o.timezone_offset <= -8 THEN 'Phase 1 - Americas West'
         WHEN o.timezone_offset <= -5 THEN 'Phase 2 - Americas East'
         WHEN o.timezone_offset <= 1 THEN 'Phase 3 - EMEA'
         ELSE 'Phase 4 - APAC'
       END as rollout_phase
```

#### Q25: Identify regional deployment dependencies
**Status:** ❌ Not Supported
```cypher
// Proposed query after enhancement
MATCH (proj:Project)-[:DEPENDS_ON]->(dep:Project)
MATCH (proj)-[:DEPLOYED_IN]->(o1:Office)
MATCH (dep)-[:DEPLOYED_IN]->(o2:Office)
WHERE o1.region <> o2.region
RETURN proj.name, dep.name, o1.region, o2.region, 'Cross-region dependency' as issue
```

#### Q26: Calculate regional project capacity
**Status:** ❌ Not Supported
```cypher
// Proposed query after enhancement
MATCH (o:Office)
MATCH (p:Person)-[:WORKS_AT]->(o)
WHERE p.role CONTAINS 'Engineer'
WITH o.region as region, 
     sum(p.capacity_hours_per_week * (100 - p.current_utilization) / 100) as available_hours
RETURN region, available_hours, available_hours / 40 as available_fte
ORDER BY available_hours DESC
```

#### Q27: Find projects at risk due to timezone gaps
**Status:** ❌ Not Supported
```cypher
// Proposed query after enhancement
MATCH (proj:Project {status: 'active'})
MATCH (proj)<-[:ALLOCATED_TO]-(p:Person)
WITH proj, collect(p.timezone) as timezones
WHERE NOT ('US/Pacific' IN timezones AND 'Europe/London' IN timezones)
   OR NOT ('Europe/London' IN timezones AND 'Asia/Singapore' IN timezones)
RETURN proj.name, timezones, 'Missing timezone coverage for 24/7 support' as risk
```

---

## 3. Regional Compliance Tracking Queries (10 queries)

### 3.1 Compliance Framework Queries

#### Q28: Find policies by compliance framework
**Status:** ⚠️ Partial
```cypher
MATCH (p:Policy)
WHERE 'GDPR' IN split(p.compliance_frameworks, ',')
RETURN p.name, p.category, p.severity
ORDER BY p.severity DESC
```

#### Q29: Map compliance requirements to regions
**Status:** ❌ Not Supported (Requires Compliance entity)
```cypher
// Proposed query after enhancement
MATCH (c:Compliance)-[:APPLIES_TO]->(o:Office)
WITH c, collect(o.region) as regions
RETURN c.framework, c.jurisdiction, regions
ORDER BY c.framework
```

#### Q30: Identify compliance gaps by region
**Status:** ❌ Not Supported
```cypher
// Proposed query after enhancement
MATCH (o:Office)
MATCH (c:Compliance {enforcement_level: 'mandatory'})
WHERE o.country IN c.applicable_countries
  AND NOT EXISTS((o)-[:IMPLEMENTS]->(c))
RETURN o.name, o.country, collect(c.framework) as missing_compliance
```

### 3.2 Data Residency Queries

#### Q31: Verify data residency compliance
**Status:** ❌ Not Supported
```cypher
// Proposed query after enhancement
MATCH (c:Client)-[:REQUIRES_COMPLIANCE]->(comp:Compliance {type: 'data_residency'})
MATCH (c)<-[:FOR_CLIENT]-(proj:Project)-[:STORES_DATA_IN]->(o:Office)
WHERE o.data_residency_zone <> comp.required_zone
RETURN c.name, proj.name, comp.required_zone, o.data_residency_zone as actual_zone
```

#### Q32: Find cross-border data transfers
**Status:** ❌ Not Supported
```cypher
// Proposed query after enhancement
MATCH (p1:Project)-[:TRANSFERS_DATA_TO]->(p2:Project)
MATCH (p1)-[:DEPLOYED_IN]->(o1:Office)
MATCH (p2)-[:DEPLOYED_IN]->(o2:Office)
WHERE o1.country <> o2.country
RETURN p1.name, p2.name, o1.country, o2.country, 
       checkDataTransferCompliance(o1.country, o2.country) as compliance_status
```

### 3.3 Audit and Tracking Queries

#### Q33: Generate compliance audit trail by region
**Status:** ❌ Not Supported
```cypher
// Proposed query after enhancement
MATCH (audit:AuditLog)-[:PERFORMED_BY]->(p:Person)-[:WORKS_AT]->(o:Office)
WHERE audit.timestamp >= datetime() - duration('P30D')
  AND audit.action_type IN ['data_access', 'data_modification', 'data_export']
RETURN o.region, audit.action_type, count(*) as action_count
ORDER BY o.region, action_count DESC
```

#### Q34: Track policy implementation status by office
**Status:** ❌ Not Supported
```cypher
// Proposed query after enhancement
MATCH (o:Office)
MATCH (p:Policy {severity: 'critical'})
OPTIONAL MATCH (o)-[impl:IMPLEMENTS]->(p)
RETURN o.name, p.name, 
       CASE WHEN impl IS NOT NULL THEN 'Implemented' ELSE 'Not Implemented' END as status,
       impl.implementation_date
ORDER BY o.name, p.severity DESC
```

#### Q35: Find employees needing compliance training
**Status:** ❌ Not Supported
```cypher
// Proposed query after enhancement
MATCH (p:Person)-[:WORKS_AT]->(o:Office)-[:OPERATES_UNDER]->(c:Compliance)
WHERE NOT EXISTS((p)-[:COMPLETED_TRAINING]->(c))
  OR EXISTS {
    MATCH (p)-[t:COMPLETED_TRAINING]->(c)
    WHERE t.completion_date < datetime() - duration('P365D')
  }
RETURN p.name, o.name, collect(c.framework) as required_training
```

#### Q36: Monitor compliance violations by region
**Status:** ❌ Not Supported
```cypher
// Proposed query after enhancement
MATCH (v:Violation)-[:VIOLATES]->(c:Compliance)
MATCH (v)-[:OCCURRED_IN]->(o:Office)
WHERE v.timestamp >= datetime() - duration('P90D')
WITH o.region as region, c.framework, count(v) as violation_count
RETURN region, c.framework, violation_count
ORDER BY violation_count DESC
```

#### Q37: Calculate compliance risk score by project
**Status:** ❌ Not Supported
```cypher
// Proposed query after enhancement
MATCH (proj:Project)-[:DEPLOYED_IN]->(o:Office)
MATCH (o)-[:OPERATES_UNDER]->(c:Compliance)
WITH proj, count(c) as compliance_count,
     sum(CASE WHEN (proj)-[:COMPLIANT_WITH]->(c) THEN 0 ELSE 1 END) as non_compliant_count
RETURN proj.name, 
       compliance_count,
       non_compliant_count,
       toFloat(non_compliant_count) / compliance_count * 100 as risk_score
ORDER BY risk_score DESC
```

---

## 4. SaaS Operational Queries (13 queries)

### 4.1 24/7 Coverage Queries

#### Q38: Analyze on-call coverage by timezone
**Status:** ❌ Not Supported (Requires on-call scheduling)
```cypher
// Proposed query after enhancement
MATCH (s:Schedule {type: 'on_call', week: date().week})
MATCH (p:Person)-[:ASSIGNED_TO]->(s)
WITH s.timeslot as timeslot, collect(p.timezone) as timezones
RETURN timeslot, timezones, size(timezones) as coverage_diversity
ORDER BY timeslot
```

#### Q39: Find gaps in 24/7 support coverage
**Status:** ❌ Not Supported
```cypher
// Proposed query after enhancement
WITH range(0, 23) as hours
UNWIND hours as hour
OPTIONAL MATCH (p:Person)-[:ON_CALL_DURING]->(t:TimeSlot {hour: hour})
WHERE p.department = 'Customer Success'
WITH hour, count(p) as coverage_count
WHERE coverage_count < 2
RETURN hour, coverage_count, '⚠️ Insufficient coverage' as alert
```

#### Q40: Calculate incident response readiness
**Status:** ❌ Not Supported
```cypher
// Proposed query after enhancement
MATCH (sev:Severity)
MATCH (p:Person)-[:CAN_HANDLE]->(sev)
WITH sev.level as severity, p.timezone as timezone, count(p) as responder_count
WITH severity, 
     collect({timezone: timezone, count: responder_count}) as coverage
RETURN severity, coverage,
       CASE 
         WHEN ALL(tz IN ['US/Pacific', 'Europe/London', 'Asia/Singapore'] 
                WHERE ANY(c IN coverage WHERE c.timezone = tz AND c.count >= 2))
         THEN '✅ Full Coverage'
         ELSE '❌ Coverage Gap'
       END as status
```

### 4.2 Platform Reliability Queries

#### Q41: Monitor SLA compliance by region
**Status:** ❌ Not Supported
```cypher
// Proposed query after enhancement
MATCH (sla:SLA)-[:APPLIES_TO]->(c:Client)-[:LOCATED_IN]->(region:Region)
MATCH (m:Metric {type: 'uptime'})-[:FOR_CLIENT]->(c)
WHERE m.period = 'last_30_days'
WITH region.name as region, sla.target_uptime as target, avg(m.value) as actual_uptime
RETURN region, target, actual_uptime, 
       CASE WHEN actual_uptime >= target THEN '✅ Met' ELSE '❌ Missed' END as sla_status
```

#### Q42: Find critical services without redundancy
**Status:** ❌ Not Supported
```cypher
// Proposed query after enhancement
MATCH (s:Service {criticality: 'high'})
MATCH (s)-[:DEPLOYED_IN]->(o:Office)
WITH s, count(DISTINCT o.region) as region_count
WHERE region_count < 2
RETURN s.name, region_count, 'Needs multi-region deployment' as recommendation
```

#### Q43: Calculate team capacity for incident response
**Status:** ⚠️ Partial
```cypher
MATCH (t:Team {focus: 'incident response'})
MATCH (p:Person)-[:MEMBER_OF]->(t)
WHERE p.current_utilization < 100
RETURN t.name, 
       count(p) as available_members,
       avg(100 - p.current_utilization) as avg_available_capacity
```

### 4.3 Customer Success Queries

#### Q44: Map customer success coverage by region
**Status:** ❌ Not Supported
```cypher
// Proposed query after enhancement
MATCH (c:Client)-[:LOCATED_IN]->(region:Region)
OPTIONAL MATCH (c)<-[:MANAGES]-(csm:Person {role: 'Customer Success Manager'})
WITH region.name as region, 
     count(c) as client_count,
     count(csm) as csm_count
RETURN region, client_count, csm_count, 
       toFloat(client_count) / CASE WHEN csm_count = 0 THEN 1 ELSE csm_count END as clients_per_csm
ORDER BY clients_per_csm DESC
```

#### Q45: Find language gaps in customer support
**Status:** ❌ Not Supported
```cypher
// Proposed query after enhancement
MATCH (c:Client)-[:REQUIRES_LANGUAGE]->(l:Language)
WITH l, count(c) as client_demand
OPTIONAL MATCH (p:Person)-[:SPEAKS {proficiency: 'fluent'}]->(l)
WHERE p.department = 'Customer Success'
WITH l.name as language, client_demand, count(p) as support_capacity
WHERE support_capacity < client_demand * 0.2  // Need at least 1 support per 5 clients
RETURN language, client_demand, support_capacity, 'Language gap' as issue
```

#### Q46: Analyze customer timezone distribution
**Status:** ❌ Not Supported
```cypher
// Proposed query after enhancement
MATCH (c:Client)-[:LOCATED_IN]->(o:Office)
WITH o.timezone as timezone, count(c) as client_count, sum(c.annual_value) as total_value
RETURN timezone, client_count, total_value, total_value / client_count as avg_value
ORDER BY total_value DESC
```

### 4.4 Performance and Optimization Queries

#### Q47: Identify performance bottlenecks by region
**Status:** ❌ Not Supported
```cypher
// Proposed query after enhancement
MATCH (m:Metric {type: 'response_time'})
MATCH (m)-[:MEASURED_IN]->(o:Office)
WHERE m.timestamp >= datetime() - duration('P7D')
WITH o.region as region, percentileCont(m.value, 0.95) as p95_latency
WHERE p95_latency > 500  // milliseconds
RETURN region, p95_latency, 'Performance issue' as alert
ORDER BY p95_latency DESC
```

#### Q48: Calculate cost efficiency by office
**Status:** ❌ Not Supported
```cypher
// Proposed query after enhancement
MATCH (o:Office)
MATCH (p:Person)-[:WORKS_AT]->(o)
MATCH (c:Client)-[:SERVICED_BY]->(o)
WITH o.name as office,
     sum(p.billing_rate * 40 * 4) as monthly_cost,
     sum(c.annual_value / 12) as monthly_revenue
RETURN office, monthly_cost, monthly_revenue, 
       monthly_revenue / monthly_cost as efficiency_ratio
ORDER BY efficiency_ratio DESC
```

#### Q49: Find underutilized global resources
**Status:** ✅ Supported
```cypher
MATCH (p:Person)
WHERE p.current_utilization < 50
RETURN p.name, p.department, p.timezone, p.current_utilization
ORDER BY p.current_utilization
LIMIT 20
```

#### Q50: Optimize global resource distribution
**Status:** ❌ Not Supported
```cypher
// Proposed query after enhancement
MATCH (demand:ResourceDemand)-[:FOR_REGION]->(r:Region)
MATCH (p:Person)-[:WORKS_AT]->(o:Office {region: r.name})
WHERE p.current_utilization < 80
WITH r.name as region, 
     demand.required_hours as demand,
     sum((100 - p.current_utilization) * p.capacity_hours_per_week / 100) as supply
RETURN region, demand, supply, 
       CASE 
         WHEN supply >= demand THEN '✅ Balanced'
         WHEN supply >= demand * 0.8 THEN '⚠️ Tight'
         ELSE '❌ Shortage'
       END as status
```

---

## Performance Benchmarks

### Query Categories and Expected Performance

| Category | Simple Queries | Complex Queries | Aggregation Queries |
|----------|---------------|-----------------|-------------------|
| Target | < 100ms | < 500ms | < 1000ms |
| Current System | ✅ Likely | ❓ Unknown | ❓ Unknown |
| Enhanced System | ✅ Expected | ✅ Expected | ⚠️ Needs optimization |

### Critical Indexes Required
```cypher
// Core indexes for global operations
CREATE INDEX ON :Person(timezone)
CREATE INDEX ON :Person(current_utilization)
CREATE INDEX ON :Office(region)
CREATE INDEX ON :Office(country)
CREATE INDEX ON :Office(timezone)
CREATE INDEX ON :Language(code)
CREATE INDEX ON :Compliance(framework)
CREATE INDEX ON :Compliance(jurisdiction)
CREATE INDEX ON :Holiday(date)
CREATE INDEX ON :Project(status)
CREATE INDEX ON :Client(tier)

// Composite indexes for complex queries
CREATE INDEX ON :Person(department, timezone)
CREATE INDEX ON :Project(status, priority)
CREATE INDEX ON :Policy(severity, category)
```

---

## Summary

### Current System Query Support
- **Fully Supported**: 8/50 queries (16%)
- **Partially Supported**: 5/50 queries (10%)
- **Not Supported**: 37/50 queries (74%)

### After Enhancement Query Support
- **Expected Full Support**: 50/50 queries (100%)
- **Performance Risk**: 5/50 queries may need optimization

### Critical Missing Capabilities
1. **Office/Location Management**: Blocks 15+ queries
2. **Language Support**: Blocks 6+ queries
3. **Compliance Tracking**: Blocks 10+ queries
4. **Holiday/Availability**: Blocks 8+ queries
5. **On-call/Coverage**: Blocks 5+ queries

### Recommended Implementation Priority
1. **Phase 1**: Office and Language entities (enables 21 queries)
2. **Phase 2**: Compliance and Holiday entities (enables 18 queries)
3. **Phase 3**: Schedule and Metric entities (enables 11 queries)
4. **Phase 4**: Performance optimization and advanced features