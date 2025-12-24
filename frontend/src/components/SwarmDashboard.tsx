"use client";

import React, { useEffect, useState } from 'react';

interface SwarmEvent {
  type: string;
  message: string;
  metadata: any;
  timestamp: string;
}

const SwarmDashboard: React.FC = () => {
  const [events, setEvents] = useState<SwarmEvent[]>([]);
  const [status, setStatus] = useState<string>("Disconnected");

  useEffect(() => {
    const eventSource = new EventSource(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080'}/stream/muse-status`);

    eventSource.onopen = () => setStatus("Connected to Neural Stream");

    eventSource.onmessage = (event) => {
      const newEvent: SwarmEvent = JSON.parse(event.data);
      setEvents((prev) => [newEvent, ...prev].slice(0, 50)); // Keep last 50
    };

    eventSource.onerror = () => setStatus("Stream Disconnected (Retrying...)");

    return () => eventSource.close();
  }, []);

  return (
    <div className="bg-black text-green-400 p-6 font-mono border-2 border-green-900 rounded-lg shadow-2xl">
      <div className="flex justify-between items-center mb-4 border-b border-green-900 pb-2">
        <h2 className="text-xl font-bold tracking-widest">SMOS v2 || NEURAL VITRINE</h2>
        <span className={`text-xs px-2 py-1 rounded ${status.includes("Connected") ? "bg-green-900" : "bg-red-900"}`}>
          {status}
        </span>
      </div>

      <div className="h-96 overflow-y-auto space-y-2 scrollbar-thin scrollbar-thumb-green-900">
        {events.length === 0 && <p className="text-green-800 italic">Waiting for swarm signals...</p>}
        {events.map((ev, i) => (
          <div key={i} className="text-sm border-l-2 border-green-800 pl-3 py-1 hover:bg-green-950 transition-colors">
            <span className="text-green-700">[{new Date(ev.timestamp).toLocaleTimeString()}]</span>{" "}
            <span className="text-white font-bold">{ev.type}</span>: {ev.message}
            {ev.metadata?.score && (
              <div className="mt-1 bg-green-900/30 rounded px-2 py-1 w-fit">
                <span className="text-xs">Similarity Index: {(ev.metadata.score * 100).toFixed(2)}%</span>
              </div>
            )}
          </div>
        ))}
      </div>

      <div className="mt-4 pt-4 border-t border-green-900 flex gap-4 text-[10px] text-green-700 uppercase tracking-tighter">
        <span>A2A Pipe: Active</span>
        <span>CFO Audit: Constitutional</span>
        <span>GKE Snapshots: Warm</span>
      </div>
    </div>
  );
};

export default SwarmDashboard;
