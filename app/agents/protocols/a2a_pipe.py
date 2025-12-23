"""Agent-to-Agent (A2A) Context Pipe for secure data flow."""

from typing import Dict, Any, List
import logging
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

class A2AContext(BaseModel):
    """The payload that circulates through the ADK TaskGraph."""
    task_id: str
    muse_id: str
    current_step: str
    data: Dict[str, Any] = Field(default_factory=dict)
    assets: List[str] = Field(default_factory=list) # GCS paths

class A2AContextPipe:
    """Manages the lifecycle of context during task execution."""

    def __init__(self, muse_id: str):
        self.muse_id = muse_id

    def create_initial_context(self, task_id: str, intent: str) -> A2AContext:
        """Initializes the pipe."""
        return A2AContext(
            task_id=task_id,
            muse_id=self.muse_id,
            current_step="perception",
            data={"intent": intent}
        )

    def transition(self, context: A2AContext, next_step: str, update_data: Dict[str, Any]) -> A2AContext:
        """Updates and validates the context during a transition."""
        logger.info(f"A2A_PIPE: Transitioning from {context.current_step} to {next_step}.")
        context.current_step = next_step
        context.data.update(update_data)
        return context