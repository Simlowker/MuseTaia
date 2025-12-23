"""Tests for Wardrobe and Prop DNA."""

import pytest
from app.matrix.models import WardrobeItem, SceneProp
from app.matrix.wardrobe_dna import WardrobeRegistry

def test_wardrobe_registry():
    registry = WardrobeRegistry()
    
    # 1. Register Item
    jacket = WardrobeItem(
        item_id="neon_jacket",
        name="Neon Mesh Jacket",
        description="A translucent mesh jacket with glowing pink neon strips.",
        visual_reference_path="assets/wardrobe/jacket.png",
        tags=["cyberpunk", "active"]
    )
    registry.register_item(jacket)
    
    # 2. Register Prop
    camera = SceneProp(
        prop_id="vintage_camera",
        name="Vintage Leica",
        description="A classic black and chrome 35mm rangefinder camera.",
        visual_reference_path="assets/props/camera.png"
    )
    registry.register_prop(camera)
    
    # 3. Verify Retrieval
    assert registry.get_item("neon_jacket").name == "Neon Mesh Jacket"
    assert registry.get_prop("vintage_camera").name == "Vintage Leica"
    
    # 4. Verify Tag filtering
    cyber_items = registry.list_by_tag("cyberpunk")
    assert len(cyber_items) == 1
    
    # 5. Verify Context
    context = registry.get_look_context(["neon_jacket"], ["vintage_camera"])
    assert "Neon Mesh Jacket" in context
    assert "Vintage Leica" in context
