'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useMood } from '@/context/MoodContext';
import { smosApi } from '@/services/api';
import VisualVortex from '@/components/VisualVortex';
import NeuralWaveform from '@/components/NeuralWaveform';
import TrendFeed from '@/components/TrendFeed';
import SwarmStatus from '@/components/SwarmStatus';
import ProposalEditor from '@/components/ProposalEditor';

export default function Home() {
  const { mood, setMood, accentColor, rawMood, isSovereign, setIsSovereign } = useMood();
  const [isTriggering, setIsTriggering] = useState(false);
  const [activeProposal, setActiveProposal] = useState<any>(null);

  const handleTriggerProduction = async (intent: string) => {
    setIsTriggering(true);
    try {
      const result = await smosApi.triggerProduction(intent);
      console.log('Production triggered:', result.task_id);
    } catch (error) {
      console.error('Trigger failed:', error);
    } finally {
      setIsTriggering(false);
    }
  };

  const openProposal = (topic: string) => {
    setActiveProposal({
      id: Math.random().toString(36).substr(2, 9),
      topic: topic,
      script: `[VISUAL: ${topic} in high-fidelity studio lighting]\n\nMUSE: Digital sovereignty isn't a goal, it's a foundation. Let's explore ${topic} together.`,
      confidence: 0.94
    });
  };

  return (
    <div className="row g-4">
      {/* Proposal Editor Modal */}
      <AnimatePresence>
        {activeProposal && (
          <>
            <div className="position-fixed top-0 start-0 w-100 h-100 bg-black bg-opacity-80 z-2" onClick={() => setActiveProposal(null)} />
            <ProposalEditor 
              proposal={activeProposal}
              onClose={() => setActiveProposal(null)}
              onReject={() => setActiveProposal(null)}
              onApprove={(id, script) => {
                handleTriggerProduction(script);
                setActiveProposal(null);
              }}
            />
          </>
        )}
      </AnimatePresence>

      {/* 1. Zone Centrale: L'Entité */}
      <div className="col-lg-6 order-lg-2">
        <div className="glass-card h-100" style={{ borderTop: `0.5px solid ${accentColor}` }}>
          <h2 className="fw-light mb-4 tracking-widest small opacity-75">THE ENTITY | SOVEREIGN HEART</h2>
          
          <div style={{ height: '400px' }}>
            <VisualVortex />
          </div>
          <NeuralWaveform />

          {/* Real-time monologue from StateDB */}
          <div className="mt-4 p-4 bg-white bg-opacity-5 rounded-1 italic small text-secondary fw-light border border-white border-opacity-5" style={{ lineHeight: '1.6' }}>
            <span className="text-white-50 font-monospace me-2" style={{ fontSize: '0.65rem' }}>INTERNAL_MONOLOGUE:</span>
            {rawMood?.current_thought || "Initialising consciousness..."}
          </div>
          
        </div>
      </div>

      {/* 2. Zone Gauche: Cognition & Perception */}
      <div className="col-lg-3 order-lg-1">
        <div className="glass-card mb-4">
          <h4 className="fw-light mb-4 tracking-widest small">COGNITION_MATRIX</h4>
          
          {/* Sovereign Switch */}
          <div className="mb-5 p-3 border border-white border-opacity-10 rounded-1">
            <div className="d-flex justify-content-between align-items-center mb-3">
              <label className="small text-secondary tracking-widest" style={{ fontSize: '0.6rem' }}>SOVEREIGN_SWITCH</label>
              <span className={`font-monospace small ${isSovereign ? 'text-success' : 'text-warning'}`} style={{ fontSize: '0.6rem' }}>
                {isSovereign ? "AUTO_MODE" : "COLLABORATIVE"}
              </span>
            </div>
            <div className="d-flex gap-2">
              <button 
                className={`btn btn-sm flex-fill fw-light small py-2 ${isSovereign ? 'bg-white bg-opacity-10 text-white border-white' : 'text-secondary border-white border-opacity-5'}`}
                onClick={async () => {
                  const newState = !isSovereign;
                  await smosApi.toggleSovereignMode(newState);
                  setIsSovereign(newState);
                }}
              >
                {isSovereign ? "[ ACTIVE ]" : "[ MANUAL ]"}
              </button>
            </div>
          </div>

          <div className="mb-4">
            <label className="form-label small text-secondary tracking-widest" style={{ fontSize: '0.6rem' }}>MOOD VECTORED</label>
            <div className="d-flex flex-column gap-2">
              <button 
                className={`btn btn-sm text-start py-2 px-3 border border-white border-opacity-10 fw-light small tracking-wide ${mood === 'authority' ? 'bg-white bg-opacity-10 text-white' : 'text-secondary'}`}
                onClick={() => setMood('authority')}
                style={{ borderLeft: mood === 'authority' ? `2px solid ${accentColor}` : '1px solid transparent' }}
              >AUTHORITY</button>
              <button 
                className={`btn btn-sm text-start py-2 px-3 border border-white border-opacity-10 fw-light small tracking-wide ${mood === 'reflection' ? 'bg-white bg-opacity-10 text-white' : 'text-secondary'}`}
                onClick={() => setMood('reflection')}
                style={{ borderLeft: mood === 'reflection' ? `2px solid ${accentColor}` : '1px solid transparent' }}
              >REFLECTION</button>
              <button 
                className={`btn btn-sm text-start py-2 px-3 border border-white border-opacity-10 fw-light small tracking-wide ${mood === 'creativity' ? 'bg-white bg-opacity-10 text-white' : 'text-secondary'}`}
                onClick={() => setMood('creativity')}
                style={{ borderLeft: mood === 'creativity' ? `2px solid ${accentColor}` : '1px solid transparent' }}
              >CREATIVITY</button>
            </div>
          </div>
          <div className="p-3 bg-white bg-opacity-5 rounded-1 border border-white border-opacity-5 text-center">
            <div className="text-secondary small font-monospace tracking-tighter" style={{ fontSize: '0.65rem' }}>
              V: {rawMood?.valence.toFixed(4) || "0.0000"} | A: {rawMood?.arousal.toFixed(4) || "0.0000"}
            </div>
          </div>
        </div>

        <TrendFeed 
          onExecute={openProposal}
          onDiscuss={openProposal}
        />
      </div>

      {/* 3. Zone Droite: L'Usine Créative */}
      <div className="col-lg-3 order-lg-3">
        <SwarmStatus />

        <div className="glass-card">
          <h4 className="fw-light mb-4 tracking-widest small">INSTANT CANVAS</h4>
          <div className="bg-black rounded-1 ratio ratio-1x1 border border-white border-opacity-5 d-flex align-items-center justify-content-center text-secondary overflow-hidden text-center shadow-inner">
            {isTriggering ? (
              <div className="p-4">
                <div className="spinner-border text-white-50 border-1 mb-3" style={{ width: '1.5rem', height: '1.5rem' }} role="status"></div>
                <br/><span className="text-white-50 small tracking-widest font-monospace" style={{ fontSize: '0.6rem' }}>DISPATCHING_SWARM...</span>
              </div>
            ) : (
              <div className="p-4">
                <span className="text-white-50 small tracking-widest font-monospace opacity-50" style={{ fontSize: '0.6rem' }}>AWAITING_RENDER_SIGNAL</span>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}