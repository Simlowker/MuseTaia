"use client";

import React, { createContext, useContext, useState } from 'react';

interface TrendContextType {
  activeTrend: string | null;
  vvsScore: number;
  trends: any[];
  loading: boolean;
}

const TrendContext = createContext<TrendContextType | undefined>(undefined);

export function TrendProvider({ children }: { children: React.ReactNode }) {
  const [activeTrend, setActiveTrend] = useState<string | null>("Cyber-Baroque");
  const [vvsScore, setVvsScore] = useState(87.5);

  return (
    <TrendContext.Provider value={{ activeTrend, vvsScore, trends: [], loading: false }}>
      {children}
    </TrendContext.Provider>
  );
}

export function useTrend() {
  const context = useContext(TrendContext);
  if (context === undefined) {
    throw new Error('useTrend must be used within a TrendProvider');
  }
  return context;
}

export const useTrends = useTrend;