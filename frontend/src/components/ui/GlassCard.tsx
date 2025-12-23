"use client";

import React from 'react';
import { motion, HTMLMotionProps } from 'framer-motion';

interface GlassCardProps extends HTMLMotionProps<"div"> {
    children: React.ReactNode;
    className?: string;
    variant?: 'default' | 'interactive';
}

export const GlassCard = ({ children, className = '', variant = 'default', ...props }: GlassCardProps) => {
    return (
        <motion.div
            className={`luxe-glass-card p-6 ${className} ${variant === 'interactive' ? 'cursor-pointer' : ''}`}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            whileHover={variant === 'interactive' ? { scale: 1.02 } : {}}
            {...props}
        >
            {children}
        </motion.div>
    );
};
