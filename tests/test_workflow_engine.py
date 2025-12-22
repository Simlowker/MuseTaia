"""Tests for the WorkflowEngine and the Critic loop."""

import pytest
from unittest.mock import MagicMock, patch
from app.core.workflow_engine import WorkflowEngine
from app.state.models import Mood
from app.agents.critic_agent import ConsistencyReport

@pytest.fixture
def mock_agents():
    with patch("app.core.workflow_engine.NarrativeAgent") as m_narrative, \
         patch("app.core.workflow_engine.VisualAgent") as m_visual, \
         patch("app.core.workflow_engine.CriticAgent") as m_critic, \
         patch("app.core.workflow_engine.DirectorAgent") as m_director, \
         patch("app.core.workflow_engine.EICAgent") as m_eic, \
         patch("app.core.workflow_engine.PromptOptimizer") as m_optimizer, \
         patch("app.core.workflow_engine.SignatureAssetsManager") as m_assets:
        
        yield {
            "narrative": m_narrative.return_value,
            "visual": m_visual.return_value,
            "critic": m_critic.return_value,
            "director": m_director.return_value,
            "eic": m_eic.return_value,
            "optimizer": m_optimizer.return_value,
            "assets": m_assets.return_value
        }

def test_workflow_critic_rejection_loop(mock_agents):
    """Verifies that the engine retries generation if the Critic rejects the asset."""
    engine = WorkflowEngine()
    
    # 1. Mock Narrative
    mock_agents["narrative"].generate_content.return_value = MagicMock(
        title="Test", script="Test script", caption="Test"
    )
    
    # 2. Mock Optimizer
    mock_agents["optimizer"].optimize.return_value = "Optimized prompt"
    
    # 3. Mock Assets
    mock_agents["assets"].download_asset.return_value = b"ref_image"
    
    # 4. Mock Visual - will be called twice
    mock_agents["visual"].generate_image.side_effect = [b"bad_image", b"good_image"]
    
    # 5. Mock Critic - first reject, then accept
    mock_agents["critic"].verify_consistency.side_effect = [
        ConsistencyReport(is_consistent=False, score=0.4, issues=["Bad eyes"]),
        ConsistencyReport(is_consistent=True, score=0.9, issues=[])
    ]
    
    # 6. Mock Director
    mock_agents["director"].generate_video.return_value = b"video_data"

    # 7. Mock EIC
    mock_agents["eic"].stage_for_review.return_value = "reviews/gen/123"
    
    # Run engine
    mood = Mood(valence=0.5)
    result = engine.produce_video_content("test intent", mood, "genesis")
    
    # Verifications
    assert result["video_bytes"] == b"video_data"
    assert result["review_path"] == "reviews/gen/123"
    assert mock_agents["visual"].generate_image.call_count == 2
    assert mock_agents["critic"].verify_consistency.call_count == 2
    assert mock_agents["director"].generate_video.called
    assert mock_agents["eic"].stage_for_review.called

def test_workflow_max_retries_failure(mock_agents):
    """Verifies that the engine fails after max retries if Critic keeps rejecting."""
    engine = WorkflowEngine()
    
    mock_agents["narrative"].generate_content.return_value = MagicMock(
        title="Test", script="Test script", caption="Test"
    )
    mock_agents["optimizer"].optimize.return_value = "Prompt"
    mock_agents["assets"].download_asset.return_value = b"ref"
    mock_agents["visual"].generate_image.return_value = b"bad"
    
    # Always reject
    mock_agents["critic"].verify_consistency.return_value = ConsistencyReport(
        is_consistent=False, score=0.1, issues=["Fail"]
    )
    
    mood = Mood(valence=0.5)
    with pytest.raises(RuntimeError, match="Failed to produce consistent visual after 3 attempts"):
        engine.produce_video_content("test", mood, "genesis", max_retries=3)
