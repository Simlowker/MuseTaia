"""RootAgent implementation using Google ADK / GenAI SDK."""

import logging

from typing import Optional, Dict, Any

import google.genai as genai



from google.genai import types

from app.core.config import settings

from app.state.models import Mood

from app.state.db_access import StateManager

from app.agents.protocols.master_sync import MasterSyncProtocol, CommandIntent

from app.agents.orchestrator import Orchestrator, TaskGraph

from app.core.vertex_init import get_genai_client



logger = logging.getLogger(__name__)



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



    def ping(self) -> str:

        """Sends a ping to the agent to verify connectivity."""

        response = self.chat_session.send_message("Ping")

        return response.text



    def process_sensory_input(self, stimulus: str) -> str:

        """Processes real-time sensory data and updates the internal thought state."""

        prompt = f"SENSORY INPUT: '{stimulus}'. Update internal thought (1-2 sentences)."

        response = self.chat_session.send_message(prompt)

        reaction = response.text.strip()

        

        current_mood = self.state_manager.get_mood()

        current_mood.current_thought = reaction

        self.state_manager.update_mood(current_mood)

        return reaction



    def parse_and_route(self, command_text: str, source_override: str = None) -> CommandIntent:

        """Parses a command and routes it through the Single-Master Protocol."""

        return self.master_sync.parse_command(command_text, source_override)



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
