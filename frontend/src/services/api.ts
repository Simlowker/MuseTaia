import {
    Mood, Wallet, TrendReport, Signal,
    Production, AgentStatus, PipelineState, Proposal
} from '../types/smos';

export type MoodState = Mood;
export type WalletState = Wallet;

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080';

export const SMOSApi = {
    // State
    getMood: async (): Promise<Mood> => {
        const res = await fetch(`${API_BASE}/state/mood`);
        return res.json();
    },
    getWallet: async (): Promise<Wallet> => {
        const res = await fetch(`${API_BASE}/finance/wallet`);
        return res.json();
    },
    getLedger: async (address: string): Promise<any[]> => {
        const res = await fetch(`${API_BASE}/finance/ledger/${address}`);
        return res.json();
    },

    // Perception
    getTrends: async (): Promise<TrendReport[]> => {
        const res = await fetch(`${API_BASE}/perception/trends/active`);
        return res.json();
    },
    getActiveSignals: async (): Promise<Signal[]> => {
        const res = await fetch(`${API_BASE}/perception/signals/queue`);
        return res.json();
    },

    // Production
    getActiveProductions: async (): Promise<Production[]> => {
        const res = await fetch(`${API_BASE}/studio/productions/active`);
        return res.json();
    },
    getProductionHistory: async (): Promise<Production[]> => {
        const res = await fetch(`${API_BASE}/studio/productions/history`);
        return res.json();
    },

    // Swarm
    getAgentStatuses: async (): Promise<AgentStatus[]> => {
        const res = await fetch(`${API_BASE}/swarm/status`);
        return res.json();
    },
    getPipeline: async (): Promise<PipelineState> => {
        const res = await fetch(`${API_BASE}/swarm/pipeline`);
        return res.json();
    },

    // HITL
    getProposals: async (): Promise<Proposal[]> => {
        const res = await fetch(`${API_BASE}/hitl/proposals`);
        return res.json();
    },
    approveProposal: async (id: string): Promise<void> => {
        await fetch(`${API_BASE}/hitl/proposals/${id}/approve`, { method: 'POST' });
    },
    rejectProposal: async (id: string): Promise<void> => {
        await fetch(`${API_BASE}/hitl/proposals/${id}/reject`, { method: 'POST' });
    },

    // SSE Stream Factory
    connectStream: (): EventSource => {
        return new EventSource(`${API_BASE}/stream/muse-status`);
    }
};

export const smosApi = SMOSApi;