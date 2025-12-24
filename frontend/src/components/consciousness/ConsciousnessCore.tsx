"use client";

import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useSystem } from '../../contexts/system-context';

export function ConsciousnessCore() {
    const { mood } = useSystem();

    // Derived color based on mood
    const getMoodColor = () => {
        if (!mood) return '#D4AF37'; // gold
        if (mood.valence > 0.5) return '#00FF88'; // emerald
        if (mood.valence < -0.5) return '#FF3366'; // ruby
        if (mood.arousal > 0.6) return '#00D4FF'; // cyan
        return '#D4AF37';
    };

    const moodColor = getMoodColor();

    return (
        <div className="flex flex-col items-center justify-center space-y-8 relative w-full max-w-md mx-auto">
            
            {/* THOUGHT BUBBLE */}
            <div className="h-24 flex items-center justify-center w-full">
                <AnimatePresence mode="wait">
                    {mood?.current_thought ? (
                        <motion.div
                            key={mood.current_thought}
                            initial={{ opacity: 0, y: 10, scale: 0.95 }}
                            animate={{ opacity: 1, y: 0, scale: 1 }}
                            exit={{ opacity: 0, y: -10, scale: 0.95 }}
                            className="relative bg-glass-bg border border-glass-border px-6 py-4 rounded-2xl max-w-sm text-center backdrop-blur-md"
                        >
                            <div className="text-white/90 text-sm font-light italic leading-relaxed">
                                "{mood.current_thought}"
                            </div>
                            {/* Speech Bubble Tail */}
                            <div className="absolute -bottom-2 left-1/2 transform -translate-x-1/2 w-4 h-4 bg-glass-bg border-r border-b border-glass-border rotate-45" />
                        </motion.div>
                    ) : (
                         <motion.div 
                            initial={{ opacity: 0 }} 
                            animate={{ opacity: 0.3 }}
                            className="text-white/20 text-xs tracking-widest uppercase"
                        >
                            ...Processing Stream...
                        </motion.div>
                    )}
                </AnimatePresence>
            </div>

            {/* AVATAR ORB */}
            <div className="relative w-64 h-64 flex items-center justify-center">
                {/* Pulse Aura */}
                <motion.div 
                    animate={{ 
                        scale: [1, 1.2, 1],
                        opacity: [0.2, 0.5, 0.2],
                    }}
                    transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}
                    className="absolute inset-0 rounded-full blur-3xl"
                    style={{ backgroundColor: moodColor }}
                />

                {/* Main Orb */}
                <div className="relative w-48 h-48 rounded-full border border-glass-border bg-black/50 backdrop-blur-sm overflow-hidden flex items-center justify-center z-10">
                     {/* Internal Fluid Animation (Simplified with gradients) */}
                     <motion.div 
                        animate={{ 
                            rotate: 360,
                            scale: [1, 1.1, 1]
                        }}
                        transition={{ duration: 15, repeat: Infinity, ease: "linear" }}
                        className="absolute inset-[-50%]"
                        style={{
                            background: `conic-gradient(from 0deg, transparent 0%, ${moodColor} 20%, transparent 40%, ${moodColor} 60%, transparent 100%)`,
                            opacity: 0.3
                        }}
                     />
                     <div className="absolute inset-2 rounded-full bg-void border border-white/5 z-20 flex items-center justify-center">
                        <span className="text-[10px] tracking-[0.3em] font-bold text-white/50 uppercase">
                            {mood?.current_state || 'IDLE'}
                        </span>
                     </div>
                </div>
            </div>

            {/* MOOD BARS */}
            <div className="w-full space-y-3 px-8">
                <MoodBar label="Valence" value={mood?.valence || 0} color="#00FF88" negColor="#FF3366" />
                <MoodBar label="Arousal" value={mood?.arousal || 0} color="#00D4FF" />
                <MoodBar label="Dominance" value={mood?.dominance || 0} color="#D4AF37" />
            </div>
        </div>
    );
}

function MoodBar({ label, value, color, negColor }: { label: string, value: number, color: string, negColor?: string }) {
    // Value is -1 to 1
    const normalized = (value + 1) / 2 * 100; // 0 to 100
    const barColor = (negColor && value < 0) ? negColor : color;

    return (
        <div className="flex items-center gap-4 text-[10px] uppercase tracking-wider text-white/40">
            <span className="w-16 text-right">{label}</span>
            <div className="flex-1 h-1 bg-white/5 rounded-full overflow-hidden relative">
                <motion.div 
                    initial={{ width: "50%" }}
                    animate={{ width: `${normalized}%` }}
                    className="h-full absolute left-0 top-0 transition-all duration-500"
                    style={{ backgroundColor: barColor }}
                />
                {/* Center marker */}
                <div className="absolute left-1/2 top-0 bottom-0 w-[1px] bg-white/10" />
            </div>
            <span className="w-8 text-right font-mono text-white/60">{value.toFixed(2)}</span>
        </div>
    );
}