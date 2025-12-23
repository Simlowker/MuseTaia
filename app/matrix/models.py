"""Pydantic models for the Muse DNA and identity anchor."""

from typing import List, Dict
from datetime import datetime, timezone
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


class WorldObject(BaseModel):
    """Represents a persistent object in the Muse's world."""
    object_id: str
    name: str
    description: str
    visual_reference_path: str  # GCS path to reference image
    properties: Dict[str, str] = Field(default_factory=dict)


class WorldLocation(BaseModel):
    """Represents a persistent location in the Muse's world."""
    location_id: str
    name: str
    description: str
    visual_reference_path: str  # GCS path to reference image
    recurring_objects: List[str] = Field(default_factory=list)  # IDs of WorldObjects
    lighting_setup: str = Field(..., description="Signature lighting for this location")


class IdentityAnchor(BaseModel):
    """Represents a 'Day 0' visual reference for regression testing."""
    anchor_id: str
    muse_id: str
    asset_path: str  # GCS path
    asset_type: str  # e.g., 'face_front', 'full_body', 'signature_style'
    embedding_vector: List[float] = Field(default_factory=list) # Conceptual for future Vector Search
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class WardrobeItem(BaseModel):
    """Represents a persistent outfit or clothing item."""
    item_id: str
    name: str
    description: str
    visual_reference_path: str  # GCS path
    tags: List[str] = Field(default_factory=list) # e.g., 'cyberpunk', 'formal'


class SceneProp(BaseModel):
    """Represents a persistent visual prop."""
    prop_id: str
    name: str
    description: str
    visual_reference_path: str  # GCS path
    is_recurring: bool = True



