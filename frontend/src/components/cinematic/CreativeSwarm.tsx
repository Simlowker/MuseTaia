"use client";

import React from 'react';
import { GlassPanel } from '@/components/ui/GlassPanel';
import { NeuralSwarm } from '@/components/viz/NeuralSwarm';
import SwarmStatus from '@/components/SwarmStatus';

export const CreativeSwarm: React.FC = () => {
    return (
        <GlassPanel className="h-full flex flex-col gap-6 p-6 bg-black/40 backdrop-blur-xl border-white/5">
            <div className="flex justify-between items-start">
                <div>
                    <h3 className="text-[10px] uppercase font-bold text-white/50 tracking-widest mb-1">Creative Swarm</h3>
                    <h2 className="text-sm font-bold text-white">VisualAgent [Organic Cotton]</h2>
                </div>
                <div className="px-2 py-1 rounded bg-white/5 border border-white/10 text-[9px] text-white/60">
                    STATUS: REFINING (90%)
                </div>
            </div>

            <div className="flex-1 bg-black/20 rounded-xl overflow-hidden relative border border-white/5">
                {/* Media Preview / Swarm Viz */}
                <SwarmStatus />
                <div className="absolute bottom-4 left-4 right-4 h-1 bg-white/10 rounded-full overflow-hidden">
                    <div className="h-full bg-gold w-[90%]" />
                </div>
            </div>

            <div className="h-1/3 flex flex-col gap-2">
                <span className="text-[9px] uppercase font-bold text-white/30 tracking-widest">Media Preview</span>
                <div className="flex-1 bg-white/5 rounded-lg border border-white/5 flex items-center justify-center">
                    <span className="text-xs text-white/20 italic">Generating Preview...</span>
                </div>
            </div>
        </GlassPanel>
    );
};
