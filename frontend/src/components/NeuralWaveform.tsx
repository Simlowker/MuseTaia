'use client';

import React from 'react';
import { motion } from 'framer-motion';
import { useMood } from '@/context/MoodContext';

export default function NeuralWaveform() {
  const { accentColor } = useMood();

  const bars = Array.from({ length: 40 });

  return (
    <div className="mt-4 p-3 border border-secondary rounded overflow-hidden">
      <div className="d-flex justify-content-between align-items-center mb-3">
        <span className="small text-secondary fw-bold">NEURAL WAVEFORM (ROOTAGENT HEARTBEAT)</span>
        <span className="badge border border-secondary" style={{ color: accentColor }}>LATENCY: 45ms</span>
      </div>
      
      <div className="d-flex align-items-center justify-content-center gap-1" style={{ height: '60px' }}>
        {bars.map((_, i) => (
          <motion.div
            key={i}
            animate={{
              height: [
                Math.random() * 20 + 5,
                Math.random() * 50 + 10,
                Math.random() * 20 + 5
              ]
            }}
            transition={{
              duration: 0.5 + Math.random() * 0.5,
              repeat: Infinity,
              ease: "easeInOut"
            }}
            style={{
              width: '3px',
              backgroundColor: accentColor,
              borderRadius: '2px',
              opacity: 0.6 + Math.random() * 0.4
            }}
          />
        ))}
      </div>
      
      <div className="mt-2 text-center">
        <span className="text-secondary small italic">"Synthesizing emergent trends..."</span>
      </div>
    </div>
  );
}
