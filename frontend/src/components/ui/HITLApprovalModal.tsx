"use client";

import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useSystem } from '../../contexts/system-context';
import { X, Check, AlertTriangle } from 'lucide-react';

export function HITLApprovalModal() {
  const { pendingProposal, approveProposal, rejectProposal } = useSystem();

  if (!pendingProposal) return null;

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 z-[100] flex items-center justify-center bg-black/80 backdrop-blur-sm"
      >
        <motion.div
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          exit={{ scale: 0.9, opacity: 0 }}
          className="w-full max-w-md bg-obsidian border border-glass-border rounded-2xl p-6 shadow-2xl"
        >
          {/* Header */}
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 bg-amber/10 rounded-lg">
              <AlertTriangle className="w-5 h-5 text-amber" />
            </div>
            <div>
              <h2 className="text-sm font-bold text-white uppercase tracking-widest">
                Approval Required
              </h2>
              <p className="text-[10px] text-white/40">{pendingProposal.type}</p>
            </div>
          </div>

          {/* Content */}
          <div className="mb-6">
            <h3 className="text-white font-medium mb-2">{pendingProposal.title}</h3>
            <p className="text-sm text-white/60 leading-relaxed">
              {pendingProposal.description}
            </p>
          </div>

          {/* Actions */}
          <div className="flex gap-3">
            <button
              onClick={() => rejectProposal(pendingProposal.id)}
              className="flex-1 flex items-center justify-center gap-2 px-4 py-3 bg-white/5 hover:bg-white/10 border border-white/10 rounded-xl text-white/70 text-sm font-medium transition-colors"
            >
              <X className="w-4 h-4" />
              Reject
            </button>
            <button
              onClick={() => approveProposal(pendingProposal.id)}
              className="flex-1 flex items-center justify-center gap-2 px-4 py-3 bg-gold hover:bg-gold/90 rounded-xl text-black text-sm font-bold transition-colors"
            >
              <Check className="w-4 h-4" />
              Approve
            </button>
          </div>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
}