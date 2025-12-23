"use client";

import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useNeural } from '@/context/NeuralContext';
import { ContextNav } from '@/components/nav/ContextNav';
import { CentralAvatar } from '@/components/cinematic/CentralAvatar';
import { TrendFeed } from '@/components/cinematic/TrendFeed';
import { CreativeSwarm } from '@/components/cinematic/CreativeSwarm';
import { ActiveThought } from '@/components/cinematic/ActiveThought';
import { WorldTimeline } from '@/components/history/WorldTimeline';
import '@/styles/ultra-realistic.css';

export default function Home() {
  const { status } = useNeural();

  // Temporary background placeholder for "Room Environment"
  const roomBg = "radial-gradient(circle at center, #2C241B 0%, #050505 80%)";

  return (
    <ContextNav>
      {(intent) => (
        <main className="h-screen w-screen overflow-hidden relative isolate bg-black text-white selection:bg-gold/30" style={{ background: roomBg }}>

          {/* LAYER 0: CENTRAL AVATAR (Background Layer) */}
          {/* Use flex to perfectly center the avatar content */}
          <div className="absolute inset-0 z-0 flex items-center justify-center pointer-events-none">
            <CentralAvatar />
          </div>

          {/* LAYER 1: HUD GRID (Foreground Layer) */}
          {/* Grid Layout: Header (Top), Main Content (Middle), Footer/Thought (Bottom) */}
          <div className="absolute inset-0 z-10 grid grid-rows-[auto_1fr_auto] p-6 pointer-events-none gap-4">

            {/* TOP ROW: Header */}
            <header className="flex justify-between items-start pb-2 opacity-70">
              <div className="flex flex-col">
                <h1 className="text-[10px] font-bold tracking-[0.4em] uppercase text-gold">Sovereign Muse OS</h1>
                <span className="text-[9px] text-white/40 tracking-widest">V.2.0.4 :: {intent.toUpperCase()} MODE</span>
              </div>

              <div className="flex gap-3 items-center px-3 py-1 bg-white/5 rounded-full backdrop-blur-md border border-white/5">
                <div className={`w-1.5 h-1.5 rounded-full shadow-[0_0_8px] ${status === 'connected' ? 'bg-emerald-500 shadow-emerald-500' : 'bg-red-500'}`} />
                <span className="text-[9px] font-mono text-white/50">{status === 'connected' ? 'SYSTEM ONLINE' : 'DISCONNECTED'}</span>
              </div>
            </header>

            {/* MIDDLE ROW: 3 Columns Grid */}
            {/* Left (Trends), Center (Spacer for Avatar), Right (Swarm) */}
            <div className="grid grid-cols-[320px_1fr_360px] gap-8 h-full items-center overflow-hidden">

              {/* LEFT COL: Trend Feed */}
              <div className="h-[60vh] pointer-events-auto flex flex-col justify-center">
                <TrendFeed />
              </div>

              {/* CENTER COL: Empty (Avatar is visually here but in Layer 0) */}
              <div className="h-full" />

              {/* RIGHT COL: Creative Swarm */}
              <div className="h-[60vh] pointers-events-auto flex flex-col justify-center">
                <CreativeSwarm />
              </div>
            </div>

            {/* BOTTOM ROW: Active Thought */}
            <div className="flex justify-center pt-2 pb-6 pointer-events-auto">
              <div className="w-[600px]">
                <ActiveThought />
              </div>
            </div>

          </div>

          {/* LAYER 2: GLOBAL NAV / TIMELINE (Conditional Overlay) */}
          <AnimatePresence>
            {intent === 'history' && (
              <motion.div
                initial={{ opacity: 0, y: 100 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: 100 }}
                className="absolute bottom-0 left-0 right-0 z-50 pointer-events-auto shadow-[0_-20px_40px_rgba(0,0,0,0.8)]"
              >
                <WorldTimeline />
              </motion.div>
            )}
          </AnimatePresence>

        </main>
      )}
    </ContextNav>
  );
}
