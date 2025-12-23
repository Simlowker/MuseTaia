"""Schemas for the Genesis Pipeline and automated Muse creation."""

from typing import List, Dict, Optional
from pydantic import BaseModel, Field

class MoralGraph(BaseModel):
    """The psychological profile of the Muse."""
    ego: float = Field(..., ge=0.0, le=1.0)
    empathy: float = Field(..., ge=0.0, le=1.0)
    chaos: float = Field(..., ge=0.0, le=1.0)

class GenesisIdentity(BaseModel):
    """Core identity traits for a new Muse."""
    name: str
    origin: str
    age: int
    niche: str
    personality_traits: List[str]
    moral_graph: MoralGraph

class VisualConstancy(BaseModel):
    """Physical anchors for visual consistency."""
    physical_features: str = Field(..., description="Detailed description of the face and body")
    signature_style: str = Field(..., description="Aesthetic and wardrobe directives")

class GenesisDNA(BaseModel):
    """The full DNA object compatible with the Strategist and Visual agents."""
    identity: GenesisIdentity
    visual_constancy: VisualConstancy
    origin_type: str = Field("surprise_me", description="How the Muse was conceived")

class MuseProposal(BaseModel):
    """Short-form proposal for the 'Surprise Me' UI."""
    proposal_id: str
    concept_summary: str
    preview_prompt: str
    draft_dna: GenesisDNA
