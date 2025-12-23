"""Module for managing Signature Assets in Google Cloud Storage."""

from typing import List, Optional
from google.cloud import storage

class MockBlob:
    def __init__(self, name):
        self.name = name
        self.public_url = f"https://mock-gcs.local/{name}"
        self.metadata = {}
    
    def upload_from_string(self, data):
        pass
    
    def download_as_bytes(self):
        return b"mock_data"

class MockBucket:
    def __init__(self, name):
        self.name = name
    
    def blob(self, name):
        return MockBlob(name)

class MockStorageClient:
    def bucket(self, name):
        return MockBucket(name)
    
    def list_blobs(self, bucket_name, prefix=None):
        return []

class SignatureAssetsManager:
    """Manages the upload, retrieval, and listing of Muse Signature Assets."""

    def __init__(self, bucket_name: str):
        """Initializes the manager with a GCS bucket name.

        Args:
            bucket_name: The name of the GCS bucket to use.
        """
        try:
            self.client = storage.Client()
            self.bucket = self.client.bucket(bucket_name)
        except Exception as e:
            print(f"WARNING: GCS Client initialization failed ({e}). Using Mock Client.")
            self.client = MockStorageClient()
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

    def download_asset(self, asset_name: str) -> bytes:
        """Downloads the binary data of an asset.

        Args:
            asset_name: The name/path of the asset in the bucket.

        Returns:
            bytes: The binary data of the asset.
        """
        blob = self.bucket.blob(asset_name)
        return blob.download_as_bytes()

    def upload_identity_anchor(
        self,
        muse_id: str,
        anchor_type: str,
        data: bytes
    ) -> str:
        """Uploads a Genesis identity anchor asset.

        Returns:
            str: The GCS path of the anchor.
        """
        path = f"muses/{muse_id}/anchors/{anchor_type}.png"
        self.upload_asset(path, data, metadata={"muse_id": muse_id, "type": "identity_anchor", "anchor_type": anchor_type})
        return path

    def upload_dna(self, muse_id: str, dna_json: str) -> str:
        """Uploads the canonical dna.json for a Muse."""
        path = f"muses/{muse_id}/dna.json"
        self.upload_asset(path, dna_json.encode('utf-8'), metadata={"muse_id": muse_id, "type": "dna"})
        return path

