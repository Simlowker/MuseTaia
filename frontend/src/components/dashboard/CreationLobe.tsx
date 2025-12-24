"use client";

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Production } from '../../types/smos';
import { SMOSApi } from '../../services/api';
import { useSSE } from '../../hooks/use-sse';
import { Palette, Play, CheckCircle2, Loader2, DollarSign } from 'lucide-react';

export function CreationLobe() {
    const [productions, setProductions] = useState<Production[]>([]);
    const { subscribe } = useSSE('http://localhost:8000/events/stream');

    useEffect(() => {
        SMOSApi.getActiveProductions().then(setProductions).catch(console.error);

        const unsub = subscribe('PRODUCTION_UPDATE', (payload: Production) => {
            setProductions(prev => {
                const index = prev.findIndex(p => p.id === payload.id);
                if (index >= 0) {
                    const next = [...prev];
                    next[index] = payload;
                    return next;
                }
                return [payload, ...prev].slice(0, 3);
            });
        });

        return unsub;
    }, [subscribe]);

    const getStatusIcon = (status: Production['status']) => {
        switch(status) {
            case 'rendering': return <Loader2 size={14} className="animate-spin text-ruby" />;
            case 'published': return <CheckCircle2 size={14} className="text-emerald" />;
            default: return <Palette size={14} className="text-gold" />;
        }
    };

    return (
        <div className="flex flex-col h-full space-y-6">
            {/* Header */}
            <div className="flex items-center justify-between border-b border-glass-border pb-2">
                <h2 className="text-xs font-bold text-ruby uppercase tracking-widest flex items-center gap-2">
                    <Palette size={14} />
                    Creation Lobe
                </h2>
                <span className="text-[10px] text-white/30 uppercase">Studio: Active</span>
            </div>

            {/* Active Production List */}
            <div className="space-y-4">
                <AnimatePresence mode="popLayout">
                    {productions.map((prod) => (
                        <motion.div
                            key={prod.id}
                            initial={{ opacity: 0, scale: 0.95 }}
                            animate={{ opacity: 1, scale: 1 }}
                            className="bg-glass-bg border border-glass-border rounded-lg overflow-hidden group"
                        >
                            {/* Preview Window */}
                            <div className="aspect-video bg-void relative flex items-center justify-center overflow-hidden">
                                {prod.thumbnail_url ? (
                                    <img src={prod.thumbnail_url} alt={prod.title} className="w-full h-full object-cover opacity-50 group-hover:opacity-80 transition-opacity" />
                                ) : (
                                    <div className="absolute inset-0 bg-gradient-to-br from-ruby/5 to-gold/5 flex items-center justify-center">
                                        <Play size={32} className="text-white/10 group-hover:text-ruby/40 transition-colors" />
                                    </div>
                                )}
                                <div className="absolute bottom-2 left-2 flex gap-1">
                                    <span className="text-[8px] px-1.5 py-0.5 rounded bg-black/60 text-white/60 uppercase border border-white/10 backdrop-blur-md">
                                        ID: {prod.id.slice(0, 6)}
                                    </span>
                                </div>
                            </div>

                            {/* Info & Progress */}
                            <div className="p-3 space-y-3">
                                <div className="flex justify-between items-start">
                                    <h3 className="text-sm font-bold text-white/90 truncate pr-4">{prod.title}</h3>
                                    {getStatusIcon(prod.status)}
                                </div>

                                <div className="space-y-1">
                                    <div className="flex justify-between text-[10px] uppercase">
                                        <span className="text-white/40">{prod.status}</span>
                                        <span className="text-ruby font-bold">{prod.progress}%</span>
                                    </div>
                                    <div className="w-full h-1 bg-white/5 rounded-full overflow-hidden">
                                        <motion.div 
                                            initial={{ width: 0 }}
                                            animate={{ width: `${prod.progress}%` }}
                                            className="h-full bg-ruby"
                                        />
                                    </div>
                                </div>

                                <div className="flex justify-between items-center pt-1 border-t border-white/5">
                                    <div className="flex items-center gap-1 text-[10px] text-white/40">
                                        <DollarSign size={10} />
                                        EST. COST: <span className="text-emerald">$0.12</span>
                                    </div>
                                    {prod.eta_seconds && (
                                        <div className="text-[10px] text-white/30 uppercase">
                                            ETA: {Math.ceil(prod.eta_seconds / 60)}m
                                        </div>
                                    )}
                                </div>
                            </div>
                        </motion.div>
                    ))}
                </AnimatePresence>

                {productions.length === 0 && (
                    <div className="flex flex-col items-center justify-center py-12 border border-dashed border-glass-border rounded-lg text-white/10 space-y-2">
                        <Palette size={24} />
                        <span className="text-xs uppercase tracking-widest">Studio Idle</span>
                    </div>
                )}
            </div>
        </div>
    );
}
