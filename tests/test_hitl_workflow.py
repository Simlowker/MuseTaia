"""End-to-end integration test for the Human-In-The-Loop (HITL) collaborative loop."""

import pytest
import asyncio
from unittest.mock import MagicMock, patch, AsyncMock
from app.core.workflow_engine import WorkflowEngine
from app.state.models import Mood, Wallet
from app.core.schemas.qa import QAReport

@pytest.fixture
def mock_agents():
    # Comprehensive patching
    with patch("app.core.workflow_engine.NarrativeAgent") as m_narrative, \
         patch("app.core.workflow_engine.VisualAgent") as m_visual, \
         patch("app.core.workflow_engine.CriticAgent") as m_critic, \
         patch("app.core.workflow_engine.DirectorAgent") as m_director, \
         patch("app.core.workflow_engine.EICAgent") as m_eic, \
         patch("app.core.workflow_engine.ArchitectAgent") as m_architect, \
         patch("app.core.workflow_engine.StylistAgent") as m_stylist, \
         patch("app.core.workflow_engine.PromptOptimizer") as m_optimizer, \
         patch("app.core.workflow_engine.WorldAssetsManager") as m_world_assets, \
         patch("app.core.workflow_engine.WardrobeAssetsManager") as m_wardrobe_assets, \
         patch("app.core.services.ledger_service.get_redis_client") as m_redis:
        
        mock_redis_client = m_redis.return_value
        yield {
            "narrative": m_narrative.return_value,
            "visual": m_visual.return_value,
            "critic": m_critic.return_value,
            "director": m_director.return_value,
            "eic": m_eic.return_value,
            "architect": m_architect.return_value,
            "stylist": m_stylist.return_value,
            "optimizer": m_optimizer.return_value,
            "world_assets": m_world_assets.return_value,
            "wardrobe_assets": m_wardrobe_assets.return_value,
            "redis": mock_redis_client
        }

@pytest.mark.asyncio
async def test_full_collaborative_workflow(mock_agents):
    """Verifies the collaborative loop with manual signals."""
    engine = WorkflowEngine()
    
    mock_agents["narrative"].generate_content.return_value = MagicMock(title="HITL", script="S", caption="C")
    from app.core.schemas.world import SceneLayout
    mock_agents["architect"].plan_scene_layout.return_value = SceneLayout(location_id="loc", scene_description="d")
    from app.core.schemas.look import LookSelection
    mock_agents["stylist"].select_look.return_value = LookSelection(stylist_note="n", visual_details="d")
    
    mock_agents["optimizer"].optimize.return_value = "P"
    mock_agents["world_assets"].download_asset.return_value = b"ref"
    mock_agents["wardrobe_assets"].download_asset.return_value = b"ref"
    mock_agents["visual"].generate_image.return_value = b"img"
    mock_agents["critic"].verify_consistency.return_value = QAReport(
        is_consistent=True, identity_drift_score=0.99, clip_semantic_score=1.0, failures=[], final_decision="APPROVED"
    )
    mock_agents["director"].generate_video.return_value = b"vid"
    mock_agents["eic"].stage_for_review.return_value = "path"
    
    with patch("app.core.services.ledger_service.StateManager.get_wallet") as m_wallet:
        m_wallet.return_value = Wallet(address="gen", balance=1.0, internal_usd_balance=100.0)
        
        call_count = 0
        def side_effect_get(key):
            nonlocal call_count
            if key == "smos:config:sovereign_mode": return b"false"
            if "smos:swarm:approve:" in key:
                call_count += 1
                if call_count > 1: return b"approve"
            return None
            
        mock_agents["redis"].get.side_effect = side_effect_get

        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(None, engine.produce_video_content, "intent", Mood(valence=0.5), "genesis")
        
        assert result["title"] == "HITL"
        assert call_count >= 2
