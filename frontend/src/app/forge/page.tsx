'use client';

import React, { useState, useEffect } from 'react';
import DriftVisualizer from '@/components/DriftVisualizer';
import { useMood } from '@/context/MoodContext';

export default function ForgePage() {
  const { accentColor } = useMood();
  const [activeReport, setActiveReport] = useState({
    score: 0.94,
    issues: ["Minor lighting mismatch on left cheek"],
    recommendations: "Increase soft light intensity in next prompt."
  });

  return (
    <div className="row g-4">
      <div className="col-12">
        <h1 className="fw-bold accent-text mb-2">THE FORGE</h1>
        <p className="text-secondary small mb-4">MASSIVE QUALITATIVE PRODUCTION & CURATION</p>
      </div>

      {/* Production Timeline */}
      <div className="col-lg-8">
        <div className="glass-card mb-4 h-100">
          <h4 className="fw-bold mb-4">PRODUCTION QUEUE</h4>
          <div className="table-responsive">
            <table className="table table-dark table-hover align-middle border-secondary">
              <thead>
                <tr className="text-secondary small">
                  <th>CAMPAIGN</th>
                  <th>STATUS</th>
                  <th>PROGRESS</th>
                  <th>EST. RELEASE</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>
                    <span className="text-white fw-bold">Cyberpunk Awakening</span><br/>
                    <span className="x-small text-secondary">#campaign_01</span>
                  </td>
                  <td>
                    <span className="badge bg-dark border border-secondary text-info">RENDERING</span>
                  </td>
                  <td style={{ width: '200px' }}>
                    <div className="progress bg-dark" style={{ height: '4px' }}>
                      <div 
                        className="progress-bar progress-bar-striped progress-bar-animated" 
                        style={{ width: '75%', backgroundColor: accentColor }}
                      />
                    </div>
                  </td>
                  <td className="small text-secondary">TODAY</td>
                </tr>
                <tr>
                  <td>
                    <span className="text-white fw-bold">Identity Sync Test</span><br/>
                    <span className="x-small text-secondary">#regression_v12</span>
                  </td>
                  <td>
                    <span className="badge bg-dark border border-success text-success">PASSED</span>
                  </td>
                  <td style={{ width: '200px' }}>
                    <div className="progress bg-dark" style={{ height: '4px' }}>
                      <div 
                        className="progress-bar" 
                        style={{ width: '100%', backgroundColor: accentColor }}
                      />
                    </div>
                  </td>
                  <td className="small text-secondary">2025-12-23</td>
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
