"use client";

import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Activity, Radio } from 'lucide-react';
import { useNeural } from '@/context/NeuralContext';

const CognitionStream: React.FC = () => {
  const { events } = useNeural();

  return (
    <div className="neural-card p-5 rounded-2xl border border-white/5 bg-white/5 backdrop-blur-xl h-full flex flex-col">
      <div className="flex items-center gap-3 mb-6">
        <div className="p-2 bg-purple-500/10 rounded-lg">
          <Activity className="w-5 h-5 text-purple-400" />
        </div>
        <h3 className="text-sm font-bold tracking-widest text-white/80 uppercase">Cognition Stream</h3>
      </div>

      <div className="flex-1 overflow-y-auto space-y-3 pr-2 scrollbar-hide">
        <AnimatePresence initial={false}>
          {events.length === 0 && (
            <div className="flex flex-col items-center justify-center h-full text-neutral-700 opacity-20">
              <Radio className="w-12 h-12 mb-2" />
              <p className="text-[10px] uppercase font-bold tracking-tighter">Waiting for synapses...</p>
            </div>
          )}
          {events.map((ev, i) => (
            <motion.div
              key={ev.timestamp + i}
              initial={{ opacity: 0, y: -10, x: -10 }}
              animate={{ opacity: 1, y: 0, x: 0 }}
              exit={{ opacity: 0, x: 20 }}
              className="p-3 rounded-xl bg-white/[0.02] border border-white/[0.05] group hover:border-purple-500/30 transition-colors"
            >
              <div className="flex justify-between items-start mb-1">
                <span className="text-[8px] font-black text-purple-500 uppercase tracking-widest">{ev.type}</span>
                <span className="text-[8px] text-neutral-600 font-mono">{new Date(ev.timestamp).toLocaleTimeString()}</span>
              </div>
              <p className="text-[11px] text-neutral-300 leading-tight tracking-tight font-medium">
                {ev.message}
              </p>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>
    </div>
  );
};

export default CognitionStream;
