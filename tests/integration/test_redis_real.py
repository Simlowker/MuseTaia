"""Integration tests for Redis StateDB using a real server."""

import pytest
from app.state.db_access import StateManager
from app.state.models import Mood, Wallet

@pytest.mark.integration
def test_mood_roundtrip(real_redis):
    """Teste l'écriture et lecture réelle dans Redis."""
    sm = StateManager()
    
    # Écrire
    mood = Mood(valence=0.75, arousal=0.5, current_thought="Integration Testing")
    sm.update_mood(mood)
    
    # Lire
    retrieved = sm.get_mood()
    
    assert retrieved.valence == 0.75
    assert retrieved.current_thought == "Integration Testing"

@pytest.mark.integration
def test_wallet_roundtrip(real_redis):
    """Teste l'écriture et lecture réelle d'un wallet."""
    sm = StateManager()
    
    wallet = Wallet(
        address="test-wallet-real",
        balance=1.5,
        internal_usd_balance=150.0
    )
    sm.update_wallet(wallet)
    
    retrieved = sm.get_wallet("test-wallet-real")
    
    assert retrieved is not None
    assert retrieved.internal_usd_balance == 150.0
    
    # Cleanup
    real_redis.delete(f"smos:state:wallet:test-wallet-real")