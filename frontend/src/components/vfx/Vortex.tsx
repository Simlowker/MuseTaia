"use client";

import React, { useEffect, useRef } from "react";
import { createNoise3D } from "simplex-noise";
import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

export const Vortex = ({
  children,
  className,
  containerClassName,
  particleCount = 700,
  rangeY = 100,
  baseHue = 220,
  baseSpeed = 0.0,
  rangeSpeed = 1.5,
  baseRadius = 1,
  rangeRadius = 2,
  backgroundColor = "#000000",
}: {
  children?: React.ReactNode;
  className?: string;
  containerClassName?: string;
  particleCount?: number;
  rangeY?: number;
  baseHue?: number;
  baseSpeed?: number;
  rangeSpeed?: number;
  baseRadius?: number;
  rangeRadius?: number;
  backgroundColor?: string;
}) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const particlePropCount = 9;
  const particlePropsLength = particleCount * particlePropCount;
  const rangeYn = rangeY;
  const baseTTL = 50;
  const rangeTTL = 150;
  const baseHueN = baseHue;
  const rangeHue = 100;
  const noise3D = createNoise3D();
  let particleProps: Float32Array;
  let center: [number, number];
  let tick: number;
  let simplex: any;
  let ctx: CanvasRenderingContext2D;

  useEffect(() => {
    const canvas = canvasRef.current;
    const container = containerRef.current;
    if (canvas && container) {
      ctx = canvas.getContext("2d") as CanvasRenderingContext2D;
      resize();
      initParticles();
      draw();

      window.addEventListener("resize", resize);
    }

    return () => {
      window.removeEventListener("resize", resize);
    };
  }, []);

  const initParticles = () => {
    tick = 0;
    simplex = createNoise3D();
    particleProps = new Float32Array(particlePropsLength);

    for (let i = 0; i < particlePropsLength; i += particlePropCount) {
      initParticle(i);
    }
  };

  const initParticle = (i: number) => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    let x, y, vx, vy, life, ttl, speed, radius, hue;

    x = RAND(canvas.width);
    y = center[1] + RAND(rangeYn);
    vx = 0;
    vy = 0;
    life = 0;
    ttl = baseTTL + RAND(rangeTTL);
    speed = baseSpeed + RAND(rangeSpeed);
    radius = baseRadius + RAND(rangeRadius);
    hue = baseHueN + RAND(rangeHue);

    particleProps.set([x, y, vx, vy, life, ttl, speed, radius, hue], i);
  };

  const draw = () => {
    tick++;

    if (!ctx) return;

    ctx.clearRect(0, 0, canvasRef.current?.width || 0, canvasRef.current?.height || 0);

    ctx.fillStyle = backgroundColor;
    ctx.fillRect(0, 0, canvasRef.current?.width || 0, canvasRef.current?.height || 0);

    drawParticles();
    renderGlow();
    renderToScreen();

    window.requestAnimationFrame(draw);
  };

  const drawParticles = () => {
    for (let i = 0; i < particlePropsLength; i += particlePropCount) {
      updateParticle(i);
    }
  };

  const updateParticle = (i: number) => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    let i2 = 1 + i,
      i3 = 2 + i,
      i4 = 3 + i,
      i5 = 4 + i,
      i6 = 5 + i,
      i7 = 6 + i,
      i8 = 7 + i,
      i9 = 8 + i;
    let n, x, y, vx, vy, life, ttl, speed, x2, y2, radius, hue;

    x = particleProps[i];
    y = particleProps[i2];
    n = simplex(x * 0.00125, y * 0.00125, tick * 0.0005) * 0.5 + 0.5;
    vx = lerp(particleProps[i3], Math.cos(n * Math.PI * 2), 0.5);
    vy = lerp(particleProps[i4], Math.sin(n * Math.PI * 2), 0.5);
    life = particleProps[i5];
    ttl = particleProps[i6];
    speed = particleProps[i7];
    x2 = x + vx * speed;
    y2 = y + vy * speed;
    radius = particleProps[i8];
    hue = particleProps[i9];

    drawParticle(x, y, x2, y2, life, ttl, radius, hue);

    life++;

    particleProps[i] = x2;
    particleProps[i2] = y2;
    particleProps[i3] = vx;
    particleProps[i4] = vy;
    particleProps[i5] = life;

    (checkBounds(x, y, canvas) || life > ttl) && initParticle(i);
  };

  const drawParticle = (
    x: number,
    y: number,
    x2: number,
    y2: number,
    life: number,
    ttl: number,
    radius: number,
    hue: number
  ) => {
    if (!ctx) return;
    ctx.save();
    ctx.lineCap = "round";
    ctx.lineWidth = radius;
    ctx.strokeStyle = `hsla(${hue},100%,60%,${fadeInOut(life, ttl)})`;
    ctx.beginPath();
    ctx.moveTo(x, y);
    ctx.lineTo(x2, y2);
    ctx.stroke();
    ctx.closePath();
    ctx.restore();
  };

  const checkBounds = (x: number, y: number, canvas: HTMLCanvasElement) => {
    return x > canvas.width || x < 0 || y > canvas.height || y < 0;
  };

  const resize = () => {
    const canvas = canvasRef.current;
    const container = containerRef.current;
    if (canvas && container) {
      canvas.width = container.offsetWidth;
      canvas.height = container.offsetHeight;
      center = [0.5 * canvas.width, 0.5 * canvas.height];
    }
  };

  const renderGlow = () => {
    if (!ctx) return;
    ctx.save();
    ctx.filter = "blur(8px) brightness(200%)";
    ctx.globalCompositeOperation = "lighter";
    ctx.drawImage(canvasRef.current!, 0, 0);
    ctx.restore();

    ctx.save();
    ctx.filter = "blur(4px) brightness(200%)";
    ctx.globalCompositeOperation = "lighter";
    ctx.drawImage(canvasRef.current!, 0, 0);
    ctx.restore();
  };

  const renderToScreen = () => {
    if (!ctx) return;
    ctx.save();
    ctx.globalCompositeOperation = "lighter";
    ctx.drawImage(canvasRef.current!, 0, 0);
    ctx.restore();
  };

  const lerp = (a: number, b: number, t: number) => {
    return a * (1 - t) + b * t;
  };

  const RAND = (n: number) => {
    return n * Math.random();
  };

  const fadeInOut = (t: number, m: number) => {
    let hm = 0.5 * m;
    return Math.abs(((t + hm) % m) - hm) / hm;
  };

  return (
    <div className={cn("relative h-full w-full", containerClassName)}>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        ref={containerRef}
        className="absolute inset-0 z-0 flex items-center justify-center bg-transparent"
      >
        <canvas ref={canvasRef}></canvas>
      </motion.div>

      <div className={cn("relative z-10", className)}>{children}</div>
    </div>
  );
};
