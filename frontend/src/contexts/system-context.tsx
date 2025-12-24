"use client";

import React, { createContext, useContext, useState, useEffect } from 'react';
import { Mood, Wallet, AgentStatus } from '../types/smos';
import { useSSE } from '../hooks/use-sse';
import { SMOSApi } from '../services/api';

interface SystemState {
    mood: Mood | null;
    wallet: Wallet | null;
    agents: AgentStatus[];
    isStreamConnected: boolean;
}

const SystemContext = createContext<SystemState | undefined>(undefined);

export function SystemProvider({ children }: { children: React.ReactNode }) {
    const [mood, setMood] = useState<Mood | null>(null);
    const [wallet, setWallet] = useState<Wallet | null>(null);
    const [agents, setAgents] = useState<AgentStatus[]>([]);
    
    // Connect to global stream
    const { status, subscribe } = useSSE('http://localhost:8000/events/stream');

    // Initial Fetch
    useEffect(() => {
        SMOSApi.getMood().then(setMood).catch(console.error);
        SMOSApi.getWallet().then(setWallet).catch(console.error);
        SMOSApi.getAgentStatuses().then(setAgents).catch(console.error);
    }, []);

    // Live Updates
    useEffect(() => {
        if (status === 'connected') {
            const unsubMood = subscribe('MOOD_UPDATE', (data: Mood) => setMood(data));
            const unsubWallet = subscribe('WALLET_UPDATE', (data: Wallet) => setWallet(data));
            const unsubAgents = subscribe('AGENT_UPDATE', (data: AgentStatus[]) => setAgents(data));

            return () => {
                unsubMood();
                unsubWallet();
                unsubAgents();
            };
        }
    }, [status, subscribe]);

    return (
        <SystemContext.Provider value={{ 
            mood, 
            wallet, 
            agents,
            isStreamConnected: status === 'connected'
        }}>
            {children}
        </SystemContext.Provider>
    );
}

export function useSystem() {
    const context = useContext(SystemContext);
    if (context === undefined) {
        throw new Error('useSystem must be used within a SystemProvider');
    }
    return context;
}
