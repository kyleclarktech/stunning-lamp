"""Index creation for FalkorDB entities."""

from typing import List, Tuple
from .connection import DatabaseConnection


class IndexCreator:
    """Creates indexes for optimal query performance."""
    
    def __init__(self, connection: DatabaseConnection):
        self.db = connection.db
    
    def create_all_indexes(self) -> None:
        """Create all required indexes."""
        print("📇 Creating indexes...")
        
        indexes = [
            # Basic entity indexes
            ("Message", "timestamp"),
            ("Person", "name"),
            ("Team", "name"),
            ("Group", "name"),
            ("Policy", "name"),
            ("Skill", "name"),
            ("Project", "name"),
            ("Client", "name"),
            ("Sprint", "name"),
            ("Office", "name"),
            ("Office", "region"),
            ("Office", "timezone"),
            ("Language", "code"),
            ("Language", "name"),
            ("Holiday", "date"),
            ("Holiday", "type"),
            ("Compliance", "framework"),
            ("Compliance", "jurisdiction"),
            ("Compliance", "type"),
            ("Compliance", "status"),
            ("DataResidency", "zone"),
            ("DataResidency", "countries"),
            ("CloudRegion", "provider"),
            ("CloudRegion", "region_code"),
            ("CloudRegion", "data_residency_zone"),
            ("PlatformComponent", "name"),
            ("PlatformComponent", "type"),
            ("PlatformComponent", "tier"),
            ("Schedule", "type"),
            ("Schedule", "coverage_type"),
            ("Schedule", "region"),
            ("Schedule", "start_datetime"),
            ("Incident", "severity"),
            ("Incident", "status"),
            ("Incident", "created_at"),
            ("Visa", "type"),
            ("Visa", "country"),
            ("Visa", "expiry_date"),
            ("Metric", "type"),
            ("Metric", "service"),
            ("Metric", "timestamp")
        ]
        
        for label, property_name in indexes:
            try:
                query = f"CREATE INDEX ON :{label}({property_name})"
                self.db.query(query)
            except:
                pass  # Index might already exist
        
        print("✅ Indexes created successfully")