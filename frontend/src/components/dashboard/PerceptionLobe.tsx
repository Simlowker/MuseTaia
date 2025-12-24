"use client";

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { TrendReport, Signal } from '../../types/smos';
import { SMOSApi } from '../../services/api';
import { useSSE } from '../../hooks/use-sse';
import { Activity, TrendingUp, Zap } from 'lucide-react';

export function PerceptionLobe() {
    const [trends, setTrends] = useState<TrendReport[]>([]);
    const [signals, setSignals] = useState<Signal[]>([]);
    const { subscribe } = useSSE('http://localhost:8000/events/stream');

    useEffect(() => {
        SMOSApi.getTrends().then(setTrends).catch(console.error);
        SMOSApi.getActiveSignals().then(setSignals).catch(console.error);

        const unsubTrend = subscribe('TREND_DETECTED', (payload: TrendReport) => {
            setTrends(prev => [payload, ...prev].slice(0, 5));
        });

        const unsubSignal = subscribe('SIGNAL_RECEIVED', (payload: Signal) => {
            setSignals(prev => [payload, ...prev].slice(0, 10));
        });

        return () => {
            unsubTrend();
            unsubSignal();
        };
    }, [subscribe]);

    return (
        <div className="flex flex-col h-full space-y-6">
            {/* Header */}
            <div className="flex items-center justify-between border-b border-glass-border pb-2">
                <h2 className="text-xs font-bold text-cyan uppercase tracking-widest flex items-center gap-2">
                    <Activity size={14} className="animate-pulse" />
                    Perception Lobe
                </h2>
                <span className="text-[10px] text-white/30 uppercase">Senses: Active</span>
            </div>

            {/* Trends Section */}
            <div className="space-y-4">
                <div className="flex items-center gap-2 text-[10px] font-bold text-white/40 uppercase">
                    <TrendingUp size={12} />
                    High ROI Trends
                </div>
                <div className="space-y-2">
                    <AnimatePresence mode="popLayout">
                        {trends.map((trend) => (
                            <motion.div
                                key={trend.topic}
                                layout
                                initial={{ opacity: 0, x: -20 }}
                                animate={{ opacity: 1, x: 0 }}
                                className="bg-glass-bg border border-glass-border p-3 rounded-lg hover:border-cyan/30 transition-colors group"
                            >
                                <div className="flex justify-between items-start mb-1">
                                    <span className="text-sm font-bold text-white/90 group-hover:text-cyan transition-colors">#{trend.topic}</span>
                                    <span className="text-[10px] px-1.5 py-0.5 rounded bg-cyan/10 text-cyan border border-cyan/20">
                                        VVS: {trend.vvs.toFixed(1)}
                                    </span>
                                </div>
                                <div className="flex justify-between items-center">
                                    <span className="text-[10px] text-white/40 uppercase">{trend.platform}</span>
                                    <div className="w-24 h-1 bg-white/5 rounded-full overflow-hidden">
                                        <motion.div 
                                            initial={{ width: 0 }}
                                            animate={{ width: `${Math.min(trend.vvs, 100)}%` }}
                                            className="h-full bg-cyan"
                                        />
                                    </div>
                                </div>
                            </motion.div>
                        ))}
                    </AnimatePresence>
                </div>
            </div>

            {/* Signals Queue */}
            <div className="flex-1 space-y-4 overflow-hidden">
                 <div className="flex items-center gap-2 text-[10px] font-bold text-white/40 uppercase">
                    <Zap size={12} />
                    Signal Queue
                </div>
                <div className="space-y-1 h-full overflow-y-auto no-scrollbar mask-image-gradient-b">
                    {signals.map((signal) => (
                        <div key={signal.id} className="text-[10px] py-1 border-l border-white/5 pl-2 text-white/60 hover:text-white/90 transition-colors">
                            <span className="text-white/30 mr-2">[{signal.source}]</span>
                            {signal.content.substring(0, 40)}...
                        </div>
                    ))}
                    {signals.length === 0 && (
                        <div className="text-[10px] italic text-white/20">Awaiting raw signals...</div>
                    )}
                </div>
            </div>
        </div>
    );
}
