"""Manual verification script for VVS Algorithm and ROI Discovery."""

from app.agents.trend_scout import TrendScout
from app.agents.strategist import StrategistAgent

def verify_vvs_roi():
    print("--- 1. Testing TrendScout VVS Discovery ---")
    scout = TrendScout()
    try:
        report = scout.scout_and_filter("virtual couture")
        print(f"Topic: {report.topic}")
        print(f"VVS Score: {report.vvs.score}/10 ({report.vvs.acceleration})")
        print(f"Estimated ROI: {report.estimated_roi}")
        
        print("\n--- 2. Testing Strategist ROI Decision ---")
        strategist = StrategistAgent()
        approved = strategist.evaluate_production_roi(report, cost_estimate=0.50)
        print(f"Decision for {report.topic} (Cost 0.50): {'APPROVED' if approved else 'REJECTED'}")
        
    except Exception as e:
        print(f"Verification failed: {e}")

if __name__ == "__main__":
    verify_vvs_roi()
