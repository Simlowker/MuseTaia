"use client";

import React from 'react';
import { motion } from 'framer-motion';

interface GlassPanelProps {
    children: React.ReactNode;
    title?: string;
    className?: string;
    action?: React.ReactNode;
}

export const GlassPanel = ({ children, title, className = '', action }: GlassPanelProps) => {
    return (
        <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className={`luxe-glass-card flex flex-col ${className}`}
        >
            {(title || action) && (
                <div className="flex items-center justify-between p-4 border-b border-[var(--glass-border)]">
                    {title && <h3 className="text-gold font-medium tracking-wider uppercase text-sm">{title}</h3>}
                    {action && <div>{action}</div>}
                </div>
            )}
            <div className="p-4 flex-1">
                {children}
            </div>
        </motion.div>
    );
};
