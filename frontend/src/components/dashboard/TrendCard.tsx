"use client";

import React from 'react';
import { motion } from 'framer-motion';

interface TrendCardProps {
  title: string;
  subtitle?: string;
  imageUrl?: string;
  source: string;
  score: number;
  status?: 'detected' | 'analyzing' | 'approved' | 'rejected';
  onClick?: () => void;
}

const sourceColors: Record<string, string> = {
  tiktok: 'bg-pink-100 text-pink-700',
  reddit: 'bg-orange-100 text-orange-700',
  instagram: 'bg-purple-100 text-purple-700',
  twitter: 'bg-blue-100 text-blue-700',
  default: 'bg-stone-100 text-stone-600',
};

export function TrendCard({ title, subtitle, imageUrl, source, score, status, onClick }: TrendCardProps) {
  const safeSource = (source || 'default').toLowerCase();
  const sourceStyle = sourceColors[safeSource] || sourceColors.default;
  
  return (
    <motion.div
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      onClick={onClick}
      className="group cursor-pointer"
    >
      <div className="relative rounded-2xl overflow-hidden bg-white/80 backdrop-blur-sm shadow-lg hover:shadow-xl transition-all duration-300">
        {/* Image */}
        {imageUrl && (
          <div className="relative h-28 overflow-hidden">
            <img 
              src={imageUrl} 
              alt={title}
              className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
            />
            {status === 'analyzing' && (
              <div className="absolute inset-0 bg-black/30 flex items-center justify-center">
                <div className="w-6 h-6 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              </div>
            )}
          </div>
        )}
        
        {/* Content */}
        <div className="p-3">
          <h3 className="font-semibold text-stone-800 text-sm leading-tight mb-1 line-clamp-2">
            {title}
          </h3>
          {subtitle && (
            <p className="text-xs text-stone-500 line-clamp-2 mb-2">{subtitle}</p>
          )}
          <div className="flex items-center justify-between">
            <span className={`text-xs px-2 py-0.5 rounded-full ${sourceStyle}`}>
              {source}
            </span>
            <span className="text-xs font-semibold text-amber-700">
              {score.toFixed(1)} VVS
            </span>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
