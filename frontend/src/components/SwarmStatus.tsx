'use client';

import React from 'react';
import { useMood } from '@/context/MoodContext';
import { motion } from 'framer-motion';
import { NeuralSwarm } from './viz/NeuralSwarm';

interface AgentStatus {
  name: string;
  status: string;
  progress: number;
  active: boolean;
}

const agents: AgentStatus[] = [
  { name: 'Narrative Lead', status: 'Ready', progress: 100, active: false },
  { name: 'Visual Virtuoso', status: 'Rendering...', progress: 65, active: true },
  { name: 'Motion Engineer', status: 'Waiting', progress: 0, active: false },
  { name: 'The Critic', status: 'Idle', progress: 0, active: false },
];

export default function SwarmStatus() {
  const { accentColor } = useMood();

  return (
    <div className="luxe-glass-card mb-4 min-h-[300px] flex flex-col">
      <div className="flex justify-between items-center p-4 border-b border-[var(--glass-border)]">
        <h4 className="text-sm font-medium tracking-widest text-gold uppercase">Swarm Orchestration</h4>
        <span className="text-[10px] text-white/50 bg-white/5 px-2 py-1 rounded">Active</span>
      </div>

      <div className="p-4 flex-1 relative">
        <NeuralSwarm agents={agents} />

        {/* Minimal Status Footer */}
        <div className="mt-4 grid grid-cols-2 gap-2">
          {agents.map(a => (
            <div key={a.name} className="flex justify-between text-[10px] text-white/40">
              <span>{a.name}</span>
              <span className={a.active ? 'text-gold' : ''}>{a.status}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
