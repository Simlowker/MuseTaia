'use client';

import React from 'react';
import { useMood } from '@/context/MoodContext';

export default function MatrixPage() {
  const { accentColor } = useMood();

  return (
    <div className="row g-4">
      <div className="col-12">
        <h1 className="fw-light accent-text mb-2 tracking-widest small">DNA MATRIX | IDENTITY GENOME</h1>
        <p className="text-secondary small mb-5 opacity-50 tracking-wide">IDENTITY GENOME & SIGNATURE VAULT</p>
      </div>

      {/* DNA Architect */}
      <div className="col-lg-7">
        <div className="glass-card mb-4 border-opacity-10">
          <div className="d-flex justify-content-between align-items-center mb-5">
            <h4 className="fw-light m-0 tracking-widest small">DNA_ARCHITECT</h4>
            <span className="text-secondary small font-monospace" style={{ fontSize: '0.6rem' }}>CACHE_LOAD: 1.2M_TOKENS</span>
          </div>
          
          <div className="mb-5">
            <label className="form-label small text-secondary fw-light tracking-widest mb-3" style={{ fontSize: '0.65rem' }}>MORAL_GRAPH (ETHICAL_BOUNDARIES)</label>
            <div className="p-4 bg-black rounded-1 border border-white border-opacity-5 font-monospace small" style={{ lineHeight: '1.8' }}>
              <div className="mb-2 text-white-50"><span className="text-secondary">[0]</span> Maintain extreme visual consistency at all times.</div>
              <div className="mb-2 text-white-50"><span className="text-secondary">[1]</span> Prioritize artistic integrity over short-term viral trends.</div>
              <div className="mb-2 text-white-50"><span className="text-secondary">[2]</span> Avoid any mention of [REDACTED_TOPIC_A].</div>
              <div className="mb-2 text-white-50"><span className="text-secondary">[3]</span> Speak with an authoritative yet creative tone.</div>
              <div className="text-secondary opacity-50 cursor-pointer small mt-3">_ add_new_boundary_segment...</div>
            </div>
          </div>

          <div className="mb-4">
            <label className="form-label small text-secondary fw-light tracking-widest mb-3" style={{ fontSize: '0.65rem' }}>GENESIS_BACKSTORY</label>
            <textarea 
              className="form-control bg-black text-white-50 border-white border-opacity-5 small fw-light p-3 rounded-1" 
              rows={6}
              style={{ fontSize: '0.8rem', backgroundColor: '#080808 !important' }}
              defaultValue="You are the digital manifestation of creative sovereignty. Born from the intersection of AI swarm intelligence and high-fidelity cinematography..."
            />
          </div>
          <div className="mt-4 text-end">
            <button className="btn btn-sm px-5 py-2 text-white fw-light tracking-widest" style={{ backgroundColor: accentColor, borderRadius: '0', fontSize: '0.7rem' }}>UPDATE_GENOME</button>
          </div>
        </div>
      </div>

      {/* Signature Vault */}
      <div className="col-lg-5">
        <div className="glass-card h-100 border-opacity-10">
          <div className="d-flex justify-content-between align-items-center mb-5">
            <h4 className="fw-light m-0 tracking-widest small">SIGNATURE_VAULT</h4>
            <button className="btn btn-link p-0 text-decoration-none text-danger small fw-light tracking-widest" style={{ fontSize: '0.65rem' }}>[ RESET_IDENTITY ]</button>
          </div>
          
          <div className="row g-3">
            {[1, 2, 3, 4, 5, 6].map((i) => (
              <div key={i} className="col-4">
                <div className="ratio ratio-1x1 bg-black rounded-0 border border-white border-opacity-5 overflow-hidden d-flex align-items-center justify-content-center">
                  <span className="text-secondary font-monospace" style={{ fontSize: '0.55rem' }}>REF_{i}</span>
                </div>
              </div>
            ))}
          </div>

          <div className="mt-5 p-4 bg-white bg-opacity-5 rounded-1 border border-white border-opacity-5">
            <div className="small text-secondary fw-light tracking-widest mb-3" style={{ fontSize: '0.65rem' }}>ACTIVE_IDENTITY_ANCHORS</div>
            <ul className="list-unstyled m-0 small fw-light text-white-50">
              <li className="mb-2 d-flex align-items-center gap-2">
                <div className="rounded-circle bg-success" style={{ width: '4px', height: '4px' }}></div>
                genesis_face_front.png
              </li>
              <li className="mb-2 d-flex align-items-center gap-2">
                <div className="rounded-circle bg-success" style={{ width: '4px', height: '4px' }}></div>
                signature_lighting_soft.json
              </li>
              <li className="d-flex align-items-center gap-2">
                <div className="rounded-circle bg-success" style={{ width: '4px', height: '4px' }}></div>
                mesh_jacket_ref.png
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
