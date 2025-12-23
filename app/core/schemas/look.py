"""Schemas for Wardrobe and Look selection."""

from typing import List, Optional
from pydantic import BaseModel, Field

class LookSelection(BaseModel):
    """Represents the selected outfit and props for a scene."""
    item_ids: List[str] = Field(default_factory=list, description="IDs of selected wardrobe items")
    prop_ids: List[str] = Field(default_factory=list, description="IDs of selected props")
    stylist_note: str = Field(..., description="Explanation of why this look was chosen for the scene")
    visual_details: str = Field(..., description="Specific visual details to add to the generation prompt (e.g., 'zipper glows brightly')")
