"use client";

import React from 'react';
import { motion } from 'framer-motion';
import { Shield, Activity, Database, Zap, Terminal } from 'lucide-react';
import '@/styles/ultra-realistic.css';
import { useNeural } from '@/context/NeuralContext';

// Components we will build next
import IdentityScanner from '@/components/IdentityScanner';
import ReactorForge from '@/components/ReactorForge';
import TacticalHud from '@/components/TacticalHud';

export default function Home() {
  const { status } = useNeural();

  return (
    <main className="h-screen w-screen bg-[#080808] flex items-center justify-center p-4 overflow-hidden">
      {/* OUTER FRAME / COCKPIT BEZEL */}
      <div className="cockpit-bezel w-full h-full rounded-[2.5rem] p-4 flex flex-col relative overflow-hidden">
        <div className="metal-texture" />
        
        {/* TOP STATUS BAR (Physical looking) */}
        <header className="h-12 border-b border-white/5 flex items-center justify-between px-8 mb-4">
          <div className="flex items-center gap-4">
            <div className="w-3 h-3 rounded-full bg-red-600 shadow-[0_0_10px_#ff0000]" />
            <span className="text-[10px] font-black tracking-widest text-neutral-500 uppercase">System: Armed</span>
          </div>
          
          <div className="flex items-center gap-8">
            <div className="flex flex-col items-end">
              <span className="text-[8px] text-neutral-600 font-bold uppercase tracking-tighter">Connection Status</span>
              <span className={`text-[10px] font-mono ${status === 'connected' ? 'text-cyan-400' : 'text-red-500'}`}>
                {status === 'connected' ? 'SECURE_LINK_ACTIVE' : 'LINK_LOST'}
              </span>
            </div>
            <div className="w-px h-6 bg-white/10" />
            <h1 className="text-sm font-black italic tracking-tighter hologram-text">SMOS v2.0 // EXOSKELETON</h1>
          </div>
        </header>

        {/* MAIN HUD INTERFACE */}
        <div className="flex-1 grid grid-cols-12 gap-4 min-h-0">
          
          {/* LEFT PANEL: NEURAL TELEMETRY */}
          <div className="col-span-3 flex flex-col gap-4">
            <div className="glass-panel rounded-3xl flex-1 p-1">
              <div className="scanline-effect absolute inset-0" />
              <TacticalHud />
            </div>
          </div>

          {/* CENTER PANEL: COMMAND CORE */}
          <div className="col-span-6 flex flex-col gap-4">
            <div className="glass-panel rounded-[3rem] flex-[2] relative group">
              <div className="scanline-effect absolute inset-0" />
              
              {/* Central Hologram Core */}
              <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                <motion.div 
                  animate={{ 
                    scale: [1, 1.05, 1],
                    opacity: [0.3, 0.5, 0.3]
                  }}
                  transition={{ duration: 4, repeat: Infinity }}
                  className="w-96 h-96 bg-cyan-500/5 rounded-full blur-[100px]"
                />
                <Database className="w-32 h-32 text-cyan-500/10" />
              </div>

              {/* Functional Controls */}
              <div className="absolute inset-0 flex flex-col items-center justify-center p-12">
                <div className="text-center space-y-2 mb-12">
                  <h2 className="text-[10px] font-bold text-cyan-500/50 uppercase tracking-[0.5em]">Materialization Core</h2>
                  <p className="text-4xl font-black tracking-tighter text-white opacity-80">READY FOR COMMAND</p>
                </div>

                <div className="flex gap-6 mt-auto">
                  <ControlButton label="Surprise Me" color="cyan" primary />
                  <ControlButton label="Genesis Launch" color="neutral" />
                </div>
              </div>
            </div>

            {/* Bottom Sector: Reactor Forge */}
            <div className="glass-panel rounded-3xl h-1/3 p-1">
              <ReactorForge />
            </div>
          </div>

          {/* RIGHT PANEL: BIOMETRIC & FINANCIAL */}
          <div className="col-span-3 flex flex-col gap-4">
            <div className="glass-panel rounded-3xl h-3/5">
              <IdentityScanner />
            </div>
            <div className="glass-panel rounded-3xl flex-1 p-6 flex flex-col">
              <div className="flex items-center gap-2 mb-4">
                <Zap className="w-4 h-4 text-amber-500" />
                <span className="text-[10px] font-bold text-amber-500 uppercase tracking-widest">Sovereign Wallet</span>
              </div>
              <div className="space-y-4">
                <div className="p-4 rounded-2xl bg-black/40 border border-white/5 shadow-inner">
                  <span className="text-[8px] text-neutral-600 uppercase font-bold">Credits / USD</span>
                  <p className="text-3xl font-black text-white/90 font-mono">$24.55</p>
                </div>
                <div className="grid grid-cols-2 gap-2">
                  <div className="p-3 rounded-xl bg-white/[0.02] border border-white/5">
                    <span className="text-[7px] text-neutral-600 uppercase font-bold block">Auth</span>
                    <span className="text-[10px] text-green-500 font-black">SOLVENT</span>
                  </div>
                  <div className="p-3 rounded-xl bg-white/[0.02] border border-white/5">
                    <span className="text-[7px] text-neutral-600 uppercase font-bold block">ROI</span>
                    <span className="text-[10px] text-white font-black">+1.8x</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* BOTTOM NOTIFICATION STRIP */}
        <footer className="h-10 mt-4 border-t border-white/5 flex items-center px-8 gap-12">
          <div className="flex gap-8 text-[8px] font-bold text-neutral-600 uppercase tracking-widest overflow-hidden">
             <span className="animate-pulse">A2A_PIPE::ACTIVE</span>
             <span>CRIU::SNAP_ARMED</span>
             <span>VVS::VELOCITY_HIGH</span>
             <span>GKE_NODE::L4_GPU_OK</span>
          </div>
          <div className="ml-auto text-[8px] font-mono text-cyan-950">BUILD_SMOS_V2_INDUSTRIAL_STABLE</div>
        </footer>
      </div>
    </main>
  );
}

const ControlButton = ({ label, color, primary = false }: { label: string, color: string, primary?: boolean }) => (
  <button className={`
    px-8 py-4 rounded-2xl text-[10px] font-black uppercase tracking-[0.2em] transition-all
    ${primary ? 'bg-cyan-500 text-black shadow-[0_0_20px_rgba(0,242,255,0.3)] hover:scale-105' : 'bg-white/5 text-white/50 border border-white/10 hover:bg-white/10'}
  `}>
    {label}
  </button>
);
