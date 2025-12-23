'use client';

import React from 'react';
import { motion } from 'framer-motion';
import { useMood } from '@/context/MoodContext';

export default function NeuralWaveform() {
  const { accentColor } = useMood();

  const bars = Array.from({ length: 60 });

  return (
    <div className="mt-4 p-4 border border-white border-opacity-10 rounded overflow-hidden">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <span className="small text-secondary tracking-widest fw-light" style={{ fontSize: '0.65rem' }}>NEURAL HEARTBEAT | ROOTAGENT_V3</span>
        <span className="text-secondary small fw-light font-monospace" style={{ fontSize: '0.6rem' }}>LATENCY: 0.042s</span>
      </div>

      <div className="d-flex align-items-center justify-content-center gap-1" style={{ height: '40px' }}>
        {bars.map((_, i) => (
          <motion.div
            key={i}
            animate={{
              height: [10, 20, 10],
              opacity: [0.3, 0.6, 0.3]
            }}
            transition={{
              duration: 1.5,
              repeat: Infinity,
              ease: "easeInOut",
              delay: i * 0.1
            }}
            style={{
              width: '1px', // Thinner, more precise
              backgroundColor: accentColor,
              borderRadius: '1px'
            }}
          />
        ))}
      </div>

      <div className="mt-3 text-center">
        <span className="text-secondary small fw-light italic opacity-50" style={{ fontSize: '0.65rem' }}>"Deep scanning cognitive patterns..."</span>
      </div>
    </div>
  );
}
