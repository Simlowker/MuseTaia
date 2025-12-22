"""Tests for the Orchestrator (Parallel Function Calling)."""

import pytest
from unittest.mock import MagicMock
from app.agents.orchestrator import Orchestrator, TaskPlan, SubTask

def test_decompose_task_simple():
    """Tests decomposing a simple task into subtasks."""
    orchestrator = Orchestrator()
    
    # Mock Gemini response
    # In a real system, the orchestrator would prompt Gemini 3
    # Here we mock the parsing logic
    
    intent_description = "Create a viral post about coffee."
    
    plan = orchestrator.decompose_intent(intent_description)
    
    assert isinstance(plan, TaskPlan)
    assert len(plan.subtasks) > 0
    # Check if we have at least a strategy task and a creation task
    task_types = [t.agent_type for t in plan.subtasks]
    assert "cso" in task_types or "narrative" in task_types
    assert "creative" in task_types or "visual" in task_types

def test_decompose_task_complex():
    """Tests decomposing a complex task."""
    orchestrator = Orchestrator()
    intent_description = "Launch a full campaign for a new sneaker drop."
    
    plan = orchestrator.decompose_intent(intent_description)
    
    assert len(plan.subtasks) >= 3 # Strategy, Visuals, Copy, maybe Social
    assert plan.original_intent == intent_description
