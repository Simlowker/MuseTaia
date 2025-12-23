# Track Plan: Sovereign Wallet (FinancialAccountant)

## Phase 1: Ledger & Economy DNA
- [x] Task: Define Wallet & Transaction Schemas
    - **Goal:** Standardize how the Muse's balance and financial history are stored.
    - **Files:** `app/state/models.py` (update), `app/core/schemas/finance.py`
    - **Tech:** Pydantic.
    - **Tests:** Validate transaction objects and balance updates.
- [x] Task: Implement Ledger Service
    - **Goal:** Create a service to record every financial event (Income/Expense).
    - **Files:** `app/core/services/ledger_service.py`
    - **Tech:** Redis (StateDB).
    - **Tests:** Verify concurrent balance updates and history retrieval.
- [ ] Task: Conductor - User Manual Verification 'Ledger & Economy' (Protocol in workflow.md)

## Phase 2: Cost Tracking (API Ledger)
- [ ] Task: Implement Production Cost Estimator
    - **Goal:** Calculate the estimated cost of agent calls (e.g., Gemini tokens, Imagen generations).
    - **Files:** `app/core/finance/cost_calculator.py`
    - **Tech:** Python logic based on model pricing.
- [ ] Task: Integrate Cost Deduction in WorkflowEngine
    - **Goal:** Automatically deduct the estimated cost from the Sovereign Wallet upon task completion.
    - **Files:** `app/core/workflow_engine.py` (update)
    - **Tests:** Verify wallet balance decreases after a production run.
- [ ] Task: Conductor - User Manual Verification 'Cost Tracking' (Protocol in workflow.md)

## Phase 3: Financial Autonomy & Budgeting
- [ ] Task: Implement Budget-Aware Production Logic
    - **Goal:** Ensure the Muse stops production if her wallet balance is insufficient.
    - **Files:** `app/core/workflow_engine.py` (update).
    - **Tests:** Simulate zero balance and verify production is blocked.
- [ ] Task: Implement Sponsorship/Income Interface
    - **Goal:** Add a mechanism to "deposit" funds into the wallet (simulated sponsorships).
    - **Files:** `app/core/services/ledger_service.py` (update).
- [ ] Task: Conductor - User Manual Verification 'Financial Autonomy' (Protocol in workflow.md)

## Phase 4: The FinancialAccountant Agent
- [ ] Task: Implement FinancialAccountant Agent (Gemini 3 Flash)
    - **Goal:** Create an agent that can summarize financial health and advise the RootAgent on production frequency.
    - **Files:** `app/agents/finance_agent.py`
    - **Tech:** Gemini 3 Flash.
    - **Tests:** Verify agent generates accurate financial summaries.
- [ ] Task: Conductor - User Manual Verification 'FinancialAccountant' (Protocol in workflow.md)
