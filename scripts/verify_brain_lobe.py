"""Manual verification script for Brain Lobe (RootAgent & StrategistAgent)."""

from app.agents.root_agent import RootAgent
from app.agents.strategist import StrategistAgent

def verify_brain_lobe():
    print("--- Verifying RootAgent ---")
    root = RootAgent()
    try:
        # 1. Test Sensory Integration
        reaction = root.process_sensory_input("A sudden surge in virtual fashion interest on social media.")
        print(f"Reaction: {reaction}")
        
        # 2. Test Intent Parsing
        intent = root.parse_and_route("create a high-fashion digital post")
        print(f"Parsed Intent: {intent.action} (Source: {intent.source})")
        
        # 3. Test Orchestration (TaskGraph)
        class MockIntent:
            command = "produce_content"
            trend_type = "fashion"
            raw_intent = "High-fashion digital post"
            
        task_graph = root.execute_intent(MockIntent())
        print(f"TaskGraph nodes: {[n.agent_type for n in task_graph.nodes]}")
        
    except Exception as e:
        print(f"RootAgent verification failed: {e}")

    print("\n--- Verifying StrategistAgent ---")
    strategist = StrategistAgent()
    try:
        strategy = strategist.define_strategy("Develop a digital jewelry collection.")
        print(f"Narrative Angle: {strategy.get('narrative_angle')}")
        print(f"Estimated Credits: {strategy.get('estimated_credits')}")
        
        approved = strategist.evaluate_production_roi(9.0, 50)
        print(f"ROI Evaluation (Score 9, Cost 50): {'Approved' if approved else 'Rejected'}")
        
    except Exception as e:
        print(f"StrategistAgent verification failed: {e}")

if __name__ == "__main__":
    verify_brain_lobe()
