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
      <h4 className="fw-bold mb-3 d-flex justify-content-between align-items-center">
        NICHE TRENDS
        <span className="badge bg-dark border border-secondary small" style={{ fontSize: '0.6rem' }}>LIVE</span>
      </h4>
      <div className="d-flex flex-column gap-3">
        {trends.map((trend, index) => (
          <motion.div 
            key={trend.id}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.1 }}
            className="p-2 border-bottom border-secondary"
          >
            <div className="d-flex justify-content-between align-items-start mb-1">
              <span className="small fw-bold text-white">{trend.topic}</span>
              <span className={`small ${trend.score > 85 ? 'text-success' : 'text-warning'}`}>{trend.score}%</span>
            </div>
            <div className="d-flex justify-content-between align-items-center">
              <span className="text-secondary" style={{ fontSize: '0.7rem' }}>{trend.category.toUpperCase()}</span>
              <button className="btn btn-link p-0 text-decoration-none accent-text small" style={{ fontSize: '0.7rem' }}>DISCUSS</button>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
