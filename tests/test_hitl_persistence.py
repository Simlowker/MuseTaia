"""Tests for the HITL task and proposal persistence."""

import pytest
import json
from unittest.mock import MagicMock, patch
from app.state.db_access import StateManager
from app.core.schemas.swarm import MissionProposal, PendingTask, ProposalStatus
from app.core.schemas.trend import IntentObject, TrendType

@pytest.fixture
def mock_redis():
    with patch("app.state.db_access.get_redis_client") as mock_get:
        mock_client = MagicMock()
        mock_get.return_value = mock_client
        yield mock_client

def test_proposal_persistence(mock_redis):
    sm = StateManager()
    
    intent = IntentObject(
        command="produce", trend_type=TrendType.FASHION, urgency="high",
        target_audience="luxury", raw_intent="Test", parameters={}
    )
    proposal = MissionProposal(
        proposal_id="prop_1",
        intent=intent,
        confidence_score=0.95
    )
    
    sm.add_proposal(proposal)
    mock_redis.rpush.assert_called_once()
    
    # Mock retrieval
    mock_redis.lrange.return_value = [proposal.model_dump_json().encode('utf-8')]
    retrieved = sm.get_proposals()
    assert len(retrieved) == 1
    assert retrieved[0].proposal_id == "prop_1"

def test_pending_task_persistence(mock_redis):
    sm = StateManager()
    task = PendingTask(
        task_id="t1", agent_id="visual_01", step_name="validation",
        context_data={"key": "val"}
    )
    
    sm.set_pending_task(task)
    mock_redis.hset.assert_called_once_with("smos:swarm:pending", "t1", task.model_dump_json())
    
    mock_redis.hget.return_value = task.model_dump_json().encode('utf-8')
    retrieved = sm.get_pending_task("t1")
    assert retrieved.step_name == "validation"
