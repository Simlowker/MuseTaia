"use client";

import React, { useRef, useLayoutEffect } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { Vortex } from "@/components/vfx/Vortex";
import { motion } from "framer-motion";

gsap.registerPlugin(ScrollTrigger);

export default function GenesisPage() {
  const containerRef = useRef<HTMLDivElement>(null);
  const dnaRef = useRef<HTMLDivElement>(null);
  const faceRef = useRef<HTMLDivElement>(null);

  useLayoutEffect(() => {
    let ctx = gsap.context(() => {
      
      // 1. DNA Sequence Animation
      gsap.fromTo(dnaRef.current, 
        { opacity: 0, scale: 0.5, y: 100 },
        {
          opacity: 1,
          scale: 1,
          y: 0,
          scrollTrigger: {
            trigger: containerRef.current,
            start: "top top",
            end: "30% top",
            scrub: 1,
          }
        }
      );

      // 2. Face Master Reveal (Flash)
      const tl = gsap.timeline({
        scrollTrigger: {
          trigger: containerRef.current,
          start: "60% top",
          end: "100% top",
          scrub: 1,
        }
      });

      tl.to(faceRef.current, { opacity: 1, scale: 1.2, filter: "blur(0px) brightness(1.5)" })
        .to(faceRef.current, { scale: 1, filter: "blur(0px) brightness(1)", duration: 0.5 });

    }, containerRef);

    return () => ctx.revert();
  }, []);

  return (
    <div ref={containerRef} className="relative h-[200vh] bg-black text-white overflow-hidden">
      
      {/* Sticky Background Vortex */}
      <div className="fixed inset-0 z-0">
        <Vortex 
            rangeY={500}
            baseHue={280}
            baseRadius={2}
            rangeSpeed={2}
            particleCount={1000}
            backgroundColor="black"
            className="h-full w-full"
        />
      </div>

      {/* Content Layer */}
      <div className="relative z-10 w-full h-full flex flex-col items-center">
        
        {/* SECTION 1: GENESIS INTRO (0-50vh) */}
        <div className="h-screen w-full flex flex-col items-center justify-center">
            <h1 className="text-6xl md:text-9xl font-bold tracking-tighter text-transparent bg-clip-text bg-gradient-to-b from-white to-white/20">
                GENESIS
            </h1>
            <p className="text-xl text-white/40 mt-4 tracking-[0.5em] uppercase">
                Constructing Identity Matrix
            </p>
            <div className="mt-12 animate-bounce text-white/20">
                ↓ SCROLL TO INITIALIZE
            </div>
        </div>

        {/* SECTION 2: DNA SEQUENCE (50-150vh) */}
        <div className="h-screen w-full flex flex-col items-center justify-center" ref={dnaRef}>
            <div className="flex gap-4 font-mono text-xs text-emerald-500/80 mb-8">
                <span>[SEQ_01: COMPLETE]</span>
                <span>[SEQ_02: PARSING]</span>
                <span>[SEQ_03: PENDING]</span>
            </div>
            
            {/* Visual DNA Bars */}
            <div className="flex gap-1 h-32 items-end">
                {[...Array(20)].map((_, i) => (
                    <motion.div 
                        key={i}
                        className="w-2 bg-emerald-500 rounded-t-sm"
                        animate={{ height: ["20%", "80%", "20%"] }}
                        transition={{ duration: 1, repeat: Infinity, delay: i * 0.1, ease: "easeInOut" }}
                    />
                ))}
            </div>
        </div>

        {/* SECTION 3: THE REVEAL (150-200vh) */}
        <div className="h-screen w-full flex items-center justify-center fixed top-0 pointer-events-none opacity-0" ref={faceRef}>
            <div className="relative w-96 h-96">
                <div className="absolute inset-0 bg-gradient-to-tr from-purple-500/30 to-blue-500/30 rounded-full blur-3xl animate-pulse" />
                <img 
                    src="/assets/genesis_face.png" // Placeholder
                    alt="Genesis Face" 
                    className="relative w-full h-full object-cover rounded-2xl border-2 border-white/20 shadow-2xl"
                />
                <div className="absolute -bottom-12 left-0 right-0 text-center">
                    <span className="text-2xl font-bold tracking-widest text-white uppercase">
                        MUSE ACTIVATED
                    </span>
                </div>
            </div>
        </div>

      </div>
    </div>
  );
}
