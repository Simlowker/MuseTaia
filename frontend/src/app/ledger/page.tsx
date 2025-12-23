'use client';

import React, { useState, useEffect } from 'react';
import { useMood } from '@/context/MoodContext';
import { smosApi, WalletState } from '@/services/api';
import { motion } from 'framer-motion';

export default function LedgerPage() {
  const { accentColor } = useMood();
  const [masterMode, setMasterMode] = useState<'direct' | 'decisory'>('direct');
  const [wallet, setWallet] = useState<WalletState | null>(null);
  const [transactions, setTransactions] = useState<any[]>([]);

  const fetchData = async () => {
    try {
      const w = await smosApi.getWallet();
      setWallet(w);
      const history = await smosApi.getLedger(w.address);
      setTransactions(history.reverse()); // Newest first
    } catch (error) {
      console.error('Failed to fetch financial data:', error);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 10000); // Poll ledger every 10s
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="row g-4">
      <div className="col-12">
        <h1 className="fw-bold accent-text mb-2">LEDGER & MASTER CONTROL</h1>
        <p className="text-secondary small mb-4">FINANCIAL SOVEREIGNTY & GOVERNANCE</p>
      </div>

      {/* Sovereign Ledger */}
      <div className="col-lg-8">
        <div className="glass-card mb-4 h-100">
          <h4 className="fw-bold mb-4">SOVEREIGN LEDGER</h4>
          
          <div className="row g-4 mb-4 text-center">
            <div className="col-md-4">
              <div className="p-3 border border-secondary rounded">
                <div className="x-small text-secondary fw-bold mb-1">INTERNAL BALANCE</div>
                <div className="h4 m-0 fw-bold">${wallet?.internal_usd_balance.toFixed(2) || "0.00"} <span className="small text-secondary">USD</span></div>
              </div>
            </div>
            <div className="col-md-4">
              <div className="p-3 border border-secondary rounded">
                <div className="x-small text-secondary fw-bold mb-1">PRIMARY BALANCE</div>
                <div className="h4 m-0 fw-bold text-success">{wallet?.balance.toFixed(4) || "0.00"} <span className="small text-secondary">{wallet?.currency}</span></div>
              </div>
            </div>
            <div className="col-md-4">
              <div className="p-3 border border-secondary rounded">
                <div className="x-small text-secondary fw-bold mb-1">SYNC STATUS</div>
                <div className="h4 m-0 fw-bold text-info">LIVE</div>
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
                {transactions.length > 0 ? (
                  transactions.map((tx, idx) => (
                    <tr key={idx}>
                      <td>{new Date(tx.timestamp).toLocaleString()}</td>
                      <td>{tx.description}</td>
                      <td><span className="text-info">{tx.category.toUpperCase()}</span></td>
                      <td className={tx.type === 'expense' ? 'text-danger' : 'text-success'}>
                        {tx.type === 'expense' ? '-' : '+'}${tx.amount.toFixed(3)}
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan={4} className="text-center text-secondary py-4 italic">No recent transactions recorded.</td>
                  </tr>
                )}
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
