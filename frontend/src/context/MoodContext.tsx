'use client';

import React, { createContext, useContext, useState, useEffect } from 'react';
import { smosApi, MoodState } from '@/services/api';

type Mood = 'authority' | 'reflection' | 'creativity';

interface MoodContextType {
  mood: Mood;
  setMood: (mood: Mood) => void;
  accentColor: string;
  rawMood: MoodState | null;
}

const MoodContext = createContext<MoodContextType | undefined>(undefined);

export const MoodProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [mood, setMood] = useState<Mood>('reflection');
  const [rawMood, setRawMood] = useState<MoodState | null>(null);

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
      console.error('Failed to sync mood from backend:', error);
    }
  };

  useEffect(() => {
    fetchMood(); // Initial fetch
    const interval = setInterval(fetchMood, 5000); // Poll every 5s
    return () => clearInterval(interval);
  }, []);

  const getAccentColor = (currentMood: Mood) => {
    switch (currentMood) {
      case 'authority': return '#FFD700'; // Gold
      case 'reflection': return '#0047AB'; // Deep Blue
      case 'creativity': return '#FF00FF'; // Magenta
      default: return '#0047AB';
    }
  };

  const accentColor = getAccentColor(mood);

  return (
    <MoodContext.Provider value={{ mood, setMood, accentColor, rawMood }}>
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
