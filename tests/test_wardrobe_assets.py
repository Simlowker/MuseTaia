"""Tests for the Wardrobe Assets Manager."""

import pytest
from unittest.mock import MagicMock, patch
from app.matrix.wardrobe_assets import WardrobeAssetsManager

@pytest.fixture
def mock_storage_client():
    with patch("google.cloud.storage.Client") as mock_client:
        yield mock_client

def test_upload_wardrobe_reference(mock_storage_client):
    manager = WardrobeAssetsManager(bucket_name="wardrobe-bucket")
    mock_bucket = mock_storage_client.return_value.bucket.return_value
    mock_blob = mock_bucket.blob.return_value

    data = b"fake-clothing-image"
    path = manager.upload_wardrobe_reference("neon_jacket", data)

    assert path == "wardrobe/items/neon_jacket/reference.png"
    mock_bucket.blob.assert_called_with(path)
    mock_blob.upload_from_string.assert_called_once_with(data)

def test_upload_prop_reference(mock_storage_client):
    manager = WardrobeAssetsManager(bucket_name="wardrobe-bucket")
    mock_bucket = mock_storage_client.return_value.bucket.return_value
    mock_blob = mock_bucket.blob.return_value

    data = b"fake-prop-image"
    path = manager.upload_prop_reference("vintage_camera", data)

    assert path == "wardrobe/props/vintage_camera/reference.png"
    mock_bucket.blob.assert_called_with(path)
    mock_blob.upload_from_string.assert_called_once_with(data)
