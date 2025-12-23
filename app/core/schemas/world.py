"""Schemas for World and Scene Layouts."""

from typing import List, Optional
from pydantic import BaseModel, Field

class SceneLayout(BaseModel):
    """Represents the environmental setup for a specific scene."""
    location_id: str = Field(..., description="ID of the selected location")
    selected_objects: List[str] = Field(default_factory=list, description="IDs of recurring objects to include")
    scene_description: str = Field(..., description="Description of the scene layout and composition")
    lighting_override: Optional[str] = Field(None, description="Specific lighting instructions if different from location default")
