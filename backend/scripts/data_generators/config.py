"""Configuration constants for data generation."""

# Entity counts
PEOPLE_COUNT = 500
TEAMS_COUNT = 37
GROUPS_COUNT = 15
POLICIES_COUNT = 20
SKILLS_COUNT = 52
PROJECTS_COUNT = 20
CLIENTS_COUNT = 20
SPRINTS_PER_PROJECT = 2
OFFICES_COUNT = 8
LANGUAGES_COUNT = 12
HOLIDAYS_COUNT = 83
COMPLIANCE_FRAMEWORKS_COUNT = 8
DATA_RESIDENCY_ZONES_COUNT = 7
INCIDENTS_COUNT = 100
VISAS_COUNT = 235
METRICS_DAYS = 30
CLOUD_REGIONS_COUNT = 18
PLATFORM_COMPONENTS_COUNT = 20

# Departments
DEPARTMENTS = [
    "Data Platform Engineering", "Analytics Engineering", "Product", "Data Science", 
    "Infrastructure & DevOps", "Security & Compliance", "Customer Success", 
    "Professional Services", "Sales", "Marketing", "Finance", "Legal", 
    "People Operations", "Engineering", "Solutions Architecture"
]

# Seniority levels
SENIORITY_LEVELS = ["Junior", "Mid", "Senior", "Staff", "Principal"]

# Time zones
TIMEZONES = [
    "US/Pacific", "US/Mountain", "US/Central", "US/Eastern", 
    "Europe/London", "Europe/Berlin", "Asia/Singapore", "Australia/Sydney"
]

# Regions
REGIONS = ["AMERICAS", "EMEA", "APAC"]

# Region timezone mappings
REGION_TIMEZONE_MAP = {
    "AMERICAS": ["America/New_York", "America/Chicago", "America/Los_Angeles", "America/Toronto"],
    "EMEA": ["Europe/London", "Europe/Paris", "Europe/Berlin", "Africa/Johannesburg"],
    "APAC": ["Asia/Tokyo", "Asia/Singapore", "Asia/Sydney", "Asia/Mumbai"]
}

# Client industries
CLIENT_INDUSTRIES = [
    "Financial Services", "Retail", "Healthcare", "Manufacturing", "Telecom", 
    "E-commerce", "Media", "Energy", "Pharmaceutical", "Logistics", 
    "Insurance", "Education", "Government", "Technology"
]

# Client tiers
CLIENT_TIERS = ["mid-market", "enterprise", "strategic"]

# Support tiers
SUPPORT_TIERS = {
    "mid-market": ["Basic", "Professional"],
    "enterprise": ["Professional", "Enterprise"],
    "strategic": ["Strategic"]
}

# Cloud providers
CLOUD_PROVIDERS = ["AWS", "GCP", "Azure"]

# Platform component types
COMPONENT_TYPES = ["service", "database", "pipeline"]

# Platform component tiers
COMPONENT_TIERS = ["core", "supporting"]

# Incident severities
INCIDENT_SEVERITIES = ["P0", "P1", "P2", "P3"]

# Incident statuses
INCIDENT_STATUSES = ["open", "investigating", "resolved", "postmortem"]

# Project types
PROJECT_TYPES = ["platform", "analytics", "ml", "integration", "optimization"]

# Project statuses
PROJECT_STATUSES = ["planning", "active", "on_hold", "completed"]

# Skill categories
SKILL_CATEGORIES = ["programming", "database", "cloud", "ml", "analytics", "soft", "domain"]

# Language proficiency levels
LANGUAGE_PROFICIENCIES = ["basic", "conversational", "professional", "fluent", "native"]

# Visa types
VISA_TYPES = ["H-1B", "L-1", "O-1", "Green Card", "Work Permit", "Business", "Permanent Residence"]

# Metric types
METRIC_TYPES = [
    "availability", "response_time", "throughput", 
    "error_rate", "cpu_utilization", "memory_utilization"
]

# Services to monitor
MONITORED_SERVICES = [
    "api-gateway", "data-pipeline", "analytics-engine", "ml-inference",
    "query-service", "streaming-processor", "batch-scheduler", 
    "metadata-service", "auth-service", "notification-service"
]