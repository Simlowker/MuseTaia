'use client';

import React, { useState } from 'react';
import { motion } from 'framer-motion';

export default function DriftVisualizer() {
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
          [ SIGNATURE ASSET: GENESIS_V1_FACE ]
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
          [ NEW RENDER: CANDIDATE_IMAGE_04 ]
        </div>

        {/* Diff Markers Placeholder */}
        <motion.div 
          animate={{ opacity: [0, 1, 0] }}
          transition={{ duration: 2, repeat: Infinity }}
          className="position-absolute border border-danger rounded-circle"
          style={{ width: '40px', height: '40px', top: '40%', left: '45%', borderWidth: '2px' }}
        />
      </div>

      <div className="px-2">
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

      <div className="mt-4 p-3 bg-dark rounded border border-danger border-opacity-25">
        <div className="text-danger small fw-bold mb-1">ISSUE DETECTED: IDENTITY DRIFT</div>
        <p className="text-secondary x-small m-0">"Bone structure in candidate image 04 deviates by 4.2% from Genesis Anchor. Reprocessing requested."</p>
      </div>
    </div>
  );
}
