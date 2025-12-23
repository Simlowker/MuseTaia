'use client';

import React from 'react';
import { motion } from 'framer-motion';

export default function VisualVortex() {
  return (
    <motion.div 
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 1 }}
      className="bg-black rounded-3 overflow-hidden shadow-lg position-relative"
      style={{ minHeight: '400px', border: '1px solid rgba(255,255,255,0.1)' }}
    >
      <div className="ratio ratio-16x9 h-100 d-flex align-items-center justify-content-center">
        {/* Placeholder for Veo 3.1 4K Stream */}
        <div className="text-center">
          <div className="spinner-grow text-secondary mb-3" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <p className="text-secondary small fw-bold tracking-widest">STREAMING REALITY (VEO 3.1)</p>
        </div>
      </div>
      
      {/* Overlay identity stats */}
      <div className="position-absolute bottom-0 start-0 p-3 w-100 d-flex justify-content-between align-items-end" style={{ background: 'linear-gradient(to top, rgba(0,0,0,0.8), transparent)' }}>
        <div>
          <div className="badge bg-danger mb-1 pulse">LIVE</div>
          <h5 className="text-white m-0 small fw-bold">IDENTITY ANCHOR: GENESIS_V1</h5>
        </div>
        <div className="text-end text-secondary small">
          RESOLUTION: 4K<br/>
          BITRATE: 45 MBPS
        </div>
      </div>
    </motion.div>
  );
}
