"use client";

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Proposal } from '../../types/smos';
import { SMOSApi } from '../../services/api';
import { useSSE } from '../../hooks/use-sse';
import { AlertCircle, Check, X, DollarSign, Target } from 'lucide-react';

export function HITLApprovalModal() {
    const [proposals, setProposals] = useState<Proposal[]>([]);
    const { subscribe } = useSSE('http://localhost:8000/events/stream');

    useEffect(() => {
        // Initial fetch
        SMOSApi.getProposals().then(setProposals).catch(console.error);

        // Listen for new proposals
        const unsub = subscribe('NEW_PROPOSAL', (payload: Proposal) => {
            setProposals(prev => [...prev, payload]);
        });

        return unsub;
    }, [subscribe]);

    const handleApprove = async (id: string) => {
        try {
            await SMOSApi.approveProposal(id);
            setProposals(prev => prev.filter(p => p.id !== id));
        } catch (e) {
            console.error('Approval failed', e);
        }
    };

    const handleReject = async (id: string) => {
        try {
            await SMOSApi.rejectProposal(id);
            setProposals(prev => prev.filter(p => p.id !== id));
        } catch (e) {
            console.error('Rejection failed', e);
        }
    };

    if (!Array.isArray(proposals) || proposals.length === 0) return null;

    const current = proposals[0];
    if (!current) return null;

    return (
        <AnimatePresence>
            <div className="fixed inset-0 z-[100] flex items-center justify-center bg-void/80 backdrop-blur-xl">
                <motion.div
                    initial={{ opacity: 0, scale: 0.9, y: 20 }}
                    animate={{ opacity: 1, scale: 1, y: 0 }}
                    exit={{ opacity: 0, scale: 0.9, y: 20 }}
                    className="w-full max-w-md bg-onyx border border-gold/30 rounded-2xl p-6 shadow-[0_0_50px_rgba(212,175,55,0.15)]"
                >
                    <div className="flex items-center gap-3 mb-6">
                        <div className="w-10 h-10 rounded-full bg-gold/10 flex items-center justify-center text-gold">
                            <AlertCircle size={24} />
                        </div>
                        <div>
                            <h2 className="text-lg font-bold text-white uppercase tracking-tighter">Human-In-The-Loop</h2>
                            <p className="text-[10px] text-gold font-bold uppercase tracking-widest">Awaiting Sovereignty Approval</p>
                        </div>
                    </div>

                    <div className="space-y-4 mb-8">
                        <div className="p-4 bg-glass-bg border border-glass-border rounded-xl">
                            <p className="text-sm text-white/80 italic">"{current.description}"</p>
                        </div>

                        <div className="grid grid-cols-2 gap-4">
                            <div className="bg-glass-bg p-3 rounded-xl border border-glass-border">
                                <div className="flex items-center gap-2 text-[10px] text-white/40 uppercase mb-1">
                                    <DollarSign size={12} /> Est. Cost
                                </div>
                                <div className="text-lg font-bold text-emerald">${current.cost_estimate.toFixed(2)}</div>
                            </div>
                            <div className="bg-glass-bg p-3 rounded-xl border border-glass-border">
                                <div className="flex items-center gap-2 text-[10px] text-white/40 uppercase mb-1">
                                    <Target size={12} /> Confidence
                                </div>
                                <div className="text-lg font-bold text-cyan">{(current.confidence * 100).toFixed(0)}%</div>
                            </div>
                        </div>
                    </div>

                    <div className="flex gap-4">
                        <button 
                            onClick={() => handleReject(current.id)}
                            className="flex-1 py-3 rounded-xl border border-ruby/30 text-ruby hover:bg-ruby/10 transition-colors font-bold uppercase tracking-widest text-xs flex items-center justify-center gap-2"
                        >
                            <X size={16} /> Discard
                        </button>
                        <button 
                            onClick={() => handleApprove(current.id)}
                            className="flex-1 py-3 rounded-xl bg-gold text-void hover:bg-gold/90 transition-colors font-bold uppercase tracking-widest text-xs flex items-center justify-center gap-2"
                        >
                            <Check size={16} /> Authorize
                        </button>
                    </div>
                </motion.div>
            </div>
        </AnimatePresence>
    );
}
