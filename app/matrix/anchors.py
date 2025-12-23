"""Management of Identity Anchors for visual regression testing."""

from typing import List, Optional
from app.matrix.models import IdentityAnchor

class AnchorRegistry:
    """Registry for managing 'Day 0' identity anchors."""

    def __init__(self):
        self.anchors: List[IdentityAnchor] = []

    def register_anchor(self, anchor: IdentityAnchor):
        """Registers a new identity anchor."""
        self.anchors.append(anchor)

    def get_anchors_for_muse(self, muse_id: str) -> List[IdentityAnchor]:
        """Retrieves all anchors associated with a specific Muse."""
        return [a for a in self.anchors if a.muse_id == muse_id]

    def get_anchor_by_type(self, muse_id: str, asset_type: str) -> Optional[IdentityAnchor]:
        """Retrieves a specific type of anchor for a Muse."""
        for a in self.anchors:
            if a.muse_id == muse_id and a.asset_type == asset_type:
                return a
        return None
