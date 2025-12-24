"use client";

import React from 'react';
import { cn } from '@/lib/utils';

interface GlassPanelProps {
  children: React.ReactNode;
  variant?: 'light' | 'dark';
  className?: string;
}

export function GlassPanel({ children, variant = 'light', className }: GlassPanelProps) {
  return (
    <div className={cn(
      'backdrop-blur-xl border shadow-2xl',
      variant === 'light' 
        ? 'bg-white/40 border-white/50 rounded-3xl' 
        : 'bg-stone-800/80 border-white/10 rounded-2xl',
      className
    )}>
      {children}
    </div>
  );
}