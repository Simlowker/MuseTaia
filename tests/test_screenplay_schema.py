"""Tests for the Screenplay schema."""

import pytest
from pydantic import ValidationError
from app.core.schemas.screenplay import Screenplay, Scene, ShotType, CameraMovement

def test_valid_screenplay():
    """Test creating a valid screenplay object."""
    scene1 = Scene(
        scene_id="s1",
        visual_description="A futuristic city skyline at sunset",
        shot_type=ShotType.WIDE,
        camera_movement=CameraMovement.PAN,
        duration=5.0
    )
    
    screenplay = Screenplay(
        title="Future City",
        concept="A look at tomorrow",
        scenes=[scene1],
        total_duration=5.0
    )
    
    assert screenplay.title == "Future City"
    assert len(screenplay.scenes) == 1
    assert screenplay.scenes[0].shot_type == ShotType.WIDE

def test_invalid_duration():
    """Test that negative duration raises validation error."""
    with pytest.raises(ValidationError):
        Scene(
            scene_id="s1",
            visual_description="Test",
            duration=-1.0
        )

def test_enum_validation():
    """Test that invalid enum values raise validation error."""
    with pytest.raises(ValidationError):
        Scene(
            scene_id="s1",
            visual_description="Test",
            shot_type="invalid_shot",
            duration=1.0
        )
