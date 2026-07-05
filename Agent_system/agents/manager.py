from abc import ABC
from gents.base_agent import BaseAgent, AgentTask, AgentMessage, AgentStatus
from typing import Dict, List, Any
from datetime import datetime

class Manager(BaseAgent):
    def __init__(self):
        super().__init__("Manager", "management")
        self.teams = {}
        self.projects = []
        self.resources = {"humans": [], "agents": [], "budget": 0.0}

    def on_message_received(self, message: AgentMessage) -> None:
        self.process_inbox()

    def process_inbox(self) -> None:
        for message in self.inbox:
            if "task" in message.content.lower() or "project" in message.content.lower():
                self.execute_management_task(message)

    def execute_management_task(self, message: AgentMessage) -> Dict[str, Any]:
        self.start_working()
        try:
            return {
                "action": "Task assignment completed",
                "assignment": {"task_id": "task_123", "priority": "high"},
                "team": "Development Team",
                "deadline": "2026-02-15",
                "resources_allocated": {"agents": 3, "time": "40 hours"},
                "next_steps": ["Review progress daily", "Update stakeholders weekly"]
            }
        finally:
            self.stop_working()

    def create_project(self, project_name: str, requirements: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "project_id": f"project_{datetime.now().timestamp()}",
            "name": project_name,
            "requirements": requirements,
            "start_date": datetime.now(),
            "estimated_duration": requirements.get("duration", "3 months"),
            "status": "planned",
            "team_allocation": {}
        }

    def allocate_resources(self, project_id: str, resource_list: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "project_id": project_id,
            "resources": resource_list,
            "allocation_date": datetime.now(),
            "budget": resource_list.get("budget", 0.0),
            "team_size": resource_list.get("team_size", 1),
            "deadlines": ["Phase 1: Week 1-2", "Phase 2: Week 3-4", "Phase 3: Week 5-6"],
            "milestones": {
                "milestone_1": "Requirements completion",
                "milestone_2": "Prototype delivery",
                "milestone_3": "Final delivery"
            }
        }

    def track_progress(self, project_id: str, metrics: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "project_id": project_id,
            "current_progress": metrics.get("progress", 0.0),
            "time_elapsed": metrics.get("time_elapsed", 0),
            "completed_tasks": metrics.get("completed", []),
            "pending_tasks": metrics.get("pending", []),
            "blockers": metrics.get("blockers", []),
            "next_actions": ["Remove blocker X", "Complete task Y", "Update documentation"],
            "risk_assessment": "Low risk - on schedule"
        }
