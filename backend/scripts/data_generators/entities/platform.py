"""Platform-related entity generators (CloudRegions, PlatformComponents)."""

from typing import List, Dict, Any
from ..base import BaseGenerator
from ..config import CLOUD_REGIONS_COUNT, PLATFORM_COMPONENTS_COUNT


class CloudRegionsGenerator(BaseGenerator):
    """Generator for CloudRegion entities."""
    
    def generate(self) -> List[Dict[str, Any]]:
        """Generate cloud region data for multi-cloud deployments."""
        regions = []
        
        # Define cloud regions for major providers
        cloud_regions = [
            # AWS Regions
            {"provider": "AWS", "region_code": "us-east-1", 
             "region_name": "US East (N. Virginia)", "availability_zones": 6, "data_residency_zone": "US"},
            {"provider": "AWS", "region_code": "us-west-2", 
             "region_name": "US West (Oregon)", "availability_zones": 4, "data_residency_zone": "US"},
            {"provider": "AWS", "region_code": "eu-west-1", 
             "region_name": "EU (Ireland)", "availability_zones": 3, "data_residency_zone": "EU"},
            {"provider": "AWS", "region_code": "eu-central-1", 
             "region_name": "EU (Frankfurt)", "availability_zones": 3, "data_residency_zone": "EU"},
            {"provider": "AWS", "region_code": "ap-southeast-1", 
             "region_name": "Asia Pacific (Singapore)", "availability_zones": 3, "data_residency_zone": "APAC"},
            {"provider": "AWS", "region_code": "ap-northeast-1", 
             "region_name": "Asia Pacific (Tokyo)", "availability_zones": 4, "data_residency_zone": "APAC"},
            
            # GCP Regions
            {"provider": "GCP", "region_code": "us-central1", 
             "region_name": "Iowa", "availability_zones": 4, "data_residency_zone": "US"},
            {"provider": "GCP", "region_code": "us-east1", 
             "region_name": "South Carolina", "availability_zones": 3, "data_residency_zone": "US"},
            {"provider": "GCP", "region_code": "europe-west1", 
             "region_name": "Belgium", "availability_zones": 3, "data_residency_zone": "EU"},
            {"provider": "GCP", "region_code": "europe-west4", 
             "region_name": "Netherlands", "availability_zones": 3, "data_residency_zone": "EU"},
            {"provider": "GCP", "region_code": "asia-southeast1", 
             "region_name": "Singapore", "availability_zones": 3, "data_residency_zone": "APAC"},
            {"provider": "GCP", "region_code": "asia-northeast1", 
             "region_name": "Tokyo", "availability_zones": 3, "data_residency_zone": "APAC"},
            
            # Azure Regions
            {"provider": "Azure", "region_code": "eastus", 
             "region_name": "East US", "availability_zones": 3, "data_residency_zone": "US"},
            {"provider": "Azure", "region_code": "westus2", 
             "region_name": "West US 2", "availability_zones": 3, "data_residency_zone": "US"},
            {"provider": "Azure", "region_code": "northeurope", 
             "region_name": "North Europe", "availability_zones": 3, "data_residency_zone": "EU"},
            {"provider": "Azure", "region_code": "westeurope", 
             "region_name": "West Europe", "availability_zones": 3, "data_residency_zone": "EU"},
            {"provider": "Azure", "region_code": "southeastasia", 
             "region_name": "Southeast Asia", "availability_zones": 3, "data_residency_zone": "APAC"},
            {"provider": "Azure", "region_code": "japaneast", 
             "region_name": "Japan East", "availability_zones": 3, "data_residency_zone": "APAC"}
        ]
        
        for i, region in enumerate(cloud_regions):
            regions.append({
                "id": f"region_{i+1}",
                "provider": region["provider"],
                "region_code": region["region_code"],
                "region_name": region["region_name"],
                "availability_zones": region["availability_zones"],
                "data_residency_zone": region["data_residency_zone"]
            })
        
        return regions


class PlatformComponentsGenerator(BaseGenerator):
    """Generator for PlatformComponent entities."""
    
    def generate(self) -> List[Dict[str, Any]]:
        """Generate platform component data for expertise mapping."""
        components = []
        
        # Define platform components with their properties
        platform_components = [
            # Core Services
            {"name": "API Gateway", "type": "service", "tier": "core", 
             "owner_team_id": "team_14", "documentation_url": "https://docs.company.com/api-gateway"},
            {"name": "Authentication Service", "type": "service", "tier": "core", 
             "owner_team_id": "team_6", "documentation_url": "https://docs.company.com/auth-service"},
            {"name": "Data Ingestion Pipeline", "type": "pipeline", "tier": "core", 
             "owner_team_id": "team_1", "documentation_url": "https://docs.company.com/data-ingestion"},
            {"name": "Stream Processing Engine", "type": "pipeline", "tier": "core", 
             "owner_team_id": "team_1", "documentation_url": "https://docs.company.com/stream-processing"},
            {"name": "Batch Processing Framework", "type": "pipeline", "tier": "core", 
             "owner_team_id": "team_1", "documentation_url": "https://docs.company.com/batch-processing"},
            
            # Data Storage
            {"name": "Data Lake Storage", "type": "database", "tier": "core", 
             "owner_team_id": "team_5", "documentation_url": "https://docs.company.com/data-lake"},
            {"name": "Time Series Database", "type": "database", "tier": "core", 
             "owner_team_id": "team_5", "documentation_url": "https://docs.company.com/tsdb"},
            {"name": "Metadata Store", "type": "database", "tier": "supporting", 
             "owner_team_id": "team_5", "documentation_url": "https://docs.company.com/metadata-store"},
            {"name": "Feature Store", "type": "database", "tier": "core", 
             "owner_team_id": "team_4", "documentation_url": "https://docs.company.com/feature-store"},
            
            # Analytics & ML
            {"name": "Analytics Engine", "type": "service", "tier": "core", 
             "owner_team_id": "team_2", "documentation_url": "https://docs.company.com/analytics-engine"},
            {"name": "ML Inference Service", "type": "service", "tier": "core", 
             "owner_team_id": "team_4", "documentation_url": "https://docs.company.com/ml-inference"},
            {"name": "Model Training Pipeline", "type": "pipeline", "tier": "supporting", 
             "owner_team_id": "team_4", "documentation_url": "https://docs.company.com/model-training"},
            {"name": "Data Visualization Service", "type": "service", "tier": "core", 
             "owner_team_id": "team_2", "documentation_url": "https://docs.company.com/visualization"},
            
            # Customer-Facing
            {"name": "Customer Portal", "type": "service", "tier": "core", 
             "owner_team_id": "team_14", "documentation_url": "https://docs.company.com/customer-portal"},
            {"name": "Admin Dashboard", "type": "service", "tier": "supporting", 
             "owner_team_id": "team_14", "documentation_url": "https://docs.company.com/admin-dashboard"},
            {"name": "Reporting Service", "type": "service", "tier": "core", 
             "owner_team_id": "team_2", "documentation_url": "https://docs.company.com/reporting"},
            
            # Infrastructure & Monitoring
            {"name": "Monitoring & Alerting", "type": "service", "tier": "supporting", 
             "owner_team_id": "team_5", "documentation_url": "https://docs.company.com/monitoring"},
            {"name": "Log Aggregation Service", "type": "service", "tier": "supporting", 
             "owner_team_id": "team_5", "documentation_url": "https://docs.company.com/logging"},
            {"name": "CI/CD Pipeline", "type": "pipeline", "tier": "supporting", 
             "owner_team_id": "team_5", "documentation_url": "https://docs.company.com/cicd"},
            {"name": "Service Mesh", "type": "service", "tier": "supporting", 
             "owner_team_id": "team_5", "documentation_url": "https://docs.company.com/service-mesh"}
        ]
        
        for i, component in enumerate(platform_components):
            components.append({
                "id": f"component_{i+1}",
                "name": component["name"],
                "type": component["type"],
                "tier": component["tier"],
                "owner_team_id": component["owner_team_id"],
                "documentation_url": component["documentation_url"]
            })
        
        return components