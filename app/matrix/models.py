"""Pydantic models for the Muse DNA and identity anchor."""

from typing import List, Dict
from pydantic import BaseModel, Field


class MuseDNA(BaseModel):
    """Represents the core 'Genesis DNA' of a Sovereign Muse."""

    name: str = Field(..., description="The unique name of the Muse.")
    version: str = Field(..., description="The DNA version.")
    backstory: str = Field(..., description="The comprehensive backstory and origin of the Muse.")
    voice_guidelines: Dict[str, str] = Field(
        ...,
        description="Guidelines for the Muse's signature voice and tone."
    )
    moral_graph: List[str] = Field(
        ...,
        description="The ethical boundaries and decision-making framework of the Muse."
    )

    def to_context_string(self) -> str:
        """Converts the DNA into a structured string suitable for context caching.

        Returns:
            str: A formatted string containing the Muse's DNA.
        """
        voice = "\n".join([f"- {k}: {v}" for k, v in self.voice_guidelines.items()])
        morals = "\n".join([f"- {m}" for m in self.moral_graph])
        
        return (
            f"Identity DNA for {self.name} (v{self.version})\n"
            f"--- Backstory ---\n{self.backstory}\n\n"
            f"--- Voice Guidelines ---\n{voice}\n\n"
            f"--- Moral Graph ---\n{morals}"
        )
