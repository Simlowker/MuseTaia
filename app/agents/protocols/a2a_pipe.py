"""Agent-to-Agent (A2A) Context Pipe for secure data flow."""

from typing import Dict, Any, List

import logging

from pydantic import BaseModel, Field

from app.state.db_access import StateManager



logger = logging.getLogger(__name__)



class A2AContext(BaseModel):

    """The payload that circulates through the ADK TaskGraph."""

    task_id: str

    muse_id: str

    current_step: str

    sandbox_dir: str = Field(..., description="Temporary scratchpad for task data (E2B-style)")

    data: Dict[str, Any] = Field(default_factory=dict)

    assets: List[str] = Field(default_factory=list) # GCS paths



class A2AContextPipe:

    """Manages the lifecycle of context during task execution."""



    def __init__(self, muse_id: str):

        self.muse_id = muse_id

        self.state_manager = StateManager()



    def create_initial_context(self, task_id: str, intent: str) -> A2AContext:

        """Initializes the pipe with a unique sandbox."""

        self.state_manager.publish_event("PIPE_INIT", f"Initializing context for {self.muse_id}", {"task_id": task_id})

        return A2AContext(

            task_id=task_id,

            muse_id=self.muse_id,

            current_step="perception",

            sandbox_dir=f"/tmp/smos/sandbox/{task_id}",

            data={"intent": intent}

        )



    def transition(self, context: A2AContext, next_step: str, update_data: Dict[str, Any]) -> A2AContext:

        """Updates and validates the context during a transition."""

        logger.info(f"A2A_PIPE: Transitioning from {context.current_step} to {next_step}.")

        self.state_manager.publish_event("PIPE_TRANSITION", f"Transition: {context.current_step} -> {next_step}", {"task_id": context.task_id})

        context.current_step = next_step

        context.data.update(update_data)

        return context
