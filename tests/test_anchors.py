"""Tests for the Identity Anchor registry."""

import pytest
from app.matrix.models import IdentityAnchor
from app.matrix.anchors import AnchorRegistry

def test_anchor_registry():
    registry = AnchorRegistry()
    
    anchor = IdentityAnchor(
        anchor_id="a1",
        muse_id="genesis",
        asset_path="muses/genesis/anchors/face.png",
        asset_type="face_front"
    )
    
    registry.register_anchor(anchor)
    
    anchors = registry.get_anchors_for_muse("genesis")
    assert len(anchors) == 1
    assert anchors[0].asset_type == "face_front"
    
    specific = registry.get_anchor_by_type("genesis", "face_front")
    assert specific.anchor_id == "a1"

def test_get_anchor_none():
    registry = AnchorRegistry()
    assert registry.get_anchor_by_type("none", "none") is None
