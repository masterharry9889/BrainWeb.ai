from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
import time
from datetime import datetime
import json
from enum import Enum

class AgentStatus(str, Enum):
    IDLE = "idle"
    WORKING = "working"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"

@dataclass
class AgentMessage:
    id: str
    from_agent: str
    to_agent: str
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    priority: int = 1
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AgentTask:
    id: str
    agent_name: str
    description: str
    requirements: Dict[str, Any]
    status: AgentStatus = AgentStatus.IDLE
    dependencies: List[str] = field(default_factory=list)
    assigned_by: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    result: Any = None
    error: Optional[str] = None

class BaseAgent(ABC):
    def __init__(self, name: str, agent_type: str):
        self.name = name
        self.agent_type = agent_type
        self.status = AgentStatus.IDLE
        self.tasks: Dict[str, AgentTask] = {}
        self.inbox: List[AgentMessage] = []
        self.skills: List[str] = []
        self.knowledge: Dict[str, Any] = {}
        self.context: Dict[str, Any] = {}

    def add_task(self, task: AgentTask) -> None:
        self.tasks[task.id] = task

    def add_message(self, message: AgentMessage) -> None:
        self.inbox.append(message)

    def process_message(self, message: AgentMessage) -> None:
        if message.to_agent == self.name:
            self.inbox.append(message)
            self.on_message_received(message)

    @abstractmethod
    def on_message_received(self, message: AgentMessage) -> None:
        pass

    @abstractmethod
    def execute_task(self, task: AgentTask) -> Any:
        pass

    def start_working(self) -> None:
        self.status = AgentStatus.WORKING

    def stop_working(self) -> None:
        self.status = AgentStatus.IDLE

    def complete_task(self, task_id: str, result: Any) -> None:
        if task_id in self.tasks:
            task = self.tasks[task_id]
            task.status = AgentStatus.COMPLETED
            task.result = result
            task.completed_at = datetime.now()
            self.status = AgentStatus.IDLE

    def fail_task(self, task_id: str, error: str) -> None:
        if task_id in self.tasks:
            task = self.tasks[task_id]
            task.status = AgentStatus.FAILED
            task.error = error
            task.completed_at = datetime.now()
            self.status = AgentStatus.IDLE

    def serialize(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "agent_type": self.agent_type,
            "status": self.status.value,
            "skills": self.skills,
            "context": self.context,
        }

    @classmethod
    def deserialize(cls, data: Dict[str, Any]) -> 'BaseAgent':
        agent = cls(data["name"], data["agent_type"])
        agent.status = AgentStatus(data.get("status", "idle"))
        agent.skills = data.get("skills", [])
        agent.context = data.get("context", {})
        return agent
