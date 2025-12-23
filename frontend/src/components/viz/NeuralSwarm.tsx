"use client";

import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';

interface AgentStatus {
    name: string;
    status: string;
    progress: number;
    active: boolean;
}

interface NeuralSwarmProps {
    agents: AgentStatus[];
}

// Agent positions in a relative coordinate system (0-100%)
const POSITIONS = [
    { x: 50, y: 20 }, // Top (Narrative)
    { x: 80, y: 50 }, // Right (Visual)
    { x: 50, y: 80 }, // Bottom (Motion)
    { x: 20, y: 50 }, // Left (Critic)
];

const Particle = ({ cx, cy, color, speed, index }: { cx: number; cy: number; color: string; speed: number; index: number }) => {
    return (
        <motion.div
            className="absolute w-1 h-1 rounded-full"
            style={{
                backgroundColor: color,
                boxShadow: `0 0 4px ${color}`
            }}
            animate={{
                x: [cx - 10, cx + 10, cx - 10], // Random orbit roughly
                y: [cy - 10, cy + 10, cy - 10],
                opacity: [0.2, 1, 0.2],
                scale: [0.5, 1.2, 0.5]
            }}
            transition={{
                duration: speed,
                repeat: Infinity,
                ease: "linear",
                times: [0, 0.5, 1], // Keyframes
                delay: (index * 0.2) % 2
            }}
        />
    );
};

export const NeuralSwarm: React.FC<NeuralSwarmProps> = ({ agents }) => {
    const [activeConnections, setActiveConnections] = useState<number[][]>([]);

    // Simulate connections periodically for "A2A" visual
    useEffect(() => {
        const interval = setInterval(() => {
            // Randomly connect two active agents
            const activeIndices = agents.map((a, i) => a.active ? i : -1).filter(i => i !== -1);
            if (activeIndices.length >= 2) {
                const start = activeIndices[Math.floor(Math.random() * activeIndices.length)];
                const end = activeIndices[Math.floor(Math.random() * activeIndices.length)];
                if (start !== end) setActiveConnections([[start, end]]);
            } else {
                setActiveConnections([]);
            }
        }, 2000);
        return () => clearInterval(interval);
    }, [agents]);

    return (
        <div className="relative w-full h-64 bg-black/20 rounded-xl overflow-hidden custom-glass-inset">
            {/* Connections (Threads) */}
            <svg className="absolute inset-0 w-full h-full pointer-events-none">
                {activeConnections.map(([start, end], i) => {
                    const p1 = POSITIONS[start % POSITIONS.length];
                    const p2 = POSITIONS[end % POSITIONS.length];
                    return (
                        <motion.line
                            key={i}
                            x1={`${p1.x}%`}
                            y1={`${p1.y}%`}
                            x2={`${p2.x}%`}
                            y2={`${p2.y}%`}
                            stroke="rgba(212, 175, 55, 0.4)"
                            strokeWidth="1"
                            initial={{ pathLength: 0, opacity: 0 }}
                            animate={{ pathLength: 1, opacity: 1 }}
                            exit={{ opacity: 0 }}
                            transition={{ duration: 0.5 }}
                        />
                    );
                })}
            </svg>

            {/* Agents Nodes */}
            {agents.map((agent, i) => {
                const pos = POSITIONS[i % POSITIONS.length];
                const isActive = agent.active;
                const color = isActive ? '#D4AF37' : '#1A2B48'; // Gold vs Blue

                return (
                    <div
                        key={agent.name}
                        className="absolute -translate-x-1/2 -translate-y-1/2 flex flex-col items-center"
                        style={{ left: `${pos.x}%`, top: `${pos.y}%` }}
                    >
                        {/* Core */}
                        <motion.div
                            className="w-3 h-3 rounded-full z-10"
                            style={{ backgroundColor: color, boxShadow: `0 0 10px ${color}` }}
                            animate={{ scale: isActive ? [1, 1.2, 1] : 1 }}
                            transition={{ duration: 2, repeat: Infinity }}
                        />

                        {/* Label */}
                        <span className="mt-2 text-[10px] uppercase tracking-wider text-white/50 text-center w-20">
                            {agent.name}
                        </span>

                        {/* Particles (Swarm) */}
                        {isActive && [...Array(8)].map((_, j) => (
                            <Particle
                                key={j}
                                index={j}
                                cx={0} // Relative to parent
                                cy={0}
                                color={color}
                                speed={1 + (j * 0.1)}
                            />
                        ))}
                    </div>
                );
            })}

            {/* Central Muse/Goal Placeholder */}
            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-16 h-16 rounded-full border border-white/5 flex items-center justify-center">
                <div className="w-1 h-1 bg-white/20 rounded-full animate-pulse" />
            </div>

        </div>
    );
};
