export interface Mood {
    valence: number;
    arousal: number;
    dominance: number;
    current_state: string;
}

export interface Wallet {
    address: string;
    balance: number;
    internal_usd_balance: number;
    daily_spend: number;
    daily_budget: number;
    currency: string;
}

export interface ViralVelocity {
    score: number;
    acceleration: string;
    engagement_rate: number;
}

export interface TrendReport {
    topic: string;
    vvs: ViralVelocity;
    platform: string;
    timestamp: string;
}

export interface Signal {
    id: string;
    source: string;
    content: string;
    score: number;
}

export interface Production {
    id: string;
    title: string;
    status: 'planning' | 'scripting' | 'visualizing' | 'rendering' | 'qa' | 'published';
    progress: number;
    thumbnail_url?: string;
    eta_seconds?: number;
}

export interface AgentStatus {
    name: string;
    status: 'idle' | 'working' | 'waiting' | 'error';
    current_task?: string;
}

export interface PipelineState {
    active_stage: string;
    gates: {
        trend: boolean;
        strategist: boolean;
        cfo: boolean;
        hlp: boolean;
        swarm: boolean;
    };
}

export interface Proposal {
    id: string;
    description: string;
    cost_estimate: number;
    confidence: number;
    variants: string[];
}
