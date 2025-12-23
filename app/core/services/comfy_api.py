"""Client for interacting with the ComfyUI API."""

import json
import logging
import requests
import time
import asyncio
import io
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

class ComfyUIClient:
    """Client for executing nodal workflows via the ComfyUI API.
    
    Finalized for SMOS v2: Handles real asset retrieval from GKE pods.
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
        """Polls the history endpoint and retrieves the actual generated asset."""
        start_time = time.time()
        url = f"http://{self.server_address}/history/{prompt_id}"
        
        logger.info(f"COMFY_API: Waiting for production {prompt_id}...")
        
        while time.time() - start_time < timeout:
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    history = response.json()
                    if prompt_id in history:
                        job_history = history[prompt_id]
                        # Find the first output image/video in the nodes
                        outputs = job_history.get("outputs", {})
                        for node_id, node_output in outputs.items():
                            if "images" in node_output:
                                file_info = node_output["images"][0]
                                filename = file_info["filename"]
                                subfolder = file_info.get("subfolder", "")
                                folder_type = file_info.get("type", "output")
                                
                                logger.info(f"COMFY_API: Asset found ({filename}). Fetching...")
                                return self.get_output_data(filename, subfolder, folder_type)
                                
            except Exception as e:
                logger.warning(f"COMFY_API: Polling error: {e}")
            
            await asyncio.sleep(2)
            
        logger.error(f"COMFY_API: Timeout reached for {prompt_id}")
        return None

    def get_output_data(self, filename: str, subfolder: str = "", folder_type: str = "output") -> Optional[bytes]:
        """Retrieves the raw bytes of a generated asset via the /view API."""
        url = f"http://{self.server_address}/view"
        params = {
            "filename": filename,
            "subfolder": subfolder,
            "type": folder_type
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.content
        except Exception as e:
            logger.error(f"COMFY_API: Failed to fetch asset data: {e}")
            return None
