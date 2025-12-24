"Tests for the WorkflowEngine and the Critic loop."

import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from app.core.workflow_engine import WorkflowEngine
from app.state.models import Mood, Wallet
from app.core.schemas.qa import QAReport, QAFailure

@pytest.fixture
def mock_agents():
    with patch("app.core.vertex_init.get_genai_client") as m_genai, \
         patch("app.core.workflow_engine.NarrativeAgent") as m_narrative, \
         patch("app.core.workflow_engine.VisualAgent") as m_visual, \
         patch("app.core.workflow_engine.CriticAgent") as m_critic, \
         patch("app.core.workflow_engine.DirectorAgent") as m_director, \
         patch("app.core.workflow_engine.EICAgent") as m_eic, \
         patch("app.core.workflow_engine.ArchitectAgent") as m_architect, \
         patch("app.core.workflow_engine.StylistAgent") as m_stylist, \
         patch("app.core.workflow_engine.CFOAgent") as m_cfo, \
         patch("app.core.workflow_engine.PromptOptimizer") as m_optimizer, \
         patch("app.core.workflow_engine.WorldAssetsManager") as m_world_assets, \
         patch("app.core.workflow_engine.WardrobeAssetsManager") as m_wardrobe_assets, \
         patch("app.core.services.ledger_service.get_redis_client") as m_redis:
        
        # Ensure sovereign mode is ON by default to avoid hanging in loops
        m_redis.return_value.get.return_value = b"true"
        
        yield {
            "narrative": m_narrative.return_value,
            "visual": m_visual.return_value,
            "critic": m_critic.return_value,
            "director": m_director.return_value,
            "eic": m_eic.return_value,
            "architect": m_architect.return_value,
            "stylist": m_stylist.return_value,
            "cfo": m_cfo.return_value,
            "optimizer": m_optimizer.return_value,
            "world_assets": m_world_assets.return_value,
            "wardrobe_assets": m_wardrobe_assets.return_value,
            "redis": m_redis.return_value
        }

@pytest.fixture
def enough_budget():
    with patch("app.state.db_access.StateManager.get_wallet") as m_get, \
         patch("app.core.services.ledger_service.LedgerService.get_transaction_history") as m_hist:
        m_get.return_value = Wallet(address="any", balance=1.0, internal_usd_balance=1000.0)
        m_hist.return_value = []
        yield m_get

def test_workflow_insufficient_budget(mock_agents):
    """Verifies that the engine blocks production if the wallet is empty."""
    engine = WorkflowEngine()
    
    from app.core.schemas.finance import SolvencyCheck
    mock_agents["cfo"].verify_solvency.return_value = SolvencyCheck(
        is_authorized=False, projected_balance=-1.0, reasoning="Insufficient budget"
    )
    
    low_wallet = Wallet(address="genesis", balance=0, internal_usd_balance=0.01)
    
    with patch("app.state.db_access.StateManager.get_wallet", return_value=low_wallet), \
         patch("app.core.services.ledger_service.LedgerService.get_transaction_history", return_value=[]):
        mood = Mood(valence=0.5)
        with pytest.raises(RuntimeError, match="Financial blockade"):
            engine.produce_video_content("test", mood, "genesis")
            
    assert not mock_agents["narrative"].generate_content.called

def test_workflow_full_swarm_orchestration(mock_agents, enough_budget):
    """Verifies the complete Narrative -> Architect -> Stylist -> Visual -> Critic -> Director flow."""
    engine = WorkflowEngine()
    
    from app.core.schemas.finance import SolvencyCheck
    mock_agents["cfo"].verify_solvency.return_value = SolvencyCheck(
        is_authorized=True, projected_balance=100.0, reasoning="OK"
    )
    
    mock_agents["narrative"].generate_content.return_value = MagicMock(title="T", script="S", caption="C")
    
    from app.core.schemas.world import SceneLayout
    mock_agents["architect"].plan_scene_layout.return_value = SceneLayout(
        location_id="loc", selected_objects=["obj"], scene_description="desc"
    )
    
    from app.core.schemas.look import LookSelection
    mock_agents["stylist"].select_look.return_value = LookSelection(
        item_ids=["item"], prop_ids=["prop"], stylist_note="note", visual_details="details"
    )
    
    mock_agents["optimizer"].optimize.return_value = "Optimized"
    mock_agents["world_assets"].download_asset.return_value = b"asset"
    mock_agents["wardrobe_assets"].download_asset.return_value = b"wardrobe"
    mock_agents["visual"].generate_image.return_value = b"image"
    mock_agents["critic"].verify_consistency.return_value = QAReport(
        is_consistent=True, identity_drift_score=0.9, clip_semantic_score=1.0, failures=[], final_decision="APPROVED"
    )
    mock_agents["director"].generate_video.return_value = b"video"
    mock_agents["eic"].stage_for_review.return_value = "path"
    
    mood = Mood(valence=0.5)
    result = engine.produce_video_content("test", mood, "genesis")
    
    assert result["video_bytes"] == b"video"
    assert "layout" in result
    assert "look" in result
    mock_agents["architect"].plan_scene_layout.assert_called_once()
    mock_agents["stylist"].select_look.assert_called_once()

def test_workflow_repair_loop(mock_agents, enough_budget):
    """Verifies the inpainting repair loop logic."""
    engine = WorkflowEngine()
    
    from app.core.schemas.finance import SolvencyCheck
    mock_agents["cfo"].verify_solvency.return_value = SolvencyCheck(
        is_authorized=True, projected_balance=100.0, reasoning="OK"
    )
    
    mock_agents["narrative"].generate_content.return_value = MagicMock(title="T", script="S", caption="C")
    mock_agents["optimizer"].optimize.return_value = "P"
    mock_agents["world_assets"].download_asset.return_value = b"ref"
    mock_agents["wardrobe_assets"].download_asset.return_value = b"wardrobe"
    
    from app.core.schemas.world import SceneLayout
    mock_agents["architect"].plan_scene_layout.return_value = SceneLayout(
        location_id="loc", selected_objects=[], scene_description="desc"
    )
    from app.core.schemas.look import LookSelection
    mock_agents["stylist"].select_look.return_value = LookSelection(
        item_ids=[], prop_ids=[], stylist_note="n", visual_details="d"
    )
    
    mock_agents["visual"].generate_image.return_value = b"bad_image"
    mock_agents["visual"].edit_image.return_value = b"repaired_image"
    
    # Critic: 1. Reject with Feedback, 2. Accept, 3+ Fallback Accept
    failure = QAFailure(
        area="face", description="Fix face", severity=0.8, 
        action_type="inpaint"
    )
    mock_agents["critic"].verify_consistency.side_effect = [
        QAReport(is_consistent=False, identity_drift_score=0.5, clip_semantic_score=1.0, failures=[failure], final_decision="REPAIR_REQUIRED"),
        QAReport(is_consistent=True, identity_drift_score=0.99, clip_semantic_score=1.0, failures=[], final_decision="APPROVED"),
        QAReport(is_consistent=True, identity_drift_score=0.99, clip_semantic_score=1.0, failures=[], final_decision="APPROVED")
    ]
    mock_agents["critic"].detect_mask_area.return_value = [100, 100, 200, 200]
    
    with patch("PIL.Image.open") as mock_img_open:
        mock_img = MagicMock()
        mock_img.size = (1000, 1000)
        mock_img_open.return_value.__enter__.return_value = mock_img
        
        mood = Mood(valence=0.5)
        result = engine.produce_video_content("test", mood, "gen")
        
        assert result["poster_image_bytes"] == b"repaired_image"
        mock_agents["visual"].edit_image.assert_called_once()

def test_workflow_max_retries_failure(mock_agents, enough_budget):
    """Verifies that the engine proceeds with best effort after max retries."""
    engine = WorkflowEngine()
    
    from app.core.schemas.finance import SolvencyCheck
    mock_agents["cfo"].verify_solvency.return_value = SolvencyCheck(
        is_authorized=True, projected_balance=100.0, reasoning="OK"
    )
    
    mock_agents["narrative"].generate_content.return_value = MagicMock(title="T", script="S", caption="C")
    from app.core.schemas.world import SceneLayout
    mock_agents["architect"].plan_scene_layout.return_value = SceneLayout(location_id="loc", selected_objects=[], scene_description="d")
    from app.core.schemas.look import LookSelection
    mock_agents["stylist"].select_look.return_value = LookSelection(item_ids=[], prop_ids=[], stylist_note="n", visual_details="d")
    
    mock_agents["optimizer"].optimize.return_value = "P"
    mock_agents["world_assets"].download_asset.return_value = b"ref"
    mock_agents["visual"].generate_image.return_value = b"bad"
    mock_agents["director"].generate_video.return_value = b"video"
    mock_agents["eic"].stage_for_review.return_value = "path"
    
    mock_agents["critic"].verify_consistency.return_value = QAReport(
        is_consistent=False, identity_drift_score=0.1, clip_semantic_score=1.0, failures=[], final_decision="REPAIR_REQUIRED"
    )
    
    mood = Mood(valence=0.5)
    result = engine.produce_video_content("test", mood, "genesis", max_retries=3)
    
    assert result["video_bytes"] == b"video"
    assert mock_agents["visual"].generate_image.call_count >= 3