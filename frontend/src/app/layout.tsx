import type { Metadata } from "next";
import { Inter, JetBrains_Mono } from "next/font/google";
import "./globals.css";
import { NeuralProvider } from "@/context/NeuralContext";
import { MoodProvider } from "@/context/MoodContext";
import { TrendProvider } from "@/context/TrendContext";
import SmoothScroll from "@/components/providers/SmoothScroll";
import { AmbientBackground } from "@/components/vfx/AmbientBackground";

const inter = Inter({ 
  subsets: ["latin"],
  variable: "--font-inter",
});

const jetbrains = JetBrains_Mono({
  subsets: ["latin"],
  variable: "--font-mono",
});

export const metadata: Metadata = {
  title: "SMOS v2 | Living Dashboard",
  description: "Autonomous Sovereign Muse Operating System",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className={`${inter.variable} ${jetbrains.variable} font-sans antialiased bg-void text-foreground overflow-hidden`}>
        <SmoothScroll>
          <MoodProvider>
            <NeuralProvider>
              <TrendProvider>
                <AmbientBackground />
                <div className="relative z-10">
                  {children}
                </div>
              </TrendProvider>
            </NeuralProvider>
          </MoodProvider>
        </SmoothScroll>
      </body>
    </html>
  );
}