from typing import List, Dict, Any
import random
from datetime import datetime, timedelta
from ..base import BaseGenerator
from ..config import REGIONS


class MetricsGenerator(BaseGenerator):
    """Generate performance metrics data for services across regions"""
    
    def generate(self) -> List[Dict[str, Any]]:
        metrics = []
        metric_id = 1
        
        # Services we track
        services = [
            "api-gateway",
            "data-pipeline",
            "analytics-engine", 
            "ml-inference",
            "query-service",
            "streaming-processor",
            "batch-scheduler",
            "metadata-service",
            "auth-service",
            "notification-service"
        ]
        
        # Metric types and their typical values
        metric_configs = [
            {
                "type": "availability",
                "unit": "percentage",
                "percentiles": [99],  # We track availability as a single value
                "base_value": 99.5,
                "variance": 0.5
            },
            {
                "type": "response_time",
                "unit": "milliseconds", 
                "percentiles": [50, 95, 99],
                "base_values": {"50": 50, "95": 200, "99": 500},
                "variance": 0.3
            },
            {
                "type": "throughput",
                "unit": "requests_per_second",
                "percentiles": [50],  # Average throughput
                "base_value": 1000,
                "variance": 0.4
            },
            {
                "type": "error_rate",
                "unit": "percentage",
                "percentiles": [50],
                "base_value": 0.1,
                "variance": 0.5
            },
            {
                "type": "cpu_utilization",
                "unit": "percentage",
                "percentiles": [50, 95],
                "base_values": {"50": 40, "95": 70},
                "variance": 0.3
            },
            {
                "type": "memory_utilization",
                "unit": "percentage",
                "percentiles": [50, 95],
                "base_values": {"50": 50, "95": 80},
                "variance": 0.2
            }
        ]
        
        # Generate metrics for the last 30 days
        now = datetime.now()
        
        for days_ago in range(30):
            timestamp = now - timedelta(days=days_ago)
            
            # Generate metrics for each service, region, and metric type
            for service in services:
                for region in REGIONS:
                    for config in metric_configs:
                        # Add some variance based on region and service
                        region_multiplier = {"AMERICAS": 1.0, "EMEA": 1.1, "APAC": 0.9}[region]
                        service_multiplier = 1.0
                        if "ml" in service or "analytics" in service:
                            service_multiplier = 1.2  # ML services are slower
                        elif "auth" in service or "gateway" in service:
                            service_multiplier = 0.8  # Auth/gateway are faster
                        
                        if config["type"] in ["availability", "throughput", "error_rate"]:
                            # Single percentile metrics
                            base = config["base_value"]
                            # Add daily variance
                            daily_variance = random.uniform(-config["variance"], config["variance"])
                            # Add hourly spikes for some hours
                            hour = timestamp.hour
                            hourly_spike = 0
                            if hour in [9, 10, 14, 15]:  # Business hours spikes
                                if config["type"] == "throughput":
                                    hourly_spike = 0.5
                                elif config["type"] == "error_rate":
                                    hourly_spike = 0.2
                            
                            value = base * region_multiplier * service_multiplier * (1 + daily_variance + hourly_spike)
                            
                            # Ensure reasonable bounds
                            if config["type"] == "availability":
                                value = min(100, max(95, value))
                            elif config["type"] == "error_rate":
                                value = max(0, min(5, value))
                            
                            metrics.append({
                                "id": f"metric_{metric_id}",
                                "type": config["type"],
                                "service": service,
                                "region": region,
                                "value": round(value, 2),
                                "unit": config["unit"],
                                "timestamp": timestamp.isoformat(),
                                "percentile": config["percentiles"][0]
                            })
                            metric_id += 1
                        
                        else:
                            # Multiple percentile metrics (response_time, cpu, memory)
                            for percentile in config["percentiles"]:
                                base = config["base_values"][str(percentile)]
                                daily_variance = random.uniform(-config["variance"], config["variance"])
                                
                                value = base * region_multiplier * service_multiplier * (1 + daily_variance)
                                
                                # Add some anomalies
                                if random.random() < 0.02:  # 2% chance of anomaly
                                    value *= random.uniform(2, 5)
                                
                                metrics.append({
                                    "id": f"metric_{metric_id}",
                                    "type": config["type"],
                                    "service": service,
                                    "region": region,
                                    "value": round(value, 2),
                                    "unit": config["unit"],
                                    "timestamp": timestamp.isoformat(),
                                    "percentile": percentile
                                })
                                metric_id += 1
        
        # Add some SLA metrics (monthly aggregates)
        for service in services:
            for region in REGIONS:
                # Monthly SLA achievement
                sla_achieved = random.uniform(99.0, 99.99)
                metrics.append({
                    "id": f"metric_{metric_id}",
                    "type": "sla_achievement",
                    "service": service,
                    "region": region,
                    "value": round(sla_achieved, 2),
                    "unit": "percentage",
                    "timestamp": now.replace(day=1).isoformat(),  # First of month
                    "percentile": 0  # Not applicable for SLA
                })
                metric_id += 1
        
        return metrics
