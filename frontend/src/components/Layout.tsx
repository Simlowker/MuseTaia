'use client';

import React from 'react';
import { useMood } from '@/context/MoodContext';
import '@/styles/globals.scss';

export default function Layout({ children }: { children: React.ReactNode }) {
  const { accentColor } = useMood();

  return (
    <div className="sovereign-shell" style={{ '--accent-color': accentColor } as React.CSSProperties}>
      <nav className="navbar navbar-expand-lg border-bottom border-secondary mb-4 px-4">
        <div className="container-fluid">
          <a className="navbar-brand text-white fw-bold" href="/">SMOS</a>
          <div className="navbar-nav ms-auto">
            <a className="nav-link text-secondary" href="/forge">Forge</a>
            <a className="nav-link text-secondary" href="/matrix">DNA Matrix</a>
            <a className="nav-link text-secondary" href="/ledger">Ledger</a>
          </div>
        </div>
      </nav>
      <main className="container-fluid px-4 pb-5">
        {children}
      </main>
    </div>
  );
}
