"use client";

import React from 'react';
import { motion } from 'framer-motion';
import { Fingerprint, Scan, ShieldAlert } from 'lucide-react';
import { useNeural } from '@/context/NeuralContext';

const IdentityScanner: React.FC = () => {
  const { lastEvent } = useNeural();
  const score = lastEvent?.metadata?.score ? (lastEvent.metadata.score * 100).toFixed(1) : "98.4";

  return (
    <div className="p-6 h-full flex flex-col relative overflow-hidden">
      <div className="scanline-effect absolute inset-0 opacity-30" />
      
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <Scan className="w-4 h-4 text-cyan-500" />
          <h3 className="text-[10px] font-bold text-cyan-500 uppercase tracking-widest">Biometric Link</h3>
        </div>
        <div className="w-2 h-2 rounded-full bg-cyan-500 animate-pulse shadow-[0_0_10px_#00f2ff]" />
      </div>

      {/* Holographic Portrait */}
      <div className="relative flex-1 rounded-2xl border border-cyan-500/20 bg-cyan-500/[0.02] overflow-hidden group">
        <div className="absolute inset-0 flex items-center justify-center">
          <Fingerprint className="w-24 h-24 text-cyan-500/10 group-hover:scale-110 transition-transform duration-1000" />
        </div>
        
        {/* Animated Scan Line */}
        <motion.div 
          animate={{ top: ["0%", "100%", "0%"] }}
          transition={{ duration: 4, repeat: Infinity, ease: "linear" }}
          className="absolute left-0 right-0 h-px bg-cyan-400/50 shadow-[0_0_15px_#00f2ff]"
        />

        <div className="absolute bottom-4 left-4 right-4 flex justify-between items-end">
          <div>
            <span className="text-[7px] text-cyan-700 uppercase font-black">Subject Anchor</span>
            <p className="text-sm font-black text-white italic">MUSE-01</p>
          </div>
          <ShieldAlert className="w-4 h-4 text-cyan-900" />
        </div>
      </div>

      <div className="mt-6 space-y-4">
        <div className="flex justify-between items-end">
          <span className="text-[8px] text-neutral-600 uppercase font-bold">Consistency Index</span>
          <span className="text-xs font-mono font-black text-cyan-400 tracking-tighter">{score}%</span>
        </div>
        
        {/* Realistic Analog Meter */}
        <div className="h-2 bg-black/50 rounded-full p-0.5 border border-white/5 shadow-inner">
          <motion.div 
            initial={{ width: 0 }}
            animate={{ width: `${score}%` }}
            className="h-full bg-gradient-to-r from-cyan-900 via-cyan-500 to-cyan-400 rounded-full shadow-[0_0_10px_rgba(0,242,255,0.4)]"
          />
        </div>
        
        <div className="flex justify-between text-[6px] text-neutral-700 font-bold uppercase">
          <span>Drift Range</span>
          <span>Threshold: 0.75</span>
        </div>
      </div>
    </div>
  );
};

export default IdentityScanner;
