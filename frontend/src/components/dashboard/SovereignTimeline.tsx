"use client";

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useSystem } from '../../contexts/system-context';
import { Clock, History } from 'lucide-react';

interface TimelineEvent {
    id: string;
    timestamp: string;
    type: 'scan' | 'analyze' | 'decide' | 'create' | 'qa' | 'publish';
    label: string;
}

export function SovereignTimeline() {
    const { isStreamConnected } = useSystem();
    const [events, setEvents] = useState<TimelineEvent[]>([
        { id: '1', timestamp: '10:00', type: 'scan', label: 'Initial Scan' },
        { id: '2', timestamp: '10:15', type: 'analyze', label: 'Trend Analysis' },
        { id: '3', timestamp: '10:30', type: 'decide', label: 'ROI Approval' },
        { id: '4', timestamp: '10:45', type: 'create', label: 'Script Generation' },
    ]);

    // In a real scenario, we'd subscribe to a TIMELINE_UPDATE event
    // For now, it shows the recent flow of the Muse's life.

    const getEventColor = (type: TimelineEvent['type']) => {
        switch(type) {
            case 'scan': return 'bg-cyan';
            case 'analyze': return 'bg-gold';
            case 'decide': return 'bg-emerald';
            case 'create': return 'bg-ruby';
            case 'qa': return 'bg-amber';
            case 'publish': return 'bg-white';
            default: return 'bg-white/20';
        }
    };

    return (
        <div className="w-full h-full flex items-center justify-between gap-4 px-4">
            <div className="flex items-center gap-2 text-white/40 text-[10px] uppercase font-bold tracking-widest min-w-[120px]">
                <Clock size={14} />
                Time Stream
            </div>

            <div className="flex-1 relative flex items-center h-12">
                {/* Connector Line */}
                <div className="absolute left-0 right-0 h-[1px] bg-gradient-to-r from-transparent via-white/10 to-transparent" />
                
                <div className="flex justify-between w-full relative z-10">
                    <AnimatePresence mode="popLayout">
                        {events.map((event, i) => (
                            <motion.div
                                key={event.id}
                                initial={{ opacity: 0, scale: 0 }}
                                animate={{ opacity: 1, scale: 1 }}
                                className="flex flex-col items-center gap-1 group cursor-help"
                            >
                                <div className={`w-2 h-2 rounded-full ${getEventColor(event.type)} ring-4 ring-black shadow-[0_0_8px_rgba(255,255,255,0.2)]`} />
                                <div className="absolute -top-6 opacity-0 group-hover:opacity-100 transition-opacity bg-glass-bg border border-glass-border px-2 py-1 rounded text-[8px] whitespace-nowrap backdrop-blur-md">
                                    <span className="text-white/40 mr-1">{event.timestamp}</span>
                                    <span className="text-white font-bold uppercase">{event.label}</span>
                                </div>
                                <span className="text-[8px] text-white/20 uppercase font-mono">{event.timestamp}</span>
                            </motion.div>
                        ))}
                        {/* Current Marker */}
                        <motion.div
                            animate={{ opacity: [0.3, 1, 0.3] }}
                            transition={{ duration: 2, repeat: Infinity }}
                            className="flex flex-col items-center gap-1"
                        >
                            <div className="w-3 h-3 rounded-full bg-gold ring-4 ring-gold/20 animate-pulse" />
                            <span className="text-[8px] text-gold font-bold uppercase tracking-tighter">NOW</span>
                        </motion.div>
                    </AnimatePresence>
                </div>
            </div>

            <div className="flex items-center gap-4 border-l border-white/5 pl-4 ml-4">
                <div className="flex flex-col items-end">
                    <span className="text-[8px] text-white/30 uppercase">Sync Status</span>
                    <span className={`text-[10px] font-bold uppercase ${isStreamConnected ? 'text-emerald' : 'text-ruby'}`}>
                        {isStreamConnected ? 'Live' : 'Desync'}
                    </span>
                </div>
                <History size={18} className="text-white/20 hover:text-white/60 transition-colors cursor-pointer" />
            </div>
        </div>
    );
}
