import React from 'react';
import { X, MessageCircle, Upload } from 'lucide-react';

interface CreateProjectModalProps {
  isModalOpen: boolean;
  setIsModalOpen: (val: boolean) => void;
  projectType: 'conversation' | 'upload';
  setProjectType: (val: 'conversation' | 'upload') => void;
  projectName: string;
  setProjectName: (val: string) => void;
  setSelectedFiles: (files: FileList | null) => void;
  handleCreateProject: () => void;
  isUploading: boolean;
}

export default function CreateProjectModal({
  isModalOpen,
  setIsModalOpen,
  projectType,
  setProjectType,
  projectName,
  setProjectName,
  setSelectedFiles,
  handleCreateProject,
  isUploading
}: CreateProjectModalProps) {
  if (!isModalOpen) return null;

  return (
    <div style={{
      position: 'fixed',
      top: 0, left: 0, right: 0, bottom: 0,
      background: 'rgba(0,0,0,0.6)',
      backdropFilter: 'blur(4px)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 100
    }}>
      <div className="glass" style={{ width: '100%', maxWidth: '500px', padding: '2rem', animation: 'slideUp 0.3s ease' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
          <h2 style={{ margin: 0, fontSize: '1.5rem' }}>Create New</h2>
          <button 
            onClick={() => setIsModalOpen(false)}
            style={{ background: 'none', border: 'none', color: 'var(--text-secondary)', cursor: 'pointer' }}
          >
            <X size={24} />
          </button>
        </div>
        
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '2rem' }}>
          <div 
            onClick={() => setProjectType('conversation')}
            style={{ 
              padding: '1.5rem 1rem', 
              borderRadius: '12px', 
              border: projectType === 'conversation' ? '2px solid var(--primary)' : '2px solid rgba(255,255,255,0.1)',
              background: projectType === 'conversation' ? 'rgba(99, 102, 241, 0.1)' : 'rgba(0,0,0,0.2)',
              cursor: 'pointer',
              textAlign: 'center',
              transition: 'all 0.2s'
            }}
          >
            <MessageCircle size={32} color={projectType === 'conversation' ? 'var(--primary)' : 'var(--text-secondary)'} style={{ margin: '0 auto 0.75rem' }} />
            <div style={{ fontWeight: 600, color: projectType === 'conversation' ? 'white' : 'var(--text-secondary)' }}>Independent Conversation</div>
          </div>
          
          <div 
            onClick={() => setProjectType('upload')}
            style={{ 
              padding: '1.5rem 1rem', 
              borderRadius: '12px', 
              border: projectType === 'upload' ? '2px solid var(--secondary)' : '2px solid rgba(255,255,255,0.1)',
              background: projectType === 'upload' ? 'rgba(236, 72, 153, 0.1)' : 'rgba(0,0,0,0.2)',
              cursor: 'pointer',
              textAlign: 'center',
              transition: 'all 0.2s'
            }}
          >
            <Upload size={32} color={projectType === 'upload' ? 'var(--secondary)' : 'var(--text-secondary)'} style={{ margin: '0 auto 0.75rem' }} />
            <div style={{ fontWeight: 600, color: projectType === 'upload' ? 'white' : 'var(--text-secondary)' }}>Upload New Project</div>
          </div>
        </div>

        <div style={{ marginBottom: '2rem' }}>
          <label className="input-label">Name</label>
          <input 
            type="text" 
            className="input-field" 
            placeholder={projectType === 'conversation' ? "e.g. Chat with Codebase" : "e.g. Q3 Marketing Plan"}
            value={projectName}
            onChange={e => setProjectName(e.target.value)}
            autoFocus
            onKeyDown={e => e.key === 'Enter' && handleCreateProject()}
          />
        </div>
        
        {projectType === 'upload' && (
          <div style={{ marginBottom: '2rem' }}>
            <label className="input-label">Select Files to Analyze</label>
            <input 
              type="file" 
              multiple
              onChange={e => setSelectedFiles(e.target.files)}
              style={{
                width: '100%',
                padding: '1rem',
                background: 'rgba(255,255,255,0.05)',
                border: '1px dashed rgba(255,255,255,0.2)',
                borderRadius: '8px',
                color: 'white'
              }}
            />
          </div>
        )}
        
        <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '1rem' }}>
          <button className="btn btn-secondary" onClick={() => setIsModalOpen(false)} disabled={isUploading}>Cancel</button>
          <button className="btn" onClick={handleCreateProject} disabled={!projectName.trim() || isUploading}>
            {isUploading ? 'Uploading...' : 'Create'}
          </button>
        </div>
      </div>
    </div>
  );
}
