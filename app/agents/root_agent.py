"""RootAgent implementation using Google ADK / GenAI SDK."""

from typing import Optional, Dict, Any
import google.genai as genai
from google.genai import types
from app.core.config import settings
from app.state.models import Mood
from app.state.db_access import StateManager
from app.agents.protocols.master_sync import MasterSyncProtocol, CommandIntent
from app.agents.orchestrator import Orchestrator, TaskGraph
from app.core.vertex_init import get_genai_client

class HighLevelPlanner:

    """The High Level Planner (HLP) of the SMOS swarm.

    

    This agent represents the 'High Cognition Lobe' (The Brain).

    It is responsible for:

    1. High-level intent analysis and strategic planning.

    2. Delegation of technical tasks to specialized Workers.

    3. Management of the collective swarm intelligence.

    """



    def __init__(self, model_name: str = "gemini-3.0-flash-preview"):

        """Initializes the HLP."""

        self.client = get_genai_client()

        self.chat_session = self.client.chats.create(

            model=model_name,

            config=types.GenerateContentConfig(

                system_instruction=(

                    "You are the High Level Planner (HLP) of the Sovereign Muse OS. "

                    "Your role is to decompose complex goals into actionable tasks for specialized workers. "

                    "You do not perform technical tasks yourself; you are the strategist and orchestrator."

                )

            )

        )

        self.state_manager = StateManager()

        self.master_sync = MasterSyncProtocol()

        self.orchestrator = Orchestrator()



    def execute_intent(self, intent: Any) -> TaskGraph:

        """HLP Role: Decomposes a high-level intent into a delegated Task Graph.

        

        Args:

            intent: A structured IntentObject or CommandIntent.

            

        Returns:

            TaskGraph: The executable graph of sub-agents (Workers).

        """

        logger.info(f"HLP: Planning delegation for intent: {intent}")

        # The Orchestrator acts as the HLP's tactical office

        task_graph = self.orchestrator.plan_execution(intent)

        return task_graph



# RootAgent remains as an alias for backward compatibility during transition

RootAgent = HighLevelPlanner
