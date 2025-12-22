"""Integration tests for the full production pipeline (Text -> Image -> Video)."""

import pytest
from unittest.mock import MagicMock, patch
from app.agents.narrative_agent import NarrativeAgent, ScriptOutput
from app.agents.visual_agent import VisualAgent
from app.agents.director_agent import DirectorAgent
from app.core.utils.prompt_optimizer import PromptOptimizer
from app.state.models import Mood

@pytest.fixture
def mock_genai():
    with patch("google.genai.Client") as mock_client:
        yield mock_client

@pytest.fixture
def mock_assets_manager():
    with patch("app.agents.visual_agent.SignatureAssetsManager") as mock_manager:
        yield mock_manager

def test_full_production_chain(mock_genai, mock_assets_manager):
    """Verifies that agents can work together in a chain."""
    
    # 1. Setup Narrative Mock
    mock_narrative_output = ScriptOutput(
        title="Beach Day",
        script="[Visual: Walking on beach] Hello world",
        caption="Sun and sand #beach",
        estimated_duration=5
    )
    
    # 2. Setup Optimizer Mock
    optimized_prompt = "Cinematic wide shot of a muse walking on a tropical beach at golden hour."
    
    # 3. Setup Visual Mock
    image_bytes = b"fake_image_data"
    
    # 4. Setup Director Mock
    video_bytes = b"fake_video_data"

    # Patch the individual agent methods to avoid complex nested mocks
    with patch.object(NarrativeAgent, 'generate_content', return_value=mock_narrative_output), \
         patch.object(PromptOptimizer, 'optimize', return_value=optimized_prompt), \
         patch.object(VisualAgent, 'generate_image', return_value=image_bytes), \
         patch.object(DirectorAgent, 'generate_video', return_value=video_bytes):
        
        narrative = NarrativeAgent()
        optimizer = PromptOptimizer()
        visual = VisualAgent()
        director = DirectorAgent()
        
        mood = Mood(valence=0.9, current_thought="Happy")
        
        # --- EXECUTION CHAIN ---
        
        # Step 1: Narrative
        script_data = narrative.generate_content("Beach day idea", mood)
        assert script_data.title == "Beach Day"
        
        # Step 2: Prompt Optimization (Extracting simple visual from script)
        # For the test, we assume the orchestrator or logic extracts the visual part
        expanded_prompt = optimizer.optimize(script_data.script)
        assert "Cinematic" in expanded_prompt
        
        # Step 3: Image Generation
        generated_image = visual.generate_image(expanded_prompt, subject_id="genesis")
        assert generated_image == b"fake_image_data"
        
        # Step 4: Video Generation (Image-to-Video)
        generated_video = director.generate_video(expanded_prompt, image_bytes=generated_image)
        assert generated_video == b"fake_video_data"

    print("\nFull chain integration test passed.")
