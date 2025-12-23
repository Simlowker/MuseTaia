"use client";

import React from 'react';
import { motion } from 'framer-motion';

interface GenesisRingProps {
    score: number; // 0-100
    size?: number;
    showLabel?: boolean;
}

export const GenesisRing: React.FC<GenesisRingProps> = ({ score, size = 120, showLabel = true }) => {
    // Logic for Drift: If score < 95, considered drifting for visual impact
    const isDrifting = score < 95;
    const color = isDrifting ? '#FFBF00' : '#D4AF37'; // Amber vs Gold

    const circumference = 2 * Math.PI * 45; // r=45
    const strokeDashoffset = circumference - (score / 100) * circumference;

    return (
        <div className="relative flex flex-col items-center justify-center" style={{ width: size, height: size }}>
            {/* Outer Rotating Rim (Horlogerie effect) */}
            <motion.div
                className="absolute inset-0 rounded-full border border-dashed border-white/10"
                animate={{ rotate: 360 }}
                transition={{ duration: 60, repeat: Infinity, ease: "linear" }}
            />

            {/* Counter-Rotating Fine Rim */}
            <motion.div
                className="absolute inset-2 rounded-full border border-dotted border-white/5"
                animate={{ rotate: -360 }}
                transition={{ duration: 40, repeat: Infinity, ease: "linear" }}
            />

            {/* Main Fidelity SVG Ring */}
            <svg width="100%" height="100%" viewBox="0 0 100 100" className="rotate-[-90deg]">
                {/* Background Ring */}
                <circle
                    cx="50"
                    cy="50"
                    r="45"
                    stroke="rgba(255, 255, 255, 0.05)"
                    strokeWidth="2"
                    fill="none"
                />

                {/* Progress Ring */}
                <motion.circle
                    cx="50"
                    cy="50"
                    r="45"
                    stroke={color}
                    strokeWidth="2"
                    fill="none"
                    strokeDasharray={circumference}
                    animate={{ strokeDashoffset }}
                    transition={{ duration: 1 }}
                    style={{ filter: `drop-shadow(0 0 5px ${color})` }}
                />
            </svg>

            {/* Drifting Pulse Effect */}
            {isDrifting && (
                <motion.div
                    className="absolute inset-0 rounded-full border-2 border-amber-500/30"
                    animate={{ opacity: [0, 1, 0], scale: [1, 1.1, 1] }}
                    transition={{ duration: 2, repeat: Infinity }}
                />
            )}

            {/* Center Content */}
            <div className="absolute inset-0 flex flex-col items-center justify-center">
                {/* Placeholder Scan Face/Icon */}
                <div className="w-16 h-16 rounded-full bg-black flex items-center justify-center border border-white/5 relative overflow-hidden">
                    {/* Scan line overlay */}
                    <motion.div
                        className="absolute w-full h-[1px] bg-white/50 shadow-[0_0_5px_white]"
                        animate={{ top: ['0%', '100%'] }}
                        transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
                    />
                    <span className="text-[10px] text-white/30 font-bold">MUSE</span>
                </div>
            </div>

            {/* Optional Floating Score */}
            {showLabel && (
                <div className="absolute -bottom-8 flex flex-col items-center">
                    <span className="text-[10px] uppercase tracking-[0.2em] text-white/40">Fidelity</span>
                    <span
                        className="text-lg font-bold"
                        style={{ color: color, textShadow: `0 0 10px ${color}` }}
                    >
                        {score}%
                    </span>
                </div>
            )}
        </div>
    );
};
