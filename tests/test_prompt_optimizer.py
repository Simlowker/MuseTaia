"""Tests for the PromptOptimizer."""

import pytest
from unittest.mock import MagicMock, patch
from app.core.utils.prompt_optimizer import PromptOptimizer

@pytest.fixture
def mock_genai():
    with patch("app.core.utils.prompt_optimizer.get_genai_client") as mock_get:
        mock_client = MagicMock()
        mock_get.return_value = mock_client
        yield mock_client

def test_optimize_prompt(mock_genai):
    """Test that PromptOptimizer expands a simple prompt."""
    mock_client = mock_genai
    mock_response = MagicMock()
    mock_response.text = "Cinematic wide shot of a muse walking on a tropical beach at golden hour, photorealistic, 8k."
    mock_client.models.generate_content.return_value = mock_response
    
    optimizer = PromptOptimizer()
    simple_prompt = "She walks on the beach"
    optimized = optimizer.optimize(simple_prompt)
    
    assert "Cinematic" in optimized
    assert "photorealistic" in optimized
    mock_client.models.generate_content.assert_called_once()
    
def test_initialization(mock_genai):
    """Test initialization."""
    optimizer = PromptOptimizer(model_name="gemini-3.0-flash-preview")
    assert optimizer.model_name == "gemini-3.0-flash-preview"
