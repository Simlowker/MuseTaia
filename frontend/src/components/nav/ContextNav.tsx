"use client";

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

type Intent = 'general' | 'finance' | 'creative' | 'history';

interface ContextNavProps {
    children: (intent: Intent) => React.ReactNode;
}

export const ContextNav: React.FC<ContextNavProps> = ({ children }) => {
    const [intent, setIntent] = useState<Intent>('general');

    // Simulate Intent changes (Mock RootAgent)
    // In real app, this would listen to Multimodal API
    useEffect(() => {
        // Expose to window for manual testing if needed
        (window as any).setIntent = setIntent;
    }, []);

    return (
        <>
            {/* Debug / Manual Control (Hidden in production or stylized) */}
            <div className="absolute top-4 left-1/2 -translate-x-1/2 z-50 flex gap-2 p-2 bg-black/50 backdrop-blur rounded-full border border-white/10 opacity-0 hover:opacity-100 transition-opacity">
                {(['general', 'finance', 'creative', 'history'] as Intent[]).map(i => (
                    <button
                        key={i}
                        onClick={() => setIntent(i)}
                        className={`text-[8px] uppercase font-bold px-3 py-1 rounded-full ${intent === i ? 'bg-white text-black' : 'text-white/50'}`}
                    >
                        {i}
                    </button>
                ))}
            </div>

            {/* Render Children with current intent */}
            {children(intent)}
        </>
    );
};
