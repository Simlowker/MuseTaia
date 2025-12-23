"""Registry for dynamic Worker discovery and management."""

from typing import Dict, Type, Any
from app.agents.base_worker import BaseWorker

class WorkerRegistry:
    """Registry to keep track of available skills and their worker implementations."""

    def __init__(self):
        self._workers: Dict[str, Type[BaseWorker]] = {}

    def register_worker(self, skill_name: str, worker_cls: Type[BaseWorker]):
        """Registers a new capability in the swarm."""
        self._workers[skill_name] = worker_cls

    def get_worker_instance(self, skill_name: str, agent_id: str, **kwargs) -> BaseWorker:
        """Instantiates a worker for a specific skill."""
        worker_cls = self._workers.get(skill_name)
        if not worker_cls:
            raise ValueError(f"No worker registered for skill: {skill_name}")
        return worker_cls(agent_id=agent_id, agent_type=skill_name, **kwargs)

# Global instance
registry = WorkerRegistry()
