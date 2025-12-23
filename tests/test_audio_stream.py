"""Tests for the AudioStreamHandler."""

import pytest
from unittest.mock import MagicMock
from app.agents.handlers.audio_stream import AudioStreamHandler
from google.genai import types

def test_extract_transcript():
    """Test extracting text from a mock server message."""
    handler = AudioStreamHandler()
    
    # Mock nested structure
    mock_message = MagicMock()
    mock_part = MagicMock()
    mock_part.text = "Hello, I am the Muse."
    mock_message.server_content.model_turn.parts = [mock_part]
    
    transcript = handler.extract_transcript(mock_message)
    assert transcript == "Hello, I am the Muse."

def test_extract_transcript_empty():
    """Test extracting from empty message."""
    handler = AudioStreamHandler()
    assert handler.extract_transcript(None) is None

def test_prepare_audio_input():
    """Test wrapping audio bytes."""
    handler = AudioStreamHandler()
    audio_bytes = b"fake_audio"
    input_msg = handler.prepare_audio_input(audio_bytes)
    
    assert isinstance(input_msg, types.LiveClientRealtimeInput)
    assert input_msg.media_chunks[0].data == audio_bytes
    assert input_msg.media_chunks[0].mime_type == "audio/pcm"
