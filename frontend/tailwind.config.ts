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
                background: "var(--background)",
                foreground: "var(--foreground)",
                void: "var(--void)",
                onyx: "var(--onyx)",
                obsidian: "var(--obsidian)",
                gold: "var(--sovereign-gold)",
                cyan: "var(--neural-cyan)",
                amber: "var(--alert-amber)",
                emerald: "var(--success-emerald)",
                ruby: "var(--danger-ruby)",
                "glass-bg": "var(--glass-bg)",
                "glass-border": "var(--glass-border)",
            },
            fontFamily: {
                luxe: ["var(--font-luxe)", "sans-serif"],
            },
        },
    },
    plugins: [],
};
export default config;
