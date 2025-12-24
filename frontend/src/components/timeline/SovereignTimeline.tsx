"use client";

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useSystem } from '../../contexts/system-context';
import { useSSE } from '../../hooks/use-sse';
import { Wallet, ShieldAlert, Activity, Clock, History } from 'lucide-react';

interface TimelineEvent {
    id: string;
    timestamp: string;
    type: 'scan' | 'analyze' | 'decide' | 'create' | 'qa' | 'publish';
    label: string;
}

export function SovereignTimeline() {
    const { wallet, isStreamConnected } = useSystem();
    const [events, setEvents] = useState<TimelineEvent[]>([
        { id: '1', timestamp: '10:00', type: 'scan', label: 'SCAN' },
        { id: '2', timestamp: '10:15', type: 'decide', label: 'ROI OK' },
        { id: '3', timestamp: '10:45', type: 'create', label: 'SCRIPT' },
    ]);

    // Mock adding events for liveness
    useEffect(() => {
        const interval = setInterval(() => {
             // Logic to fetch or receive events would go here
        }, 10000);
        return () => clearInterval(interval);
    }, []);

    const getEventColor = (type: TimelineEvent['type']) => {
        switch(type) {
            case 'scan': return 'bg-cyan shadow-cyan/50';
            case 'decide': return 'bg-emerald shadow-emerald/50';
            case 'create': return 'bg-ruby shadow-ruby/50';
            default: return 'bg-white/20';
        }
    };

    const spendPercentage = wallet ? (wallet.daily_spend / wallet.daily_budget) * 100 : 0;
    const isCritical = spendPercentage > 85;

    return (
        <div className="w-full h-full flex items-center justify-between px-6 bg-obsidian border-t border-glass-border">
            
            {/* LEFT: TIMELINE */}
            <div className="flex-1 flex items-center gap-6 mr-12">
                <div className="flex items-center gap-2 text-white/30 text-[10px] uppercase font-bold tracking-widest min-w-[80px]">
                    <History size={14} />
                    Events
                </div>

                <div className="flex-1 relative h-8 flex items-center">
                    {/* Line */}
                    <div className="absolute left-0 right-0 top-1/2 h-[1px] bg-white/10" />
                    
                    {/* Events */}
                    <div className="flex justify-between w-full max-w-xl relative z-10">
                        {events.map((event) => (
                            <div key={event.id} className="group relative">
                                <div className={`w-2 h-2 rounded-full ring-4 ring-obsidian ${getEventColor(event.type)}`} />
                                <div className="absolute bottom-4 left-1/2 -translate-x-1/2 opacity-0 group-hover:opacity-100 transition-opacity bg-glass-bg border border-glass-border px-2 py-1 rounded text-[8px] whitespace-nowrap backdrop-blur-md pointer-events-none">
                                    <span className="text-white/40 mr-1">{event.timestamp}</span>
                                    <span className="text-white font-bold">{event.label}</span>
                                </div>
                            </div>
                        ))}
                        {/* Current Head */}
                        <div className="relative">
                            <div className="w-3 h-3 rounded-full bg-gold ring-4 ring-obsidian animate-pulse shadow-[0_0_10px_var(--sovereign-gold)]" />
                            <div className="absolute top-4 left-1/2 -translate-x-1/2 text-[8px] text-gold font-bold tracking-widest uppercase">NOW</div>
                        </div>
                    </div>
                </div>
            </div>

            {/* RIGHT: WALLET & CFO */}
            <div className="flex items-center gap-8 border-l border-white/5 pl-8 h-12">
                
                {/* Wallet Balance */}
                <div className="flex flex-col items-end">
                    <div className="flex items-center gap-2 text-emerald">
                        <Wallet size={16} />
                        <span className="text-lg font-bold tracking-tighter text-white">
                            {wallet?.balance.toLocaleString('en-US', { style: 'currency', currency: wallet?.currency || 'USD' }) || "$0.00"}
                        </span>
                    </div>
                    <span className="text-[9px] text-white/30 uppercase tracking-widest">Sovereign Wallet</span>
                </div>

                {/* CFO Circuit Breaker */}
                <div className="w-40 space-y-1.5">
                    <div className="flex justify-between items-center text-[9px] font-bold uppercase tracking-tighter">
                        <div className="flex items-center gap-1 text-white/40">
                            <ShieldAlert size={10} className={isCritical ? 'text-ruby' : 'text-emerald'} />
                            CFO Gate
                        </div>
                        <span className={isCritical ? 'text-ruby' : 'text-emerald'}>
                            {wallet?.daily_spend.toFixed(2)} / {wallet?.daily_budget.toFixed(2)}
                        </span>
                    </div>
                    <div className="h-1.5 w-full bg-white/5 rounded-full overflow-hidden border border-white/5">
                        <motion.div
                            initial={{ width: 0 }}
                            animate={{ width: `${Math.min(spendPercentage, 100)}%` }}
                            className={`h-full rounded-full ${isCritical ? 'bg-ruby' : 'bg-emerald'}`}
                        />
                    </div>
                </div>

                {/* System Status */}
                <div className="flex flex-col items-center justify-center pl-4 border-l border-white/5">
                    <div className={`w-2 h-2 rounded-full ${isStreamConnected ? 'bg-emerald shadow-[0_0_8px_var(--success-emerald)]' : 'bg-ruby'}`} />
                    <span className="text-[8px] text-white/20 uppercase mt-1 tracking-widest">
                        {isStreamConnected ? 'SYNC' : 'LOST'}
                    </span>
                </div>
            </div>
        </div>
    );
}
