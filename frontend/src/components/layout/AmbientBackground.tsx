"use client";

import React from 'react';
import { motion } from 'framer-motion';
import { useMood } from '@/context/MoodContext';

export const AmbientBackground = () => {
    const { rawMood, mood } = useMood();

    // Default safe values if rawMood is null
    const valence = rawMood?.valence ?? 0;
    const arousal = rawMood?.arousal ?? 0;

    // Map mood to colors/gradients
    // High Valence (Positive) -> Gold/Warm
    // Low Valence (Negative) -> icy blue/cold
    // High Arousal -> Faster movement, sharper contrast
    // Low Arousal -> Slow, blurred

    const getGradient = () => {
        if (mood === 'authority') return 'radial-gradient(circle at 50% 50%, rgba(212, 175, 55, 0.15), transparent 60%)'; // Gold
        if (mood === 'reflection') return 'radial-gradient(circle at 50% 50%, rgba(20, 40, 60, 0.2), transparent 70%)'; // Deep Blue
        return 'radial-gradient(circle at 50% 50%, rgba(255, 255, 255, 0.05), transparent 60%)'; // Neutral
    };

    return (
        <div className="fixed inset-0 z-[-1] overflow-hidden pointer-events-none bg-black">
            {/* Deep Onyx Base Texture */}
            <div
                className="absolute inset-0 opacity-20"
                style={{
                    backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E")`,
                }}
            />

            {/* Arousal Pulse Layer */}
            <motion.div
                className="absolute inset-0"
                animate={{
                    background: getGradient(),
                    scale: [1, 1.1 + (arousal * 0.2), 1],
                    opacity: [0.5, 0.8, 0.5],
                }}
                transition={{
                    duration: 10 - (arousal * 8), // High arousal = fast duration
                    repeat: Infinity,
                    ease: "easeInOut"
                }}
            />

            {/* Valence Shift Layer (Color Tint) */}
            <motion.div
                className="absolute inset-0 mix-blend-overlay"
                animate={{
                    backgroundColor: valence > 0.5 ? 'rgba(212, 175, 55, 0.1)' : 'rgba(0, 20, 40, 0.2)'
                }}
                transition={{ duration: 2 }}
            />
        </div>
    );
};
