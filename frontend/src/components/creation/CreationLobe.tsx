"use client";

import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useSystem } from '../../contexts/system-context';
import { Palette, Play, Clock, DollarSign, FileText, Image as ImageIcon, Video, CheckCircle2 } from 'lucide-react';

export function CreationLobe() {
    const { activeProduction } = useSystem();

    return (
        <div className="flex flex-col h-full space-y-6">
            {/* Header */}
            <div className="flex items-center justify-between border-b border-glass-border pb-4">
                <h2 className="text-xs font-bold text-ruby uppercase tracking-widest flex items-center gap-2">
                    <Palette size={14} />
                    Creation Lobe
                </h2>
                <div className="flex items-center gap-2 text-[9px] text-white/40">
                    <span className={`w-2 h-2 rounded-full ${activeProduction ? 'bg-ruby animate-pulse' : 'bg-white/10'}`} />
                    STUDIO {activeProduction ? 'ACTIVE' : 'IDLE'}
                </div>
            </div>

            {activeProduction ? (
                <div className="flex flex-col gap-6">
                    {/* Main Preview Area */}
                    <div className="relative aspect-video bg-black/50 rounded-lg border border-glass-border overflow-hidden group">
                        <div className="absolute inset-0 flex flex-col items-center justify-center text-white/20 gap-2">
                            <div className="w-12 h-12 rounded-full border border-white/10 flex items-center justify-center">
                                <Play size={20} className="ml-1" />
                            </div>
                            <span className="text-[10px] uppercase tracking-widest">Rendering Preview...</span>
                        </div>
                        
                        {/* Overlay Stats */}
                        <div className="absolute bottom-0 left-0 right-0 p-3 bg-gradient-to-t from-black/90 to-transparent flex justify-between items-end">
                            <div>
                                <h3 className="text-sm font-bold text-white">{activeProduction.title}</h3>
                                <div className="text-[10px] text-ruby uppercase tracking-wider font-bold">
                                    {activeProduction.status} • {activeProduction.progress}%
                                </div>
                            </div>
                            <div className="text-right text-[10px] text-white/60">
                                <div className="flex items-center gap-1 justify-end text-emerald">
                                    <DollarSign size={10} />
                                    ${activeProduction.cost_usd.toFixed(2)} est.
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
                            status={getStepStatus('scripting', activeProduction.current_stage)} 
                        />
                        <PipelineStep 
                            label="Visualization" 
                            icon={ImageIcon} 
                            status={getStepStatus('visualizing', activeProduction.current_stage)} 
                        />
                        <PipelineStep 
                            label="Motion Synthesis" 
                            icon={Video} 
                            status={getStepStatus('rendering', activeProduction.current_stage)} 
                        />
                        <PipelineStep 
                            label="Quality Assurance" 
                            icon={CheckCircle2} 
                            status={getStepStatus('qa', activeProduction.current_stage)} 
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

function getStepStatus(step: string, currentStage: string): 'pending' | 'active' | 'complete' {
    const order = ['planning', 'scripting', 'visualizing', 'rendering', 'qa', 'complete'];
    const stepIdx = order.indexOf(step);
    const currentIdx = order.indexOf(currentStage.toLowerCase());

    if (currentIdx > stepIdx) return 'complete';
    if (currentIdx === stepIdx) return 'active';
    return 'pending';
}