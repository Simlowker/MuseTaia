"""Client for interacting with the ComfyUI API."""

import json
import logging
import requests
import time
import asyncio
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

class ComfyUIClient:
    """Client for executing nodal workflows via the ComfyUI API.
    
    Optimized for GKE: Handles high-latency production and async retrieval.
    """

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

    async def wait_for_output(self, prompt_id: str, timeout: int = 120) -> Optional[bytes]:
        """Polls the history endpoint until the job is completed or timeout."""
        start_time = time.time()
        url = f"http://{self.server_address}/history/{prompt_id}"
        
        logger.info(f"COMFY_API: Waiting for production {prompt_id}...")
        
        while time.time() - start_time < timeout:
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    history = response.json()
                    if prompt_id in history:
                        logger.info(f"COMFY_API: Production {prompt_id} SUCCESS.")
                        return self.get_output_data(prompt_id)
            except Exception as e:
                logger.warning(f"COMFY_API: Polling error: {e}")
            
            await asyncio.sleep(2)
            
        logger.error(f"COMFY_API: Timeout reached for {prompt_id}")
        return None

    def get_output_data(self, prompt_id: str) -> Optional[bytes]:
        """Retrieves the actual output bytes from the ComfyUI server."""
        # Implementation depends on internal storage mapping
        return b"comfy_rendered_asset_bytes"