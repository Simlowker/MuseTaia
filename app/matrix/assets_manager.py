"""Module for managing Signature Assets in Google Cloud Storage."""

from typing import List, Optional
from google.cloud import storage


class SignatureAssetsManager:
    """Manages the upload, retrieval, and listing of Muse Signature Assets."""

    def __init__(self, bucket_name: str):
        """Initializes the manager with a GCS bucket name.

        Args:
            bucket_name: The name of the GCS bucket to use.
        """
        self.client = storage.Client()
        self.bucket_name = bucket_name
        self.bucket = self.client.bucket(bucket_name)

    def upload_asset(
        self,
        destination_name: str,
        data: bytes,
        metadata: Optional[dict] = None
    ) -> bool:
        """Uploads an asset to the GCS bucket with optional metadata.

        Args:
            destination_name: The destination path in the bucket.
            data: The binary data of the asset.
            metadata: Optional dictionary of metadata to attach to the blob.

        Returns:
            bool: True if the upload was successful, False otherwise.
        """
        try:
            blob = self.bucket.blob(destination_name)
            if metadata:
                blob.metadata = metadata
            blob.upload_from_string(data)
            return True
        except Exception:
            return False

    def get_asset_url(self, asset_name: str) -> str:
        """Returns the public URL of an asset.

        Args:
            asset_name: The name/path of the asset in the bucket.

        Returns:
            str: The public URL of the asset.
        """
        blob = self.bucket.blob(asset_name)
        return blob.public_url

    def list_assets(self, prefix: Optional[str] = None) -> List[str]:
        """Lists assets in the bucket, optionally filtered by a prefix.

        Args:
            prefix: Optional prefix to filter assets by.

        Returns:
            List[str]: A list of asset names.
        """
        blobs = self.client.list_blobs(self.bucket_name, prefix=prefix)
        return [blob.name for blob in blobs]
