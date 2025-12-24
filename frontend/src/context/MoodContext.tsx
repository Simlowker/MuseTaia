'use client';

import React, { createContext, useContext, useState, useEffect } from 'react';
import { smosApi, MoodState } from '@/services/api';

type Mood = 'authority' | 'reflection' | 'creativity';

interface MoodContextType {
  mood: Mood;
  setMood: (mood: Mood) => void;
  accentColor: string;
  rawMood: MoodState | null;
  isSovereign: boolean;
  setIsSovereign: (active: boolean) => void;
}

const MoodContext = createContext<MoodContextType | undefined>(undefined);

export const MoodProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [mood, setMood] = useState<Mood>('reflection');
  const [rawMood, setRawMood] = useState<MoodState | null>(null);
  const [isSovereign, setIsSovereign] = useState<boolean>(true);

  const fetchMood = async () => {
    try {
      const state = await smosApi.getMood();
      setRawMood(state);

      // Dynamic Mood Logic: Map backend valence/arousal to UI labels
      // High Dominance -> Authority
      // High Valence + High Arousal -> Creativity
      // Neutral -> Reflection
      if (state.dominance > 0.7) {
        setMood('authority');
      } else if (state.valence > 0.6 && state.arousal > 0.6) {
        setMood('creativity');
      } else {
        setMood('reflection');
      }
    } catch (error) {
      // Backend might be offline, be silent or warn gently
      // console.warn('Mood sync skipped (backend offline?)'); 
    }
  };

  useEffect(() => {
    // Initial fetch handled by state default or separate async
    const interval = setInterval(fetchMood, 5000); // Poll every 5s
    fetchMood();
    return () => clearInterval(interval);
  }, []);

  const getAccentColor = (currentMood: Mood) => {
    switch (currentMood) {
      case 'authority': return '#D4AF37'; // Authority Gold
      case 'reflection': return '#1A2B48'; // Analytical Blue
      case 'creativity': return '#E0E0E0'; // Swiss Silver (Muted Luxe)
      default: return '#1A2B48';
    }
  };

  const accentColor = getAccentColor(mood);

  return (
    <MoodContext.Provider value={{ mood, setMood, accentColor, rawMood, isSovereign, setIsSovereign }}>
      {children}
    </MoodContext.Provider>
  );
};

export const useMood = () => {
  const context = useContext(MoodContext);
  if (context === undefined) {
    throw new Error('useMood must be used within a MoodProvider');
  }
  return context;
};
