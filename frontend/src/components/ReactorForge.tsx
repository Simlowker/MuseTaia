"use client";

import React from 'react';
import { motion } from 'framer-motion';
import { Cpu, Wind } from 'lucide-react';
import { useNeural } from '@/context/NeuralContext';

const ReactorForge: React.FC = () => {
  const { lastEvent } = useNeural();
  const isBurst = lastEvent?.type.includes("BURST");

  return (
    <div className="p-6 h-full flex flex-col relative">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <Cpu className="w-4 h-4 text-neutral-500" />
          <h3 className="text-[10px] font-bold text-neutral-500 uppercase tracking-widest">GKE Reactor Grid</h3>
        </div>
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-1">
            <div className="w-1 h-1 rounded-full bg-blue-500" />
            <span className="text-[7px] text-neutral-600 font-bold uppercase">Ready</span>
          </div>
          <div className="flex items-center gap-1">
            <div className="w-1 h-1 rounded-full bg-cyan-400 animate-pulse" />
            <span className="text-[7px] text-neutral-600 font-bold uppercase">Active</span>
          </div>
        </div>
      </div>

      {/* Physical Reactor Slots */}
      <div className="flex-1 grid grid-cols-8 gap-3 items-center">
        {[...Array(16)].map((_, i) => (
          <ReactorCore key={i} isActive={isBurst ? i < 12 : i < 4} />
        ))}
      </div>

      <div className="mt-4 flex items-center justify-between text-[7px] font-bold text-neutral-700 uppercase tracking-tighter">
        <div className="flex items-center gap-2">
          <Wind className="w-3 h-3" />
          <span>Thermal Load: Optimized</span>
        </div>
        <span>CRIU Snapshots: Primed (2.4s)</span>
      </div>
    </div>
  );
};

const ReactorCore = ({ isActive }: { isActive: boolean }) => (
  <div className={`
    relative aspect-square rounded-lg border flex items-center justify-center
    ${isActive ? 'border-cyan-500/30 bg-cyan-500/10 shadow-[0_0_15px_rgba(0,242,255,0.1)]' : 'border-white/5 bg-black/40'}
    transition-all duration-700
  `}>
    <div className={`
      w-1.5 h-1.5 rounded-sm rotate-45
      ${isActive ? 'bg-cyan-400 shadow-[0_0_10px_#00f2ff]' : 'bg-neutral-900'}
    `} />
    {isActive && (
      <motion.div 
        animate={{ opacity: [0.3, 0.6, 0.3] }}
        transition={{ duration: 2, repeat: Infinity }}
        className="absolute inset-0 bg-cyan-500/5 rounded-lg"
      />
    )}
  </div>
);

export default ReactorForge;
