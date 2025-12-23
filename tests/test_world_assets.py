"""Tests for the World Assets Manager."""

import pytest
from unittest.mock import MagicMock, patch
from app.matrix.world_assets import WorldAssetsManager

@pytest.fixture
def mock_storage_client():
    with patch("google.cloud.storage.Client") as mock_client:
        yield mock_client

def test_upload_location_reference(mock_storage_client):
    manager = WorldAssetsManager(bucket_name="world-bucket")
    mock_bucket = mock_storage_client.return_value.bucket.return_value
    mock_blob = mock_bucket.blob.return_value

    data = b"fake-location-image"
    path = manager.upload_location_reference("paris_studio", data)

    assert path == "world/locations/paris_studio/reference.png"
    mock_bucket.blob.assert_called_with(path)
    mock_blob.upload_from_string.assert_called_once_with(data)

def test_upload_object_reference(mock_storage_client):
    manager = WorldAssetsManager(bucket_name="world-bucket")
    mock_bucket = mock_storage_client.return_value.bucket.return_value
    mock_blob = mock_bucket.blob.return_value

    data = b"fake-object-image"
    path = manager.upload_object_reference("blue_sofa", data)

    assert path == "world/objects/blue_sofa/reference.png"
    mock_bucket.blob.assert_called_with(path)
    mock_blob.upload_from_string.assert_called_once_with(data)
