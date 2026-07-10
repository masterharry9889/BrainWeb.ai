"use client";

import Link from 'next/link';
import { Settings, MessageSquare, Network, PenTool, Home, Bot } from 'lucide-react';
import { usePathname } from 'next/navigation';
import { use } from 'react';

export default function ProjectLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: Promise<{ id: string }>;
}) {
  const resolvedParams = use(params);
  const projectId = resolvedParams.id;
  const pathname = usePathname();

  return (
    <>
      <nav className="notch-navbar glass">
        <Link href="/" className="notch-icon-btn" style={{ marginLeft: '0.5rem', marginRight: '0.5rem' }} title="Dashboard">
          <Home size={18} />
        </Link>
        <div className="notch-links">
          <Link href={`/project/${projectId}/chat`} className={`notch-link ${pathname.includes('/chat') ? 'active' : ''}`} title="Chat Console">
            <MessageSquare size={18} />
            <span className="notch-text">Chat</span>
          </Link>
          <Link href={`/project/${projectId}/graph`} className={`notch-link ${pathname.includes('/graph') ? 'active' : ''}`} title="Knowledge Graph">
            <Network size={18} />
            <span className="notch-text">Graph</span>
          </Link>
          <Link href={`/project/${projectId}/canvas`} className={`notch-link ${pathname.includes('/canvas') ? 'active' : ''}`} title="Canvas">
            <PenTool size={18} />
            <span className="notch-text">Canvas</span>
          </Link>
          <div className="notch-separator" style={{ width: '1px', height: '24px', background: 'var(--glass-border)', margin: '0 0.5rem' }}></div>
          <Link href={`/project/${projectId}/agents`} className={`notch-link ${pathname.includes('/agents') ? 'active' : ''}`} title="Active Agents">
            <Bot size={18} />
            <span className="notch-text">Agents</span>
          </Link>
        </div>
        <Link href="/settings" className="notch-icon-btn" title="Settings">
          <Settings size={18} />
        </Link>
      </nav>
      {children}
    </>
  );
}
