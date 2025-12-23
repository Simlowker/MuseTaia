'use client';

import React from 'react';
import DriftVisualizer from '@/components/DriftVisualizer';
import { useMood } from '@/context/MoodContext';

const campaigns = [
  { id: '1', title: 'Cyberpunk Awakening', status: 'In Production', progress: 75, date: '2025-12-23' },
  { id: '2', title: 'Digital Couture Vlog', status: 'Verification', progress: 95, date: '2025-12-24' },
  { id: '3', title: 'Metaverse Gallery Opening', status: 'Scheduled', progress: 0, date: '2025-12-26' },
];

export default function ForgePage() {
  const { accentColor } = useMood();

  return (
    <div className="row g-4">
      <div className="col-12">
        <h1 className="fw-bold accent-text mb-2">THE FORGE</h1>
        <p className="text-secondary small mb-4">MASSIVE QUALITATIVE PRODUCTION & CURATION</p>
      </div>

      {/* Production Timeline */}
      <div className="col-lg-8">
        <div className="glass-card mb-4 h-100">
          <h4 className="fw-bold mb-4">PRODUCTION TIMELINE</h4>
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
                {campaigns.map((c) => (
                  <tr key={c.id}>
                    <td>
                      <span className="text-white fw-bold">{c.title}</span><br/>
                      <span className="x-small text-secondary">#campaign_{c.id}</span>
                    </td>
                    <td>
                      <span className="badge bg-dark border border-secondary">{c.status}</span>
                    </td>
                    <td style={{ width: '200px' }}>
                      <div className="progress bg-dark" style={{ height: '4px' }}>
                        <div 
                          className="progress-bar" 
                          style={{ width: `${c.progress}%`, backgroundColor: accentColor }}
                        />
                      </div>
                    </td>
                    <td className="small text-secondary">{c.date}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* The Critic Dashboard Side */}
      <div className="col-lg-4">
        <DriftVisualizer />
      </div>
    </div>
  );
}
