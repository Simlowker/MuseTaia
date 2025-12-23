"use client";

import React, { useMemo } from 'react';
import { motion } from 'framer-motion';
import { useMood } from '@/context/MoodContext';

export const CentralAvatar: React.FC = () => {
    const { rawMood } = useMood();

    // Derived visual properties based on mood
    // Valence (Happiness/Positivity): 0 (Blue/Cold) -> 1 (Gold/Warm)
    // Arousal (Energy): 0 (Slow Pulse) -> 1 (Fast Pulse, Sharp Glitch)

    const valence = rawMood?.valence || 0.5;
    const arousal = rawMood?.arousal || 0.5;

    const coreColor = useMemo(() => {
        if (valence > 0.6) return 'rgba(212, 175, 55, 0.4)'; // Gold
        if (valence < 0.4) return 'rgba(0, 100, 255, 0.4)';  // Blue
        return 'rgba(255, 255, 255, 0.3)';                   // Neutral
    }, [valence]);

    const pulseDuration = useMemo(() => {
        // High arousal = fast pulse (0.5s), Low arousal = slow breathing (4s)
        return 4 - (arousal * 3.5);
    }, [arousal]);

    return (
        <div className="absolute inset-0 flex items-center justify-center z-0 pointer-events-none">
            <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 2 }}
                className="w-full h-full flex items-center justify-center pb-20"
            >
                {/* Dynamic Aura */}
                <motion.div
                    animate={{
                        scale: [1, 1.05 + (arousal * 0.1), 1],
                        opacity: [0.3, 0.5 + (arousal * 0.2), 0.3]
                    }}
                    transition={{ duration: pulseDuration, repeat: Infinity, ease: "easeInOut" }}
                    className="w-[800px] h-[800px] rounded-full blur-3xl"
                    style={{
                        background: `radial-gradient(circle, ${coreColor} 0%, transparent 70%)`
                    }}
                />

                {/* Core Avatar Placeholder */}
                <div className="absolute w-[40vh] h-[40vh] bg-black/80 rounded-full border border-white/10 flex items-center justify-center overflow-hidden shadow-2xl backdrop-blur-sm">
                    <span className="text-white/20 font-luxe text-xs tracking-widest animate-pulse">
                        AVATAR::SYNCING
                    </span>

                    {/* Inner Glitch Ring */}
                    <motion.div
                        animate={{ rotate: 360 }}
                        transition={{ duration: 20 / (arousal + 0.1), repeat: Infinity, ease: "linear" }}
                        className="absolute inset-4 border border-dashed border-white/10 rounded-full opacity-50"
                    />
                </div>
            </motion.div>
        </div>
    );
};
