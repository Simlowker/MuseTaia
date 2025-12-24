"use client";

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Mic } from 'lucide-react';
import { useSystem } from '@/contexts/system-context';
import { GlassPanel } from '@/components/ui/GlassPanel';
import { Waveform } from '@/components/ui/Waveform';
import { TrendCard } from './TrendCard';
import { ActiveThought } from './ActiveThought';
import { CreativeSwarm } from './CreativeSwarm';
import { MuseAvatar } from './MuseAvatar';

// Placeholder images (replace with real ones or GCS URLs)
const PLACEHOLDER_AVATAR = "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=400&h=400&fit=crop&crop=face";
const PLACEHOLDER_PREVIEW = "https://images.unsplash.com/photo-1591085686350-798c0f9faa7f?w=400&h=300&fit=crop";

// Mock trend images mapping
const trendImages: Record<string, string> = {
  'Cyber-Baroque Aesthetics': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=300&h=200&fit=crop',
  'Mycelium Materials': 'https://images.unsplash.com/photo-1530836369250-ef72a3f5cda8?w=300&h=200&fit=crop',
  'Neo-Brutalist Interiors': 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=300&h=200&fit=crop',
  'default': 'https://images.unsplash.com/photo-1558171813-4c088753af8f?w=300&h=200&fit=crop',
};

export function LuxeDashboard() {
  const { mood, wallet, trends, activeProduction, isConnected } = useSystem();
  const [isListening, setIsListening] = useState(false);

  // Derive mood for avatar
  const avatarMood = mood?.valence && mood.valence > 0.3 
    ? 'positive' 
    : mood?.valence && mood.valence < -0.3 
      ? 'negative' 
      : 'neutral';

  // Current thought
  const currentThought = mood?.current_thought || "System initializing...";

  return (
    <div 
      className="min-h-screen w-full p-6 relative overflow-hidden"
      style={{
        background: 'linear-gradient(135deg, #E8DCC4 0%, #D4C4A8 30%, #C9B896 60%, #BEA882 100%)'
      }}
    >
      {/* Ambient Light Effects */}
      <div className="absolute top-0 left-1/4 w-96 h-96 bg-amber-200/30 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute bottom-0 right-1/4 w-80 h-80 bg-orange-100/40 rounded-full blur-3xl pointer-events-none" />
      
      {/* Main Container */}
      <div className="relative z-10 max-w-7xl mx-auto h-[calc(100vh-48px)] flex flex-col">
        
        {/* Header */}
        <header className="flex justify-between items-center mb-4">
          <div className="flex items-center gap-3">
            <motion.div 
              animate={{ scale: [1, 1.2, 1] }}
              transition={{ duration: 2, repeat: Infinity }}
              className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`} 
            />
            <h1 className="text-xl font-bold tracking-widest text-stone-800 uppercase">
              Sovereign Muse OS
            </h1>
          </div>
          <div className="flex items-center gap-6 text-xs text-stone-500">
            <span>V.2.0.5</span>
            <span className="flex items-center gap-2">
              STATUS: 
              <span className={isConnected ? 'text-green-600 font-semibold' : 'text-red-600'}>
                {isConnected ? 'ONLINE' : 'OFFLINE'}
              </span>
            </span>
            {wallet && (
              <span className="font-semibold text-stone-700">
                ${wallet.balance.toFixed(2)}
              </span>
            )}
          </div>
        </header>
        
        {/* Main Glass Panel */}
        <GlassPanel className="flex-1 p-6 overflow-hidden">
          
          {/* Grid Layout */}
          <div className="grid grid-cols-12 gap-6 h-full">
            
            {/* LEFT: Niche Trends Feed */}
            <div className="col-span-3 flex flex-col min-h-0">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-sm font-bold text-stone-700 tracking-wide uppercase">
                  Niche Trends Feed
                </h2>
                <span className="text-xs text-stone-400">
                  {trends.length} signals
                </span>
              </div>
              
              <div className="flex-1 overflow-y-auto space-y-3 pr-2">
                {trends.length > 0 ? (
                  trends.map((trend) => (
                    <TrendCard
                      key={trend.id}
                      title={trend.title}
                      subtitle={trend.category}
                      imageUrl={trendImages[trend.title] || trendImages.default}
                      source={trend.platform || 'Unknown'}
                      score={trend.vvs_score}
                      status={trend.status}
                    />
                  ))
                ) : (
                  <div className="text-center text-stone-400 text-sm py-8">
                    No trends detected yet...
                  </div>
                )}
              </div>
            </div>
            
            {/* CENTER: Avatar & Consciousness */}
            <div className="col-span-6 flex flex-col min-h-0">
              
              {/* Avatar Area */}
              <div className="flex-1 flex items-center justify-center">
                <MuseAvatar 
                  imageUrl={PLACEHOLDER_AVATAR}
                  isActive={isConnected}
                  mood={avatarMood}
                />
              </div>
              
              {/* Active Thought */}
              <div className="mb-4">
                <ActiveThought thought={currentThought} />
              </div>
              
              {/* Waveform */}
              <GlassPanel variant="dark" className="p-4">
                <Waveform color="#D4AF37" speed={0.05} />
              </GlassPanel>
            </div>
            
            {/* RIGHT: Creative Swarm */}
            <div className="col-span-3 min-h-0">
              <CreativeSwarm
                agentName="VisualAgent"
                taskName={activeProduction?.title || "Idle"}
                status={activeProduction?.status || "waiting"}
                progress={activeProduction?.progress || 0}
                previewUrl={activeProduction?.thumbnail_url || PLACEHOLDER_PREVIEW}
                onApprove={() => console.log('Approved!')}
                onRetry={() => console.log('Retry!')}
              />
            </div>
            
          </div>
          
        </GlassPanel>
        
        {/* Microphone Button */}
        <div className="flex justify-center mt-4">
          <motion.button 
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => setIsListening(!isListening)}
            className={`w-14 h-14 rounded-full flex items-center justify-center transition-all duration-300 shadow-xl ${
              isListening 
                ? 'bg-amber-500' 
                : 'bg-white/80 hover:bg-white'
            }`}
          >
            <Mic className={`w-6 h-6 ${isListening ? 'text-white' : 'text-stone-600'}`} />
          </motion.button>
        </div>
        
      </div>
    </div>
  );
}
