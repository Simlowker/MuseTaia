"use client";

import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useSystem } from '../../contexts/system-context';
import { ArrowRight, ShieldCheck, Brain, Zap, Search, Users } from 'lucide-react';

export function DecisionPipeline() {
    const { pipeline } = useSystem();

    const stages = [
        { key: 'PERCEPTION', label: 'TREND', icon: Search },
        { key: 'STRATEGIST', label: 'STRATEGIST', icon: Brain },
        { key: 'CFO GATE', label: 'CFO GATE', icon: ShieldCheck },
        { key: 'HLP', label: 'HLP', icon: Zap },
        { key: 'SWARM', label: 'SWARM', icon: Users },
    ];

    return (
        <div className="w-full max-w-3xl">
            {/* Connection Line */}
            <div className="relative">
                <div className="absolute top-1/2 left-0 right-0 h-[2px] bg-white/5 -z-10" />
                
                <div className="flex justify-between items-center">
                    {stages.map((stage, i) => {
                        const nodeData = pipeline.find(p => p.stage === stage.key);
                        const isActive = nodeData?.status === 'active';
                        const isComplete = nodeData?.status === 'complete';
                        
                        return (
                            <div key={stage.key} className="flex flex-col items-center gap-3 bg-void px-2">
                                <motion.div
                                    animate={isActive ? { 
                                        scale: [1, 1.1, 1],
                                        boxShadow: ["0 0 0px #D4AF37", "0 0 20px #D4AF37", "0 0 0px #D4AF37"]
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
            <div className="mt-8 text-center min-h-[20px]">
                 <AnimatePresence mode="wait">
                    {pipeline.find(p => p.status === 'active')?.message ? (
                        <motion.div
                            key={pipeline.find(p => p.status === 'active')?.stage}
                            initial={{ opacity: 0, y: 5 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: -5 }}
                            className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full border border-gold/20 bg-gold/5 text-gold text-[10px] uppercase tracking-widest"
                        >
                            <span className="w-1.5 h-1.5 rounded-full bg-gold animate-pulse" />
                            {pipeline.find(p => p.status === 'active')?.message}
                        </motion.div>
                    ) : (
                        <div className="text-white/20 text-[10px] uppercase tracking-widest">System Idle</div>
                    )}
                 </AnimatePresence>
            </div>
        </div>
    );
}