import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "SMOS v2 | Living Dashboard",
  description: "Autonomous Sovereign Muse Operating System",
};

import { NeuralProvider } from "@/context/NeuralContext";
import { MoodProvider } from "@/context/MoodContext";
import { TrendProvider } from "@/context/TrendContext";

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className={`${inter.className} antialiased bg-void text-foreground overflow-hidden`}>
        <MoodProvider>
          <NeuralProvider>
            <TrendProvider>
              {children}
            </TrendProvider>
          </NeuralProvider>
        </MoodProvider>
      </body>
    </html>
  );
}
