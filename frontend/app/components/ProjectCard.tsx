import React from 'react';
import { Trash2, MessageCircle, Upload, ArrowRight } from 'lucide-react';

export interface Project {
  id: string;
  name: string;
  date: string;
  type: 'conversation' | 'upload';
}

interface ProjectCardProps {
  project: Project;
  onDelete: (id: string, e: React.MouseEvent) => void;
}

export default function ProjectCard({ project: p, onDelete }: ProjectCardProps) {
  return (
    <div 
      onClick={() => window.location.href = `./project/view/chat/index.html?id=${p.id}`}
      className="glass" 
      style={{ 
        padding: '1.5rem', 
        cursor: 'pointer',
        transition: 'transform 0.2s, background 0.2s',
        display: 'flex',
        flexDirection: 'column',
        gap: '1rem'
      }}
      onMouseEnter={e => e.currentTarget.style.transform = 'translateY(-4px)'}
      onMouseLeave={e => e.currentTarget.style.transform = 'translateY(0)'}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <h3 style={{ margin: 0, fontSize: '1.2rem', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', paddingRight: '1rem' }}>{p.name}</h3>
        <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'center' }}>
          <button 
            onClick={(e) => onDelete(p.id, e)}
            style={{ background: 'transparent', border: 'none', color: 'var(--text-secondary)', cursor: 'pointer', padding: 0, display: 'flex', alignItems: 'center', transition: 'color 0.2s' }}
            onMouseEnter={(e) => e.currentTarget.style.color = '#ef4444'}
            onMouseLeave={(e) => e.currentTarget.style.color = 'var(--text-secondary)'}
            title="Delete Project"
          >
            <Trash2 size={18} />
          </button>
          {p.type === 'conversation' ? <MessageCircle size={20} color="var(--primary)" /> : <Upload size={20} color="var(--secondary)" />}
        </div>
      </div>
      <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: 'auto' }}>
        <span>Created {p.date}</span>
        <ArrowRight size={16} />
      </div>
    </div>
  );
}
