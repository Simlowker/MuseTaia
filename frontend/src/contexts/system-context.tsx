"use client";

import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';

// ============================================================================
// TYPES
// ============================================================================

export interface MoodState {
  valence: number;
  arousal: number;
  dominance: number;
  current_state?: string;
  current_thought?: string;
}

export interface WalletState {
  balance: number;
  currency: string;
  daily_spend: number;
  daily_budget: number;
}

export interface TrendSignal {
  id: string;
  title: string;
  vvs_score: number;
  platform: string;
  category: string;
  status: 'detected' | 'analyzing' | 'approved' | 'rejected';
}

export interface Production {
  id: string;
  title: string;
  status: 'pending' | 'active' | 'complete' | 'failed';
  progress: number;
  current_stage: string;
  cost_usd: number;
  thumbnail_url?: string;
}

export interface PipelineNode {
  stage: string;
  status: 'idle' | 'active' | 'complete' | 'blocked';
  message?: string;
}

export interface HITLProposal {
  id: string;
  type: string;
  title: string;
  description: string;
  data: Record<string, unknown>;
}

export interface TimelineEvent {
  id: string;
  type: string;
  label: string;
  timestamp: string;
}

// ============================================================================
// CONTEXT
// ============================================================================

interface SystemContextType {
  // Connection
  isConnected: boolean;

  // State
  mood: MoodState | null;
  wallet: WalletState | null;
  trends: TrendSignal[];
  activeProduction: Production | null;
  pipeline: PipelineNode[];
  timelineEvents: TimelineEvent[];

  // HITL
  pendingProposal: HITLProposal | null;
  approveProposal: (id: string) => void;
  rejectProposal: (id: string) => void;

  // Actions
  refreshState: () => void;
}

const SystemContext = createContext<SystemContextType | null>(null);

// ============================================================================
// MOCK DATA (pour test sans backend)
// ============================================================================

const MOCK_MOOD: MoodState = {
  valence: 0.6,
  arousal: 0.4,
  dominance: 0.7,
  current_state: 'CONFIDENT',
  current_thought: "Analyzing 'Slow Living' trend for potential content...",
};

const MOCK_WALLET: WalletState = {
  balance: 47.82,
  currency: 'USD',
  daily_spend: 12.45,
  daily_budget: 50.00,
};

const MOCK_TRENDS: TrendSignal[] = [
  { id: '1', title: 'Cyber-Baroque Aesthetics', vvs_score: 87.3, platform: 'TikTok', category: 'Design', status: 'analyzing' },
  { id: '2', title: 'Mycelium Materials', vvs_score: 72.1, platform: 'Reddit', category: 'Materials', status: 'detected' },
  { id: '3', title: 'Neo-Brutalist Interiors', vvs_score: 68.5, platform: 'Instagram', category: 'Architecture', status: 'detected' },
];

const MOCK_PIPELINE: PipelineNode[] = [
  { stage: 'PERCEPTION', status: 'complete' },
  { stage: 'STRATEGIST', status: 'complete' },
  { stage: 'CFO GATE', status: 'active', message: 'Evaluating ROI...' },
  { stage: 'HLP', status: 'idle' },
  { stage: 'SWARM', status: 'idle' },
];

const MOCK_TIMELINE: TimelineEvent[] = [
  { id: '1', type: 'scan', label: 'Trend Scan', timestamp: '10:00' },
  { id: '2', type: 'analyze', label: 'Analysis', timestamp: '10:15' },
  { id: '3', type: 'decide', label: 'CFO Review', timestamp: '10:32' },
];

// ============================================================================
// PROVIDER
// ============================================================================

export function SystemProvider({ children }: { children: React.ReactNode }) {
  const [isConnected, setIsConnected] = useState(true);
  const [mood, setMood] = useState<MoodState | null>(MOCK_MOOD);
  const [wallet, setWallet] = useState<WalletState | null>(MOCK_WALLET);
  const [trends, setTrends] = useState<TrendSignal[]>(MOCK_TRENDS);
  const [activeProduction, setActiveProduction] = useState<Production | null>(null);
  const [pipeline, setPipeline] = useState<PipelineNode[]>(MOCK_PIPELINE);
  const [timelineEvents, setTimelineEvents] = useState<TimelineEvent[]>(MOCK_TIMELINE);
  const [pendingProposal, setPendingProposal] = useState<HITLProposal | null>(null);

  // SSE Connection (try real backend, fallback to mock)
  useEffect(() => {
    let eventSource: EventSource | null = null;

    const connect = () => {
      try {
        eventSource = new EventSource('http://localhost:8000/stream/muse-status');

        eventSource.onopen = () => {
          console.log('[SSE] Connected to backend');
          setIsConnected(true);
        };

        eventSource.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data);

            switch (data.type) {
              case 'MOOD_UPDATE':
                setMood(data.metadata);
                break;
              case 'WALLET_UPDATE':
                setWallet(data.metadata);
                break;
              case 'TREND_DETECTED':
                setTrends(prev => [data.metadata, ...prev].slice(0, 10));
                break;
              case 'PIPELINE_UPDATE':
                setPipeline(data.metadata);
                break;
              case 'THOUGHT_STREAM':
                setMood(prev => prev ? { ...prev, current_thought: data.message } : null);
                break;
              case 'HITL_PROPOSAL':
                setPendingProposal(data.metadata);
                break;
            }
          } catch (e) {
            console.error('[SSE] Parse error:', e);
          }
        };

        eventSource.onerror = () => {
          console.log('[SSE] Connection error, using mock data');
          setIsConnected(true); // Still show as connected with mock data
          eventSource?.close();
        };
      } catch (e) {
        console.log('[SSE] Failed to connect, using mock data');
        setIsConnected(true);
      }
    };

    connect();

    return () => {
      eventSource?.close();
    };
  }, []);

  const approveProposal = useCallback((id: string) => {
    console.log('[HITL] Approved:', id);
    setPendingProposal(null);
    // TODO: Send to backend
  }, []);

  const rejectProposal = useCallback((id: string) => {
    console.log('[HITL] Rejected:', id);
    setPendingProposal(null);
    // TODO: Send to backend
  }, []);

  const refreshState = useCallback(() => {
    // Force refresh from backend
    console.log('[System] Refresh requested');
  }, []);

  return (
    <SystemContext.Provider
      value={{
        isConnected,
        mood,
        wallet,
        trends,
        activeProduction,
        pipeline,
        timelineEvents,
        pendingProposal,
        approveProposal,
        rejectProposal,
        refreshState,
      }}
    >
      {children}
    </SystemContext.Provider>
  );
}

// ============================================================================
// HOOK
// ============================================================================

export function useSystem() {
  const context = useContext(SystemContext);
  if (!context) {
    throw new Error('useSystem must be used within SystemProvider');
  }
  return context;
}