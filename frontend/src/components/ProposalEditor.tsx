'use client';

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface Proposal {
  id: string;
  topic: string;
  script: string;
  confidence: number;
}

interface ProposalEditorProps {
  proposal: Proposal;
  onApprove: (id: string, script: string) => void;
  onReject: (id: string) => void;
  onClose: () => void;
}

export default function ProposalEditor({ proposal, onApprove, onReject, onClose }: ProposalEditorProps) {
  const [editedScript, setEditedScript] = useState(proposal.script);

  return (
    <motion.div 
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.95 }}
      className="glass-card position-fixed top-50 start-50 translate-middle shadow-2xl z-3"
      style={{ width: '600px', maxWidth: '90vw', border: '1px solid rgba(212, 175, 55, 0.2)' }}
    >
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h4 className="fw-light m-0 tracking-widest small">MISSION_CONTROL | EDIT_PROPOSAL</h4>
        <button className="btn btn-link p-0 text-white-50" onClick={onClose}>[ X ]</button>
      </div>

      <div className="mb-4">
        <label className="small text-secondary tracking-widest mb-2" style={{ fontSize: '0.6rem' }}>TARGET_TOPIC</label>
        <div className="p-2 border border-white border-opacity-5 text-white fw-light">{proposal.topic}</div>
      </div>

      <div className="mb-4">
        <label className="small text-secondary tracking-widest mb-2" style={{ fontSize: '0.6rem' }}>SUGGESTED_NARRATIVE</label>
        <textarea 
          className="form-control bg-black text-white-50 border-white border-opacity-10 small fw-light p-3"
          rows={8}
          value={editedScript}
          onChange={(e) => setEditedScript(e.target.value)}
          style={{ fontSize: '0.8rem', lineHeight: '1.6' }}
        />
      </div>

      <div className="d-flex justify-content-between align-items-center mt-5">
        <div className="small font-monospace text-secondary">CONFIDENCE: {proposal.confidence * 100}%</div>
        <div className="d-flex gap-3">
          <button className="btn btn-sm px-4 btn-outline-danger fw-light tracking-widest" onClick={() => onReject(proposal.id)}>REJECT</button>
          <button className="btn btn-sm px-4 fw-light tracking-widest text-white" style={{ backgroundColor: '#D4AF37' }} onClick={() => onApprove(proposal.id, editedScript)}>APPROVE_AND_RENDER</button>
        </div>
      </div>
    </motion.div>
  );
}
