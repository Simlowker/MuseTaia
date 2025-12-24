"use client";

import React from 'react';
import { motion } from 'framer-motion';

export function SynapseLines() {
  return (
    <svg className="absolute inset-0 w-full h-full pointer-events-none z-10 opacity-20">
      <defs>
        <linearGradient id="synapseGradient" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stopColor="transparent" />
          <stop offset="50%" stopColor="var(--sovereign-gold)" />
          <stop offset="100%" stopColor="transparent" />
        </linearGradient>
      </defs>
      
      {/* Left to Center */}
      <motion.line
        x1="300" y1="50%" x2="50%" y2="50%"
        stroke="url(#synapseGradient)"
        strokeWidth="1"
        initial={{ pathLength: 0, opacity: 0 }}
        animate={{ pathLength: 1, opacity: 0.3 }}
        transition={{ duration: 2, repeat: Infinity, repeatType: "reverse" }}
      />
      
      {/* Center to Right */}
      <motion.line
        x1="50%" y1="50%" x2="calc(100% - 360px)" y2="50%"
        stroke="url(#synapseGradient)"
        strokeWidth="1"
        initial={{ pathLength: 0, opacity: 0 }}
        animate={{ pathLength: 1, opacity: 0.3 }}
        transition={{ duration: 2, delay: 0.5, repeat: Infinity, repeatType: "reverse" }}
      />
    </svg>
  );
}