'use client';

import React, { useState, useEffect } from 'react';
import { useMood } from '@/context/MoodContext';
import { smosApi, WalletState } from '@/services/api';
import { motion, AnimatePresence } from 'framer-motion';

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
        <h1 className="fw-light accent-text mb-2 tracking-widest small">LEDGER & MASTER CONTROL</h1>
        <p className="text-secondary small mb-5 opacity-50 tracking-wide">FINANCIAL SOVEREIGNTY & GOVERNANCE</p>
      </div>

      {/* Sovereign Ledger */}
      <div className="col-lg-8">
        <div className="glass-card mb-4 h-100 border-opacity-10">
          <h4 className="fw-light mb-5 tracking-widest small">SOVEREIGN_LEDGER</h4>
          
          <div className="row g-4 mb-5 text-center">
            <div className="col-md-4">
              <div className="p-4 bg-white bg-opacity-5 rounded-1 border border-white border-opacity-5">
                <div className="x-small text-secondary fw-light tracking-widest mb-2" style={{ fontSize: '0.6rem' }}>INTERNAL_USD_BALANCE</div>
                <div className="h4 m-0 fw-light text-white">${wallet?.internal_usd_balance.toFixed(2) || "0.00"}</div>
              </div>
            </div>
            <div className="col-md-4">
              <div className="p-4 bg-white bg-opacity-5 rounded-1 border border-white border-opacity-5">
                <div className="x-small text-secondary fw-light tracking-widest mb-2" style={{ fontSize: '0.6rem' }}>PRIMARY_LEDGER</div>
                <div className="h4 m-0 fw-light text-white">{wallet?.balance.toFixed(4) || "0.00"} <span className="small opacity-50">{wallet?.currency}</span></div>
              </div>
            </div>
            <div className="col-md-4">
              <div className="p-4 bg-white bg-opacity-5 rounded-1 border border-white border-opacity-5">
                <div className="x-small text-secondary fw-light tracking-widest mb-2" style={{ fontSize: '0.6rem' }}>SYNC_STATUS</div>
                <div className="h4 m-0 fw-light" style={{ color: accentColor }}>LIVE_ACTIVE</div>
              </div>
            </div>
          </div>

          <div className="table-responsive">
            <table className="table table-dark small border-white border-opacity-5">
              <thead>
                <tr className="text-secondary tracking-widest" style={{ fontSize: '0.65rem' }}>
                  <th>TIMESTAMP_UTC</th>
                  <th>EVENT_ID</th>
                  <th>CATEGORY</th>
                  <th>AMOUNT_USD</th>
                </tr>
              </thead>
              <tbody>
                {transactions.length > 0 ? (
                  transactions.map((tx, idx) => (
                    <tr key={idx} className="border-white border-opacity-5">
                      <td className="py-3 font-monospace" style={{ fontSize: '0.7rem' }}>{new Date(tx.timestamp).toISOString().replace('T', ' ').slice(0, 19)}</td>
                      <td className="py-3 text-white-50">{tx.description}</td>
                      <td className="py-3"><span className="text-secondary font-monospace" style={{ fontSize: '0.65rem' }}>{tx.category.toUpperCase()}</span></td>
                      <td className={`py-3 fw-light ${tx.type === 'expense' ? 'text-danger' : 'text-success'}`}>
                        {tx.type === 'expense' ? '-' : '+'}${tx.amount.toFixed(3)}
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan={4} className="text-center text-secondary py-5 italic opacity-50 fw-light">No recent transactions recorded in the ledger.</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* Master Sync Controller */}
      <div className="col-lg-4">
        <div className="glass-card h-100 border-opacity-10">
          <h4 className="fw-light mb-5 tracking-widest small">MASTER_SYNC_ORCHESTRATOR</h4>
          
          <div className="d-flex flex-column gap-3 mb-5">
            <button 
              className={`btn btn-lg p-4 text-start rounded-1 border transition-all ${masterMode === 'direct' ? 'bg-white bg-opacity-10 border-white border-opacity-20' : 'bg-transparent border-white border-opacity-5 opacity-40'}`}
              onClick={() => setMasterMode('direct')}
              style={{ borderLeft: masterMode === 'direct' ? `3px solid ${accentColor}` : '1px solid rgba(255,255,255,0.05)' }}
            >
              <div className="fw-light text-white tracking-widest mb-2 small">DIRECT_MODE</div>
              <div className="x-small text-secondary fw-light" style={{ lineHeight: '1.4' }}>Human Priority. Full manual override active. Sovereign control via command interface.</div>
            </button>

            <button 
              className={`btn btn-lg p-4 text-start rounded-1 border transition-all ${masterMode === 'decisory' ? 'bg-white bg-opacity-10 border-white border-opacity-20' : 'bg-transparent border-white border-opacity-5 opacity-40'}`}
              onClick={() => setMasterMode('decisory')}
              style={{ borderLeft: masterMode === 'decisory' ? `3px solid ${accentColor}` : '1px solid rgba(255,255,255,0.05)' }}
            >
              <div className="fw-light text-white tracking-widest mb-2 small">DECISORY_MODE</div>
              <div className="x-small text-secondary fw-light" style={{ lineHeight: '1.4' }}>Community Governance. Autonomous decision-making based on collective voting metrics.</div>
            </button>
          </div>

          <AnimatePresence>
            {masterMode === 'decisory' && (
              <motion.div 
                initial={{ opacity: 0, scale: 0.98 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.98 }}
                className="p-4 bg-white bg-opacity-5 rounded-1 border border-white border-opacity-10"
              >
                <div className="small fw-light text-secondary tracking-widest mb-3" style={{ fontSize: '0.65rem' }}>COMMUNITY_VOTE_LIVE</div>
                <div className="progress bg-black" style={{ height: '2px', borderRadius: 0 }}>
                  <div className="progress-bar" style={{ width: '68%', backgroundColor: accentColor }}></div>
                </div>
                <div className="d-flex justify-content-between mt-2 font-monospace" style={{ fontSize: '0.55rem' }}>
                  <span className="text-white-50">PROPOSE_NEW_ASSET (68%)</span>
                  <span className="text-secondary">RE_GENERATE (32%)</span>
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          <div className="mt-auto pt-5 text-center">
            <div className="small fw-light text-secondary tracking-tighter mb-2" style={{ fontSize: '0.6rem' }}>ENCRYPTION_LAYER: AES-256-GCM</div>
            <div className="d-flex align-items-center justify-content-center gap-3">
              <motion.div 
                animate={{ opacity: [0.3, 1, 0.3] }}
                transition={{ duration: 2, repeat: Infinity }}
                className="rounded-circle" 
                style={{ width: '6px', height: '6px', backgroundColor: '#00ff00' }}
              />
              <span className="small fw-light text-white-50 tracking-widest" style={{ fontSize: '0.65rem' }}>SOVEREIGN_LINK_ESTABLISHED</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
