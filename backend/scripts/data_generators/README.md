# Data Generators - Modular Seed Data System

This directory contains a modular system for generating and seeding test data into FalkorDB.

## Structure

```
data_generators/
├── __init__.py
├── base.py                  # Base generator class and utilities
├── config.py               # Shared configuration and constants
├── entities/               # Entity generators (nodes)
│   ├── __init__.py
│   ├── people.py           # People, Teams, Groups
│   ├── organizational.py   # Teams, Groups, Offices
│   ├── skills.py          # Skills, Languages
│   ├── projects.py        # Projects, Sprints
│   ├── clients.py         # Clients
│   ├── platform.py        # Cloud Regions, Platform Components
│   ├── compliance.py      # Policies, Compliance, Data Residency, Holidays
│   ├── operations.py      # Schedules, Incidents, Visas
│   └── metrics.py         # Metrics
├── relationships/         # Relationship generators
│   ├── __init__.py
│   ├── organizational.py  # Team/group memberships, reporting
│   ├── skills.py         # Skill assignments, expertise
│   ├── projects.py       # Project allocations, deliveries
│   ├── platform.py       # Component deployments, usage
│   ├── support.py        # On-call, incidents, visas
│   └── compliance.py     # Compliance relationships
└── database/             # Database interaction
    ├── __init__.py
    ├── connection.py     # Database connection management
    ├── indexes.py        # Index creation
    └── seeder.py         # Orchestrates seeding process

```

## Usage

### Running the New Modular Script

```bash
cd backend
python scripts/seed_data_new.py
```

### Migration from Old Script

The original monolithic script (`seed_data.py`) is being replaced by this modular structure. Both scripts produce the same data, but the new structure is:

- More maintainable
- Easier to test
- Allows selective data generation
- Better separation of concerns

### Adding New Generators

1. **Entity Generator**: Create a new class in `entities/` that inherits from `BaseGenerator`
2. **Relationship Generator**: Create a new class in `relationships/` that accepts required entities
3. **Update Imports**: Add your generator to the appropriate `__init__.py` file
4. **Update Orchestrator**: Modify `seed_data_new.py` to use your generator

### Example: Adding a New Entity

```python
# entities/departments.py
from typing import List, Dict, Any
from ..base import BaseGenerator

class DepartmentsGenerator(BaseGenerator):
    def generate(self) -> List[Dict[str, Any]]:
        departments = []
        # Generate department data
        return departments
```

### Example: Adding a New Relationship

```python
# relationships/department.py
from typing import List, Dict, Any
from ..base import BaseGenerator

class PersonDepartmentGenerator(BaseGenerator):
    def __init__(self, people: List[Dict[str, Any]], departments: List[Dict[str, Any]]):
        self.people = people
        self.departments = departments
    
    def generate(self) -> List[Dict[str, Any]]:
        relationships = []
        # Generate relationships
        return relationships
```

## Docker Integration

To use the new script in Docker, update your docker commands:

```bash
# Old command
docker exec -it stunning-lamp-api-1 python scripts/seed_data.py

# New command
docker exec -it stunning-lamp-api-1 python scripts/seed_data_new.py
```

## Data Model

The system generates the following entity types:

### Nodes
- Person (500 employees)
- Team (37 teams)
- Group (15 cross-functional groups)
- Policy (20 policies)
- Skill (52 technical skills)
- Project (20 projects)
- Client (20 clients)
- Sprint (project sprints)
- Office (8 global offices)
- Language (12 languages)
- Holiday (regional holidays)
- Compliance (8 frameworks)
- DataResidency (7 zones)
- Schedule (on-call schedules)
- Incident (historical incidents)
- Visa (work authorizations)
- Metric (performance metrics)
- CloudRegion (18 regions)
- PlatformComponent (20 components)

### Relationships
- MEMBER_OF (person → team/group)
- RESPONSIBLE_FOR (team/group → policy)
- REPORTS_TO (person → person)
- HAS_SKILL (person → skill)
- ALLOCATED_TO (person → project)
- DELIVERS (team → project)
- FOR_CLIENT (project → client)
- WORKS_AT (person → office)
- SPEAKS (person → language)
- ON_CALL (person → schedule)
- RESPONDED_TO (person → incident)
- HAS_VISA (person → visa)
- And many more...

## Testing

To test individual generators:

```python
from scripts.data_generators.entities import PeopleGenerator

gen = PeopleGenerator()
people = gen.generate()
print(f"Generated {len(people)} people")
```

## Future Enhancements

- Add configuration file support
- Implement data validation
- Add unit tests for generators
- Support for custom data sizes
- Export/import functionality
- Incremental updates instead of full rebuilds