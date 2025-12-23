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
      <h4 className="fw-bold mb-3">SWARM STATUS</h4>
      <div className="d-flex flex-column gap-3">
        {agents.map((agent) => (
          <div key={agent.name} className="small">
            <div className="d-flex justify-content-between mb-1">
              <span className={agent.active ? 'text-white fw-bold' : 'text-secondary'}>{agent.name}</span>
              <span className="text-secondary" style={{ fontSize: '0.7rem' }}>{agent.status}</span>
            </div>
            <div className="progress bg-dark" style={{ height: '4px' }}>
              <motion.div 
                className="progress-bar"
                initial={{ width: 0 }}
                animate={{ width: `${agent.progress}%` }}
                style={{ 
                  backgroundColor: accentColor,
                  boxShadow: agent.active ? `0 0 10px ${accentColor}` : 'none'
                }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
