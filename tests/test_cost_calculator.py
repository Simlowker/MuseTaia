"""Tests for the CostCalculator."""

import pytest
from app.core.finance.cost_calculator import CostCalculator

def test_estimate_text_cost():
    # 10k input, 1k output on Pro
    cost = CostCalculator.estimate_text_cost("gemini-3-pro-preview-preview", 10000, 1000)
    # (10 * 0.00125) + (1 * 0.00375) = 0.0125 + 0.00375 = 0.01625
    assert cost == 0.01625

def test_estimate_image_cost():
    cost = CostCalculator.estimate_image_cost("imagen-3.0-generate-002", 2)
    assert cost == 0.06

def test_estimate_video_cost():
    cost = CostCalculator.estimate_video_cost("veo-3.1", 5.0)
    assert cost == 0.50
