"use client";

import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
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
        { key: 'trend', label: 'Perception', icon: Search },
        { key: 'strategist', label: 'Strategist', icon: Brain },
        { key: 'cfo', label: 'CFO Gate', icon: ShieldCheck },
        { key: 'hlp', label: 'Planning', icon: Zap },
        { key: 'swarm', label: 'Execution', icon: Users },
    ];

    return (
        <div className="w-full max-w-4xl bg-glass-bg border border-glass-border rounded-xl p-4 backdrop-blur-md">
            <div className="flex items-center justify-between">
                {stages.map((stage, i) => {
                    const isActive = pipeline?.active_stage === stage.key;
                    const isComplete = pipeline?.gates[stage.key as keyof PipelineState['gates']];
                    
                    return (
                        <React.Fragment key={stage.key}>
                            <div className="flex flex-col items-center gap-2 flex-1">
                                <motion.div
                                    animate={isActive ? { 
                                        scale: [1, 1.1, 1],
                                        boxShadow: ["0 0 0px var(--sovereign-gold)", "0 0 15px var(--sovereign-gold)", "0 0 0px var(--sovereign-gold)"]
                                    } : {}}
                                    transition={{ duration: 2, repeat: Infinity }}
                                    className={`w-12 h-12 rounded-full flex items-center justify-center border-2 transition-colors ${
                                        isActive ? 'border-gold bg-gold/10' : 
                                        isComplete ? 'border-emerald bg-emerald/10' : 
                                        'border-white/10 bg-white/5'
                                    }`}
                                >
                                    <stage.icon size={20} className={
                                        isActive ? 'text-gold' : 
                                        isComplete ? 'text-emerald' : 
                                        'text-white/20'
                                    } />
                                </motion.div>
                                <span className={`text-[10px] uppercase font-bold tracking-tighter ${
                                    isActive ? 'text-gold' : 
                                    isComplete ? 'text-emerald' : 
                                    'text-white/20'
                                }`}>
                                    {stage.label}
                                </span>
                            </div>
                            {i < stages.length - 1 && (
                                <div className="flex items-center justify-center text-white/10">
                                    <ArrowRight size={14} />
                                </div>
                            )}
                        </React.Fragment>
                    );
                })}
            </div>

            {/* Current Context Message */}
            <div className="mt-4 border-t border-white/5 pt-2 flex items-center justify-center">
                 <div className="text-[10px] text-white/40 uppercase tracking-widest flex items-center gap-2">
                    <span className="w-1 h-1 bg-gold rounded-full animate-ping"></span>
                    Current Context: <span className="text-white/80 font-bold">{pipeline?.active_stage || 'IDLE'}</span>
                 </div>
            </div>
        </div>
    );
}
