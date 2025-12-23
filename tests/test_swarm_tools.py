"""Tests for the SwarmToolbox."""

import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from app.agents.tools.swarm_tools import SwarmToolbox
from app.state.models import Mood
from app.core.schemas.trend import TrendReport, RelevanceScore, Sentiment

@pytest.fixture
def mock_swarm():
    with patch("app.agents.tools.swarm_tools.SearchService") as m_search, \
         patch("app.agents.tools.swarm_tools.NarrativeAgent") as m_narrative, \
         patch("app.agents.tools.swarm_tools.VisualAgent") as m_visual, \
         patch("app.agents.tools.swarm_tools.TrendScanner") as m_trend, \
         patch("app.agents.tools.swarm_tools.StateManager") as m_state:
        
        yield {
            "search": m_search.return_value,
            "narrative": m_narrative.return_value,
            "visual": m_visual.return_value,
            "trend": m_trend.return_value,
            "state": m_state.return_value
        }

@pytest.mark.asyncio
async def test_execute_search_tool(mock_swarm):
    toolbox = SwarmToolbox()
    mock_swarm["search"].search.return_value = "Search result"
    
    result = await toolbox.execute_tool("search_web", {"query": "test"})
    assert result == {"result": "Search result"}
    mock_swarm["search"].search.assert_called_with("test")

@pytest.mark.asyncio
async def test_execute_narrative_tool(mock_swarm):
    toolbox = SwarmToolbox()
    mock_swarm["state"].get_mood.return_value = Mood()
    mock_swarm["narrative"].generate_content.return_value = MagicMock(
        model_dump=lambda: {"title": "Script"}
    )
    
    result = await toolbox.execute_tool("generate_narrative", {"topic": "cyberpunk"})
    assert result["title"] == "Script"
    mock_swarm["narrative"].generate_content.assert_called()

def test_tool_definitions(mock_swarm):
    toolbox = SwarmToolbox()
    defs = toolbox.get_tool_definitions()
    assert len(defs) == 1
    assert len(defs[0].function_declarations) == 4
    names = [fd.name for fd in defs[0].function_declarations]
    assert "search_web" in names
    assert "generate_visual_asset" in names
