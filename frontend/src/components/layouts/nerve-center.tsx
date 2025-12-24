"use client";

import React, { useEffect, useRef, useState } from "react";
import { useSystem } from "@/contexts/system-context";
import { cn } from "@/lib/utils";
import { SplitThought } from "./SplitThought";
import { IdentityScanner } from "@/components/hud/IdentityScanner";
import { BentoGrid, BentoGridItem } from "@/components/ui/BentoGrid";
import { AnimatedBeam } from "@/components/ui/AnimatedBeam";
import { Vortex } from "@/components/vfx/Vortex";
import { Brain, Wallet, Activity, Search, Users } from "lucide-react";

export default function NerveCenterLayout({ children }: { children?: React.ReactNode }) {
  const { mood, wallet, trends, activeProduction, pipeline } = useSystem();
  
  // Refs for AnimatedBeams
  const perceptionRef = useRef<HTMLDivElement>(null);
  const coreRef = useRef<HTMLDivElement>(null);
  const creationRef = useRef<HTMLDivElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  // Derived state for visuals
  const moodColor = mood?.valence && mood.valence > 0 ? "emerald" : "ruby";
  const thought = mood?.current_thought || "System Idle...";

  return (
    <div className="relative w-full h-screen bg-black text-white overflow-hidden font-sans" ref={containerRef}>
      
      {/* Background VFX */}
      <div className="absolute inset-0 z-0 opacity-30">
        <Vortex 
            rangeY={800}
            baseHue={200}
            baseSpeed={0.2}
            rangeSpeed={1.0}
            particleCount={300}
            containerClassName="w-full h-full"
        />
      </div>

      {/* Main Grid Layout */}
      <div className="relative z-10 w-full h-full p-6 flex flex-col gap-6">
        
        {/* Header */}
        <header className="flex justify-between items-center border-b border-white/10 pb-4">
            <div className="flex items-center gap-3">
                <div className="w-2 h-2 bg-gold animate-pulse rounded-full" />
                <h1 className="text-xl font-bold tracking-[0.2em] text-gold uppercase">Sovereign Muse OS</h1>
            </div>
            <div className="flex gap-6 text-xs font-mono text-white/40">
                <span>V.2.0.5</span>
                <span>STATUS: <span className="text-emerald-400">ONLINE</span></span>
            </div>
        </header>

        {/* Bento Grid Content */}
        <BentoGrid className="flex-1 max-w-full md:auto-rows-[minmax(0,1fr)]">
            
            {/* 1. PERCEPTION (Left) */}
            <BentoGridItem
                className="md:col-span-1 dark:bg-black/40 dark:border-white/10"
                header={<div ref={perceptionRef} className="h-full flex flex-col gap-4">
                    <div className="flex items-center gap-2 text-cyan-400 font-mono text-xs uppercase tracking-widest">
                        <Search size={14} /> Perception Lobe
                    </div>
                    <div className="flex-1 overflow-y-auto no-scrollbar space-y-2">
                        {trends.map(t => (
                            <div key={t.id} className="p-3 bg-white/5 border border-white/5 rounded-lg hover:border-cyan-500/30 transition-colors">
                                <div className="flex justify-between text-xs mb-1">
                                    <span className="font-bold text-white/90">#{t.title}</span>
                                    <span className="text-cyan-400">{t.vvs_score} VVS</span>
                                </div>
                                <div className="w-full h-1 bg-white/10 rounded-full overflow-hidden">
                                    <div className="h-full bg-cyan-500" style={{ width: `${Math.min(t.vvs_score, 100)}%` }} />
                                </div>
                            </div>
                        ))}
                    </div>
                </div>}
            />

            {/* 2. CONSCIOUSNESS CORE (Center - Large) */}
            <BentoGridItem
                className="md:col-span-1 md:row-span-2 dark:bg-black/60 border-gold/20"
                header={<div ref={coreRef} className="h-full flex flex-col items-center justify-center relative">
                    <IdentityScanner />
                    <div className="absolute bottom-8 left-0 right-0 px-8 text-center">
                        <SplitThought words={thought} className="text-lg font-light italic text-gold/80" />
                    </div>
                </div>}
            />

            {/* 3. CREATION (Right) */}
            <BentoGridItem
                className="md:col-span-1 dark:bg-black/40 dark:border-white/10"
                header={<div ref={creationRef} className="h-full flex flex-col gap-4">
                    <div className="flex items-center gap-2 text-ruby-400 font-mono text-xs uppercase tracking-widest">
                        <Activity size={14} /> Creation Lobe
                    </div>
                    {activeProduction ? (
                        <div className="flex-1 flex flex-col justify-end p-4 bg-gradient-to-t from-ruby-900/20 to-transparent rounded-lg border border-ruby-500/20">
                            <h3 className="text-lg font-bold text-white">{activeProduction.title}</h3>
                            <div className="flex justify-between text-xs text-ruby-300 mt-2">
                                <span>{activeProduction.status}</span>
                                <span>{activeProduction.progress}%</span>
                            </div>
                        </div>
                    ) : (
                        <div className="flex-1 flex items-center justify-center text-white/20 text-xs uppercase tracking-widest border border-dashed border-white/10 rounded-lg">
                            Studio Idle
                        </div>
                    )}
                </div>}
            />

            {/* 4. SOVEREIGN WALLET (Bottom Left) */}
            <BentoGridItem
                className="md:col-span-1 dark:bg-black/40 dark:border-white/10"
                header={<div className="h-full flex flex-col justify-between">
                    <div className="flex items-center gap-2 text-emerald-400 font-mono text-xs uppercase tracking-widest">
                        <Wallet size={14} /> Sovereign Wallet
                    </div>
                    <div className="text-4xl font-bold text-white tracking-tighter">
                        ${wallet?.balance.toFixed(2) || "0.00"}
                    </div>
                    <div className="w-full h-1.5 bg-white/10 rounded-full overflow-hidden">
                        <div 
                            className={`h-full ${wallet && (wallet.daily_spend / wallet.daily_budget) > 0.8 ? 'bg-ruby' : 'bg-emerald'}`} 
                            style={{ width: `${wallet ? (wallet.daily_spend / wallet.daily_budget) * 100 : 0}%` }} 
                        />
                    </div>
                    <div className="flex justify-between text-[10px] text-white/40 font-mono">
                        <span>SPEND: ${wallet?.daily_spend.toFixed(2)}</span>
                        <span>CAP: ${wallet?.daily_budget.toFixed(2)}</span>
                    </div>
                </div>}
            />

            {/* 5. SWARM STATUS (Bottom Right) */}
            <BentoGridItem
                className="md:col-span-1 dark:bg-black/40 dark:border-white/10"
                header={<div className="h-full flex flex-col gap-2">
                    <div className="flex items-center gap-2 text-purple-400 font-mono text-xs uppercase tracking-widest">
                        <Users size={14} /> Swarm Status
                    </div>
                    <div className="grid grid-cols-2 gap-2 flex-1">
                        {pipeline.map(node => (
                            <div key={node.stage} className={`p-2 rounded border text-[10px] uppercase flex items-center justify-center ${node.status === 'active' ? 'bg-gold/10 border-gold text-gold' : 'bg-white/5 border-white/5 text-white/30'}`}>
                                {node.stage}
                            </div>
                        ))}
                    </div>
                </div>}
            />

        </BentoGrid>

        {/* Animated Beams (Visual Connections) */}
        <AnimatedBeam containerRef={containerRef} fromRef={perceptionRef} toRef={coreRef} curvature={-50} gradientStartColor="#00D4FF" gradientStopColor="#D4AF37" />
        <AnimatedBeam containerRef={containerRef} fromRef={coreRef} toRef={creationRef} curvature={50} gradientStartColor="#D4AF37" gradientStopColor="#FF3366" />

      </div>
    </div>
  );
}
