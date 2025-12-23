"use client";

import React from 'react';
import { motion } from 'framer-motion';
import { Fingerprint } from 'lucide-react';
import { useNeural } from '@/context/NeuralContext';
import { GenesisRing } from './hud/GenesisRing';

const IdentityCard: React.FC = () => {
  const { lastEvent } = useNeural();

  // Extract score from last event if available
  const score = lastEvent?.metadata?.score ? parseFloat((lastEvent.metadata.score * 100).toFixed(1)) : 98.4;

  return (
    <div className="luxe-glass-card p-6 h-full flex flex-col items-center justify-center relative overflow-hidden">
      {/* Background Decor */}
      <div className="absolute top-0 right-0 p-4 opacity-50">
        <Fingerprint className="w-6 h-6 text-white/20" />
      </div>

      <div className="mb-8">
        <GenesisRing score={score} size={180} />
      </div>

      {/* Footer Info */}
      <div className="w-full mt-8 border-t border-[var(--glass-border)] pt-4 flex justify-between items-center text-[10px] uppercase tracking-widest text-white/40 font-bold">
        <span>Genesis Anchor</span>
        <span>ID: MUSE-01</span>
      </div>
    </div>
  );
};


export default IdentityCard;
