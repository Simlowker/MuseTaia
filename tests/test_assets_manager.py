import pytest
from unittest.mock import MagicMock, patch
from app.matrix.assets_manager import SignatureAssetsManager

@pytest.fixture
def mock_storage_client():
    with patch("google.cloud.storage.Client") as mock_client:
        yield mock_client

def test_upload_asset_success(mock_storage_client):
    manager = SignatureAssetsManager(bucket_name="test-bucket")
    mock_bucket = mock_storage_client.return_value.bucket.return_value
    mock_blob = mock_bucket.blob.return_value

    asset_data = b"fake-image-content"
    destination_name = "muses/genesis/face_front.png"
    metadata = {"muse_id": "genesis", "type": "face"}

    result = manager.upload_asset(destination_name, asset_data, metadata=metadata)

    assert result is True
    mock_bucket.blob.assert_called_with(destination_name)
    mock_blob.upload_from_string.assert_called_once_with(asset_data)
    assert mock_blob.metadata == metadata

def test_get_asset_url(mock_storage_client):
    manager = SignatureAssetsManager(bucket_name="test-bucket")
    mock_blob = mock_storage_client.return_value.bucket.return_value.blob.return_value
    mock_blob.public_url = "https://storage.googleapis.com/test-bucket/asset.png"

    url = manager.get_asset_url("asset.png")
    assert url == "https://storage.googleapis.com/test-bucket/asset.png"

def test_list_assets_by_prefix(mock_storage_client):
    manager = SignatureAssetsManager(bucket_name="test-bucket")
    mock_blob = MagicMock()
    mock_blob.name = "muses/genesis/face.png"
    mock_storage_client.return_value.list_blobs.return_value = [mock_blob]

    assets = manager.list_assets(prefix="muses/genesis/")
    assert "muses/genesis/face.png" in assets

def test_upload_asset_failure(mock_storage_client):
    manager = SignatureAssetsManager(bucket_name="test-bucket")
    mock_bucket = mock_storage_client.return_value.bucket.return_value
    mock_blob = mock_bucket.blob.return_value
    mock_blob.upload_from_string.side_effect = Exception("Upload failed")

    result = manager.upload_asset("fail.png", b"data")
    assert result is False
