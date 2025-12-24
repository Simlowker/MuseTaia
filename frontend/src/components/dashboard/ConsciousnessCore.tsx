"use client";

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useSystem } from '../../contexts/system-context';
import { useSSE } from '../../hooks/use-sse';

export function ConsciousnessCore() {
    const { mood } = useSystem();
    const [thoughts, setThoughts] = useState<{id: string, text: string}[]>([]);
    const { subscribe } = useSSE('http://localhost:8000/events/stream');

    useEffect(() => {
        const unsub = subscribe('THOUGHT_STREAM', (payload: {text: string}) => {
            const newThought = { id: Math.random().toString(36), text: payload.text };
            setThoughts(prev => [newThought, ...prev].slice(0, 3));
        });
        return unsub;
    }, [subscribe]);

    // Derived color based on mood
    const getMoodColor = () => {
        if (!mood) return 'var(--sovereign-gold)';
        if (mood.valence > 0.5) return 'var(--success-emerald)';
        if (mood.valence < -0.5) return 'var(--danger-ruby)';
        return 'var(--neural-cyan)';
    };

    return (
        <div className="flex flex-col items-center justify-center space-y-12">
            {/* MOOD RING & AVATAR */}
            <div className="relative group">
                {/* Outer Glow */}
                <motion.div 
                    animate={{ 
                        scale: [1, 1.05, 1],
                        opacity: [0.3, 0.6, 0.3]
                    }}
                    transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}
                    className="absolute inset-[-40px] rounded-full blur-3xl opacity-30"
                    style={{ backgroundColor: getMoodColor() }}
                />

                {/* Rotating Rings */}
                <motion.div 
                    animate={{ rotate: 360 }}
                    transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
                    className="absolute inset-[-20px] border border-gold/20 rounded-full border-dashed"
                />
                
                {/* The "Brain" / Avatar */}
                <motion.div 
                    className="w-48 h-48 rounded-full bg-void border-2 border-glass-border flex items-center justify-center relative z-10 overflow-hidden"
                    whileHover={{ scale: 1.02 }}
                >
                    <div className="absolute inset-0 bg-gradient-to-tr from-gold/10 via-transparent to-cyan/10" />
                    <motion.div 
                        animate={{ 
                            borderRadius: ["40% 60% 70% 30% / 40% 50% 60% 50%", "30% 60% 70% 40% / 50% 60% 30% 60%", "40% 60% 70% 30% / 40% 50% 60% 50%"]
                        }}
                        transition={{ duration: 10, repeat: Infinity, ease: "easeInOut" }}
                        className="w-32 h-32 bg-gold/20 backdrop-blur-xl border border-gold/30"
                    />
                    <div className="absolute text-gold text-[10px] tracking-[0.2em] font-bold uppercase opacity-50">
                        {mood?.current_state || 'STABLE'}
                    </div>
                </motion.div>
            </div>

            {/* THOUGHT STREAM */}
            <div className="w-full max-w-md h-32 flex flex-col items-center justify-start space-y-4 overflow-hidden">
                <AnimatePresence mode="popLayout">
                    {thoughts.length > 0 ? thoughts.map((t, i) => (
                        <motion.div
                            key={t.id}
                            initial={{ opacity: 0, y: 20, scale: 0.9 }}
                            animate={{ opacity: 1 - i * 0.3, y: 0, scale: 1 - i * 0.05 }}
                            exit={{ opacity: 0, scale: 0.8 }}
                            className="text-white/80 text-center text-sm font-light italic bg-glass-bg px-4 py-2 rounded-full border border-glass-border backdrop-blur-sm"
                        >
                            "{t.text}"
                        </motion.div>
                    )) : (
                         <div className="text-white/20 text-xs italic tracking-widest animate-pulse">
                            CONSCIOUSNESS STREAM IDLE
                         </div>
                    )}
                </AnimatePresence>
            </div>
        </div>
    );
}
