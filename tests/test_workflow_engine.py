"""Tests for the WorkflowEngine and the Critic loop."""

import pytest
from unittest.mock import MagicMock, patch
from app.core.workflow_engine import WorkflowEngine
from app.state.models import Mood
from app.core.schemas.qa import ConsistencyReport, FeedbackItem

@pytest.fixture
def mock_agents():
    with patch("app.core.workflow_engine.NarrativeAgent") as m_narrative, \
         patch("app.core.workflow_engine.VisualAgent") as m_visual, \
         patch("app.core.workflow_engine.CriticAgent") as m_critic, \
         patch("app.core.workflow_engine.DirectorAgent") as m_director, \
         patch("app.core.workflow_engine.EICAgent") as m_eic, \
         patch("app.core.workflow_engine.ArchitectAgent") as m_architect, \
         patch("app.core.workflow_engine.PromptOptimizer") as m_optimizer, \
         patch("app.core.workflow_engine.WorldAssetsManager") as m_assets:
        
        yield {
            "narrative": m_narrative.return_value,
            "visual": m_visual.return_value,
            "critic": m_critic.return_value,
            "director": m_director.return_value,
            "eic": m_eic.return_value,
            "architect": m_architect.return_value,
            "optimizer": m_optimizer.return_value,
            "assets": m_assets.return_value
        }

def test_workflow_repair_loop(mock_agents):
    """Verifies the inpainting repair loop logic."""
    engine = WorkflowEngine()
    
    # Setup mocks for a repair flow
    mock_agents["narrative"].generate_content.return_value = MagicMock(title="T", script="S", caption="C")
    mock_agents["optimizer"].optimize.return_value = "P"
    mock_agents["assets"].download_asset.return_value = b"ref"
    
    # Architect Mock
    from app.core.schemas.world import SceneLayout
    mock_agents["architect"].plan_scene_layout.return_value = SceneLayout(
        location_id="loc", selected_objects=["obj"], scene_description="desc"
    )
    
    # Visual: 1. Initial Gen (Bad), 2. Inpainted (Good)
    mock_agents["visual"].generate_image.return_value = b"bad_image" # Initial call
    mock_agents["visual"].edit_image.return_value = b"repaired_image" # Repair call
    
    # Critic: 1. Reject with Feedback, 2. Accept
    feedback = FeedbackItem(
        category="identity", description="Fix face", severity=0.8, 
        action_type="inpaint", target_area="face"
    )
    mock_agents["critic"].verify_consistency.side_effect = [
        ConsistencyReport(is_consistent=False, score=0.5, feedback=[feedback]),
        ConsistencyReport(is_consistent=True, score=0.95)
    ]
    
    # Critic Detect Mask
    mock_agents["critic"].detect_mask_area.return_value = [100, 100, 200, 200]
    
    # Mock Mask Creation
    with patch("PIL.Image.open") as mock_img_open:
        mock_img = MagicMock()
        mock_img.size = (1000, 1000)
        mock_img_open.return_value.__enter__.return_value = mock_img
        
        mood = Mood(valence=0.5)
        result = engine.produce_video_content("test", mood, "gen")
        
        assert result["poster_image_bytes"] == b"repaired_image"
        mock_agents["visual"].generate_image.assert_called_once()
        mock_agents["critic"].detect_mask_area.assert_called_with(b"bad_image", "face")
        mock_agents["visual"].edit_image.assert_called_once()

def test_workflow_critic_rejection_loop(mock_agents):
    """Verifies that the engine retries generation if the Critic rejects the asset."""
    engine = WorkflowEngine()
    
    # 1. Mock Narrative
    mock_agents["narrative"].generate_content.return_value = MagicMock(
        title="Test", script="Test script", caption="Test"
    )
    
    # 2. Mock Architect
    from app.core.schemas.world import SceneLayout
    mock_agents["architect"].plan_scene_layout.return_value = SceneLayout(
        location_id="loc", selected_objects=[], scene_description="desc"
    )
    
    # 3. Mock Optimizer
    mock_agents["optimizer"].optimize.return_value = "Optimized prompt"
    
    # 4. Mock Assets
    mock_agents["assets"].download_asset.return_value = b"ref_image"
    
    # 5. Mock Visual - will be called twice
    mock_agents["visual"].generate_image.side_effect = [b"bad_image", b"good_image"]
    
    # 6. Mock Critic - first reject, then accept
    mock_agents["critic"].verify_consistency.side_effect = [
        ConsistencyReport(is_consistent=False, score=0.4, issues=["Bad eyes"]),
        ConsistencyReport(is_consistent=True, score=0.9, issues=[])
    ]
    
    # 7. Mock Director
    mock_agents["director"].generate_video.return_value = b"video_data"

    # 8. Mock EIC
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
    """Verifies that the engine proceeds with best effort after max retries."""
    engine = WorkflowEngine()
    
    mock_agents["narrative"].generate_content.return_value = MagicMock(
        title="Test", script="Test script", caption="Test"
    )
    from app.core.schemas.world import SceneLayout
    mock_agents["architect"].plan_scene_layout.return_value = SceneLayout(
        location_id="loc", selected_objects=[], scene_description="desc"
    )
    mock_agents["optimizer"].optimize.return_value = "Prompt"
    mock_agents["assets"].download_asset.return_value = b"ref"
    mock_agents["visual"].generate_image.return_value = b"bad"
    mock_agents["director"].generate_video.return_value = b"video"
    mock_agents["eic"].stage_for_review.return_value = "path"
    
    # Always reject
    mock_agents["critic"].verify_consistency.return_value = ConsistencyReport(
        is_consistent=False, score=0.1, issues=["Fail"]
    )
    
    mood = Mood(valence=0.5)
    
    # Should NOT raise RuntimeError anymore, just proceed
    result = engine.produce_video_content("test", mood, "genesis", max_retries=3)
    
    assert result["video_bytes"] == b"video"
    # verify retries happened
    assert mock_agents["visual"].generate_image.call_count >= 3
