"""End-End simulation of the SMOS v2 Muse lifecycle."""

import asyncio
import logging
import uuid
from app.agents.trend_scout import TrendScout
from app.agents.strategist import StrategistAgent
from app.agents.finance_agent import CFOAgent
from app.agents.root_agent import RootAgent
from app.core.workflow_engine import WorkflowEngine
from app.state.models import Mood, Wallet
from app.core.schemas.trend import IntentObject, TrendType

# Logging configuration
logging.basicConfig(level=logging.INFO, format="%(name)s: %(message)s")
logger = logging.getLogger("LifecycleSim")

async def run_simulation():
    print("=== SMOS v2: STARTING FULL LIFECYCLE SIMULATION ===")
    
    # Subject Config
    subject_id = "muse-01"
    
    # 1. PERCEPTION (The Scout Lobe)
    print("\n[PHASE 1: PERCEPTION]")
    scout = TrendScout()
    # Simulate discovering a high-velocity trend
    print("TrendScout: Scanning Reddit/TikTok for high-VVS signals...")
    # Using a fake report for the simulation to avoid API calls if token is missing
    class MockVVS:
        score = 8.5
        acceleration = "Peaking"
        engagement_rate = 1200.0
        
    class MockTrend:
        topic = "Cyber-Baroque Digital Couture"
        vvs = MockVVS()
        estimated_roi = 1.8
        suggested_intent = "produce --trend 'Cyber-Baroque' --vvs 8.5"

    trend_report = MockTrend()
    print(f"-> Found Trend: {trend_report.topic} (VVS: {trend_report.vvs.score}, ROI: {trend_report.estimated_roi})")

    # 2. STRATEGY (The Brain Lobe)
    print("\n[PHASE 2: STRATEGY]")
    strategist = StrategistAgent()
    print("Strategist: Evaluating ROI...")
    
    # Production cost estimate (USD)
    est_cost = 0.45 
    
    approved = strategist.evaluate_production_roi(trend_report, est_cost)
    if not approved:
        print("-> Result: ROI too low. Production aborted.")
        return
    
    print(f"-> Result: APPROVED for production. Cost estimate: {est_cost} USD")

    # 3. AUDIT & GOVERNANCE (The Governance Lobe)
    print("\n[PHASE 3: GOVERNANCE AUDIT]")
    cfo = CFOAgent()
    # Mocking a wallet with enough balance
    wallet = Wallet(address=subject_id, internal_usd_balance=10.0, balance=100.0)
    history = [] # Fresh history
    
    print("CFO: Verifying solvency and circuit breakers...")
    solvency = cfo.verify_solvency(wallet, history, est_cost)
    
    if not solvency.is_authorized:
        print(f"-> Result: BLOCKADE. Reason: {solvency.reasoning}")
        return
    
    print(f"-> Result: AUTHORIZED. Projected Balance: {solvency.projected_balance} USD")

    # 4. ORCHESTRATION & PRODUCTION (The Creative Studio Lobe)
    print("\n[PHASE 4: PRODUCTION ORCHESTRATION]")
    root = RootAgent()
    
    # Create the Intent from the perception
    intent = IntentObject(
        command="produce_content",
        trend_type=TrendType.FASHION,
        urgency="high",
        target_audience="luxury-segment",
        raw_intent=f"High-fidelity visual for {trend_report.topic}",
        parameters={"vvs": trend_report.vvs.score}
    )
    
    print("RootAgent: Decomposing intent into TaskGraph...")
    task_graph = root.execute_intent(intent)
    
    for node in task_graph.nodes:
        print(f"-> Executing Node: {node.agent_type} (ID: {node.agent_id})")
        print(f"   Instruction: {node.instruction}")

    # 5. CLOSING THE LOOP (Ledger Settlement)
    print("\n[PHASE 5: SETTLEMENT]")
    tx = cfo.settle_production_cost(est_cost, task_id=str(uuid.uuid4())[:8])
    print(f"-> Ledger: Recorded transaction {tx.transaction_id}. Type: {tx.type}. Amount: {tx.amount}")

    print("\n=== SIMULATION COMPLETED SUCCESSFULLY ===")
    print("SMOS v2 has autonomously perceived, audited, planned and settled a production cycle.")

if __name__ == "__main__":
    asyncio.run(run_simulation())
