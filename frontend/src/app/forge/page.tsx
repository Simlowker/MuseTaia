'use client';

import React, { useState } from 'react';
import DriftVisualizer from '@/components/DriftVisualizer';
import { useMood } from '@/context/MoodContext';

export default function ForgePage() {
  const { accentColor } = useMood();
  const [activeReport] = useState({
    score: 0.94,
    issues: ["Minor lighting mismatch on left cheek"],
    recommendations: "Increase soft light intensity in next prompt."
  });

  return (
    <div className="row g-4">
      <div className="col-12">
        <h1 className="fw-light accent-text mb-2 tracking-widest small">THE FORGE | PRODUCTION HUB</h1>
        <p className="text-secondary small mb-5 opacity-50 tracking-wide">MASSIVE QUALITATIVE PRODUCTION & CURATION</p>
      </div>

      {/* Production Timeline */}
      <div className="col-lg-8">
        <div className="glass-card mb-4 h-100 border-opacity-10">
          <h4 className="fw-light mb-4 tracking-widest small">PRODUCTION_QUEUE</h4>
          <div className="table-responsive">
            <table className="table table-dark align-middle border-white border-opacity-5">
              <thead>
                <tr className="text-secondary tracking-widest" style={{ fontSize: '0.65rem' }}>
                  <th>CAMPAIGN_ID</th>
                  <th>STATUS_TOKEN</th>
                  <th>PROGRESS</th>
                  <th>EST_RELEASE</th>
                </tr>
              </thead>
              <tbody>
                <tr className="border-white border-opacity-5">
                  <td className="py-4">
                    <span className="text-white fw-light tracking-wide small">CYBERPUNK_AWAKENING</span><br/>
                    <span className="font-monospace text-secondary" style={{ fontSize: '0.6rem' }}>UUID: 8F2A-4B9C</span>
                  </td>
                  <td>
                    <span className="badge rounded-0 bg-white bg-opacity-5 text-white-50 border border-white border-opacity-10 small fw-light tracking-widest">RENDERING</span>
                  </td>
                  <td style={{ width: '200px' }}>
                    <div className="progress bg-white bg-opacity-5" style={{ height: '1px' }}>
                      <div 
                        className="progress-bar" 
                        style={{ width: '75%', backgroundColor: accentColor }}
                      />
                    </div>
                  </td>
                  <td className="small text-secondary font-monospace" style={{ fontSize: '0.65rem' }}>2025.12.23_14:00</td>
                </tr>
                <tr className="border-white border-opacity-5">
                  <td className="py-4">
                    <span className="text-white fw-light tracking-wide small">IDENTITY_SYNC_TEST</span><br/>
                    <span className="font-monospace text-secondary" style={{ fontSize: '0.6rem' }}>UUID: 3D1E-9F0A</span>
                  </td>
                  <td>
                    <span className="badge rounded-0 bg-success bg-opacity-10 text-success border border-success border-opacity-20 small fw-light tracking-widest">PASSED</span>
                  </td>
                  <td style={{ width: '200px' }}>
                    <div className="progress bg-white bg-opacity-5" style={{ height: '1px' }}>
                      <div 
                        className="progress-bar" 
                        style={{ width: '100%', backgroundColor: accentColor, opacity: 0.5 }}
                      />
                    </div>
                  </td>
                  <td className="small text-secondary font-monospace" style={{ fontSize: '0.65rem' }}>2025.12.23_12:30</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* The Critic Dashboard Side */}
      <div className="col-lg-4">
        <DriftVisualizer 
          score={activeReport.score}
          issues={activeReport.issues}
          recommendations={activeReport.recommendations}
        />
      </div>
    </div>
  );
}