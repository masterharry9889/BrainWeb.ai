import React from 'react';
import { X, Save, Trash2, Link as LinkIcon, GitMerge } from 'lucide-react';

interface NodeEditorPanelProps {
  editMode: boolean;
  panelOpen: boolean;
  selectedNode: any;
  closePanel: () => void;
  editLabel: string;
  setEditLabel: (val: string) => void;
  editType: string;
  setEditType: (val: string) => void;
  handleUpdateNode: () => void;
  handleDeleteNode: () => void;
  setConnectSource: (node: any) => void;
  setMergeSource: (node: any) => void;
  setPanelOpen: (val: boolean) => void;
}

export default function NodeEditorPanel({
  editMode,
  panelOpen,
  selectedNode,
  closePanel,
  editLabel,
  setEditLabel,
  editType,
  setEditType,
  handleUpdateNode,
  handleDeleteNode,
  setConnectSource,
  setMergeSource,
  setPanelOpen
}: NodeEditorPanelProps) {
  if (!editMode || !panelOpen || !selectedNode) return null;

  return (
    <div style={{
      position: 'absolute', top: '1rem', right: '1rem', width: '320px',
      background: 'rgba(15, 17, 21, 0.85)', backdropFilter: 'blur(12px)',
      border: '1px solid var(--glass-border)', borderRadius: '16px',
      padding: '1.5rem', color: 'white', boxShadow: '0 8px 32px rgba(0,0,0,0.5)',
      display: 'flex', flexDirection: 'column', gap: '1rem'
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h3 style={{ margin: 0, fontSize: '1.1rem', fontWeight: 600 }}>Edit Node</h3>
        <button onClick={closePanel} style={{ background: 'none', border: 'none', color: '#94a3b8', cursor: 'pointer' }}><X size={18} /></button>
      </div>
      
      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
        <label style={{ fontSize: '0.85rem', color: '#94a3b8' }}>Label</label>
        <input 
          type="text" 
          value={editLabel} 
          onChange={e => setEditLabel(e.target.value)}
          style={{
            background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.1)',
            padding: '0.75rem', borderRadius: '8px', color: 'white', fontSize: '0.95rem'
          }}
        />
      </div>
      
      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
        <label style={{ fontSize: '0.85rem', color: '#94a3b8' }}>Type</label>
        <input 
          type="text" 
          value={editType} 
          onChange={e => setEditType(e.target.value)}
          style={{
            background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.1)',
            padding: '0.75rem', borderRadius: '8px', color: 'white', fontSize: '0.95rem'
          }}
        />
      </div>
      
      <div style={{ display: 'flex', gap: '0.5rem', marginTop: '0.5rem' }}>
        <button onClick={handleUpdateNode} style={{
          flex: 1, display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '0.5rem',
          background: 'var(--primary)', border: 'none', padding: '0.75rem', borderRadius: '8px',
          color: 'white', fontWeight: 600, cursor: 'pointer'
        }}>
          <Save size={16} /> Save
        </button>
        <button onClick={handleDeleteNode} style={{
          padding: '0.75rem', background: 'rgba(239, 68, 68, 0.1)', border: '1px solid rgba(239, 68, 68, 0.2)',
          borderRadius: '8px', color: '#ef4444', cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center'
        }}>
          <Trash2 size={16} />
        </button>
      </div>
      
      <hr style={{ border: 'none', borderTop: '1px solid rgba(255,255,255,0.1)', margin: '0.5rem 0' }} />
      
      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
        <button 
          onClick={() => { setConnectSource(selectedNode); setPanelOpen(false); }}
          style={{
            display: 'flex', alignItems: 'center', gap: '0.5rem', padding: '0.75rem',
            background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.1)',
            borderRadius: '8px', color: '#e2e8f0', cursor: 'pointer', transition: 'all 0.2s'
          }}
        >
          <LinkIcon size={16} color="#fbbf24" /> Create Connection...
        </button>
        <button 
          onClick={() => { setMergeSource(selectedNode); setPanelOpen(false); }}
          style={{
            display: 'flex', alignItems: 'center', gap: '0.5rem', padding: '0.75rem',
            background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.1)',
            borderRadius: '8px', color: '#e2e8f0', cursor: 'pointer', transition: 'all 0.2s'
          }}
        >
          <GitMerge size={16} color="#f87171" /> Merge Into...
        </button>
      </div>
    </div>
  );
}
