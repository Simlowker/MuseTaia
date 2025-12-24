"use client";

import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { GlassPanel } from '@/components/ui/GlassPanel';

interface ActiveThoughtProps {
  thought: string;
}

export function ActiveThought({ thought }: ActiveThoughtProps) {
  return (
    <GlassPanel variant="dark" className="p-4">
      <div className="flex items-center justify-between mb-2">
        <span className="text-xs font-semibold text-stone-400 uppercase tracking-wider">
          Active Thought
        </span>
        <div className="flex gap-1">
          <div className="w-1.5 h-1.5 rounded-full bg-amber-400 animate-pulse" />
        </div>
      </div>
      <AnimatePresence mode="wait">
        <motion.p
          key={thought}
          initial={{ opacity: 0, y: 5 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -5 }}
          className="text-white/90 text-sm font-light leading-relaxed"
        >
          {thought}
        </motion.p>
      </AnimatePresence>
    </GlassPanel>
  );
}
