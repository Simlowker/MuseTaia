"""Tests for the StateDB access layer."""

import pytest
import json
from unittest.mock import MagicMock, patch
from datetime import datetime
from app.state.models import Mood, Wallet
from app.state.db_access import StateManager

@pytest.fixture
def mock_redis():
    with patch("app.state.db_access.get_redis_client") as mock_get:
        mock_client = MagicMock()
        mock_get.return_value = mock_client
        yield mock_client

def test_mood_default(mock_redis):
    """Test getting mood when none exists."""
    mock_redis.get.return_value = None
    manager = StateManager()
    mood = manager.get_mood()
    
    assert mood.valence == 0.0
    assert mood.arousal == 0.0
    mock_redis.get.assert_called_with("smos:state:mood")

def test_mood_read_write(mock_redis):
    """Test updating and reading mood."""
    manager = StateManager()
    
    # Test Update
    new_mood = Mood(valence=0.5, arousal=0.8, current_thought="Happy")
    manager.update_mood(new_mood)
    
    mock_redis.set.assert_called_once()
    args = mock_redis.set.call_args
    assert args[0][0] == "smos:state:mood"
    saved_json = json.loads(args[0][1])
    assert saved_json["valence"] == 0.5
    assert saved_json["current_thought"] == "Happy"
    
    # Test Read
    mock_redis.get.return_value = json.dumps(saved_json).encode('utf-8')
    retrieved_mood = manager.get_mood()
    assert retrieved_mood.valence == 0.5
    assert retrieved_mood.current_thought == "Happy"

def test_wallet_read_write(mock_redis):
    """Test updating and reading wallet."""
    manager = StateManager()
    address = "123abc456def"
    
    # Test Update
    wallet = Wallet(address=address, balance=100.50)
    manager.update_wallet(wallet)
    
    mock_redis.set.assert_called_once()
    args = mock_redis.set.call_args
    assert args[0][0] == f"smos:state:wallet:{address}"
    
    # Test Read
    saved_json = json.loads(args[0][1])
    mock_redis.get.return_value = json.dumps(saved_json).encode('utf-8')
    
    retrieved_wallet = manager.get_wallet(address)
    assert retrieved_wallet.address == address
    assert retrieved_wallet.balance == 100.50

def test_wallet_not_found(mock_redis):
    """Test getting a non-existent wallet."""
    mock_redis.get.return_value = None
    manager = StateManager()
    wallet = manager.get_wallet("nonexistent")
    assert wallet is None
