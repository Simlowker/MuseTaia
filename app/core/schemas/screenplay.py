"""Schemas for the Screenplay format, used by Narrative, Visual, and Director agents."""

from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, Field

class ShotType(str, Enum):
    """Standard cinematographic shot types."""
    EXTREME_WIDE = "extreme_wide_shot"
    WIDE = "wide_shot"
    MEDIUM = "medium_shot"
    CLOSE_UP = "close_up"
    EXTREME_CLOSE_UP = "extreme_close_up"

class CameraMovement(str, Enum):
    """Camera movement types for Veo."""
    STATIC = "static"
    PAN = "pan"
    TILT = "tilt"
    ZOOM_IN = "zoom_in"
    ZOOM_OUT = "zoom_out"
    DOLLY = "dolly"
    TRACKING = "tracking"

class Scene(BaseModel):
    """Represents a single scene or shot in the screenplay."""
    scene_id: str = Field(..., description="Unique ID for the scene")
    visual_description: str = Field(..., description="Detailed visual description for Imagen")
    audio_description: Optional[str] = Field(None, description="Sound effects or music cues")
    voiceover: Optional[str] = Field(None, description="Spoken dialogue")
    shot_type: ShotType = Field(ShotType.MEDIUM, description="Camera shot type")
    camera_movement: CameraMovement = Field(CameraMovement.STATIC, description="Camera movement")
    duration: float = Field(..., gt=0, description="Duration in seconds")
    attention_boost: bool = Field(False, description="Force une rupture de motif dans cette scène")

class AttentionDynamics(BaseModel):
    """Paramètres pour maximiser le ROI attentionnel."""
    pattern_interruption_trigger: float = Field(8.0, description="Rupture visuelle toutes les X secondes")
    interruption_type: str = Field("visual_snap", description="Type de transition (glitch, snap, zoom)")

class Screenplay(BaseModel):
    """The full screenplay document."""
    title: str
    concept: str = Field(..., description="High-level concept or summary")
    scenes: List[Scene]
    attention_dynamics: AttentionDynamics = Field(default_factory=AttentionDynamics)
    total_duration: float = Field(..., description="Total estimated duration")
