"""Tests for the Genesis DNA schema and loader."""

import pytest
from pydantic import ValidationError
from unittest.mock import MagicMock, patch
from app.matrix.models import MuseDNA
from app.matrix.dna_loader import DNALoader

def test_muse_dna_model_validation():
    """Tests that the MuseDNA model validates data correctly."""
    # Test valid DNA
    valid_data = {
        "name": "Genesis Muse",
        "version": "1.0",
        "backstory": "Created in the void...",
        "voice_guidelines": {"tone": "Mysterious", "style": "Poetic"},
        "moral_graph": ["No harm", "Seek truth"]
    }
    dna = MuseDNA(**valid_data)
    assert dna.name == "Genesis Muse"
    assert dna.version == "1.0"

    # Test invalid DNA (missing required field 'backstory')
    invalid_data = {
        "name": "Incomplete",
        "version": "1.0",
        "voice_guidelines": {"tone": "Mysterious"},
        "moral_graph": []
    }
    with pytest.raises(ValidationError):
        MuseDNA(**invalid_data)

@patch("app.matrix.dna_loader.ContextCacheManager")
def test_load_genesis_dna(mock_cache_manager_cls):
    """Tests that the DNALoader correctly interacts with the cache manager."""
    mock_manager = mock_cache_manager_cls.return_value
    mock_manager.create_bible_cache.return_value = "cache/resource/123"
    
    loader = DNALoader(cache_manager=mock_manager)
    
    dna_data = {
        "name": "Genesis Muse",
        "version": "1.0",
        "backstory": "Created in the void...",
        "voice_guidelines": {"tone": "Mysterious", "style": "Poetic"},
        "moral_graph": ["No harm", "Seek truth"]
    }
    
    resource_name = loader.load_dna(dna_data)
    
    assert resource_name == "cache/resource/123"
    # Verify that create_bible_cache was called
    mock_manager.create_bible_cache.assert_called_once()
    _, kwargs = mock_manager.create_bible_cache.call_args
    content_arg = kwargs.get("system_instruction")
    assert content_arg is not None
    assert "Genesis Muse" in content_arg
    assert "Mysterious" in content_arg
