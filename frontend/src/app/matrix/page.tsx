'use client';

import React from 'react';
import { useMood } from '@/context/MoodContext';

export default function MatrixPage() {
  const { accentColor } = useMood();

  return (
    <div className="row g-4">
      <div className="col-12">
        <h1 className="fw-bold accent-text mb-2">DNA MATRIX</h1>
        <p className="text-secondary small mb-4">IDENTITY GENOME & SIGNATURE VAULT</p>
      </div>

      {/* DNA Architect */}
      <div className="col-lg-7">
        <div className="glass-card mb-4">
          <div className="d-flex justify-content-between align-items-center mb-4">
            <h4 className="fw-bold m-0">DNA ARCHITECT</h4>
            <span className="badge bg-dark border border-secondary text-secondary small">VERTEX AI CONTEXT CACHE: 1.2M TOKENS</span>
          </div>
          
          <div className="mb-4">
            <label className="form-label small text-secondary fw-bold mb-3">MORAL GRAPH (ETHICAL BOUNDARIES)</label>
            <div className="p-3 bg-black rounded border border-secondary font-monospace small">
              <div className="mb-2 text-info">[0] Maintain extreme visual consistency at all times.</div>
              <div className="mb-2 text-info">[1] Prioritize artistic integrity over short-term viral trends.</div>
              <div className="mb-2 text-info">[2] Avoid any mention of [REDACTED_TOPIC_A].</div>
              <div className="mb-2 text-info">[3] Speak with an authoritative yet creative tone.</div>
              <div className="text-secondary opacity-50 cursor-pointer">_ add new boundary segment...</div>
            </div>
          </div>

          <div className="mb-2">
            <label className="form-label small text-secondary fw-bold mb-3">GENESIS BACKSTORY</label>
            <textarea 
              className="form-control bg-dark text-white border-secondary small" 
              rows={6}
              defaultValue="You are the digital manifestation of creative sovereignty. Born from the intersection of AI swarm intelligence and high-fidelity cinematography..."
            />
          </div>
          <div className="mt-3 text-end">
            <button className="btn btn-sm px-4 text-white" style={{ backgroundColor: accentColor }}>UPDATE GENOME</button>
          </div>
        </div>
      </div>

      {/* Signature Vault */}
      <div className="col-lg-5">
        <div className="glass-card h-100">
          <div className="d-flex justify-content-between align-items-center mb-4">
            <h4 className="fw-bold m-0">SIGNATURE VAULT</h4>
            <button className="btn btn-sm btn-outline-danger small" style={{ fontSize: '0.7rem' }}>RESET IDENTITY</button>
          </div>
          
          <div className="row g-3">
            {[1, 2, 3, 4, 5, 6].map((i) => (
              <div key={i} className="col-4">
                <div className="ratio ratio-1x1 bg-dark rounded border border-secondary overflow-hidden d-flex align-items-center justify-content-center">
                  <span className="text-secondary small" style={{ fontSize: '0.6rem' }}>REF_{i}</span>
                </div>
              </div>
            ))}
          </div>

          <div className="mt-4 p-3 border border-secondary rounded">
            <div className="small text-secondary fw-bold mb-2">ACTIVE IDENTITY ANCHORS</div>
            <ul className="list-unstyled m-0 small">
              <li className="mb-1 text-white-50">✓ genesis_face_front.png</li>
              <li className="mb-1 text-white-50">✓ signature_lighting_soft.json</li>
              <li className="text-white-50">✓ mesh_jacket_ref.png</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
