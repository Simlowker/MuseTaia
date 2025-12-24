import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "SMOS v2",
  description: "Fresh Start",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        {children}
      </body>
    </html>
  );
}