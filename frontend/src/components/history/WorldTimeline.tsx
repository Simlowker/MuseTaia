"use client";

import React, { useRef, useState } from 'react';
import { motion } from 'framer-motion';

const WORLD_STATES = [
    { id: 'genesis', label: 'GENESIS: VOID', date: '2024.01' },
    { id: 'epoch1', label: 'EPOCH I: FIRST LIGHT', date: '2024.03' },
    { id: 'epoch2', label: 'EPOCH II: NEURAL BLOOM', date: '2024.06' },
    { id: 'epoch3', label: 'EPOCH III: SWARM AWAKENING', date: '2024.09' },
    { id: 'present', label: 'CURRENT: EXOSKELETON', date: '2025.12' },
];

export const WorldTimeline = () => {
    const [selected, setSelected] = useState('present');
    const scrollRef = useRef(null);

    return (
        <div className="w-full h-32 relative overflow-hidden bg-gradient-to-t from-black to-transparent border-t border-[var(--glass-border)]">
            <div className="absolute inset-x-0 bottom-0 h-10 bg-[var(--deep-onyx)]/80 blur-xl z-0" />

            {/* Analog Ruler Ticks */}
            <div className="absolute top-0 left-0 w-full h-4 flex justify-between px-10 opacity-30">
                {[...Array(50)].map((_, i) => (
                    <div key={i} className={`w-[1px] h-full ${i % 5 === 0 ? 'bg-gold h-4' : 'bg-white/20 h-2'}`} />
                ))}
            </div>

            {/* Timeline Items */}
            <div className="flex items-end gap-20 px-20 pb-8 overflow-x-auto no-scrollbar h-full relative z-10 snap-x">
                {WORLD_STATES.map((state, index) => {
                    const isSelected = selected === state.id;
                    return (
                        <motion.div
                            key={state.id}
                            onClick={() => setSelected(state.id)}
                            className={`flex flex-col items-center cursor-pointer min-w-[200px] snap-center transition-all duration-500 group ${isSelected ? 'opacity-100 scale-105' : 'opacity-30 hover:opacity-100'}`}
                        >
                            <div className="flex flex-col items-center gap-2 mb-2">
                                <span className="text-[8px] font-mono tracking-widest text-gold opacity-80">{state.date}</span>
                                <div className={`w-2 h-2 rounded-full ${isSelected ? 'bg-gold shadow-[0_0_10px_#D4AF37]' : 'bg-white/20'}`} />
                                <div className={`w-[1px] h-8 ${isSelected ? 'bg-gold' : 'bg-white/10'}`} />
                            </div>
                            <h3 className={`text-[10px] font-bold uppercase tracking-[0.2em] ${isSelected ? 'text-white' : 'text-neutral-500'}`}>
                                {state.label}
                            </h3>
                        </motion.div>
                    );
                })}
            </div>

            {/* Current Indicator "Needle" */}
            <div className="absolute bottom-0 left-1/2 -translate-x-1/2 w-[1px] h-12 bg-red-500/50 z-20 pointer-events-none mix-blend-screen" />
        </div>
    );
};
