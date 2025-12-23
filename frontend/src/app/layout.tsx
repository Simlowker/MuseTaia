import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import "@/styles/sovereign.css";
import { NeuralProvider } from "@/context/NeuralContext";
import { MoodProvider } from "@/context/MoodContext";
import { AmbientBackground } from "@/components/layout/AmbientBackground";
import { TrendProvider } from "@/context/TrendContext";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "SMOS v2 | Sovereign Vitrine",
  description: "Autonomous Digital Entity Swarm Controller",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark h-full w-full">
      <body className={`${inter.className} antialiased h-full w-full overflow-hidden bg-black text-white`}>
        <MoodProvider>
          <NeuralProvider>
            <TrendProvider>
              <AmbientBackground />
              <main className="relative z-10 w-full h-full">
                {children}
              </main>
            </TrendProvider>
          </NeuralProvider>
        </MoodProvider>
      </body>
    </html>
  );
}
