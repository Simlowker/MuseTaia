'use client';

import { useMood } from '@/context/MoodContext';
import VisualVortex from '@/components/VisualVortex';
import NeuralWaveform from '@/components/NeuralWaveform';
import TrendFeed from '@/components/TrendFeed';
import SwarmStatus from '@/components/SwarmStatus';

export default function Home() {
  const { mood, setMood, accentColor } = useMood();

  return (
    <div className="row g-4">
      {/* 1. Zone Centrale: L'Entité */}
      <div className="col-lg-6 order-lg-2">
        <div className="glass-card accent-border h-100" style={{ borderTop: '4px solid' }}>
          <h2 className="fw-bold mb-4 accent-text">THE ENTITY</h2>
          
          <VisualVortex />
          <NeuralWaveform />
          
        </div>
      </div>

      {/* 2. Zone Gauche: Cognition & Perception */}
      <div className="col-lg-3 order-lg-1">
        <div className="glass-card mb-4">
          <h4 className="fw-bold mb-3">COGNITION</h4>
          <div className="mb-3">
            <label className="form-label small text-secondary">MOOD VECTORED</label>
            <div className="d-flex gap-2">
              <button 
                className={`btn btn-sm btn-outline-secondary ${mood === 'authority' ? 'active' : ''}`}
                onClick={() => setMood('authority')}
              >Authority</button>
              <button 
                className={`btn btn-sm btn-outline-secondary ${mood === 'reflection' ? 'active' : ''}`}
                onClick={() => setMood('reflection')}
              >Reflection</button>
              <button 
                className={`btn btn-sm btn-outline-secondary ${mood === 'creativity' ? 'active' : ''}`}
                onClick={() => setMood('creativity')}
              >Creativity</button>
            </div>
          </div>
          <div className="p-3 border border-secondary rounded text-center small text-secondary">
            [ Mood Matrix Chart Sync ]
          </div>
        </div>

        <TrendFeed />
      </div>

      {/* 3. Zone Droite: L'Usine Créative */}
      <div className="col-lg-3 order-lg-3">
        <SwarmStatus />

        <div className="glass-card">
          <h4 className="fw-bold mb-3">INSTANT CANVAS</h4>
          <div className="bg-dark rounded-3 ratio ratio-1x1 d-flex align-items-center justify-content-center text-secondary overflow-hidden">
            <div className="p-4 text-center">
              <span className="small">WAITING FOR CRITIC APPROVAL...</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}