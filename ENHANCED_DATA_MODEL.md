# Enhanced Data Model for Project Management & Capacity Planning

## Overview

The data model has been significantly enhanced to support comprehensive project management, capacity planning, and resource allocation capabilities. These enhancements enable sophisticated queries for finding available resources, matching skills to project needs, and tracking capacity utilization.

## New Entity Types

### 1. **Skill**
Technical skills, certifications, and domain expertise
- **Attributes**: id, name, category (programming, cloud, data, ml, devops, database, domain, certification), type
- **Examples**: Python, AWS, Kubernetes, Data Architecture, AWS Certified Solutions Architect

### 2. **Project**
Active projects with timelines, budgets, and requirements
- **Attributes**: id, name, type, status (planning, active, on_hold, completed), start_date, end_date, budget, priority, client_id, description
- **Types**: infrastructure, platform, ml, analytics, optimization, governance

### 3. **Sprint**
Agile iterations for project planning
- **Attributes**: id, name, project_id, sprint_number, start_date, end_date, status, velocity

### 4. **Client**
Customer relationships and dedicated resources
- **Attributes**: id, name, industry, tier (enterprise, mid-market, strategic), annual_value, relationship_start

### 5. **Technology**
Dynamic nodes created for specialization areas
- **Attributes**: name
- **Examples**: Real-time Processing, NLP, Microservices, Data Governance

## Enhanced Person Attributes

The Person entity now includes:
- **seniority**: Junior/Mid/Senior/Staff/Principal
- **capacity_hours_per_week**: Standard 40 hours
- **current_utilization**: Percentage (60-100%)
- **billing_rate**: Hourly rate for project budgeting
- **years_experience**: Total years of experience
- **timezone**: Work timezone (mapped from location)

## New Relationships

### Resource Planning
- **(Person)-[:HAS_SKILL]->(Skill)**
  - Properties: proficiency_level (beginner/intermediate/advanced/expert), years_experience, last_used
  
- **(Person)-[:ALLOCATED_TO]->(Project)**
  - Properties: allocation_percentage, start_date, end_date, role_on_project (lead/contributor/advisor/reviewer)

- **(Project)-[:REQUIRES_SKILL]->(Skill)**
  - Properties: priority (critical/high/medium/low), min_proficiency_level, headcount_needed

- **(Team)-[:DELIVERS]->(Project)**
  - Properties: responsibility (primary/supporting/consulting), committed_capacity

### Knowledge Transfer & Coverage
- **(Person)-[:MENTORED_BY]->(Person)**
  - Properties: start_date, focus_area (technical skills/career development/domain expertise/leadership)

- **(Person)-[:BACKUP_FOR]->(Person)**
  - Properties: coverage_type (full/partial/emergency), readiness_level (ready/in_training/identified)

- **(Person)-[:SPECIALIZES_IN]->(Technology)**
  - Properties: expertise_level (recognized/expert/thought_leader), years_in_specialty

### Project Structure
- **(Project)-[:FOR_CLIENT]->(Client)**
- **(Sprint)-[:PART_OF]->(Project)**

## Example Queries

### Find Available Python Experts with AWS Experience
```cypher
MATCH (p:Person)-[hs:HAS_SKILL]->(s:Skill) 
WHERE s.name IN ['Python', 'AWS'] 
  AND hs.proficiency_level IN ['advanced', 'expert'] 
  AND p.current_utilization < 80 
WITH p, collect(s.name) as skills 
WHERE size(skills) = 2 
RETURN p.id, p.name, p.email, p.current_utilization, p.capacity_hours_per_week
```

### Show Teams with Capacity for New Projects
```cypher
MATCH (t:Team)-[d:DELIVERS]->(pr:Project) 
WHERE pr.status = 'active' 
WITH t, sum(d.committed_capacity) as total_committed 
WHERE total_committed < 70 AND t.department CONTAINS 'Data' 
RETURN t.id, t.name, t.department, total_committed as current_capacity_used
```

### Identify Skill Gaps for ML Projects
```cypher
MATCH (pr:Project)-[rs:REQUIRES_SKILL]->(s:Skill) 
WHERE pr.type = 'ml' AND pr.status IN ['planning', 'active'] 
WITH s, pr, rs 
OPTIONAL MATCH (p:Person)-[hs:HAS_SKILL]->(s) 
WHERE hs.proficiency_level >= rs.min_proficiency_level 
WITH s, pr, rs.headcount_needed as needed, count(p) as available 
RETURN s.name, collect(pr.name) as projects, 
       sum(needed) as total_needed, 
       sum(available) as total_available, 
       sum(needed) - sum(available) as gap
```

### Find Mentors for Kubernetes
```cypher
MATCH (mentor:Person)-[hs:HAS_SKILL]->(s:Skill {name: 'Kubernetes'}) 
WHERE hs.proficiency_level IN ['advanced', 'expert'] 
  AND mentor.seniority IN ['Senior', 'Staff', 'Principal'] 
OPTIONAL MATCH (mentor)<-[:MENTORED_BY]-(mentee) 
WITH mentor, count(mentee) as current_mentees 
WHERE current_mentees < 3 
RETURN mentor.id, mentor.name, mentor.email, mentor.department, current_mentees
```

### Calculate Project Feasibility
```cypher
MATCH (pr:Project {status: 'planning'})-[rs:REQUIRES_SKILL]->(s:Skill) 
WITH pr, s, rs 
OPTIONAL MATCH (p:Person)-[hs:HAS_SKILL]->(s) 
WHERE hs.proficiency_level >= rs.min_proficiency_level 
  AND p.current_utilization < 90 
WITH pr, count(DISTINCT s) as skills_needed, count(DISTINCT p) as people_available 
RETURN pr.id, pr.name, pr.priority, skills_needed, people_available
```

## Data Generation Summary

The seed script generates:
- 500 people with enhanced attributes across 15 departments
- 52 technical skills across 8 categories
- 12 active projects linked to clients
- 12 enterprise clients across various industries  
- 32 sprints for active projects
- ~2400 person-skill relationships
- ~30 project allocations
- ~40 project skill requirements
- ~50 mentorship relationships
- ~150 backup coverage relationships

## Benefits

1. **Resource Optimization**: Find available experts based on skills, proficiency, and current utilization
2. **Capacity Planning**: Track team and individual capacity across projects
3. **Skill Gap Analysis**: Identify missing skills for upcoming initiatives
4. **Knowledge Management**: Track mentorship and backup coverage for business continuity
5. **Project Feasibility**: Assess if projects can be staffed with available resources
6. **Cost Estimation**: Calculate project costs based on billing rates and allocations

The enhanced model enables data-driven decisions for project staffing, skill development, and resource optimization across the organization.