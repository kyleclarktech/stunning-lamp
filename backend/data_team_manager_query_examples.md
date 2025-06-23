# Data Team Manager Query Examples

Based on the database structure, there's no single "Data team" but rather multiple teams with "Data" in their names across different departments:

## Teams with "Data" in the name:
1. Data Ingestion (Data Platform Engineering)
2. Data Processing (Data Platform Engineering)
3. Data Quality (Data Platform Engineering)
4. Data Modeling (Analytics Engineering)
5. Data Security (Security & Compliance)
6. Data Architecture (Professional Services)
7. Data Science Tools (Data Science)
8. Database Operations (Infrastructure & DevOps)

## Correct Query Approaches

### 1. Find all team leads for teams with "Data" in the name:
```cypher
MATCH (p:Person)-[m:MEMBER_OF {is_lead: true}]->(t:Team)
WHERE t.name CONTAINS 'Data' OR t.department CONTAINS 'Data'
RETURN p.id, p.name, p.email, p.role, t.name as team_name, t.department, labels(p) as labels
LIMIT 25
```

### 2. Find managers/leads by role in data-related teams:
```cypher
MATCH (p:Person)-[:MEMBER_OF]->(t:Team)
WHERE (t.name CONTAINS 'Data' OR t.department CONTAINS 'Data')
AND (p.role CONTAINS 'Manager' OR p.role CONTAINS 'Lead' OR p.role CONTAINS 'Director' OR p.role CONTAINS 'Head')
RETURN p.id, p.name, p.email, p.role, t.name as team_name, t.department, labels(p) as labels
LIMIT 25
```

### 3. Find the department head for Data Platform Engineering:
```cypher
MATCH (p:Person)
WHERE p.department = 'Data Platform Engineering' 
AND (p.role CONTAINS 'VP' OR p.role CONTAINS 'Director' OR p.role CONTAINS 'Head')
RETURN p.id, p.name, p.email, p.role, p.department, labels(p) as labels
LIMIT 10
```

## The Issue with "Who manages the data team?"

The query "Who manages the data team?" is ambiguous because:
1. There's no single entity called "the data team"
2. Multiple teams work with data across different departments
3. Each team has its own lead(s)

The system should ideally:
1. Recognize the ambiguity
2. Return leads/managers for all data-related teams
3. Format the results to show which specific data team each person manages

## Expected Response Format

When asked "Who manages the data team?", the ideal response would be:

```markdown
I found multiple data-related teams across the organization. Here are their leaders:

## Data Platform Engineering Teams
- **Mariah Kemp** (Platform Engineering Manager) - leads Data Ingestion team
- **Timothy Grimes** (Platform Engineering Manager) - leads Data Quality team
- **Sara Lowery** (Platform Engineering Manager) - leads Data Processing team

## Analytics Engineering
- **Walter Caldwell** (Lead Analytics Engineer) - leads Data Modeling team

## Security & Compliance
- **Kimberly Henderson** (CISO) - leads Data Security team

## Infrastructure & DevOps
- **Travis Evans** (Database Administrator Manager) - leads Database Operations team

## Professional Services
- **Michaela Ramos** (Professional Services Manager) - leads Data Architecture team

## Data Science
- **Andrew Cole** (Data Science Manager) - leads Advanced Analytics team

Since there are multiple data teams, please let me know if you're looking for a specific team or department.
```