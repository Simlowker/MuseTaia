"use client";

import React, { createContext, useContext, useState } from 'react';
import { MoodState } from '../contexts/system-context';

interface MoodContextType {
  mood: MoodState | null;
  accentColor: string;
  rawMood: MoodState | null;
}

const MoodContext = createContext<MoodContextType | undefined>(undefined);

export function MoodProvider({ children }: { children: React.ReactNode }) {
  const [mood, setMood] = useState<MoodState | null>({
      valence: 0.5,
      arousal: 0.6,
      dominance: 0.8,
      current_state: "FOCUSED",
      current_thought: "Calibrating S-Tier Interface..."
  });

  return (
    <MoodContext.Provider value={{ mood, rawMood: mood, accentColor: '#D4AF37' }}>
      {children}
    </MoodContext.Provider>
  );
}

export function useMood() {
  const context = useContext(MoodContext);
  if (context === undefined) {
    throw new Error('useMood must be used within a MoodProvider');
  }
  return context;
}