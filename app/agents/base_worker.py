"""Base class for modular 'Worker' agents in the HLP/Worker dichotomy."""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
from pydantic import BaseModel

class WorkerOutput(BaseModel):
    """Standardized output for any worker task."""
    status: str # 'success', 'failure', 'retry'
    data: Dict[str, Any]
    artifacts: List[str] = [] # GCS paths or asset IDs

class BaseWorker(ABC):
    """Abstract base class ensuring a strict execution contract."""

    def __init__(self, agent_id: str, agent_type: str):
        self.agent_id = agent_id
        self.agent_type = agent_type

    @abstractmethod
    async def execute_task(self, instruction: str, context: Dict[str, Any]) -> WorkerOutput:
        """Main execution entry point for the worker."""
        pass

    def validate_capability(self, required_skill: str) -> bool:
        """Checks if the worker can handle a specific skill."""
        return required_skill == self.agent_type
