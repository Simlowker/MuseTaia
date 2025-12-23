'use client';

import React from 'react';
import { useMood } from '@/context/MoodContext';
import { motion } from 'framer-motion';

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
    <div className="glass-card mb-4">
      <h4 className="fw-light mb-4 tracking-widest small">SWARM ORCHESTRATION</h4>
      <div className="d-flex flex-column gap-4">
        {agents.map((agent) => (
          <div key={agent.name} className="small">
            <div className="d-flex justify-content-between mb-2">
              <span className={`tracking-wide ${agent.active ? 'text-white' : 'text-secondary'}`} style={{ fontSize: '0.75rem' }}>{agent.name.toUpperCase()}</span>
              <span className="text-white-50 font-monospace" style={{ fontSize: '0.6rem' }}>{agent.status}</span>
            </div>
            <div className="progress bg-white bg-opacity-5" style={{ height: '1px', borderRadius: 0 }}>
              <motion.div 
                className="progress-bar"
                initial={{ width: 0 }}
                animate={{ width: `${agent.progress}%` }}
                style={{ 
                  backgroundColor: accentColor,
                  opacity: agent.active ? 1 : 0.3
                }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
