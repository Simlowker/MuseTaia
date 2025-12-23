"""Tests for the World DNA schemas and registry."""

import pytest
from app.matrix.models import WorldLocation, WorldObject
from app.matrix.world_dna import WorldRegistry

def test_world_registry():
    registry = WorldRegistry()
    
    # 1. Register Object
    sofa = WorldObject(
        object_id="blue_sofa",
        name="Blue Velvet Sofa",
        description="A deep blue vintage velvet sofa with gold legs.",
        visual_reference_path="assets/objects/blue_sofa.png",
        properties={"style": "vintage", "color": "blue"}
    )
    registry.register_object(sofa)
    
    # 2. Register Location
    studio = WorldLocation(
        location_id="paris_studio",
        name="Paris Studio Loft",
        description="A bright, airy studio loft in Le Marais with large windows.",
        visual_reference_path="assets/locations/paris_studio.png",
        recurring_objects=["blue_sofa"],
        lighting_setup="Soft morning sunlight"
    )
    registry.register_location(studio)
    
    # 3. Verify Retrieval
    assert registry.get_object("blue_sofa").name == "Blue Velvet Sofa"
    assert registry.get_location("paris_studio").lighting_setup == "Soft morning sunlight"
    
    # 4. Verify Context String
    context = registry.get_location_context("paris_studio")
    assert "Paris Studio Loft" in context
    assert "Blue Velvet Sofa" in context
    assert "Soft morning sunlight" in context

def test_invalid_location_retrieval():
    registry = WorldRegistry()
    assert registry.get_location("none") is None
    assert registry.get_location_context("none") == ""
