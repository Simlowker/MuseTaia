"use client";

import React from 'react';
import { motion } from 'framer-motion';
import { useSystem } from '../../contexts/system-context';
import { Wallet, ShieldAlert, Activity } from 'lucide-react';

export function WalletWidget() {
    const { wallet } = useSystem();

    if (!wallet) return null;

    const spendPercentage = (wallet.daily_spend / wallet.daily_budget) * 100;
    const isCritical = spendPercentage > 85;

    return (
        <div className="flex items-center gap-6 h-full border-l border-white/5 pl-6 ml-6">
            {/* Wallet Info */}
            <div className="flex flex-col items-end group">
                <div className="flex items-center gap-2">
                    <motion.div
                        animate={{ scale: [1, 1.1, 1] }}
                        transition={{ duration: 1.5, repeat: Infinity, ease: "easeInOut" }}
                        className={isCritical ? 'text-ruby' : 'text-emerald'}
                    >
                        <Wallet size={16} />
                    </motion.div>
                    <span className="text-xl font-bold tracking-tighter text-white">
                        {wallet.balance.toLocaleString('en-US', { style: 'currency', currency: wallet.currency })}
                    </span>
                </div>
                <span className="text-[10px] text-white/40 uppercase tracking-widest group-hover:text-emerald transition-colors">Sovereign Wallet</span>
            </div>

            {/* CFO Circuit Breaker */}
            <div className="w-48 space-y-1">
                <div className="flex justify-between items-center text-[9px] font-bold uppercase tracking-tighter">
                    <div className="flex items-center gap-1 text-white/40">
                        <ShieldAlert size={10} className={isCritical ? 'text-ruby' : 'text-white/40'} />
                        CFO Circuit Breaker
                    </div>
                    <span className={isCritical ? 'text-ruby' : 'text-emerald'}>
                        {wallet.daily_spend.toFixed(2)} / {wallet.daily_budget.toFixed(2)}
                    </span>
                </div>
                <div className="h-1.5 w-full bg-white/5 rounded-full overflow-hidden border border-white/10 p-[1px]">
                    <motion.div
                        initial={{ width: 0 }}
                        animate={{ width: `${Math.min(spendPercentage, 100)}%` }}
                        className={`h-full rounded-full ${
                            spendPercentage > 90 ? 'bg-ruby' : 
                            spendPercentage > 70 ? 'bg-amber' : 
                            'bg-emerald'
                        }`}
                        transition={{ duration: 1 }}
                    />
                </div>
                <div className="flex justify-between items-center text-[8px] text-white/20 uppercase">
                    <span>Usage: {spendPercentage.toFixed(1)}%</span>
                    <span className="flex items-center gap-1">
                        <Activity size={8} className="animate-pulse" />
                        Gate: Solvent
                    </span>
                </div>
            </div>
        </div>
    );
}
