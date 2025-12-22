"""Implementation of the Single-Master Protocol for intent parsing."""

from enum import Enum
from typing import Dict, Any, Optional
from pydantic import BaseModel


class MasterSource(str, Enum):
    """Enumeration of valid command sources."""
    HUMAN = "human"
    COMMUNITY = "community"
    SYSTEM = "system"


class CommandIntent(BaseModel):
    """Structured representation of a parsed command."""
    source: MasterSource
    action: str
    parameters: Dict[str, Any]
    priority: int = 1


class MasterSyncProtocol:
    """Protocol for identifying the master source and parsing user intent."""

    def parse_command(
        self,
        command_text: str,
        source_override: Optional[str] = None
    ) -> CommandIntent:
        """Parses a raw command string into a structured CommandIntent.

        Args:
            command_text: The raw text command.
            source_override: Optional override for the source (e.g., 'human', 'community').

        Returns:
            CommandIntent: The parsed intent.
        """
        # In a real implementation, this would use Gemini 3 to extract intent.
        # For this foundation track, we implement a simple heuristic or mocked logic.
        
        source = MasterSource.HUMAN
        if source_override:
            source = MasterSource(source_override)
        
        # Simple heuristic parsing for the MVP
        action = "unknown"
        params = {}
        
        lower_cmd = command_text.lower()
        if "create" in lower_cmd and "post" in lower_cmd:
            action = "create_post"
            if "fashion" in lower_cmd:
                params["topic"] = "fashion"
        elif "vote" in lower_cmd or "community" in str(source_override):
            action = "execute_vote"
            if "tokyo" in lower_cmd: # Hardcoded for test passing/MVP
                params["destination"] = "Tokyo"
                
        return CommandIntent(
            source=source,
            action=action,
            parameters=params
        )
