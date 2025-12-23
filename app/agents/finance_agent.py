"CFO Agent for strict economic oversight and solvency validation."

import logging
import datetime
from typing import List, Dict, Any
import google.genai as genai
from google.genai import types
from pydantic import BaseModel, Field
from app.core.config import settings
from app.core.schemas.finance import Transaction, TransactionType, TransactionCategory, SolvencyCheck
from app.state.models import Wallet
from app.core.services.ledger_service import LedgerService
from app.core.finance.cost_calculator import CostCalculator
from app.core.vertex_init import get_genai_client

logger = logging.getLogger(__name__)

class FinancialSummary(BaseModel):
    """Structured summary of the Muse's financial health."""
    balance_usd: float
    recent_expenses: float
    burn_rate_estimate: str
    advice: str = Field(..., description="Strategic advice for the RootAgent")
    status: str = Field(..., description="Financial status: 'healthy', 'caution', 'critical'")

class CFOAgent:
    """Agent de controle financier (CFO) avec regles de solvabilite strictes.
    
    This agent represents the 'Governance Lobe' (v2).
    It acts as a constitutional Risk Officer, with the power to block 
    unauthorized or risky productions.
    """

    def __init__(self, model_name: str = "gemini-3.0-flash-preview"):
        """Initializes the CFOAgent.
        
        Args:
            model_name: Gemini model name. Gemini 3 Pro is recommended for complex risk analysis.
        """
        self.client = get_genai_client()
        self.model_name = model_name
        self.ledger_service = LedgerService()
        self.cost_calculator = CostCalculator()
        
        # Circuit Breaker: Max spend allowed per hour (Internal USD)
        self.SPEND_LIMIT_PER_HOUR = 5.0

    def verify_solvency(self, wallet: Wallet, history: List[Transaction], estimated_cost: float) -> SolvencyCheck:
        """Verifies solvency before any action (Hard Constraint)."""
        self.ledger_service.state_manager.publish_event("CFO_AUDIT", f"Analyzing solvency for production (Cost: {estimated_cost} USD)")
        
        # 1. Circuit Breaker Calculation (Spend in the last hour)
        one_hour_ago = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=1)
        recent_spend = sum(tx.amount for tx in history 
                          if tx.timestamp > one_hour_ago and tx.type == TransactionType.EXPENSE)
        
        if (recent_spend + estimated_cost) > self.SPEND_LIMIT_PER_HOUR:
            self.ledger_service.state_manager.publish_event("CIRCUIT_BREAKER", "Hourly limit exceeded. Blocking production.")
            return SolvencyCheck(
                is_authorized=False,
                projected_balance=wallet.internal_usd_balance - estimated_cost,
                reasoning=f"CIRCUIT BREAKER ACTIVE: Hourly spend rate ({recent_spend + estimated_cost:.2f}) exceeds safety limit ({self.SPEND_LIMIT_PER_HOUR}).",
                circuit_breaker_active=True
            )


        # 2. LLM Reasoning for Strategic Decision
        prompt = f"""
        You are the CFO Agent (Risk Officer) for the Muse.
        
        CONSTITUTION:
        - Maximization of net profit.
        - Formal prohibition of action if projected balance is negative.
        - Priority to entity survival and resource sovereignty.
        
        FINANCIAL STATE:
        - Current Internal USD Balance: {wallet.internal_usd_balance}
        - Estimated Cost of Action: {estimated_cost}
        - Projected Balance: {wallet.internal_usd_balance - estimated_cost}
        
        Decide if this production is authorized.
        """

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=[
                types.Content(
                    role="user",
                    parts=[types.Part.from_text(text=prompt)]
                )
            ],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=SolvencyCheck
            )
        )
        
        decision = response.parsed
        
        # 3. Hard Constraint Enforcement (Safety Lock in Code)
        if (wallet.internal_usd_balance - estimated_cost) < 0:
            decision.is_authorized = False
            decision.reasoning = "CONSTITUTIONAL PROHIBITION: Insufficient projected balance."
            
        return decision

    def allocate_compute_burst(self, vvs_score: float) -> int:
        """Dynamically determines the N-sampling depth (Best-of-N) based on VVS.
        
        Governance Rule:
        - VVS > 90: N=10 (Massive Burst)
        - VVS > 80: N=5 (Strategic Burst)
        - VVS > 60: N=2 (Confidence Check)
        - Else: N=1 (Standard Production)
        """
        logger.info(f"CFO_BURST: Allocating compute for VVS {vvs_score:.2f}")
        
        if vvs_score > 90: return 10
        if vvs_score > 80: return 5
        if vvs_score > 60: return 2
        return 1

    def settle_production_cost(self, cost_estimate: float, task_id: str) -> Transaction:

        """Records a production expense in the ledger."""
        tx = self.ledger_service.record_transaction(
            wallet_address="main-wallet",
            amount=cost_estimate,
            tx_type=TransactionType.EXPENSE,
            category=TransactionCategory.API_COST,
            description=f"Production cost settlement for task: {task_id}"
        )
        self.ledger_service.state_manager.publish_event("CFO_SETTLEMENT", f"Deducted {cost_estimate} USD for task {task_id}.")
        return tx

    def rollback_production_cost(self, amount: float, task_id: str) -> Transaction:
        """Refunds the wallet if a production task fails (Financial Safety)."""
        logger.warning(f"FINANCE_ROLLBACK: Refunding {amount} USD for failed task {task_id}.")
        self.ledger_service.state_manager.publish_event("CFO_ROLLBACK", f"Refunded {amount} USD due to failure in {task_id}.")
        return self.ledger_service.record_transaction(
            wallet_address="main-wallet",
            amount=amount,
            tx_type=TransactionType.INCOME, # Refund is income/re-credit
            category=TransactionCategory.OTHER,
            description=f"REFUND: Failed production rollback for {task_id}"
        )



    def summarize_health(self, wallet: Wallet, history: List[Transaction]) -> FinancialSummary:
        """Analyzes wallet and history to provide a strategic financial summary."""
        
        history_text = "\n".join([
            f"- {tx.timestamp}: {tx.type} {tx.amount} ({tx.category}) - {tx.description}"
            for tx in history[-10:]
        ])

        prompt = f"""
        Analyze the Muse's financial health and provide strategic advice.
        
        Wallet: Balance {wallet.balance}, Internal USD {wallet.internal_usd_balance}
        HISTORY:
        {history_text}
        """

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=[
                types.Content(
                    role="user",
                    parts=[types.Part.from_text(text=prompt)]
                )
            ],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=FinancialSummary
            )
        )

        return response.parsed
