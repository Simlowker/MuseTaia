"use client";

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { PipelineState } from '../../types/smos';
import { SMOSApi } from '../../services/api';
import { useSSE } from '../../hooks/use-sse';
import { ArrowRight, ShieldCheck, Brain, Zap, Search, Users } from 'lucide-react';

export function DecisionPipeline() {
    const [pipeline, setPipeline] = useState<PipelineState | null>(null);
    const { subscribe } = useSSE('http://localhost:8000/events/stream');

    useEffect(() => {
        SMOSApi.getPipeline().then(setPipeline).catch(console.error);

        const unsub = subscribe('PIPELINE_UPDATE', (payload: PipelineState) => {
            setPipeline(payload);
        });

        return unsub;
    }, [subscribe]);

    const stages = [
        { key: 'trend', label: 'TREND', icon: Search },
        { key: 'strategist', label: 'STRATEGIST', icon: Brain },
        { key: 'cfo', label: 'CFO GATE', icon: ShieldCheck },
        { key: 'hlp', label: 'HLP', icon: Zap },
        { key: 'swarm', label: 'SWARM', icon: Users },
    ];

    return (
        <div className="w-full max-w-3xl">
            {/* Connection Line */}
            <div className="relative">
                <div className="absolute top-1/2 left-0 right-0 h-[2px] bg-white/5 -z-10" />
                
                <div className="flex justify-between items-center">
                    {stages.map((stage, i) => {
                        const isActive = pipeline?.active_stage === stage.key;
                        const isComplete = pipeline?.gates[stage.key as keyof PipelineState['gates']] || isActive; // Logic simplified for visual flow
                        
                        return (
                            <div key={stage.key} className="flex flex-col items-center gap-3 bg-void px-2">
                                <motion.div
                                    animate={isActive ? { 
                                        scale: [1, 1.1, 1],
                                        boxShadow: ["0 0 0px var(--sovereign-gold)", "0 0 20px var(--sovereign-gold)", "0 0 0px var(--sovereign-gold)"]
                                    } : {}}
                                    transition={{ duration: 2, repeat: Infinity }}
                                    className={`w-12 h-12 rounded-full flex items-center justify-center border-2 transition-colors relative z-10 ${
                                        isActive ? 'border-gold bg-gold/10 text-gold' : 
                                        isComplete ? 'border-emerald bg-emerald/10 text-emerald' : 
                                        'border-white/10 bg-onyx text-white/20'
                                    }`}
                                >
                                    <stage.icon size={20} />
                                    
                                    {/* Active Pulse Ring */}
                                    {isActive && (
                                        <motion.div 
                                            initial={{ scale: 1, opacity: 0.5 }}
                                            animate={{ scale: 2, opacity: 0 }}
                                            transition={{ duration: 1.5, repeat: Infinity }}
                                            className="absolute inset-0 rounded-full border border-gold"
                                        />
                                    )}
                                </motion.div>
                                
                                <span className={`text-[10px] font-bold tracking-widest ${
                                    isActive ? 'text-gold' : 
                                    isComplete ? 'text-emerald' : 
                                    'text-white/20'
                                }`}>
                                    {stage.label}
                                </span>
                            </div>
                        );
                    })}
                </div>
            </div>

            {/* Status Message */}
            <div className="mt-8 text-center">
                 <AnimatePresence mode="wait">
                    {pipeline?.active_stage ? (
                        <motion.div
                            key={pipeline.active_stage}
                            initial={{ opacity: 0, y: 5 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: -5 }}
                            className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full border border-gold/20 bg-gold/5 text-gold text-[10px] uppercase tracking-widest"
                        >
                            <span className="w-1.5 h-1.5 rounded-full bg-gold animate-pulse" />
                            Current Decision Node: {pipeline.active_stage}
                        </motion.div>
                    ) : (
                        <div className="text-white/20 text-[10px] uppercase tracking-widest">System Idle</div>
                    )}
                 </AnimatePresence>
            </div>
        </div>
    );
}
