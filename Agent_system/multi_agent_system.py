from agents.base_agent import BaseAgent, AgentTask, AgentMessage, AgentStatus
from agents.researcher import ResearcherAgent
from agents.machine_learning import MachineLearningAgent
from agents.senior_math_professor import SeniorMathProfessor
from agents.frontend_expert import FrontendExpert
from agents.senior_artist import SeniorArtist
from agents.backend_expert import SeniorBackendExpert
from agents.manager import Manager
from agents.simulator import Simulator
from agents.team_of_coders import TeamOfCoders
from agents.orchestrator import Orchestrator
from typing import Dict, List, Any
from datetime import datetime

class INGOTMultiAgentSystem:
    """
    Main class for the INGOT AI Multi-Agent System.

    This system coordinates 9 specialized agents to provide comprehensive
    solutions through collaborative problem-solving and workflow orchestration.
    """

    def __init__(self):
        self.orchestrator = Orchestrator()
        self.initialize_agents()
        self.setup_system()

    def initialize_agents(self):
        """Initialize all specialist agents."""
        agents = [
            ResearcherAgent(),
            MachineLearningAgent(),
            SeniorMathProfessor(),
            FrontendExpert(),
            SeniorArtist(),
            SeniorBackendExpert(),
            Manager(),
            Simulator(),
            TeamOfCoders()
        ]

        for agent in agents:
            self.orchestrator.add_agent(agent)

    def setup_system(self):
        """Setup system configuration and initial tasks."""
        self.initialize_project("AI Analytics Dashboard")

    def initialize_project(self, project_name: str):
        """
        Initialize a new project with all necessary tasks distributed across agents.

        Args:
            project_name: Name of the project to initialize
        """
        print(f"\n🚀 Initializing Project: {project_name}")
        print("=" * 60)

        # Project planning
        manager = self.orchestrator.agents["Manager"]
        planning_task = AgentTask(
            id="task_planning_001",
            agent_name="Manager",
            description=f"Create project plan for {project_name} with timeline and resource allocation",
            requirements={
                "duration": "3 months",
                "budget": "$50,000",
                "team_size": 5,
                "milestones": ["Week 1-2: Requirements", "Week 3-4: Design", "Week 5-8: Development", "Week 9-10: Testing"]]
            },
            assigned_by="System"
        )
        self.orchestrator.distribute_task(planning_task, "Manager")
        print("✓ Project planning initiated")

        # Research phase
        researcher = self.orchestrator.agents["Researcher"]
        research_task = AgentTask(
            id="task_research_001",
            agent_name="Researcher",
            description="Research market competitors, user needs, and technical requirements for analytics dashboard",
            requirements={
                "market_analysis": True,
                "user_research": True,
                "technical_assessment": True
            }
        )
        self.orchestrator.distribute_task(research_task, "Researcher")
        print("✓ Market research initiated")

        # Architecture design
        backend_expert = self.orchestrator.agents["SeniorBackendExpert"]
        frontend_expert = self.orchestrator.agents["FrontendExpert"]
        ml_expert = self.orchestrator.agents["MachineLearningExpert"]

        backend_task = AgentTask(
            id="task_backend_001",
            agent_name="BackendExpert",
            description="Design microservices architecture with API gateway, database schema, and authentication",
            requirements={
                "api_type": "RESTful",
                "database": "PostgreSQL",
                "auth": "OAuth2",
                "microservices": ["auth", "data-processing", "analytics", "notification"]
            }
        )
        self.orchestrator.distribute_task(backend_task, "SeniorBackendExpert")
        print("✓ Backend architecture design initiated")

        frontend_task = AgentTask(
            id="task_frontend_001",
            agent_name="FrontendExpert",
            description="Design React-based frontend with responsive UI and state management",
            requirements={
                "framework": "React",
                "state_management": "Redux",
                "components": ["Dashboard", "Charts", "Forms", "Analytics"],
                "responsive": True
            }
        )
        self.orchestrator.distribute_task(frontend_task, "FrontendExpert")
        print("✓ Frontend architecture design initiated")

        ml_task = AgentTask(
            id="task_ml_001",
            agent_name="MLExpert",
            description="Design ML pipeline for data processing and predictive analytics",
            requirements={
                "model_types": ["classification", "regression", "clustering"],
                "data_sources": ["PostgreSQL", "CSV files", "API endpoints"],
                "features": ["feature_engineering", "model_validation", "performance_monitoring"]
            }
        )
        self.orchestrator.distribute_task(ml_task, "MachineLearningExpert")
        print("✓ ML pipeline design initiated")

        # Mathematical modeling
        math_professor = self.orchestrator.agents["SeniorMathProfessor"]
        math_task = AgentTask(
            id="task_math_001",
            agent_name="MathProfessor",
            description="Develop mathematical models for predictive analytics and optimization",
            requirements={
                "objective_function": "Maximize prediction accuracy",
                "variables": ["x1", "x2", "x3"],
                "constraints": ["data_quality > 0.95", "computation_time < 1h"],
                "methodology": "Gradient descent optimization"
            }
        )
        self.orchestrator.distribute_task(math_task, "SeniorMathProfessor")
        print("✓ Mathematical modeling initiated")

        # Visual design
        artist = self.orchestrator.agents["SeniorArtist"]
        design_task = AgentTask(
            id="task_art_001",
            agent_name="Artist",
            description="Create visual identity, color schemes, and design patterns for the dashboard",
            requirements={
                "style": "Modern and professional",
                "color_palette": {"primary": "#3498DB", "secondary": "#2ECC71"},
                "typography": "Montserrat and Roboto",
                "components": ["Charts", "Tables", "Icons", "Typography"]
            }
        )
        self.orchestrator.distribute_task(design_task, "SeniorArtist")
        print("✓ Visual design initiated")

        # Development
        coders = self.orchestrator.agents["TeamOfCoders"]
        development_task = AgentTask(
            id="task_dev_001",
            agent_name="Coders",
            description="Generate and implement code for all system components",
            requirements={
                "languages": ["Python", "JavaScript", "TypeScript"],
                "frameworks": ["Flask", "React", "Redux"],
                "tests": 150,
                "coverage": 90
            }
        )
        self.orchestrator.distribute_task(development_task, "TeamOfCoders")
        print("✓ Development initiation")

        # Performance testing
        simulator = self.orchestrator.agents["Simulator"]
        simulation_task = AgentTask(
            id="task_sim_001",
            agent_name="Simulator",
            description="Run performance simulations and stress testing",
            requirements={
                "duration": "2 hours",
                "load": "High traffic (1000+ users)",
                "metrics": ["response_time", "throughput", "resource_usage"]
            }
        )
        self.orchestrator.distribute_task(simulation_task, "Simulator")
        print("✓ Performance testing initiated")

        return [planning_task, research_task, backend_task, frontend_task, ml_task, math_task, design_task, development_task, simulation_task]

    def run_collaborative_task(self, task_description: str, target_agents: List[str] = None):
        """
        Run a collaborative task across multiple agents.

        Args:
            task_description: Description of the task to execute
            target_agents: List of agent names to target (optional)

        Returns:
            Dict containing results from all participating agents
        """
        task_id = f"task_{datetime.now().timestamp()}"

        # Create a task
        task = AgentTask(
            id=task_id,
            agent_name="Orchestration",
            description=task_description,
            requirements={},
            assigned_by="User"
        )

        # Distribute to agents
        if target_agents:
            for agent_name in target_agents:
                if agent_name in self.orchestrator.agents:
                    self.orchestrator.distribute_task(task, agent_name)
        else:
            # Distribute to all relevant agents
            for agent in self.orchestrator.agents.values():
                if any(keyword in task_description.lower() for keyword in ["research", "learn", "data"]):
                    if "Researcher" in agent.name or "ML" in agent.name:
                        self.orchestrator.distribute_task(task, agent.name)
                elif any(keyword in task_description.lower() for keyword in ["design", "frontend", "backend", "develop"]):
                    if any(skill in agent.name.lower() for skill in ["frontend", "backend", "coder"]):
                        self.orchestrator.distribute_task(task, agent.name)
                elif any(keyword in task_description.lower() for keyword in ["math", "calculate", "analyze"]):
                    if "Math" in agent.name:
                        self.orchestrator.distribute_task(task, agent.name)
                elif any(keyword in task_description.lower() for keyword in ["visual", "design", "art"]):
                    if "Artist" in agent.name:
                        self.orchestrator.distribute_task(task, agent.name)
                elif any(keyword in task_description.lower() for keyword in ["simulate", "test", "performance"]):
                    if "Simulator" in agent.name:
                        self.orchestrator.distribute_task(task, agent.name)

        # Process the task
        self.orchestrator.process_workflows()

        # Collect results
        results = {}
        for agent in self.orchestrator.agents.values():
            if task_id in agent.tasks:
                task = agent.tasks[task_id]
                if task.status == AgentStatus.COMPLETED:
                    results[agent.name] = task.result

        return results

    def send_message(self, from_agent: str, to_agent: str, content: str, priority: int = 1):
        """
        Send a message from one agent to another.

        Args:
            from_agent: Name of the sender agent
            to_agent: Name of the receiver agent
            content: Message content
            priority: Message priority (1-5)

        Returns:
            The created AgentMessage object
        """
        message_id = f"msg_{datetime.now().timestamp()}"
        message = AgentMessage(
            id=message_id,
            from_agent=from_agent,
            to_agent=to_agent,
            content=content,
            priority=priority
        )
        self.orchestrator.broadcast_message(message)
        return message

    def get_system_status(self):
        """
        Get the current status of the multi-agent system.

        Returns:
            Dict containing system status and agent information
        """
        status = self.orchestrator.get_agent_status()
        total_tasks = 0
        completed_tasks = 0

        for agent in self.orchestrator.agents.values():
            for task in agent.tasks.values():
                total_tasks += 1
                if task.status == AgentStatus.COMPLETED:
                    completed_tasks += 1

        system_status = {
            "timestamp": datetime.now(),
            "total_agents": status["total_agents"],
            "active_agents": sum(1 for agent in self.orchestrator.agents.values() if agent.status == AgentStatus.WORKING),
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "completion_rate": completed_tasks / total_tasks if total_tasks > 0 else 0,
            "agent_details": status["agents"]
        }

        return system_status

    def run_demo(self, topic: str = "AI Analytics Dashboard"):
        """
        Run a complete demonstration of the multi-agent system.

        Args:
            topic: The topic for the demo
        """
        print("\n" + "=" * 70)
        print("INGOT AI Multi-Agent System - DEMO")
        print("=" * 70)

        # Initialize project
        tasks = self.initialize_project(topic)

        # Run specific demos based on topic
        if "research" in topic.lower():
            results = self.run_collaborative_task(
                "Conduct comprehensive market research and competitive analysis",
                ["Researcher", "MLExpert"]
            )
            print(f"\n📊 Research Results: {len(results)} agents contributed")

        elif "development" in topic.lower():
            results = self.run_collaborative_task(
                "Develop complete codebase with tests and documentation",
                ["BackendExpert", "FrontendExpert", "TeamOfCoders"]
            )
            print(f"\n💻 Development Results: {len(results)} agents contributed")

        elif "ml" in topic.lower():
            results = self.run_collaborative_task(
                "Build and validate machine learning models for analytics",
                ["MLExpert", "MathProfessor"]
            )
            print(f"\n🧠 ML Results: {len(results)} agents contributed")

        else:
            # Run all demos
            print("\n🔄 Running complete system demonstration...")

            # Send a coordination message
            self.send_message(
                "Manager",
                "Researcher",
                "Start market research for the analytics dashboard project",
                1
            )

            # Process one workflow iteration
            self.orchestrator.process_workflows()

            # Show system status
            status = self.get_system_status()
            print(f"\n📈 System Status:")
            print(f"   • Active Agents: {status['active_agents']}/{status['total_agents']}")
            print(f"   • Task Completion Rate: {status['completion_rate']*100:.1f}%")

    def get_agent_by_name(self, name: str) -> BaseAgent:
        """
        Get an agent by its name.

        Args:
            name: Name of the agent to retrieve

        Returns:
            The BaseAgent object or None if not found
        """
        return self.orchestrator.agents.get(name)

    def list_agents(self) -> List[str]:
        """
        Get a list of all agent names.

        Returns:
            List of agent names
        """
        return list(self.orchestrator.agents.keys())

    def clear_tasks(self):
        """Clear all tasks from all agents."""
        for agent in self.orchestrator.agents.values():
            agent.tasks.clear()
        print("✓ All tasks cleared")


def main():
    """
    Main entry point for the INGOT Multi-Agent System.

    This function creates the system instance and runs demonstrations.
    """
    print("\n" + "🏢" + "=" * 70 + "🏢")
    print("INGOT AI Multi-Agent System - Main Interface")
    print("=" * 70)

    # Initialize the system
    system = INGOTMultiAgentSystem()

    # Display available agents
    print("\n📋 Available Agents:")
    for i, agent_name in enumerate(system.list_agents(), 1):
        print(f"   {i}. {agent_name}")

    # Run a demonstration
    system.run_demo("AI Analytics Dashboard")

    # Show final status
    print("\n" + "=" * 70)
    status = system.get_system_status()
    print("📊 FINAL SYSTEM STATUS")
    print("=" * 70)
    print(f"Total Agents: {status['total_agents']}")
    print(f"Active Agents: {status['active_agents']}")
    print(f"Tasks Created: {status['total_tasks']}")
    print(f"Tasks Completed: {status['completed_tasks']}")
    print(f"Completion Rate: {status['completion_rate']*100:.1f}%")

    print("\n✨ Multi-Agent System is fully operational!")
    print("The system can now:")
    print("  • Coordinate 9 specialized agents")
    print("  • Process complex workflows")
    print("  • Generate AI-powered solutions")
    print("  • Adapt to different project requirements")

    return 0


if __name__ == "__main__":
    exit(main())
