"""Base classes and utilities for data generation."""

from datetime import datetime, timedelta
from faker import Faker
import random
from typing import List, Dict, Any

fake = Faker()


class BaseGenerator:
    """Base class for all data generators."""
    
    def __init__(self, seed: int = None):
        """Initialize the generator with an optional seed for reproducibility."""
        if seed:
            random.seed(seed)
            Faker.seed(seed)
        self.fake = fake
    
    def generate(self) -> List[Dict[str, Any]]:
        """Generate and return the data. Must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement generate()")


def escape_string(value: str) -> str:
    """Escape single quotes in strings for Cypher queries."""
    return value.replace("'", "''") if value else ""


def generate_date_range(start_days_ago: int, end_days_ago: int = 0) -> str:
    """Generate a random date within the specified range."""
    return fake.date_between(
        start_date=f'-{start_days_ago}d', 
        end_date=f'-{end_days_ago}d'
    ).isoformat()


def generate_datetime_range(start_days_ago: int, end_days_ago: int = 0) -> str:
    """Generate a random datetime within the specified range."""
    base = datetime.now() - timedelta(days=random.randint(end_days_ago, start_days_ago))
    return base.isoformat()


def weighted_choice(choices: List[tuple]) -> Any:
    """Make a weighted random choice from a list of (value, weight) tuples."""
    values, weights = zip(*choices)
    return random.choices(values, weights=weights)[0]