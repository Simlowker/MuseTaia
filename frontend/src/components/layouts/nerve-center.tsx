"use client";

import React from 'react';
import { SystemProvider } from '../../contexts/system-context';
import { PerceptionLobe } from '../dashboard/PerceptionLobe';
import { ConsciousnessCore } from '../dashboard/ConsciousnessCore';
import { CreationLobe } from '../dashboard/CreationLobe';
import { DecisionPipeline } from '../dashboard/DecisionPipeline';

import { SovereignTimeline } from '../dashboard/SovereignTimeline';
import { WalletWidget } from '../dashboard/WalletWidget';
import { HITLApprovalModal } from '../dashboard/HITLApprovalModal';
import { MoodAura } from '../dashboard/MoodAura';
import { SynapseLines } from '../dashboard/SynapseLines';

export default function NerveCenterLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <SystemProvider>
      <div className="min-h-screen bg-void text-foreground grid grid-rows-[60px_1fr_80px] overflow-hidden font-luxe relative">
        <HITLApprovalModal />
        
        {/* HEADER BAR */}
        <header className="border-b border-glass-border bg-glass-bg backdrop-blur-md flex items-center justify-between px-6 z-50">
          <div className="flex items-center gap-3">
            <div className="w-3 h-3 rounded-full bg-emerald animate-pulse" />
            <h1 className="text-lg font-bold tracking-widest text-gold uppercase">SMOS v2 <span className="text-white/40 text-xs ml-2">Sovereign Muse</span></h1>
          </div>
          <div className="flex items-center gap-6 text-xs text-white/60">
              <span>MODE: <span className="text-white font-bold">AUTONOMOUS</span></span>
              <span>UPTIME: <span className="text-white font-bold">42h 12m</span></span>
          </div>
        </header>

        {/* MAIN CONTENT GRID (3 LOBES) */}
        <main className="grid grid-cols-[300px_1fr_350px] gap-0 relative">
          <SynapseLines />
          
          {/* PERCEPTION LOBE (Left) */}
          <section className="border-r border-glass-border bg-onyx/40 p-4 relative overflow-hidden">
               <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-cyan/20 to-transparent"></div>
               <div className="h-full border border-glass-border rounded-lg bg-glass-bg p-4 overflow-y-auto no-scrollbar relative z-20">
                  <PerceptionLobe />
               </div>
          </section>

          {/* CONSCIOUSNESS CORE (Center) */}
          <section className="relative flex flex-col items-center justify-center p-8 overflow-hidden">
               <MoodAura />
               <div className="relative z-20 flex flex-col items-center justify-center h-full w-full">
                   <ConsciousnessCore />
                   
                   {/* Decision Pipeline Overlay */}
                   <div className="mt-auto pb-4 w-full flex justify-center">
                      <DecisionPipeline />
                   </div>
               </div>
          </section>

          {/* CREATION LOBE (Right) */}
          <section className="border-l border-glass-border bg-onyx/40 p-4 relative overflow-hidden">
               <div className="absolute top-0 right-0 w-full h-1 bg-gradient-to-r from-transparent via-ruby/20 to-transparent"></div>
               <div className="h-full border border-glass-border rounded-lg bg-glass-bg p-4 overflow-y-auto no-scrollbar relative z-20">
                  <CreationLobe />
               </div>
          </section>
        </main>

        {/* TIMELINE (Bottom) */}
        <footer className="border-t border-glass-border bg-obsidian z-50 flex items-center justify-between px-6">
           <SovereignTimeline />
           <WalletWidget />
        </footer>
      </div>
    </SystemProvider>
  );
}
