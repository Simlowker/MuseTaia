"""Module for managing World Assets (Locations and Objects) in Google Cloud Storage."""

from typing import List, Optional
from google.cloud import storage
from app.matrix.assets_manager import SignatureAssetsManager

class WorldAssetsManager(SignatureAssetsManager):
    """Manages the upload, retrieval, and listing of World persistent assets."""

    def __init__(self, bucket_name: str):
        """Initializes the manager with a GCS bucket name."""
        super().__init__(bucket_name)

    def upload_location_reference(
        self,
        location_id: str,
        data: bytes,
        content_type: str = "image/png"
    ) -> str:
        """Uploads a reference image for a location.

        Returns:
            str: The GCS path of the uploaded asset.
        """
        path = f"world/locations/{location_id}/reference.png"
        self.upload_asset(path, data, metadata={"location_id": location_id, "type": "location_ref"})
        return path

    def upload_object_reference(
        self,
        object_id: str,
        data: bytes,
        content_type: str = "image/png"
    ) -> str:
        """Uploads a reference image for a persistent object.

        Returns:
            str: The GCS path of the uploaded asset.
        """
        path = f"world/objects/{object_id}/reference.png"
        self.upload_asset(path, data, metadata={"object_id": object_id, "type": "object_ref"})
        return path
