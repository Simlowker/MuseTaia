"use client";

import { useEffect, useRef, useCallback } from 'react';

type EventHandler = (payload: any) => void;

export function useSSE(url: string) {
  const eventSourceRef = useRef<EventSource | null>(null);
  const handlersRef = useRef<Map<string, Set<EventHandler>>>(new Map());

  useEffect(() => {
    const connect = () => {
      try {
        eventSourceRef.current = new EventSource(url);

        eventSourceRef.current.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data);
            const handlers = handlersRef.current.get(data.type);
            if (handlers) {
              handlers.forEach(handler => handler(data.metadata || data));
            }
          } catch (e) {
            console.error('[useSSE] Parse error:', e);
          }
        };

        eventSourceRef.current.onerror = () => {
          console.log('[useSSE] Connection error, retrying in 5s...');
          eventSourceRef.current?.close();
          setTimeout(connect, 5000);
        };
      } catch (e) {
        console.error('[useSSE] Failed to connect:', e);
      }
    };

    connect();

    return () => {
      eventSourceRef.current?.close();
    };
  }, [url]);

  const subscribe = useCallback((eventType: string, handler: EventHandler) => {
    if (!handlersRef.current.has(eventType)) {
      handlersRef.current.set(eventType, new Set());
    }
    handlersRef.current.get(eventType)!.add(handler);

    return () => {
      handlersRef.current.get(eventType)?.delete(handler);
    };
  }, []);

  return { subscribe };
}