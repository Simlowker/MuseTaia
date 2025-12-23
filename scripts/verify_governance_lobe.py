"""Manual verification script for Governance Lobe and System CLI."""

import subprocess
import os
from app.agents.critic_agent import CriticAgent
from app.agents.finance_agent import CFOAgent
from app.state.models import Wallet

def verify_governance_lobe():
    print("--- Verifying CriticAgent ---")
    critic = CriticAgent()
    try:
        # Mocking small images for prompt validation
        # Adjusting signature to match current verify_consistency(gen_bytes, ref_bytes)
        report = critic.verify_consistency(b"fake_target", b"fake_ref")
        print(f"Drift Score: {report.identity_drift_score}")
        print(f"Decision: {report.final_decision}")
    except Exception as e:
        print(f"CriticAgent verification failed: {e}")

    print("\n--- Verifying CFOAgent ---")
    finance = CFOAgent()
    try:
        wallet = Wallet(balance=1000.0, internal_usd_balance=100.0)
        summary = finance.summarize_health(wallet, [])
        print(f"Financial Status: {summary.status}")
        print(f"Strategic Advice: {summary.advice}")
    except Exception as e:
        print(f"CFOAgent verification failed: {e}")

    print("\n--- Verifying Full System CLI ---")
    try:
        # Simulate CLI call
        env = os.environ.copy()
        env["PYTHONPATH"] = "."
        result = subprocess.run(
            ["./.venv/bin/python", "app/main.py", "produce", "--intent", "cyber-punk fashion"],
            capture_output=True,
            text=True,
            env=env
        )
        print(result.stdout)
        if result.stderr:
            print(f"CLI Stderr: {result.stderr}")
    except Exception as e:
        print(f"CLI verification failed: {e}")

if __name__ == "__main__":
    verify_governance_lobe()
