/**
 * API Service for interacting with the SMOS Backend.
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface MoodState {
  valence: number;
  arousal: number;
  dominance: number;
  current_thought?: string;
  last_updated: string;
}

export interface WalletState {
  address: string;
  balance: number;
  currency: string;
  internal_usd_balance: number;
  last_updated: string;
}

export const smosApi = {
  // 1. State Management
  async getMood(): Promise<MoodState> {
    const res = await fetch(`${API_BASE_URL}/state/mood`);
    if (!res.ok) throw new Error('Failed to fetch mood');
    return res.json();
  },

  async getWallet(): Promise<WalletState> {
    const res = await fetch(`${API_BASE_URL}/state/wallet`);
    if (!res.ok) throw new Error('Failed to fetch wallet');
    return res.json();
  },

  // 2. Swarm Control
  async triggerProduction(intent: string, subjectId: string = 'genesis'): Promise<{ task_id: string }> {
    const res = await fetch(`${API_BASE_URL}/swarm/produce`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ intent, subject_id: subjectId }),
    });
    if (!res.ok) throw new Error('Failed to trigger production');
    return res.json();
  },

  // 3. Trends
  async getTrends(): Promise<any[]> {
    const res = await fetch(`${API_BASE_URL}/perception/trends`);
    if (!res.ok) throw new Error('Failed to fetch trends');
    return res.json();
  },

  // 4. Ledger
  async getLedger(walletAddress: string): Promise<any[]> {
    const res = await fetch(`${API_BASE_URL}/finance/ledger/${walletAddress}`);
    if (!res.ok) throw new Error('Failed to fetch ledger');
    return res.json();
  }
};
