"""FinancialAccountant Agent for summarizing health and providing economic advice."""

import google.genai as genai
from google.genai import types
from typing import List
from pydantic import BaseModel, Field
from app.core.config import settings
from app.core.schemas.finance import Transaction
from app.state.models import Wallet

class FinancialSummary(BaseModel):
    """Structured summary of the Muse's financial health."""
    balance_usd: float
    recent_expenses: float
    burn_rate_estimate: str
    advice: str = Field(..., description="Strategic advice for the RootAgent")
    status: str = Field(..., description="Financial status: 'healthy', 'caution', 'critical'")

class FinanceAgent:
    """The FinancialAccountant agent responsible for economic oversight."""

    def __init__(self, model_name: str = "gemini-3.0-flash-preview"):
        self.client = genai.Client(
            vertexai=True,
            project=settings.PROJECT_ID,
            location=settings.LOCATION
        )
        self.model_name = model_name

    def summarize_health(self, wallet: Wallet, history: List[Transaction]) -> FinancialSummary:
        """Analyzes wallet and history to provide a strategic financial summary.

        Args:
            wallet: The current wallet state.
            history: List of recent transactions.

        Returns:
            FinancialSummary: Actionable financial insights.
        """
        
        history_text = "\n".join([
            f"- {tx.timestamp}: {tx.type} {tx.amount} ({tx.category}) - {tx.description}"
            for tx in history[-10:] # Last 10
        ])

        prompt = f"""
        You are the FinancialAccountant for a Sovereign Muse.
        
        CURRENT WALLET:
        - Internal USD Balance: {wallet.internal_usd_balance}
        - Primary Balance: {wallet.balance} {wallet.currency}
        
        RECENT TRANSACTIONS:
        {history_text}
        
        Analyze the Muse's financial health. 
        - Estimate the 'burn rate' based on production costs.
        - Provide strategic advice: Should she produce more, slow down, or seek sponsorships?
        - Assign a status: healthy, caution, or critical.
        
        Output a structured JSON response.
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
