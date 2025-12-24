"use client";

import React, { useState, useEffect } from 'react';

interface WaveformProps {
  color?: string;
  speed?: number;
}

export function Waveform({ color = '#D4AF37', speed = 0.05 }: WaveformProps) {
  const [phase, setPhase] = useState(0);
  
  useEffect(() => {
    const interval = setInterval(() => {
      setPhase(p => (p + speed) % (Math.PI * 2));
    }, 50);
    return () => clearInterval(interval);
  }, [speed]);

  const points = Array.from({ length: 100 }, (_, i) => {
    const x = (i / 99) * 100;
    const y = 50 + Math.sin((i / 10) + phase) * 15 + Math.sin((i / 5) + phase * 1.5) * 10;
    return `${x},${y}`;
  }).join(' ');

  return (
    <svg viewBox="0 0 100 100" className="w-full h-16" preserveAspectRatio="none">
      <defs>
        <linearGradient id="waveGradient" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stopColor={color} stopOpacity="0.3" />
          <stop offset="50%" stopColor={color} stopOpacity="0.8" />
          <stop offset="100%" stopColor={color} stopOpacity="0.3" />
        </linearGradient>
      </defs>
      <polyline
        points={points}
        fill="none"
        stroke="url(#waveGradient)"
        strokeWidth="0.8"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}
