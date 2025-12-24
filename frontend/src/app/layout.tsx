import type { Metadata } from "next";
import "./globals.css";
import "@/styles/luxe-theme.css";
import { SystemProvider } from "@/contexts/system-context";
import { MoodProvider } from "@/context/MoodContext";
import { NeuralProvider } from "@/context/NeuralContext";
import { TrendProvider } from "@/context/TrendContext";

export const metadata: Metadata = {
  title: "SMOS v2 | Sovereign Muse",
  description: "Autonomous Digital Muse Operating System",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased font-sans">
        <SystemProvider>
          <MoodProvider>
            <NeuralProvider>
              <TrendProvider>
                {children}
              </TrendProvider>
            </NeuralProvider>
          </MoodProvider>
        </SystemProvider>
      </body>
    </html>
  );
}
