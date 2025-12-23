"""Main entry point for SMOS CLI and System."""

import argparse
import sys
import asyncio
from app.agents.root_agent import RootAgent
from app.core.schemas.trend import IntentObject, TrendType

async def produce_content(topic: str):
    """Simulates the full production flow via the Lobe architecture."""
    print(f"--- SMOS: Initiating Production for topic: {topic} ---")
    
    root = RootAgent()
    
    # 1. Perception & Cognition
    # (In a real run, TrendScout would generate this intent)
    intent = IntentObject(
        command="produce_content",
        trend_type=TrendType.FASHION,
        urgency="medium",
        target_audience="creatives",
        raw_intent=f"High-fashion digital piece about {topic}",
        parameters={}
    )
    
    # 2. Planning (The Brain)
    print("Brain Lobe: Planning execution graph...")
    task_graph = root.execute_intent(intent)
    
    # 3. Execution (Studio & Governance)
    for node in task_graph.nodes:
        print(f"Executing Node: {node.agent_id} ({node.agent_type}) - {node.instruction}")
        # In a real run, the WorkflowEngine would dispatch these to specific agents.
        # Here we just simulate the sequence for the Lobe validation.
        
    print("--- SMOS: Production Intent Processed Successfully ---")

def main():
    parser = argparse.ArgumentParser(description="Sovereign Muse OS CLI")
    subparsers = parser.add_subparsers(dest="command")
    
    produce_parser = subparsers.add_parser("produce", help="Trigger content production")
    produce_parser.add_argument("--intent", required=True, help="The topic or intent for production")
    
    args = parser.parse_args()
    
    if args.command == "produce":
        asyncio.run(produce_content(args.intent))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()