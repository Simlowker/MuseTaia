import type { Metadata } from "next";
import { MoodProvider } from "@/context/MoodContext";
import Layout from "@/components/Layout";

export const metadata: Metadata = {
  title: "Sovereign Muse OS (SMOS)",
  description: "Autonomous Content Engine (ACE) - Swarm Management",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <MoodProvider>
          <Layout>
            {children}
          </Layout>
        </MoodProvider>
      </body>
    </html>
  );
}