"use client";

import React, { createContext, useContext, useState, useEffect } from 'react';

export interface TrendItem {
    id: string;
    title: string;
    category: string;
    imageUrl?: string;
    score: number;
}

interface TrendContextType {
    trends: TrendItem[];
    loading: boolean;
    refreshTrends: () => void;
}

const TrendContext = createContext<TrendContextType | undefined>(undefined);

// Mock Data Service
const fetchMockTrends = async (): Promise<TrendItem[]> => {
    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 800));

    return [
        { id: '1', title: 'Sustainable Mycofabrication', category: 'Materials', score: 98, imageUrl: 'bg-emerald-900' },
        { id: '2', title: 'Neo-Brutalist Furniture', category: 'Design', score: 85, imageUrl: 'bg-stone-800' },
        { id: '3', title: 'Analog Photography Revival', category: 'Culture', score: 92, imageUrl: 'bg-amber-900' },
        { id: '4', title: 'Hyper-Local Agriculture', category: 'Food', score: 78, imageUrl: 'bg-green-900' },
        { id: '5', title: 'Digital Detox Retreats', category: 'Wellness', score: 88, imageUrl: 'bg-sky-900' },
    ];
};

export const TrendProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [trends, setTrends] = useState<TrendItem[]>([]);
    const [loading, setLoading] = useState(true);

    const refreshTrends = async () => {
        setLoading(true);
        try {
            const data = await fetchMockTrends();
            setTrends(data);
        } catch (err) {
            console.error("Failed to fetch trends", err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        refreshTrends();
    }, []);

    return (
        <TrendContext.Provider value={{ trends, loading, refreshTrends }}>
            {children}
        </TrendContext.Provider>
    );
};

export const useTrends = () => {
    const context = useContext(TrendContext);
    if (!context) throw new Error("useTrends must be used within a TrendProvider");
    return context;
};
