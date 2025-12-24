"""Tests for the Librarian agent."""

import pytest
from unittest.mock import MagicMock, patch
from app.agents.librarian import Librarian

@pytest.fixture
def mock_genai_client():
    with patch("app.agents.librarian.get_genai_client") as mock_get:
        mock_client = MagicMock()
        mock_get.return_value = mock_client
        yield mock_client

def test_librarian_initialization(mock_genai_client):
    librarian = Librarian()
    assert librarian.model_name == "gemini-3.0-flash-preview"

def test_extract_viral_structure(mock_genai_client):
    librarian = Librarian()
    
    # Mock response
    mock_response = MagicMock()
    mock_response.text = '{"narrative_skeleton": "Hook-Payoff", "viral_score": 9}'
    librarian.client.models.generate_content.return_value = mock_response
    
    structure = librarian.extract_viral_structure("Sample viral video script.")
    
    assert structure["narrative_skeleton"] == "Hook-Payoff"
    assert structure["viral_score"] == 9

def test_get_embeddings(mock_genai_client):
    librarian = Librarian()
    
    # Mock embedding response
    mock_embedding_response = MagicMock()
    mock_values = MagicMock()
    mock_values.values = [0.1, 0.2, 0.3]
    mock_embedding_response.embeddings = [mock_values]
    librarian.client.models.embed_content.return_value = mock_embedding_response
    
    embeddings = librarian.get_embeddings("Test text")
    
    assert embeddings == [0.1, 0.2, 0.3]
    librarian.client.models.embed_content.assert_called_with(
        model="text-embedding-004",
        contents="Test text"
    )
