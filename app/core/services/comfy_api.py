"""Client for interacting with the ComfyUI API."""

import json
import logging
import requests
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

class ComfyUIClient:
    """Client for executing nodal workflows via the ComfyUI API."""

    def __init__(self, server_address: str = "localhost:8188"):
        self.server_address = server_address

    def queue_prompt(self, workflow_json: Dict[str, Any]) -> str:
        """Queues a new workflow for execution."""
        p = {"prompt": workflow_json}
        data = json.dumps(p).encode('utf-8')
        url = f"http://{self.server_address}/prompt"
        
        try:
            response = requests.post(url, data=data)
            response.raise_for_status()
            res_json = response.json()
            return res_json['prompt_id']
        except Exception as e:
            logger.error(f"COMFY_API: Failed to queue prompt: {e}")
            return "error"

    def get_history(self, prompt_id: str) -> Dict[str, Any]:
        """Retrieves the history/result of a completed workflow."""
        url = f"http://{self.server_address}/history/{prompt_id}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"COMFY_API: Failed to get history: {e}")
            return {}

    def get_output_data(self, prompt_id: str) -> Optional[bytes]:
        """Conceptual method to retrieve the actual output bytes (image/video)."""
        # In a real ComfyUI setup, we would parse history to find filenames
        # and then fetch from /view endpoint.
        return b"fake_comfy_output"
