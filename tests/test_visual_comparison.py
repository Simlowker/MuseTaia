"""Tests for the VisualComparator."""

import pytest
from unittest.mock import MagicMock, patch
from app.core.utils.visual_comparison import VisualComparator, SimilarityResult

@pytest.fixture
def mock_genai():
    with patch("app.core.utils.visual_comparison.genai") as mock_gen:
        yield mock_gen

def test_compare_identity(mock_genai):
    """Test that identity comparison parses correctly."""
    mock_client = mock_genai.Client.return_value
    
    # Mock result
    mock_result = SimilarityResult(
        similarity_score=0.98,
        identity_match=True,
        deviation_details="Perfect match."
    )
    mock_response = MagicMock()
    mock_response.parsed = mock_result
    mock_client.models.generate_content.return_value = mock_response
    
    comparator = VisualComparator()
    result = comparator.compare_identity(b"anchor", b"render")
    
    assert result.similarity_score == 0.98
    assert result.identity_match is True
    mock_client.models.generate_content.assert_called_once()

def test_calculate_pixel_similarity():
    """Test pixel-level comparison."""
    from PIL import Image
    import io
    
    # Create two identical small images
    img = Image.new("RGB", (10, 10), color="red")
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    data = img_bytes.getvalue()
    
    comparator = VisualComparator()
    score = comparator.calculate_pixel_similarity(data, data)
    
    assert score == 1.0
    
    # Create a different image
    img2 = Image.new("RGB", (10, 10), color="blue")
    img_bytes2 = io.BytesIO()
    img2.save(img_bytes2, format="PNG")
    data2 = img_bytes2.getvalue()
    
    score2 = comparator.calculate_pixel_similarity(data, data2)
    assert score2 < 1.0
