"""Manual verification script for Governance Lobe and System CLI."""

import subprocess
import os
from app.agents.critic_agent import CriticAgent
from app.agents.finance_agent import FinanceAgent
from app.state.models import Wallet

def verify_governance_lobe():
    print("--- Verifying CriticAgent ---")
    critic = CriticAgent()
    try:
        # Mocking small images for prompt validation
        report = critic.verify_consistency(b"fake_target", [b"fake_ref"])
        print(f"Consistency Score: {report.score}")
        print(f"Is Consistent (>=0.98): {report.is_consistent}")
    except Exception as e:
        print(f"CriticAgent verification failed: {e}")

    print("\n--- Verifying FinanceAgent ---")
    finance = FinanceAgent()
    try:
        wallet = Wallet(balance=1000.0, internal_usd_balance=100.0)
        summary = finance.summarize_health(wallet, [])
        print(f"Financial Status: {summary.status}")
        print(f"Strategic Advice: {summary.advice}")
    except Exception as e:
        print(f"FinanceAgent verification failed: {e}")

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
