"use client";

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Production } from '../../types/smos';
import { SMOSApi } from '../../services/api';
import { useSSE } from '../../hooks/use-sse';
import { Palette, Play, Clock, DollarSign, FileText, Image as ImageIcon, Video, CheckCircle2 } from 'lucide-react';

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
                return [payload, ...prev].slice(0, 1); // Focus on single active production for detailed view
            });
        });

        return unsub;
    }, [subscribe]);

    const activeProduction = productions[0];

    return (
        <div className="flex flex-col h-full space-y-6">
            {/* Header */}
            <div className="flex items-center justify-between border-b border-glass-border pb-4">
                <h2 className="text-xs font-bold text-ruby uppercase tracking-widest flex items-center gap-2">
                    <Palette size={14} />
                    Creation Lobe
                </h2>
                <div className="flex items-center gap-2 text-[9px] text-white/40">
                    <span className="w-2 h-2 rounded-full bg-ruby animate-pulse" />
                    STUDIO ACTIVE
                </div>
            </div>

            {activeProduction ? (
                <div className="flex flex-col gap-6">
                    {/* Main Preview Area */}
                    <div className="relative aspect-video bg-black/50 rounded-lg border border-glass-border overflow-hidden group">
                        {activeProduction.thumbnail_url ? (
                            <img src={activeProduction.thumbnail_url} alt="Preview" className="w-full h-full object-cover opacity-60 group-hover:opacity-100 transition-opacity" />
                        ) : (
                            <div className="absolute inset-0 flex flex-col items-center justify-center text-white/20 gap-2">
                                <div className="w-12 h-12 rounded-full border border-white/10 flex items-center justify-center">
                                    <Play size={20} className="ml-1" />
                                </div>
                                <span className="text-[10px] uppercase tracking-widest">Rendering Preview...</span>
                            </div>
                        )}
                        
                        {/* Overlay Stats */}
                        <div className="absolute bottom-0 left-0 right-0 p-3 bg-gradient-to-t from-black/90 to-transparent flex justify-between items-end">
                            <div>
                                <h3 className="text-sm font-bold text-white">{activeProduction.title}</h3>
                                <div className="text-[10px] text-ruby uppercase tracking-wider font-bold">
                                    {activeProduction.status} • {activeProduction.progress}%
                                </div>
                            </div>
                            <div className="text-right text-[10px] text-white/60">
                                <div className="flex items-center gap-1 justify-end">
                                    <Clock size={10} />
                                    {Math.ceil((activeProduction.eta_seconds || 0) / 60)}m remaining
                                </div>
                                <div className="flex items-center gap-1 justify-end text-emerald">
                                    <DollarSign size={10} />
                                    $0.12 est.
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Vertical Pipeline Visualization */}
                    <div className="space-y-2">
                        <div className="text-[10px] font-bold text-white/40 uppercase mb-2">Production Pipeline</div>
                        <PipelineStep 
                            label="Scripting" 
                            icon={FileText} 
                            status={getStepStatus('scripting', activeProduction.status)} 
                        />
                        <PipelineStep 
                            label="Visualization" 
                            icon={ImageIcon} 
                            status={getStepStatus('visualizing', activeProduction.status)} 
                        />
                        <PipelineStep 
                            label="Motion Synthesis" 
                            icon={Video} 
                            status={getStepStatus('rendering', activeProduction.status)} 
                        />
                        <PipelineStep 
                            label="Quality Assurance" 
                            icon={CheckCircle2} 
                            status={getStepStatus('qa', activeProduction.status)} 
                        />
                    </div>
                </div>
            ) : (
                <div className="flex-1 flex flex-col items-center justify-center border border-dashed border-white/10 rounded-lg text-white/20 gap-2">
                    <Palette size={24} />
                    <span className="text-xs uppercase tracking-widest">Studio Idle</span>
                </div>
            )}
        </div>
    );
}

function PipelineStep({ label, icon: Icon, status }: { label: string, icon: any, status: 'pending' | 'active' | 'complete' }) {
    const getStyles = () => {
        switch(status) {
            case 'complete': return 'text-emerald border-emerald/20 bg-emerald/5';
            case 'active': return 'text-ruby border-ruby/20 bg-ruby/5';
            default: return 'text-white/20 border-white/5 bg-transparent';
        }
    };

    return (
        <div className={`flex items-center gap-3 p-2 rounded border transition-colors ${getStyles()}`}>
            <Icon size={14} className={status === 'active' ? 'animate-pulse' : ''} />
            <span className="text-[10px] uppercase tracking-wider flex-1">{label}</span>
            {status === 'active' && <div className="w-2 h-2 rounded-full bg-ruby animate-pulse" />}
            {status === 'complete' && <CheckCircle2 size={12} />}
        </div>
    );
}

function getStepStatus(step: string, currentStatus: string): 'pending' | 'active' | 'complete' {
    const order = ['planning', 'scripting', 'visualizing', 'rendering', 'qa', 'published'];
    const stepIdx = order.indexOf(step);
    const currentIdx = order.indexOf(currentStatus);

    if (currentIdx > stepIdx) return 'complete';
    if (currentIdx === stepIdx) return 'active';
    return 'pending';
}
