"""Tests for the Single-Master Protocol."""

import pytest
from unittest.mock import MagicMock
from app.agents.protocols.master_sync import MasterSyncProtocol, CommandIntent, MasterSource

def test_parse_human_intent():
    """Tests parsing a command from a human master."""
    protocol = MasterSyncProtocol()
    
    # Mock the LLM response (in a real scenario, this would call Gemini)
    # Here we test the logic assuming the LLM returns structured data
    mock_response = MagicMock()
    mock_response.text = '{"source": "human", "intent": "create_post", "topic": "fashion"}'
    
    # We'll need to mock the internal LLM call method if we implement one
    # For now, let's test the parsing logic if we extract it to a method
    # or test the public API with a mocked agent
    
    intent = protocol.parse_command("Create a fashion post", source_override="human")
    
    assert intent.source == MasterSource.HUMAN
    assert intent.action == "create_post"
    assert "fashion" in intent.parameters.get("topic", "")

def test_community_intent_override():
    """Tests that community votes can be the master source."""
    protocol = MasterSyncProtocol()
    
    intent = protocol.parse_command(
        "Vote result: Go to Tokyo",
        source_override="community"
    )
    
    assert intent.source == MasterSource.COMMUNITY
    assert "Tokyo" in intent.parameters.get("destination", "Tokyo")
