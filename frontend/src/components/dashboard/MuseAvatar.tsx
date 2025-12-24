"use client";

import React from 'react';
import { motion } from 'framer-motion';

interface MuseAvatarProps {
  imageUrl?: string;
  isActive?: boolean;
  mood?: 'positive' | 'neutral' | 'negative';
}

export function MuseAvatar({ imageUrl, isActive = true, mood = 'neutral' }: MuseAvatarProps) {
  const glowColor = {
    positive: 'rgba(212, 175, 55, 0.4)',
    neutral: 'rgba(168, 162, 158, 0.3)',
    negative: 'rgba(220, 38, 38, 0.3)',
  }[mood];

  return (
    <div className="relative flex items-center justify-center">
      {/* Glow Effect */}
      <motion.div
        animate={{
          scale: [1, 1.1, 1],
          opacity: [0.3, 0.6, 0.3],
        }}
        transition={{
          duration: 4,
          repeat: Infinity,
          ease: "easeInOut"
        }}
        className="absolute w-96 h-96 rounded-full blur-3xl"
        style={{ backgroundColor: glowColor }}
      />
      
      {/* Avatar Container */}
      <div className="relative w-72 h-72 rounded-full overflow-hidden border-4 border-white/50 shadow-2xl">
        {imageUrl ? (
          <img 
            src={imageUrl}
            alt="Muse Avatar"
            className="w-full h-full object-cover"
          />
        ) : (
          <div className="w-full h-full bg-gradient-to-br from-stone-300 to-stone-400 flex items-center justify-center">
            <span className="text-stone-500 text-sm">Avatar</span>
          </div>
        )}
        
        {/* Active Indicator */}
        {isActive && (
          <div className="absolute bottom-4 right-4 w-4 h-4 bg-green-500 rounded-full border-2 border-white shadow-lg" />
        )}
      </div>
      
      {/* Subtle Overlay */}
      <div className="absolute inset-0 rounded-full bg-gradient-to-br from-amber-200/10 to-transparent pointer-events-none" />
    </div>
  );
}
