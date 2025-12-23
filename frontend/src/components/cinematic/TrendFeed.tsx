"use client";

import React from 'react';
import { motion } from 'framer-motion';
import { GlassPanel } from '@/components/ui/GlassPanel';
import { useTrends } from '@/context/TrendContext';

export const TrendFeed: React.FC = () => {
    const { trends, loading } = useTrends();

    return (
        <GlassPanel className="h-full flex flex-col p-4 gap-4 bg-black/40 backdrop-blur-xl border-white/5">
            <div className="flex justify-between items-center mb-2">
                <h3 className="text-[10px] uppercase font-bold text-white/50 tracking-widest">Niche Trends Feed</h3>
                <div className={`w-1 h-1 rounded-full animate-pulse ${loading ? 'bg-amber-500' : 'bg-green-500'}`} />
            </div>

            <div className="space-y-4 overflow-y-auto no-scrollbar mask-image-gradient-b">
                {trends.map((trend, i) => (
                    <motion.div
                        key={trend.id}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: i * 0.2 }}
                        className="rounded-xl overflow-hidden group cursor-pointer border border-white/5 hover:border-gold/30 transition-colors"
                    >
                        <div className={`h-32 w-full ${trend.imageUrl || 'bg-neutral-800'} relative bg-cover bg-center`}>
                            {/* Overlay */}
                            <div className="absolute inset-0 bg-gradient-to-t from-black/90 via-black/20 to-transparent p-3 flex flex-col justify-end">
                                <span className="text-[9px] text-gold/80 uppercase tracking-widest mb-1">{trend.category}</span>
                                <span className="text-xs font-bold text-white/90 leading-tight">{trend.title}</span>
                            </div>

                            {/* Score Badge */}
                            <div className="absolute top-2 right-2 px-2 py-1 bg-black/50 backdrop-blur-md rounded border border-white/10">
                                <span className="text-[8px] font-mono text-white/70">{trend.score}%</span>
                            </div>
                        </div>
                    </motion.div>
                ))}

                {loading && <div className="text-[9px] text-white/30 text-center animate-pulse">Syncing Global Streams...</div>}
            </div>
        </GlassPanel>
    );
};
