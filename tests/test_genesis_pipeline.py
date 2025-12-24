"""Tests for the Genesis Pipeline and automated Muse creation."""

import pytest
from unittest.mock import MagicMock, patch
from app.agents.genesis_agent import GenesisAgent
from app.core.schemas.genesis import MuseProposal

@pytest.fixture
def mock_genai():
    with patch("app.agents.genesis_agent.get_genai_client") as mock_get:
        mock_client = MagicMock()
        mock_get.return_value = mock_client
        yield mock_client

def test_genesis_conceptualization(mock_genai):
    """Tests that GenesisAgent generates a valid proposal."""
    agent = GenesisAgent()
    mock_response = MagicMock()
    
    # Mock data following MuseProposal schema
    mock_proposal = {
        "proposal_id": "test-id",
        "concept_summary": "Cyberpunk Nomad",
        "preview_prompt": "Portrait of a nomad",
        "draft_dna": {
            "identity": {
                "name": "Aria", "origin": "Berlin", "age": 24, "niche": "Tech",
                "personality_traits": ["brave"],
                "moral_graph": {
                    "ego": 0.5, "empathy": 0.5, "chaos": 0.5,
                    "autonomy": 0.8, "sophistication": 0.7, "technophilia": 0.9
                }
            },
            "visual_constancy": {
                "physical_features": "Blue eyes",
                "signature_style": "Minimalist"
            }
        }
    }
    
    mock_response.parsed = MuseProposal(**mock_proposal)
    agent.client.models.generate_content.return_value = mock_response
    
    proposal = agent.generate_random_concept()
    
    assert proposal.draft_dna.identity.name == "Aria"
    assert proposal.concept_summary == "Cyberpunk Nomad"

def test_genesis_storage_logic():
    """Tests the automated GCS storage calls."""
    with patch("app.matrix.assets_manager.storage.Client"), \
         patch("app.matrix.assets_manager.SignatureAssetsManager.upload_asset") as mock_upload:
        
        from app.matrix.assets_manager import SignatureAssetsManager
        manager = SignatureAssetsManager(bucket_name="test-bucket")
        
        # Test DNA upload
        dna_json = '{"identity": {"name": "Test"}}'
        manager.upload_dna("test-muse", dna_json)
        
        assert mock_upload.called
        # Verify path
        args = mock_upload.call_args[0]
        assert "muses/test-muse/dna.json" == args[0]
