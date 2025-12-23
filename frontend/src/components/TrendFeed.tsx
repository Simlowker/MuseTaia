'use client';

import React from 'react';
import { motion } from 'framer-motion';

interface Trend {
  id: string;
  topic: string;
  score: number;
  category: string;
  isProposal?: boolean;
}

interface TrendFeedProps {
  onExecute?: (topic: string) => void;
  onDiscuss?: (topic: string) => void;
}

const trends: Trend[] = [
  { id: '1', topic: 'Digital Couture #PFW', score: 92, category: 'Fashion', isProposal: true },
  { id: '2', topic: 'Generative Architecture', score: 74, category: 'Tech' },
  { id: '3', topic: 'Holographic Fabrics', score: 88, category: 'Fashion', isProposal: true },
  { id: '4', topic: 'AI Persona Rights', score: 65, category: 'Ethics' },
];

export default function TrendFeed({ onExecute, onDiscuss }: TrendFeedProps) {
  return (
    <div className="glass-card">
      <h4 className="fw-light mb-4 tracking-widest small d-flex justify-content-between align-items-center">
        SUGGESTED_COMMANDS
        <span className="text-secondary small font-monospace" style={{ fontSize: '0.6rem' }}>PROACTIVE_QUEUE</span>
      </h4>
      <div className="d-flex flex-column gap-4">
        {trends.map((trend, index) => (
          <motion.div 
            key={trend.id}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1, ease: "easeOut" }}
            className="pb-3 border-bottom border-white border-opacity-5"
          >
            <div className="d-flex justify-content-between align-items-start mb-2">
              <span className={`small tracking-wide ${trend.isProposal ? 'text-info' : 'text-white-50'}`}>
                {trend.isProposal ? '> MISSION_PROPOSAL' : 'TREND_SIGNAL'}
              </span>
              <span className={`small font-monospace ${trend.score > 85 ? 'text-white' : 'text-secondary'}`} style={{ fontSize: '0.75rem' }}>{trend.score}.00</span>
            </div>
            
            <div className="text-white-50 small mb-3">{trend.topic}</div>

            <div className="d-flex justify-content-between align-items-center">
              <span className="text-secondary tracking-widest" style={{ fontSize: '0.6rem' }}>{trend.category.toUpperCase()}</span>
              <div className="d-flex gap-3">
                {trend.isProposal ? (
                  <button 
                    className="btn btn-link p-0 text-decoration-none text-white small fw-light" 
                    style={{ fontSize: '0.65rem', letterSpacing: '0.1em' }}
                    onClick={() => onExecute?.(trend.topic)}
                  >[ EXECUTE ]</button>
                ) : (
                  <button 
                    className="btn btn-link p-0 text-decoration-none text-white small fw-light opacity-50" 
                    style={{ fontSize: '0.65rem', letterSpacing: '0.1em' }}
                    onClick={() => onDiscuss?.(trend.topic)}
                  >[ DISCUSS ]</button>
                )}
              </div>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
