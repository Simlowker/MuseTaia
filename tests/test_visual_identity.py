"""Tests for Visual Identity and ComfyUI Workflow Integration."""

import pytest
from unittest.mock import MagicMock, patch
from app.core.services.comfy_workflow import IdentityLockedWorkflow
from app.agents.visual_virtuoso import VisualVirtuoso

def test_identity_workflow_generation():
    """Tests that the workflow JSON contains the necessary identity nodes."""
    engine = IdentityLockedWorkflow()
    workflow = engine.build_workflow(
        prompt="A high-fashion portrait",
        face_master_path="muses/genesis/face.png",
        pose_ref_path="poses/dynamic.png"
    )
    
    # Verify PuLID node
    assert workflow["4"]["class_type"] == "PuLID_Apply"
    assert workflow["4"]["inputs"]["weight"] == 0.8
    
    # Verify FaceID node
    assert workflow["5"]["class_type"] == "IPAdapterFaceID"
    
    # Verify ControlNet node
    assert workflow["9"]["class_type"] == "ControlNetApply"
    assert workflow["6"]["inputs"]["model"] == ["9", 0]

@patch("app.core.services.comfy_api.requests.post")
def test_visual_virtuoso_identity_call(mock_post):
    """Tests that VisualVirtuoso triggers the identity workflow."""
    mock_response = MagicMock()
    mock_response.json.return_value = {"prompt_id": "comfy-id-123"}
    mock_post.return_value = mock_response
    
    virtuoso = VisualVirtuoso()
    prompt_id = virtuoso.generate_identity_image(
        prompt="Cyberpunk Muse",
        subject_id="muse-01",
        pulid_weight=0.9
    )
    
    assert prompt_id == "comfy-id-123"
    assert mock_post.called
    # Ensure the workflow sent to requests contains the PuLID weight
    sent_data = mock_post.call_args.kwargs["data"].decode('utf-8')
    assert '"weight": 0.9' in sent_data
