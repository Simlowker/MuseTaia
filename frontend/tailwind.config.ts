import type { Config } from "tailwindcss";

const config: Config = {
    content: [
        "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
        "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
        "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
    ],
    theme: {
        extend: {
            colors: {
                background: "#000000",
                foreground: "#ededed",
                void: "#000000",
                onyx: "#0A0A0A",
                obsidian: "#1A1A1A",
                gold: "#D4AF37",
                cyan: "#00D4FF",
                amber: "#FF9500",
                emerald: "#00FF88",
                ruby: "#FF3366",
                "glass-bg": "rgba(255, 255, 255, 0.03)",
                "glass-border": "rgba(255, 255, 255, 0.08)",
            },
            fontFamily: {
                luxe: ["var(--font-luxe)", "sans-serif"],
            },
        },
    },
    plugins: [],
};
export default config;
