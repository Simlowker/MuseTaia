"""A2A (Agent-to-Agent) Pipe protocol for secure context passing."""

import logging
from typing import Any, Dict
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class A2AContext(BaseModel):
    """The secure context package passed between agents."""
    source_agent: str
    target_agent: str
    payload: Dict[str, Any]
    metadata: Dict[str, Any] = {}

class A2APipe:
    """Implements the secure context 'Pipe' between swarm agents."""

    @staticmethod
    def wrap(source: str, target: str, data: Any) -> A2AContext:
        """Wraps agent output into a secure A2A context."""
        logger.info(f"A2A_PIPE: Wrapping context from {source} to {target}")
        return A2AContext(
            source_agent=source,
            target_agent=target,
            payload=data if isinstance(data, dict) else {"data": data}
        )

    @staticmethod
    def unwrap(context: A2AContext) -> Dict[str, Any]:
        """Unwraps the context for the target agent."""
        logger.info(f"A2A_PIPE: Unwrapping context for {context.target_agent}")
        return context.payload
