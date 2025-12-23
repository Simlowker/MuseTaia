'use client';

import React, { useState } from 'react';
import { useMood } from '@/context/MoodContext';
import { motion } from 'framer-motion';

export default function LedgerPage() {
  const { accentColor } = useMood();
  const [masterMode, setMasterMode] = useState<'direct' | 'decisory'>('direct');

  return (
    <div className="row g-4">
      <div className="col-12">
        <h1 className="fw-bold accent-text mb-2">LEDGER & MASTER CONTROL</h1>
        <p className="text-secondary small mb-4">FINANCIAL SOVEREIGNTY & GOVERNANCE</p>
      </div>

      {/* Sovereign Ledger */}
      <div className="col-lg-8">
        <div className="glass-card mb-4">
          <h4 className="fw-bold mb-4">SOVEREIGN LEDGER</h4>
          
          <div className="row g-4 mb-4 text-center">
            <div className="col-md-4">
              <div className="p-3 border border-secondary rounded">
                <div className="x-small text-secondary fw-bold mb-1">INTERNAL BALANCE</div>
                <div className="h4 m-0 fw-bold">$42.85 <span className="small text-secondary">USD</span></div>
              </div>
            </div>
            <div className="col-md-4">
              <div className="p-3 border border-secondary rounded">
                <div className="x-small text-secondary fw-bold mb-1">TOTAL ROI</div>
                <div className="h4 m-0 fw-bold text-success">+12.4%</div>
              </div>
            </div>
            <div className="col-md-4">
              <div className="p-3 border border-secondary rounded">
                <div className="x-small text-secondary fw-bold mb-1">OPEX (24H)</div>
                <div className="h4 m-0 fw-bold text-danger">$1.42</div>
              </div>
            </div>
          </div>

          <div className="table-responsive">
            <table className="table table-dark small border-secondary">
              <thead>
                <tr className="text-secondary">
                  <th>TIMESTAMP</th>
                  <th>EVENT</th>
                  <th>CATEGORY</th>
                  <th>AMOUNT</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>2025-12-22 14:20</td>
                  <td>Imagen 3 Generation</td>
                  <td><span className="text-info">API_COST</span></td>
                  <td className="text-danger">-$0.030</td>
                </tr>
                <tr>
                  <td>2025-12-22 13:45</td>
                  <td>Sponsorship: Digital Mesh</td>
                  <td><span className="text-success">INCOME</span></td>
                  <td className="text-success">+$5.000</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* Master Sync Controller */}
      <div className="col-lg-4">
        <div className="glass-card h-100">
          <h4 className="fw-bold mb-4">MASTER SYNC</h4>
          
          <div className="d-flex flex-column gap-3 mb-4">
            <button 
              className={`btn btn-lg p-4 text-start border-secondary ${masterMode === 'direct' ? 'bg-primary bg-opacity-25 border-primary' : 'bg-dark opacity-50'}`}
              onClick={() => setMasterMode('direct')}
            >
              <div className="fw-bold mb-1">DIRECT MODE</div>
              <div className="small text-secondary">Human Priority. Manual command override active.</div>
            </button>

            <button 
              className={`btn btn-lg p-4 text-start border-secondary ${masterMode === 'decisory' ? 'bg-warning bg-opacity-25 border-warning' : 'bg-dark opacity-50'}`}
              onClick={() => setMasterMode('decisory')}
            >
              <div className="fw-bold mb-1">DECISORY MODE</div>
              <div className="small text-secondary">Community Governance. RootAgent follows majority votes.</div>
            </button>
          </div>

          {masterMode === 'decisory' && (
            <motion.div 
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="p-3 border border-warning border-opacity-50 rounded bg-warning bg-opacity-10"
            >
              <div className="small fw-bold text-warning mb-2">LIVE COMMUNITY VOTE</div>
              <div className="progress bg-dark mb-2" style={{ height: '8px' }}>
                <div className="progress-bar bg-warning" style={{ width: '68%' }}></div>
              </div>
              <div className="d-flex justify-content-between x-small text-secondary">
                <span>NEW ASSET (68%)</span>
                <span>RE-GENERATE (32%)</span>
              </div>
            </motion.div>
          )}

          <div className="mt-auto pt-4 text-center">
            <div className="small text-secondary mb-2">SYNC STATUS</div>
            <div className="d-flex align-items-center justify-content-center gap-2">
              <div className="rounded-circle bg-success" style={{ width: '8px', height: '8px' }}></div>
              <span className="small fw-bold">ENCRYPTED TUNNEL ACTIVE</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
