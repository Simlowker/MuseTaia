"""Manual verification script for Perception Lobe (TrendScout & Librarian)."""

import os
from app.agents.trend_scout import TrendScout
from app.agents.librarian import Librarian

def verify_perception_lobe():
    print("--- Verifying TrendScout ---")
    scout = TrendScout()
    try:
        report = scout.scout_and_filter("digital jewelry")
        print(f"Topic: {report.topic}")
        print(f"Relevance: {report.relevance}")
        print(f"Summary: {report.summary}")
    except Exception as e:
        print(f"TrendScout failed (likely due to API access): {e}")

    print("\n--- Verifying Librarian ---")
    librarian = Librarian()
    sample_content = "A sovereign digital entity creates high-end virtual fashion items using autonomous AI agents."
    try:
        structure = librarian.extract_viral_structure(sample_content)
        print("Extracted Structure:")
        for key, value in structure.items():
            print(f"  {key}: {value}")
    except Exception as e:
        print(f"Librarian failed (likely due to API access): {e}")

if __name__ == "__main__":
    verify_perception_lobe()

