"use client";

import React, { createContext, useContext, useState, useEffect } from 'react';

interface NeuralContextType {
  status: 'connected' | 'disconnected' | 'processing';
  lastPing: number;
  lastEvent: { message: string, type: string, metadata?: any } | null;
  events: any[];
}

const NeuralContext = createContext<NeuralContextType | undefined>(undefined);

export function NeuralProvider({ children }: { children: React.ReactNode }) {
  const [status, setStatus] = useState<'connected' | 'disconnected' | 'processing'>('connected');
  const [lastPing, setLastPing] = useState(Date.now());
  const [lastEvent, setLastEvent] = useState<{ message: string, type: string, metadata?: any } | null>(null);

  // Simulate heartbeat
  useEffect(() => {
    const interval = setInterval(() => {
      setLastPing(Date.now());
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <NeuralContext.Provider value={{ status, lastPing, lastEvent, events: [] }}>
      {children}
    </NeuralContext.Provider>
  );
}

export function useNeural() {
  const context = useContext(NeuralContext);
  if (context === undefined) {
    throw new Error('useNeural must be used within a NeuralProvider');
  }
  return context;
}