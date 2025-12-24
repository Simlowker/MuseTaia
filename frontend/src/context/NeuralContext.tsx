"use client";

import React, { createContext, useContext, useEffect, useState } from 'react';

interface SwarmEvent {
  type: string;
  message: string;
  metadata: any;
  timestamp: string;
}

interface NeuralContextType {
  events: SwarmEvent[];
  lastEvent: SwarmEvent | null;
  status: 'connected' | 'disconnected' | 'connecting';
}

const NeuralContext = createContext<NeuralContextType | undefined>(undefined);

export const NeuralProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [events, setEvents] = useState<SwarmEvent[]>([]);
  const [lastEvent, setLastEvent] = useState<SwarmEvent | null>(null);
  const [status, setStatus] = useState<'connected' | 'disconnected' | 'connecting'>('connecting');

  useEffect(() => {
    const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    const eventSource = new EventSource(`${API_URL}/stream/muse-status`);

    eventSource.onopen = () => setStatus('connected');

    eventSource.onmessage = (event) => {
      const newEvent: SwarmEvent = JSON.parse(event.data);
      setLastEvent(newEvent);
      setEvents((prev) => [newEvent, ...prev].slice(0, 100));
    };

    eventSource.onerror = () => setStatus('disconnected');

    return () => eventSource.close();
  }, []);

  return (
    <NeuralContext.Provider value={{ events, lastEvent, status }}>
      {children}
    </NeuralContext.Provider>
  );
};

export const useNeural = () => {
  const context = useContext(NeuralContext);
  if (!context) throw new Error("useNeural must be used within a NeuralProvider");
  return context;
};
