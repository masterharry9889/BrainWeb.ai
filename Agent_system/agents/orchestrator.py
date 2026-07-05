from abc import ABC
from agents.base_agent import BaseAgent, AgentTask, AgentMessage, AgentStatus
from typing import Dict, List, Any
from datetime import datetime
import asyncio

class Orchestrator(BaseAgent):
    def __init__(self):
        super().__init__("Orchestrator", "coordination")
        self.agents: Dict[str, BaseAgent] = {}
        self.task_queue: List[AgentTask] = []
        self.workflow_history: List[Dict[str, Any]] = []
        self.communication_log: List[AgentMessage] = []

    def add_agent(self, agent: BaseAgent) -> None:
        self.agents[agent.name] = agent

    def distribute_task(self, task: AgentTask, target_agent: str = None) -> None:
        if target_agent and target_agent in self.agents:
            self.agents[target_agent].add_task(task)
        else:
            for agent in self.agents.values():
                if task.agent_name in agent.name.lower() or any(skill in task.description.lower() for skill in agent.name.lower().split()):
                    agent.add_task(task)
                    return
        self.task_queue.append(task)

    def process_workflows(self) -> None:
        for agent in self.agents.values():
            for task in list(agent.tasks.values()):
                if task.status == AgentStatus.IDLE:
                    task.status = AgentStatus.WORKING
                    result = agent.execute_task(task)
                    task.status = AgentStatus.COMPLETED
                    task.result = result

    def broadcast_message(self, message: AgentMessage) -> None:
        for agent in self.agents.values():
            agent.process_message(message)
        self.communication_log.append(message)

    def create_workflow(self, steps: List[Dict[str, Any]]) -> Dict[str, Any]:
        workflow_id = f"workflow_{datetime.now().timestamp()}"
        workflow = {
            "id": workflow_id,
            "steps": steps,
            "status": "in_progress",
            "created_at": datetime.now(),
            "agents_involved": list(self.agents.keys()),
            "progress": 0.0
        }
        self.workflow_history.append(workflow)
        return workflow

    def get_agent_status(self) -> Dict[str, Any]:
        return {
            "agents": {name: agent.serialize() for name, agent in self.agents.items()},
            "total_agents": len(self.agents),
            "active_tasks": sum(1 for agent in self.agents.values() for task in agent.tasks.values() if task.status == AgentStatus.WORKING),
            "completed_tasks": sum(1 for agent in self.agents.values() for task in agent.tasks.values() if task.status == AgentStatus.COMPLETED)
        }

    def reset_agents(self) -> None:
        for agent in self.agents.values():
            agent.context = {}
            agent.knowledge = {}
