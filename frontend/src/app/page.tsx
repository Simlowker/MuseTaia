'use client';

import { useMood } from '@/context/MoodContext';

export default function Home() {
  const { mood, setMood, accentColor } = useMood();

  return (
    <div className="row g-4">
      {/* 1. Zone Centrale: L'Entité */}
      <div className="col-lg-6 order-lg-2">
        <div className="glass-card accent-border" style={{ minHeight: '600px', borderTop: '4px solid' }}>
          <h2 className="fw-bold mb-4 accent-text">THE ENTITY</h2>
          <div className="bg-dark rounded-3 d-flex align-items-center justify-content-center" style={{ minHeight: '400px' }}>
            <span className="text-secondary">[ Veo 3.1 4K Visual Vortex Placeholder ]</span>
          </div>
          <div className="mt-4 p-3 border border-secondary rounded">
            <div className="d-flex justify-content-between align-items-center">
              <span className="small text-secondary">NEURAL WAVEFORM</span>
              <span className="badge border border-secondary" style={{ color: accentColor }}>ACTIVE</span>
            </div>
            <div className="mt-2 text-secondary small">[ Sinusoidal Particle Animation ]</div>
          </div>
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

        <div className="glass-card">
          <h4 className="fw-bold mb-3">NICHE TRENDS</h4>
          <ul className="list-group list-group-flush bg-transparent">
            <li className="list-group-item bg-transparent text-white border-secondary small">
              Digital Couture #PFW <span className="float-end text-success">92%</span>
            </li>
            <li className="list-group-item bg-transparent text-white border-secondary small">
              Generative Arch <span className="float-end text-warning">74%</span>
            </li>
          </ul>
        </div>
      </div>

      {/* 3. Zone Droite: L'Usine Créative */}
      <div className="col-lg-3 order-lg-3">
        <div className="glass-card mb-4">
          <h4 className="fw-bold mb-3">SWARM STATUS</h4>
          <div className="mb-3 small">
            <div className="d-flex justify-content-between mb-1">
              <span>Narrative Lead</span>
              <span className="text-secondary">Ready</span>
            </div>
            <div className="progress bg-dark" style={{ height: '4px' }}>
              <div className="progress-bar" style={{ width: '100%', backgroundColor: accentColor }}></div>
            </div>
          </div>
          <div className="mb-3 small">
            <div className="d-flex justify-content-between mb-1">
              <span>Visual Virtuoso</span>
              <span className="text-secondary">Rendering...</span>
            </div>
            <div className="progress bg-dark" style={{ height: '4px' }}>
              <div className="progress-bar progress-bar-animated progress-bar-striped" style={{ width: '60%', backgroundColor: accentColor }}></div>
            </div>
          </div>
        </div>

        <div className="glass-card">
          <h4 className="fw-bold mb-3">INSTANT CANVAS</h4>
          <div className="bg-dark rounded-3 ratio ratio-1x1 d-flex align-items-center justify-content-center text-secondary">
            [ Preview Slot ]
          </div>
        </div>
      </div>
    </div>
  );
}