import { useEffect, useRef, useState } from 'react';

type SSEHandler = (data: any) => void;

export function useSSE(endpoint: string) {
    const [status, setStatus] = useState<'connecting' | 'connected' | 'error'>('connecting');
    const eventSourceRef = useRef<EventSource | null>(null);
    const handlersRef = useRef<Map<string, SSEHandler>>(new Map());

    useEffect(() => {
        const source = new EventSource(endpoint);
        eventSourceRef.current = source;

        source.onopen = () => setStatus('connected');
        source.onerror = () => setStatus('error');

        // Setup generic listener to route events
        const routeEvent = (event: MessageEvent) => {
            try {
                const data = JSON.parse(event.data);
                const type = data.type || 'message';
                const handler = handlersRef.current.get(type);
                if (handler) handler(data.payload);
            } catch (e) {
                console.error('SSE Parse Error', e);
            }
        };

        source.addEventListener('message', routeEvent);
        // Also listen for specific named events if backend sends them as separate event types
        ['MOOD_UPDATE', 'TREND_DETECTED', 'PRODUCTION_UPDATE', 'WALLET_UPDATE'].forEach(type => {
             source.addEventListener(type, routeEvent);
        });

        return () => {
            source.close();
        };
    }, [endpoint]);

    const subscribe = (eventType: string, handler: SSEHandler) => {
        handlersRef.current.set(eventType, handler);
        return () => {
            handlersRef.current.delete(eventType);
        };
    };

    return { status, subscribe };
}
