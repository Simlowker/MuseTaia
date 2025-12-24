"use client";

import React from 'react';
import { motion } from 'framer-motion';

export function SynapseLines() {
    return (
        <div className="absolute inset-0 pointer-events-none overflow-hidden z-10">
            {/* Left to Center Line */}
            <div className="absolute top-1/2 left-0 w-[300px] h-[1px] bg-gradient-to-r from-cyan/20 to-transparent">
                <motion.div 
                    animate={{ x: [0, 300], opacity: [0, 1, 0] }}
                    transition={{ duration: 3, repeat: Infinity, ease: "linear" }}
                    className="w-8 h-full bg-cyan shadow-[0_0_8px_var(--neural-cyan)]"
                />
            </div>

            {/* Right to Center Line */}
            <div className="absolute top-1/2 right-0 w-[350px] h-[1px] bg-gradient-to-l from-ruby/20 to-transparent">
                 <motion.div 
                    animate={{ x: [0, -350], opacity: [0, 1, 0] }}
                    transition={{ duration: 4, repeat: Infinity, ease: "linear", delay: 1 }}
                    className="w-8 h-full bg-ruby shadow-[0_0_8px_var(--danger-ruby)]"
                />
            </div>
        </div>
    );
}
