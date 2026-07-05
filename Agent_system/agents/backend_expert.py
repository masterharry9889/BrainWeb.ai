from abc import ABC
from agents.base_agent import BaseAgent, AgentTask, AgentMessage, AgentStatus
from typing import Dict, List, Any
from datetime import datetime

class SeniorBackendExpert(BaseAgent):
    def __init__(self):
        super().__init__("SeniorBackendExpert", "backend")
        self.technologies = ["microservices", "api_design", "databases", "cloud_infrastructure"]

    def on_message_received(self, message: AgentMessage) -> None:
        self.process_inbox()

    def process_inbox(self) -> None:
        for message in self.inbox:
            if any(keyword in message.content.lower() for keyword in ["api", "database", "server", "backend", "architecture", "system"]):
                self.execute_backend_task(message)

    def execute_backend_task(self, message: AgentMessage) -> Dict[str, Any]:
        self.start_working()
        try:
            return {
                "architecture": "Microservice-based architecture",
                "recommendations": ["Use Docker for containerization", "Implement API Gateway", "Set up monitoring"],
                "technologies": ["Node.js", "Python", "PostgreSQL", "Redis"],
                "security_measures": ["OAuth2 authentication", "Rate limiting", "Input validation"],
                "performance_optimizations": ["Caching layers", "Database indexing", "Load balancing"]
            }
        finally:
            self.stop_working()

    def design_api(self, endpoints: List[str], auth_type: str) -> Dict[str, Any]:
        return {
            "api_type": "RESTful API",
            "authentication": auth_type,
            "endpoints": endpoints,
            "data_formats": {"request": "JSON", "response": "JSON"},
            "versioning_strategy": "Semantic versioning",
            "error_handling": {"standard_codes": True, "custom_messages": True},
            "rate_limiting": {"enabled": True, "limits": {"per_minute": 60}}
        }

    def setup_database_schema(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "database_type": requirements.get("type", "relational"),
            "tables": [
                {"name": "users", "fields": ["id", "name", "email", "created_at"]},
                {"name": "projects", "fields": ["id", "title", "description", "status"]},
                {"name": "collaborations", "fields": ["id", "project_id", "user_id", "role"]}
            ],
            "relationships": {"foreign_keys": True, "constraints": True},
            "indexes": ["idx_email", "idx_project_status", "idx_user_project"],
            "migrations": {"automated": True, "rollback_supported": True}
        }
