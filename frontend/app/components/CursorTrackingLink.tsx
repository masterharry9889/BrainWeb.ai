"use client";

import { useState, useEffect } from 'react';
import { createPortal } from 'react-dom';
import { Globe, Network } from 'lucide-react';

interface CursorTrackingLinkProps extends React.AnchorHTMLAttributes<HTMLAnchorElement> {
  href?: string;
  children?: React.ReactNode;
}

export default function CursorTrackingLink({ href, children, ...props }: CursorTrackingLinkProps) {
  const [isHovered, setIsHovered] = useState(false);
  const [coords, setCoords] = useState({ x: 0, y: 0 });
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  const handleMouseEnter = () => setIsHovered(true);
  const handleMouseLeave = () => setIsHovered(false);
  const handleMouseMove = (e: React.MouseEvent) => {
    setCoords({ x: e.clientX, y: e.clientY });
  };

  const isInternalGraphLink = href?.includes('/graph');

  return (
    <>
      <a 
        href={href} 
        {...props}
        onMouseEnter={handleMouseEnter}
        onMouseLeave={handleMouseLeave}
        onMouseMove={handleMouseMove}
        className="agent-inline-link"
        target={href?.startsWith('http') ? '_blank' : undefined}
        rel="noopener noreferrer"
      >
        {children}
      </a>

      {mounted && isHovered && createPortal(
        <div 
          className="cursor-preview-card glass"
          style={{
            position: 'fixed',
            left: coords.x + 20,
            top: coords.y + 20,
            zIndex: 99999,
            pointerEvents: 'none',
            padding: '1rem',
            borderRadius: '16px',
            display: 'flex',
            alignItems: 'center',
            gap: '1rem',
            animation: 'fadeIn 0.2s ease-out forwards',
            boxShadow: '0 10px 40px rgba(0, 0, 0, 0.4)'
          }}
        >
          <div style={{ background: 'rgba(99, 102, 241, 0.1)', padding: '0.5rem', borderRadius: '50%' }}>
             {isInternalGraphLink ? <Network size={24} color="var(--primary)" /> : <Globe size={24} color="var(--primary)" />}
          </div>
          <div style={{ display: 'flex', flexDirection: 'column' }}>
            <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.05em', fontWeight: 600 }}>
              {isInternalGraphLink ? 'Knowledge Node' : 'External Link'}
            </span>
            <span style={{ fontSize: '0.9rem', maxWidth: '250px', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
              {href}
            </span>
          </div>
        </div>,
        document.body
      )}
    </>
  );
}
