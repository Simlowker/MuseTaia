"use client";

import React from 'react';
import { motion } from 'framer-motion';

interface CreativeSwarmProps {
  agentName: string;
  taskName: string;
  status: string;
  progress: number;
  previewUrl?: string;
  onApprove?: () => void;
  onRetry?: () => void;
}

export function CreativeSwarm({ 
  agentName, 
  taskName, 
  status, 
  progress, 
  previewUrl,
  onApprove,
  onRetry 
}: CreativeSwarmProps) {
  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-sm font-bold text-stone-700 tracking-wide uppercase">
          Creative Swarm
        </h2>
      </div>
      
      {/* Agent Status */}
      <div className="bg-white/60 backdrop-blur-sm rounded-2xl p-4 mb-4">
        <div className="text-xs text-stone-600 mb-1">
          {agentName} [{taskName}]
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs font-medium text-amber-700">
            STATUS: {status.toUpperCase()}
          </span>
          <span className="text-xs text-stone-500">({progress}%)</span>
        </div>
        <div className="mt-2 h-1.5 bg-stone-200 rounded-full overflow-hidden">
          <motion.div 
            className="h-full bg-gradient-to-r from-amber-400 to-amber-600 rounded-full"
            initial={{ width: 0 }}
            animate={{ width: `${progress}%` }}
            transition={{ duration: 0.5 }}
          />
        </div>
      </div>
      
      {/* Media Preview */}
      <div className="flex-1 bg-white/60 backdrop-blur-sm rounded-2xl p-4">
        <div className="text-xs font-semibold text-stone-600 uppercase tracking-wider mb-3">
          Media Preview
        </div>
        <div className="rounded-xl overflow-hidden shadow-lg bg-stone-200">
          {previewUrl ? (
            <img 
              src={previewUrl}
              alt="Preview"
              className="w-full h-40 object-cover"
            />
          ) : (
            <div className="w-full h-40 flex items-center justify-center text-stone-400 text-xs">
              Rendering...
            </div>
          )}
        </div>
      </div>
      
      {/* Action Buttons */}
      <div className="flex gap-3 mt-4">
        <button 
          onClick={onRetry}
          className="flex-1 py-3 bg-stone-200/80 hover:bg-stone-300/80 text-stone-700 font-semibold rounded-xl transition-colors text-sm"
        >
          RETRY
        </button>
        <button 
          onClick={onApprove}
          className="flex-1 py-3 bg-gradient-to-r from-amber-400 to-amber-500 hover:from-amber-500 hover:to-amber-600 text-white font-semibold rounded-xl transition-colors text-sm shadow-lg"
        >
          APPROVE
        </button>
      </div>
    </div>
  );
}
