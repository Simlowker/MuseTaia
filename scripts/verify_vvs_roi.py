"""Manual verification script for VVS Algorithm and ROI Discovery (Perception v2)."""

import asyncio
from app.agents.trend_scout import TrendScout
from app.agents.strategist import StrategistAgent

async def verify_vvs_roi():
    print("--- 1. Testing TrendScout VVS Discovery (Async Apify) ---")
    scout = TrendScout()
    try:
        # Note: This will return empty if APIFY_TOKEN is not set, 
        # but we can verify the formula execution.
        insights = await scout.scan_niche(["virtual couture", "cyberpunk"])
        if not insights:
            print("No insights found (check APIFY_TOKEN).")
        else:
            for insight in insights[:3]:
                print(f"Topic: {insight.topic}")
                print(f"VVS Score: {insight.vvs_score}")
                print(f"Suggested Intent: {insight.suggested_intent}")
        
        # Test mathematical formula directly
        vvs = scout.calculate_vvs(1000, 1.0, 99)
        print(f"\nFormula Verification: 1000 upvotes, 1h age, 99 comments -> VVS: {vvs}")
        
    except Exception as e:
        print(f"Verification failed: {e}")

if __name__ == "__main__":
    asyncio.run(verify_vvs_roi())