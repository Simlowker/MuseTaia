"use client";

import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Cpu, Zap } from 'lucide-react';
import { useNeural } from '@/context/NeuralContext';

const GKEForge: React.FC = () => {
  const { lastEvent } = useNeural();
  const isBurst = lastEvent?.type.includes("BURST");

  return (
    <div className="neural-card p-6 rounded-2xl border border-white/5 bg-white/5 backdrop-blur-xl h-full">
      <div className="flex justify-between items-center mb-8">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-blue-500/10 rounded-lg">
            <Cpu className="w-5 h-5 text-blue-400" />
          </div>
          <h3 className="text-sm font-bold tracking-widest text-white/80 uppercase">GKE Forge</h3>
        </div>
        {isBurst && (
          <motion.div 
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            className="flex items-center gap-1 bg-amber-500/20 text-amber-400 text-[10px] px-2 py-1 rounded-full font-bold uppercase tracking-tighter"
          >
            <Zap className="w-3 h-3 fill-current" /> Burst Mode
          </motion.div>
        )}
      </div>

      <div className="grid grid-cols-4 gap-4">
        {[...Array(12)].map((_, i) => (
          <PodUnit key={i} index={i} isActive={isBurst ? i < 10 : i < 3} isSelected={i === 0} />
        ))}
      </div>

      <div className="mt-8 flex justify-between items-center text-[10px] text-neutral-500 uppercase tracking-widest font-bold">
        <span>Latency: 2.4s (Snapshot)</span>
        <span>Throughput: High</span>
      </div>
    </div>
  );
};

const PodUnit = ({ index, isActive, isSelected }: { index: number, isActive: boolean, isSelected: boolean }) => (
  <div className="relative group">
    <motion.div 
      animate={{ 
        backgroundColor: isActive ? (isSelected ? "rgba(34, 197, 94, 0.2)" : "rgba(59, 130, 246, 0.1)") : "rgba(255, 255, 255, 0.02)",
        borderColor: isActive ? (isSelected ? "rgba(34, 197, 94, 0.4)" : "rgba(59, 130, 246, 0.3)") : "rgba(255, 255, 255, 0.05)"
      }}
      className={`aspect-square rounded-lg border flex items-center justify-center transition-all duration-500`}
    >
      <div className={`w-1 h-1 rounded-full ${isActive ? (isSelected ? "bg-green-400 animate-ping" : "bg-blue-400") : "bg-neutral-800"}`} />
    </motion.div>
    {isActive && (
      <motion.div 
        layoutId="glow"
        className="absolute inset-0 bg-blue-500/5 blur-md -z-10"
      />
    )}
  </div>
);

export default GKEForge;
