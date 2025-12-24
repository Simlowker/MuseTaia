"use client";

import React from 'react';
import { motion } from 'framer-motion';
import { useSystem } from '../../contexts/system-context';

export function MoodAura() {
    const { mood } = useSystem();

    const getMoodColor = () => {
        if (!mood) return 'rgba(212, 175, 55, 0.05)'; // Gold default
        if (mood.valence > 0.5) return 'rgba(0, 255, 136, 0.08)'; // Emerald
        if (mood.valence < -0.5) return 'rgba(255, 51, 102, 0.08)'; // Ruby
        if (mood.arousal > 0.7) return 'rgba(0, 212, 255, 0.08)'; // Cyan
        return 'rgba(212, 175, 55, 0.05)';
    };

    return (
        <motion.div 
            animate={{ 
                opacity: [0.4, 0.7, 0.4],
                scale: [1, 1.1, 1]
            }}
            transition={{ duration: 8, repeat: Infinity, ease: "easeInOut" }}
            className="absolute inset-0 pointer-events-none z-0"
            style={{ 
                background: `radial-gradient(circle at center, ${getMoodColor()} 0%, transparent 70%)` 
            }}
        />
    );
}
