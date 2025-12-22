"""Orchestrator for decomposing intents into parallel subtasks."""

from typing import List, Dict, Any
from pydantic import BaseModel


class SubTask(BaseModel):
    """Represents a single unit of work for a specific agent."""
    task_id: str
    agent_type: str  # e.g., 'cso', 'narrative', 'visual'
    instruction: str
    dependencies: List[str] = []  # IDs of tasks that must complete first


class TaskPlan(BaseModel):
    """Represents the full execution plan for an intent."""
    original_intent: str
    subtasks: List[SubTask]


class Orchestrator:
    """Manages the decomposition and execution of tasks."""

    def decompose_intent(self, intent_description: str) -> TaskPlan:
        """Decomposes a high-level intent into a structured TaskPlan.

        Args:
            intent_description: The user's high-level goal.

        Returns:
            TaskPlan: A plan containing subtasks for the swarm.
        """
        # In a real implementation, this would use Gemini's function calling
        # or a structured prompt to generate the plan dynamically.
        
        # Heuristic implementation for the MVP foundation
        subtasks = []
        intent_lower = intent_description.lower()
        
        # 1. Strategy Layer (Always needed for complex tasks)
        if "campaign" in intent_lower or "launch" in intent_lower:
            subtasks.append(SubTask(
                task_id="task_1",
                agent_type="cso",
                instruction="Define campaign strategy and key messaging."
            ))
        
        # 2. Narrative Layer
        subtasks.append(SubTask(
            task_id="task_2",
            agent_type="narrative",
            instruction=f"Write script/copy for: {intent_description}",
            dependencies=["task_1"] if len(subtasks) > 0 else []
        ))
        
        # 3. Visual Layer
        subtasks.append(SubTask(
            task_id="task_3",
            agent_type="visual",
            instruction="Generate key visuals/frames.",
            dependencies=["task_2"]
        ))
        
        return TaskPlan(
            original_intent=intent_description,
            subtasks=subtasks
        )
