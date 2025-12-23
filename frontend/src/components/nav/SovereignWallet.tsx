"use client";

import React from 'react';
import { motion } from 'framer-motion';
import { Zap } from 'lucide-react';
import { GlassPanel } from '@/components/ui/GlassPanel';

export const SovereignWallet: React.FC = () => {
    return (
        <GlassPanel className="h-full">
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
        </GlassPanel>
    );
};
