'use client';

import React from 'react';
import { motion } from 'framer-motion';

interface Trend {
  id: string;
  topic: string;
  score: number;
  category: string;
}

const trends: Trend[] = [
  { id: '1', topic: 'Digital Couture #PFW', score: 92, category: 'Fashion' },
  { id: '2', topic: 'Generative Architecture', score: 74, category: 'Tech' },
  { id: '3', topic: 'Holographic Fabrics', score: 88, category: 'Fashion' },
  { id: '4', topic: 'AI Persona Rights', score: 65, category: 'Ethics' },
];

export default function TrendFeed() {
  return (
    <div className="glass-card">
      <h4 className="fw-light mb-4 tracking-widest small d-flex justify-content-between align-items-center">
        NICHE TRENDS
        <span className="text-secondary small font-monospace" style={{ fontSize: '0.6rem' }}>GROUNDING_ACTIVE</span>
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
              <span className="small text-white-50 tracking-wide">{trend.topic}</span>
              <span className={`small font-monospace ${trend.score > 85 ? 'text-white' : 'text-secondary'}`} style={{ fontSize: '0.75rem' }}>{trend.score}.00</span>
            </div>
            <div className="d-flex justify-content-between align-items-center">
              <span className="text-secondary tracking-widest" style={{ fontSize: '0.6rem' }}>{trend.category.toUpperCase()}</span>
              <button className="btn btn-link p-0 text-decoration-none text-white small fw-light" style={{ fontSize: '0.65rem', letterSpacing: '0.1em' }}>[ DISCUSS ]</button>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
