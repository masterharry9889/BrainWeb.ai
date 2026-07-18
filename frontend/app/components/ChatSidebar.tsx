import React from 'react';
import { Plus, Edit2, Trash2, Check } from 'lucide-react';

export interface Chat {
  id: string;
  name: string;
}

interface ChatSidebarProps {
  chats: Chat[];
  activeChatId: string;
  setActiveChatId: (id: string) => void;
  editingChatId: string | null;
  editingChatName: string;
  setEditingChatName: (name: string) => void;
  saveRenameChat: (e?: React.MouseEvent | React.KeyboardEvent) => void;
  startRenameChat: (chat: Chat, e: React.MouseEvent) => void;
  deleteChat: (id: string, e: React.MouseEvent) => void;
  createNewChat: () => void;
}

export default function ChatSidebar({
  chats,
  activeChatId,
  setActiveChatId,
  editingChatId,
  editingChatName,
  setEditingChatName,
  saveRenameChat,
  startRenameChat,
  deleteChat,
  createNewChat
}: ChatSidebarProps) {
  return (
    <div className="sidebar" style={{ width: '260px', borderRight: '1px solid var(--glass-border)', display: 'flex', flexDirection: 'column', background: 'var(--bg-secondary)', padding: '1.5rem', zIndex: 10 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <h2 style={{ fontSize: '1.2rem', margin: 0, fontFamily: 'Outfit', fontWeight: 600, color: 'white' }}>Chats</h2>
        <button className="notch-icon-btn" style={{ margin: 0, width: '32px', height: '32px' }} onClick={createNewChat} title="New Chat">
          <Plus size={18} />
        </button>
      </div>
      <div style={{ flex: 1, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
        {chats.map(chat => (
          <div 
            key={chat.id} 
            onClick={() => setActiveChatId(chat.id)}
            style={{ 
              padding: '0.75rem', 
              borderRadius: '8px', 
              background: activeChatId === chat.id ? 'rgba(255,255,255,0.08)' : 'transparent',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              transition: 'all 0.2s ease',
              borderLeft: activeChatId === chat.id ? '2px solid var(--primary)' : '2px solid transparent',
              color: activeChatId === chat.id ? 'var(--text-primary)' : 'var(--text-secondary)'
            }}
            onMouseEnter={(e) => { if(activeChatId !== chat.id) e.currentTarget.style.background = 'rgba(255,255,255,0.05)'; }}
            onMouseLeave={(e) => { if(activeChatId !== chat.id) e.currentTarget.style.background = 'transparent'; }}
          >
            {editingChatId === chat.id ? (
              <div style={{ display: 'flex', alignItems: 'center', width: '100%', gap: '0.5rem' }}>
                <input 
                  autoFocus
                  value={editingChatName}
                  onChange={(e) => setEditingChatName(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && saveRenameChat(e)}
                  onBlur={() => saveRenameChat()}
                  onClick={(e) => e.stopPropagation()}
                  style={{ flex: 1, width: '100%', background: '#000', border: '1px solid var(--primary)', color: 'white', padding: '0.25rem 0.5rem', borderRadius: '4px', outline: 'none', fontSize: '0.9rem' }}
                />
                <button onClick={saveRenameChat} style={{ background: 'none', border: 'none', color: 'var(--success)', cursor: 'pointer', padding: 0 }}><Check size={16} /></button>
              </div>
            ) : (
              <>
                <div style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', flex: 1, fontWeight: 500, fontSize: '0.95rem' }}>
                  {chat.name}
                </div>
                <div style={{ display: 'flex', gap: '0.4rem', opacity: activeChatId === chat.id ? 1 : 0.5, transition: 'opacity 0.2s' }}>
                  <button onClick={(e) => startRenameChat(chat, e)} style={{ background: 'none', border: 'none', color: 'inherit', cursor: 'pointer', padding: '0.1rem' }} title="Rename">
                    <Edit2 size={14} style={{ transition: 'color 0.2s' }} onMouseEnter={e => e.currentTarget.style.color = 'var(--primary)'} onMouseLeave={e => e.currentTarget.style.color = 'inherit'} />
                  </button>
                  <button onClick={(e) => deleteChat(chat.id, e)} style={{ background: 'none', border: 'none', color: 'inherit', cursor: 'pointer', padding: '0.1rem' }} title="Delete">
                    <Trash2 size={14} style={{ transition: 'color 0.2s' }} onMouseEnter={e => e.currentTarget.style.color = '#ef4444'} onMouseLeave={e => e.currentTarget.style.color = 'inherit'} />
                  </button>
                </div>
              </>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
