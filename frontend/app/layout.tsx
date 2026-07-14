import type { Metadata } from "next";
import { Inter, Outfit } from "next/font/google";
import "./globals.css";
import Link from 'next/link';
import { Settings, MessageSquare, Network, PenTool } from 'lucide-react';

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });
const outfit = Outfit({ subsets: ["latin"], variable: "--font-outfit" });

export const metadata: Metadata = {
  title: "BrainWeb.ai - AI Orchestration",
  description: "Enterprise Multi-Agent Orchestration Engine",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${inter.variable} ${outfit.variable}`} suppressHydrationWarning>
        <div className="app-container" suppressHydrationWarning>
          <main className="main-content">
            {children}
          </main>
        </div>
      </body>
    </html>
  );
}
