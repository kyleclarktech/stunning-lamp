"""Skills and Languages entity generators."""

from typing import List, Dict, Any
from ..base import BaseGenerator
from ..config import SKILLS_COUNT, LANGUAGES_COUNT, SKILL_CATEGORIES


class SkillsGenerator(BaseGenerator):
    """Generator for Skill entities."""
    
    def generate(self) -> List[Dict[str, Any]]:
        """Generate technical and soft skills."""
        skills = [
            # Programming Languages
            {"id": "skill_1", "name": "Python", "category": "programming", "type": "technical"},
            {"id": "skill_2", "name": "Java", "category": "programming", "type": "technical"},
            {"id": "skill_3", "name": "Scala", "category": "programming", "type": "technical"},
            {"id": "skill_4", "name": "JavaScript", "category": "programming", "type": "technical"},
            {"id": "skill_5", "name": "TypeScript", "category": "programming", "type": "technical"},
            {"id": "skill_6", "name": "Go", "category": "programming", "type": "technical"},
            {"id": "skill_7", "name": "Rust", "category": "programming", "type": "technical"},
            {"id": "skill_8", "name": "SQL", "category": "programming", "type": "technical"},
            
            # Data & Analytics Tools
            {"id": "skill_9", "name": "Apache Spark", "category": "analytics", "type": "technical"},
            {"id": "skill_10", "name": "Apache Kafka", "category": "analytics", "type": "technical"},
            {"id": "skill_11", "name": "Apache Flink", "category": "analytics", "type": "technical"},
            {"id": "skill_12", "name": "Databricks", "category": "analytics", "type": "technical"},
            {"id": "skill_13", "name": "Snowflake", "category": "analytics", "type": "technical"},
            {"id": "skill_14", "name": "BigQuery", "category": "analytics", "type": "technical"},
            {"id": "skill_15", "name": "Redshift", "category": "analytics", "type": "technical"},
            {"id": "skill_16", "name": "dbt", "category": "analytics", "type": "technical"},
            {"id": "skill_17", "name": "Airflow", "category": "analytics", "type": "technical"},
            
            # Cloud Platforms
            {"id": "skill_18", "name": "AWS", "category": "cloud", "type": "technical"},
            {"id": "skill_19", "name": "Google Cloud", "category": "cloud", "type": "technical"},
            {"id": "skill_20", "name": "Azure", "category": "cloud", "type": "technical"},
            {"id": "skill_21", "name": "Kubernetes", "category": "cloud", "type": "technical"},
            {"id": "skill_22", "name": "Docker", "category": "cloud", "type": "technical"},
            {"id": "skill_23", "name": "Terraform", "category": "cloud", "type": "technical"},
            
            # Databases
            {"id": "skill_24", "name": "PostgreSQL", "category": "database", "type": "technical"},
            {"id": "skill_25", "name": "MySQL", "category": "database", "type": "technical"},
            {"id": "skill_26", "name": "MongoDB", "category": "database", "type": "technical"},
            {"id": "skill_27", "name": "Cassandra", "category": "database", "type": "technical"},
            {"id": "skill_28", "name": "Redis", "category": "database", "type": "technical"},
            {"id": "skill_29", "name": "Elasticsearch", "category": "database", "type": "technical"},
            
            # Machine Learning
            {"id": "skill_30", "name": "TensorFlow", "category": "ml", "type": "technical"},
            {"id": "skill_31", "name": "PyTorch", "category": "ml", "type": "technical"},
            {"id": "skill_32", "name": "Scikit-learn", "category": "ml", "type": "technical"},
            {"id": "skill_33", "name": "MLflow", "category": "ml", "type": "technical"},
            {"id": "skill_34", "name": "Deep Learning", "category": "ml", "type": "technical"},
            {"id": "skill_35", "name": "NLP", "category": "ml", "type": "technical"},
            {"id": "skill_36", "name": "Computer Vision", "category": "ml", "type": "technical"},
            
            # Soft Skills
            {"id": "skill_37", "name": "Leadership", "category": "soft", "type": "soft"},
            {"id": "skill_38", "name": "Communication", "category": "soft", "type": "soft"},
            {"id": "skill_39", "name": "Project Management", "category": "soft", "type": "soft"},
            {"id": "skill_40", "name": "Problem Solving", "category": "soft", "type": "soft"},
            {"id": "skill_41", "name": "Mentoring", "category": "soft", "type": "soft"},
            {"id": "skill_42", "name": "Public Speaking", "category": "soft", "type": "soft"},
            {"id": "skill_43", "name": "Agile/Scrum", "category": "soft", "type": "soft"},
            
            # Domain Skills
            {"id": "skill_44", "name": "Financial Analysis", "category": "domain", "type": "domain"},
            {"id": "skill_45", "name": "Healthcare Analytics", "category": "domain", "type": "domain"},
            {"id": "skill_46", "name": "E-commerce", "category": "domain", "type": "domain"},
            {"id": "skill_47", "name": "Supply Chain", "category": "domain", "type": "domain"},
            {"id": "skill_48", "name": "Marketing Analytics", "category": "domain", "type": "domain"},
            {"id": "skill_49", "name": "Risk Management", "category": "domain", "type": "domain"},
            {"id": "skill_50", "name": "Compliance", "category": "domain", "type": "domain"},
            {"id": "skill_51", "name": "Data Governance", "category": "domain", "type": "domain"},
            {"id": "skill_52", "name": "Business Intelligence", "category": "domain", "type": "domain"}
        ]
        
        return skills


class LanguagesGenerator(BaseGenerator):
    """Generator for Language entities."""
    
    def generate(self) -> List[Dict[str, Any]]:
        """Generate spoken language data."""
        languages = [
            {"id": "lang_1", "code": "en", "name": "English", "native_name": "English", 
             "script": "Latin", "direction": "ltr", "is_business_language": True},
            {"id": "lang_2", "code": "es", "name": "Spanish", "native_name": "Español", 
             "script": "Latin", "direction": "ltr", "is_business_language": True},
            {"id": "lang_3", "code": "fr", "name": "French", "native_name": "Français", 
             "script": "Latin", "direction": "ltr", "is_business_language": True},
            {"id": "lang_4", "code": "de", "name": "German", "native_name": "Deutsch", 
             "script": "Latin", "direction": "ltr", "is_business_language": True},
            {"id": "lang_5", "code": "zh", "name": "Chinese", "native_name": "中文", 
             "script": "Chinese", "direction": "ltr", "is_business_language": True},
            {"id": "lang_6", "code": "ja", "name": "Japanese", "native_name": "日本語", 
             "script": "Japanese", "direction": "ltr", "is_business_language": True},
            {"id": "lang_7", "code": "ko", "name": "Korean", "native_name": "한국어", 
             "script": "Korean", "direction": "ltr", "is_business_language": False},
            {"id": "lang_8", "code": "pt", "name": "Portuguese", "native_name": "Português", 
             "script": "Latin", "direction": "ltr", "is_business_language": True},
            {"id": "lang_9", "code": "ru", "name": "Russian", "native_name": "Русский", 
             "script": "Cyrillic", "direction": "ltr", "is_business_language": False},
            {"id": "lang_10", "code": "ar", "name": "Arabic", "native_name": "العربية", 
             "script": "Arabic", "direction": "rtl", "is_business_language": False},
            {"id": "lang_11", "code": "hi", "name": "Hindi", "native_name": "हिन्दी", 
             "script": "Devanagari", "direction": "ltr", "is_business_language": False},
            {"id": "lang_12", "code": "it", "name": "Italian", "native_name": "Italiano", 
             "script": "Latin", "direction": "ltr", "is_business_language": False}
        ]
        
        return languages