"use client";

import React, { useEffect, useState } from 'react';
import NeuralWaveform from '@/components/NeuralWaveform';
import { GlassPanel } from '@/components/ui/GlassPanel';
import { useNeural } from '@/context/NeuralContext';
import { motion, AnimatePresence } from 'framer-motion';

export const ActiveThought: React.FC = () => {
    const { lastEvent } = useNeural();
    const [displayMessage, setDisplayMessage] = useState("Awaiting neural input...");

    useEffect(() => {
        if (lastEvent?.message) {
            setDisplayMessage(lastEvent.message);
        }
    }, [lastEvent]);

    return (
        <GlassPanel className="w-full flex items-center justify-between px-8 py-6 bg-black/60 backdrop-blur-2xl border-t border-white/10 rounded-t-[3rem] rounded-b-none">
            <div className="flex flex-col gap-1">
                <span className="text-[9px] uppercase font-bold text-white/40 tracking-widest">Active Thought</span>
                <AnimatePresence mode='wait'>
                    <motion.p
                        key={displayMessage}
                        initial={{ opacity: 0, y: 5 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -5 }}
                        className="text-sm font-light text-white/80 w-64 leading-tight truncate"
                    >
                        {displayMessage}
                    </motion.p>
                </AnimatePresence>
            </div>

            <div className="flex-1 px-12 h-16 flex items-center justify-center">
                <NeuralWaveform />
            </div>

            <div className="w-64 flex justify-end gap-4">
                <button className="px-6 py-2 rounded-full border border-gold/20 text-[10px] font-bold text-gold hover:bg-gold/10 transition-colors uppercase tracking-widest">Retry</button>
                <button className="px-6 py-2 rounded-full bg-gold text-black text-[10px] font-bold hover:bg-white transition-colors uppercase tracking-widest shadow-[0_0_15px_rgba(212,175,55,0.3)]">Approve</button>
            </div>
        </GlassPanel>
    );
};
