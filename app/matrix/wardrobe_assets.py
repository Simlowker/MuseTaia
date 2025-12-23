"""Module for managing Wardrobe and Prop Assets in Google Cloud Storage."""

from typing import Optional
from app.matrix.assets_manager import SignatureAssetsManager

class WardrobeAssetsManager(SignatureAssetsManager):
    """Manages the upload and retrieval of visual references for the Stylist."""

    def __init__(self, bucket_name: str):
        super().__init__(bucket_name)

    def upload_wardrobe_reference(
        self,
        item_id: str,
        data: bytes
    ) -> str:
        """Uploads a reference image for a wardrobe item."""
        path = f"wardrobe/items/{item_id}/reference.png"
        self.upload_asset(path, data, metadata={"item_id": item_id, "type": "wardrobe_ref"})
        return path

    def upload_prop_reference(
        self,
        prop_id: str,
        data: bytes
    ) -> str:
        """Uploads a reference image for a scene prop."""
        path = f"wardrobe/props/{prop_id}/reference.png"
        self.upload_asset(path, data, metadata={"prop_id": prop_id, "type": "prop_ref"})
        return path
