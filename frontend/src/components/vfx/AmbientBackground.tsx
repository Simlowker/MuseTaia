"use client";

import React from 'react';

export function AmbientBackground() {
  return (
    <div className="fixed inset-0 z-0 pointer-events-none">
      {/* Deep Void Base */}
      <div className="absolute inset-0 bg-void" />
      
      {/* Subtle Gradient Spots */}
      <div className="absolute top-[-20%] left-[-10%] w-[50%] h-[50%] rounded-full bg-sovereign-gold/5 blur-[120px] animate-pulse-slow" />
      <div className="absolute bottom-[-20%] right-[-10%] w-[50%] h-[50%] rounded-full bg-neural-cyan/5 blur-[120px] animate-pulse-slow delay-1000" />
      
      {/* Noise Texture Overlay */}
      <div className="absolute inset-0 opacity-[0.03]" 
           style={{ backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E")` }} 
      />
    </div>
  );
}
