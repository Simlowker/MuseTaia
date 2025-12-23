'use client';

import React, { createContext, useContext, useState, useEffect } from 'react';

type Mood = 'authority' | 'reflection' | 'creativity';

interface MoodContextType {
  mood: Mood;
  setMood: (mood: Mood) => void;
  accentColor: string;
}

const MoodContext = createContext<MoodContextType | undefined>(undefined);

export const MoodProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [mood, setMood] = useState<Mood>('reflection');

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
    <MoodContext.Provider value={{ mood, setMood, accentColor }}>
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
