"""Utility for calculating estimated costs of AI model usage."""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

# Approximate pricing per 1k tokens or per generation (Internal USD units)
MODEL_PRICING = {
    "gemini-3-pro-preview-preview": {
        "input_1k": 0.00125,
        "output_1k": 0.00375
    },
    "gemini-3-flash-preview": {
        "input_1k": 0.0001,
        "output_1k": 0.0003
    },
    "imagen-3.0-generate-002": {
        "per_gen": 0.03
    },
    "veo-3.1": {
        "per_second": 0.10 # Conceptual pricing
    }
}

class CostCalculator:
    """Calculates estimated costs based on usage metrics."""

    @staticmethod
    def estimate_text_cost(model_name: str, input_tokens: int, output_tokens: int) -> float:
        """Estimates cost for text generation."""
        pricing = MODEL_PRICING.get(model_name)
        if not pricing:
            return 0.01 # Default fallback
            
        cost = (input_tokens / 1000 * pricing.get("input_1k", 0)) + \
               (output_tokens / 1000 * pricing.get("output_1k", 0))
        return round(cost, 6)

    @staticmethod
    def estimate_image_cost(model_name: str, count: int = 1) -> float:
        """Estimates cost for image generation."""
        pricing = MODEL_PRICING.get(model_name)
        if not pricing:
            return 0.03 * count
        return pricing.get("per_gen", 0.03) * count

    @staticmethod
    def estimate_video_cost(model_name: str, duration_seconds: float) -> float:
        """Estimates cost for video generation."""
        pricing = MODEL_PRICING.get(model_name)
        if not pricing:
            return 0.50 # Default fallback
        return pricing.get("per_second", 0.10) * duration_seconds
