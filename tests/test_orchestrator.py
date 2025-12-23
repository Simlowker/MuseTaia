"""Tests for the ADK Orchestrator."""

import pytest
from unittest.mock import MagicMock
from app.agents.orchestrator import Orchestrator, TaskGraph, SequentialAgent, ParallelAgent
from app.core.schemas.trend import IntentObject, TrendType

@pytest.fixture
def mock_intent():
    return IntentObject(
        command="produce_content",
        trend_type=TrendType.FASHION,
        urgency="high",
        target_audience="luxury",
        raw_intent="Create fashion asset",
        parameters={"--style": "minimalist"}
    )

def test_plan_execution_structure(mock_intent):
    """Tests the TaskGraph structure generation."""
    orchestrator = Orchestrator()
    
    graph = orchestrator.plan_execution(mock_intent)
    
    assert isinstance(graph, TaskGraph)
    assert len(graph.nodes) == 3
    
    # 1. Strategy Node
    assert graph.nodes[0].agent_type == "cso"
    
    # 2. Parallel Swarm Node
    assert isinstance(graph.nodes[1], ParallelAgent)
    assert len(graph.nodes[1].swarm) == 2
    
    # 3. Sequential Pipe Node
    assert isinstance(graph.nodes[2], SequentialAgent)
    assert len(graph.nodes[2].pipeline) == 2

def test_adk_pipeline_logic(mock_intent):
    """Tests that the plan includes specific ADK components."""
    orchestrator = Orchestrator()
    graph = orchestrator.plan_execution(mock_intent)
    
    agent_types = [n.agent_type for n in graph.nodes]
    assert "cso" in agent_types
    assert "creative_swarm" in agent_types
    assert "production_pipe" in agent_types

