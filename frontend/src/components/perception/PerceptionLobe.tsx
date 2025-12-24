"use client";

import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useSystem } from '../../contexts/system-context';
import { Activity, TrendingUp, Radio, CheckCircle } from 'lucide-react';

export function PerceptionLobe() {
    const { trends } = useSystem();
    
    const scanStatus = {
        last: '2 min ago',
        next: '58 min',
        state: 'idle'
    };

    const getPlatformBadge = (platform: string) => {
        const colors: Record<string, string> = {
            'tiktok': 'bg-[#ff0050]/10 text-[#ff0050] border-[#ff0050]/20',
            'reddit': 'bg-[#ff4500]/10 text-[#ff4500] border-[#ff4500]/20',
            'twitter': 'bg-[#1da1f2]/10 text-[#1da1f2] border-[#1da1f2]/20',
            'instagram': 'bg-[#e1306c]/10 text-[#e1306c] border-[#e1306c]/20',
            'default': 'bg-white/10 text-white/60 border-white/20'
        };
        const safePlatform = platform ? platform.toLowerCase() : 'unknown';
        const style = colors[safePlatform] || colors['default'];
        return (
            <span className={`text-[9px] px-1.5 py-0.5 rounded border uppercase tracking-wider ${style}`}>
                {platform || 'UNKNOWN'}
            </span>
        );
    };

    return (
        <div className="flex flex-col h-full space-y-6">
             {/* Header with Scan Status */}
            <div className="flex items-center justify-between border-b border-glass-border pb-4">
                <div className="flex flex-col">
                    <h2 className="text-xs font-bold text-cyan uppercase tracking-widest flex items-center gap-2">
                        <Radio size={14} />
                        Perception Lobe
                    </h2>
                    <div className="text-[9px] text-white/30 mt-1 flex gap-2">
                        <span>LAST SCAN: <span className="text-white/60">{scanStatus.last}</span></span>
                        <span>NEXT: <span className="text-white/60">{scanStatus.next}</span></span>
                    </div>
                </div>
                <div className={`w-2 h-2 rounded-full ${scanStatus.state === 'scanning' ? 'bg-cyan animate-pulse shadow-[0_0_8px_var(--neural-cyan)]' : 'bg-white/10'}`} />
            </div>

            {/* Trends List */}
            <div className="space-y-3 overflow-y-auto no-scrollbar pr-2">
                <div className="flex items-center gap-2 text-[10px] font-bold text-white/40 uppercase mb-2">
                    <TrendingUp size={12} />
                    Active Signals
                </div>
                
                <AnimatePresence mode="popLayout">
                    {trends.map((trend) => (
                        <motion.div
                            key={trend.id}
                            layout
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            className="bg-glass-bg border border-glass-border p-3 rounded-lg group hover:border-cyan/30 transition-all"
                        >
                            <div className="flex justify-between items-start mb-2">
                                <span className="text-sm font-bold text-white/90 group-hover:text-cyan transition-colors">
                                    {trend.title}
                                </span>
                                {getPlatformBadge(trend.platform)}
                            </div>

                            <div className="grid grid-cols-2 gap-2 text-[10px] text-white/40">
                                <div>
                                    <div className="uppercase tracking-wider mb-0.5">VVS Score</div>
                                    <div className="text-cyan font-mono text-xs">{trend.vvs_score.toFixed(1)}</div>
                                </div>
                                <div>
                                    <div className="uppercase tracking-wider mb-0.5">Status</div>
                                    <div className={`flex items-center gap-1 ${trend.status === 'approved' ? 'text-emerald' : 'text-gold'}`}>
                                        <CheckCircle size={10} />
                                        {trend.status.toUpperCase()}
                                    </div>
                                </div>
                            </div>
                            
                            {/* VVS Bar */}
                            <div className="mt-2 w-full h-1 bg-white/5 rounded-full overflow-hidden">
                                <motion.div 
                                    initial={{ width: 0 }}
                                    animate={{ width: `${Math.min(trend.vvs_score, 100)}%` }}
                                    className="h-full bg-cyan"
                                />
                            </div>
                        </motion.div>
                    ))}
                </AnimatePresence>

                {trends.length === 0 && (
                    <div className="text-center py-8 text-white/20 text-xs italic border border-dashed border-white/10 rounded-lg">
                        No active signals detected.
                    </div>
                )}
            </div>
        </div>
    );
}