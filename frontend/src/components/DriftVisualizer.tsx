'use client';

import React, { useState } from 'react';
import { motion } from 'framer-motion';

interface DriftVisualizerProps {
  score?: number;
  issues?: string[];
  recommendations?: string;
}

export default function DriftVisualizer({ score = 0.95, issues = [], recommendations }: DriftVisualizerProps) {
  const [opacity, setOpacity] = useState(0.5);

  return (
    <div className="glass-card h-100">
      <h4 className="fw-bold mb-4">THE CRITIC: DRIFT VISUALIZER</h4>
      
      <div className="bg-black rounded-3 overflow-hidden position-relative ratio ratio-1x1 mb-4 border border-secondary shadow-lg">
        {/* Layer 1: Signature Asset (Background) */}
        <div 
          className="position-absolute w-100 h-100 d-flex align-items-center justify-content-center text-secondary small"
          style={{ opacity: 1 - opacity }}
        >
          [ SIGNATURE ASSET ]
        </div>
        
        {/* Layer 2: New Render (Foreground with dynamic opacity) */}
        <div 
          className="position-absolute w-100 h-100 d-flex align-items-center justify-content-center text-info small"
          style={{ 
            opacity: opacity,
            background: 'rgba(0, 212, 255, 0.1)',
            backdropFilter: 'blur(2px)'
          }}
        >
          [ NEW RENDER ]
        </div>

        {/* Diff Markers Placeholder - only shown if score is low */}
        {score < 0.9 && (
          <motion.div 
            animate={{ opacity: [0, 1, 0] }}
            transition={{ duration: 2, repeat: Infinity }}
            className="position-absolute border border-danger rounded-circle"
            style={{ width: '40px', height: '40px', top: '40%', left: '45%', borderWidth: '2px' }}
          />
        )}
      </div>

      <div className="px-2 mb-4">
        <label className="form-label small text-secondary d-flex justify-content-between">
          <span>SIGNATURE</span>
          <span>COMPARE DRIFT</span>
          <span>NEW RENDER</span>
        </label>
        <input 
          type="range" 
          className="form-range custom-range" 
          min="0" 
          max="1" 
          step="0.01" 
          value={opacity}
          onChange={(e) => setOpacity(parseFloat(e.target.value))}
        />
      </div>

      <div className={`p-3 rounded border ${score < 0.9 ? 'border-danger bg-danger' : 'border-success bg-success'} bg-opacity-10`}>
        <div className={`small fw-bold mb-1 ${score < 0.9 ? 'text-danger' : 'text-success'}`}>
          {score < 0.9 ? 'IDENTITY DRIFT DETECTED' : 'VISUAL CONSISTENCY PASSED'}
        </div>
        <div className="h5 fw-bold mb-2">SCORE: {(score * 100).toFixed(1)}%</div>
        {issues.length > 0 && (
          <p className="text-secondary x-small m-0">"{issues[0]}"</p>
        )}
        {recommendations && (
          <p className="text-white x-small mt-2 m-0 italic">{recommendations}</p>
        )}
      </div>
    </div>
  );
}
