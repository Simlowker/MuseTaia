'use client';

import React from 'react';
import { motion } from 'framer-motion';

export default function VisualVortex() {
  return (
    <motion.div 
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 1.5, ease: "easeOut" }}
      className="bg-black rounded-1 overflow-hidden shadow-lg position-relative h-100"
      style={{ minHeight: '400px', border: '0.5px solid rgba(255,255,255,0.05)' }}
    >
      <div className="ratio ratio-16x9 h-100 d-flex align-items-center justify-content-center" style={{ backgroundColor: '#050505' }}>
        {/* Placeholder for Veo 3.1 4K Studio Render */}
        <div className="text-center">
          <p className="text-secondary small tracking-widest opacity-50" style={{ letterSpacing: '0.3em' }}>VEO 3.1 | REALITY SYNTHESIS</p>
          <div className="mt-2 text-white-50 small font-monospace" style={{ fontSize: '0.65rem' }}>RESOLVING IDENTITY_V1_REMBRANDT...</div>
        </div>
      </div>
      
      {/* Precision silk-thread overlays */}
      <div className="position-absolute top-0 end-0 p-3">
        <div className="text-end">
          <div className="text-white-50 small font-monospace" style={{ fontSize: '0.6rem' }}>DATA_STREAM: 4K_RAW</div>
          <div className="text-white-50 small font-monospace" style={{ fontSize: '0.6rem' }}>LIGHTING: REMBRANDT_ACTIVE</div>
        </div>
      </div>

      <div className="position-absolute bottom-0 start-0 p-4 w-100" style={{ background: 'linear-gradient(to top, rgba(0,0,0,0.9), transparent)' }}>
        <div className="d-flex justify-content-between align-items-end">
          <div>
            <h5 className="text-white m-0 small fw-light tracking-widest">IDENTITY ANCHOR: GENESIS</h5>
            <div className="text-secondary x-small mt-1">SOVEREIGN PERSISTENCE ENGINE ACTIVE</div>
          </div>
          <div className="text-end">
            <span className="badge rounded-pill px-3 py-1 bg-white bg-opacity-5 text-white border border-white border-opacity-10 small fw-light">LIVE_SYNC</span>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
