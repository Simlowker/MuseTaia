"use client";

import React, { useEffect, useRef, useState } from "react";
import { useSystem } from "@/contexts/system-context";
import { cn } from "@/lib/utils";

export function IdentityScanner() {
  const { mood } = useSystem();
  const [scanning, setScanning] = useState(true);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const timer = setInterval(() => {
        setScanning(prev => !prev);
    }, 5000);
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="relative w-full h-full overflow-hidden rounded-xl bg-black border border-white/10 group">
      
      {/* Background Grid */}
      <div className="absolute inset-0 z-0 opacity-20" 
           style={{ backgroundImage: `linear-gradient(#333 1px, transparent 1px), linear-gradient(90deg, #333 1px, transparent 1px)`, backgroundSize: '20px 20px' }} 
      />

      {/* Main Image Placeholder (Eventually replaced by ComfyUI stream) */}
      <div className="absolute inset-0 z-10 flex items-center justify-center">
         <div className="w-32 h-32 rounded-full bg-gradient-to-br from-gold/20 to-transparent border border-gold/30 blur-sm animate-pulse" />
      </div>

      {/* Laser Scanner */}
      <div className={cn(
          "absolute left-0 right-0 h-1 bg-red-500/50 shadow-[0_0_15px_rgba(255,0,0,0.8)] z-20 transition-all duration-[2000ms] ease-linear",
          scanning ? "top-[100%]" : "top-[0%]"
      )} />

      {/* HUD Overlay */}
      <div className="absolute inset-0 z-30 p-4 flex flex-col justify-between pointer-events-none">
          <div className="flex justify-between items-start">
              <div className="text-[10px] font-mono text-red-500/80">REC • LIVE</div>
              <div className="text-[10px] font-mono text-gold/80">ID: MUSE-01</div>
          </div>
          
          <div className="flex justify-between items-end">
              <div className="space-y-1">
                  <div className="text-[9px] text-white/40">VALENCE</div>
                  <div className="w-16 h-1 bg-white/10 rounded-full overflow-hidden">
                      <div className="h-full bg-gold" style={{ width: `${((mood?.valence || 0) + 1) * 50}%` }} />
                  </div>
              </div>
              <div className="text-[9px] font-mono text-cyan/80">
                  DRIFT: 0.02%
              </div>
          </div>
      </div>

      {/* Corner Brackets */}
      <div className="absolute top-2 left-2 w-4 h-4 border-t border-l border-white/30 z-30" />
      <div className="absolute top-2 right-2 w-4 h-4 border-t border-r border-white/30 z-30" />
      <div className="absolute bottom-2 left-2 w-4 h-4 border-b border-l border-white/30 z-30" />
      <div className="absolute bottom-2 right-2 w-4 h-4 border-b border-r border-white/30 z-30" />

    </div>
  );
}
