"use client";

import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Activity, Terminal, Crosshair } from 'lucide-react';
import { useNeural } from '@/context/NeuralContext';

const TacticalHud: React.FC = () => {
  const { events } = useNeural();

  return (
    <div className="p-6 h-full flex flex-col relative">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <Terminal className="w-4 h-4 text-cyan-500" />
          <h3 className="text-[10px] font-bold text-cyan-500 uppercase tracking-widest">Neural Telemetry</h3>
        </div>
        <Crosshair className="w-3 h-3 text-cyan-950" />
      </div>

      <div className="flex-1 overflow-y-auto space-y-2 pr-2 scrollbar-hide">
        <AnimatePresence initial={false}>
          {events.length === 0 && (
            <div className="flex flex-col items-center justify-center h-full opacity-10">
              <Activity className="w-8 h-8 mb-2" />
              <span className="text-[8px] uppercase font-black">Link Pending</span>
            </div>
          )}
          {events.map((ev, i) => (
            <motion.div
              key={ev.timestamp + i}
              initial={{ opacity: 0, x: -5 }}
              animate={{ opacity: 1, x: 0 }}
              className="group border-l border-cyan-500/30 pl-3 py-1"
            >
              <div className="flex items-center gap-2 mb-0.5">
                <span className="text-[6px] font-mono text-cyan-900">{new Date(ev.timestamp).toLocaleTimeString()}</span>
                <span className="text-[7px] font-black text-cyan-500 uppercase tracking-tighter bg-cyan-500/10 px-1 rounded-sm">
                  {ev.type}
                </span>
              </div>
              <p className="text-[10px] text-neutral-400 font-medium leading-tight group-hover:text-white transition-colors">
                {ev.message}
              </p>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>

      <div className="mt-4 pt-4 border-t border-white/5">
        <div className="flex justify-between items-center text-[7px] font-black text-cyan-950 uppercase italic">
          <span>A2A_CONTEXT_PIPE</span>
          <span>STABLE</span>
        </div>
      </div>
    </div>
  );
};

export default TacticalHud;
