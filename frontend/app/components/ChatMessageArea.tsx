import React from 'react';
import { Send, Bot, User } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import CursorTrackingLink from '@/app/components/CursorTrackingLink';

export interface Message {
  id: string;
  role: 'user' | 'agent';
  content: string;
  status?: 'streaming' | 'finished' | 'error';
  agentName?: string;
  parsedData?: any;
}

interface ChatMessageAreaProps {
  messages: Message[];
  input: string;
  setInput: (input: string) => void;
  handleSend: () => void;
  isProcessing: boolean;
  messagesEndRef: React.RefObject<HTMLDivElement | null>;
}

export default function ChatMessageArea({
  messages,
  input,
  setInput,
  handleSend,
  isProcessing,
  messagesEndRef
}: ChatMessageAreaProps) {
  return (
    <div className="chat-container" style={{ flex: 1, padding: '2rem 10%', height: 'calc(100vh - 5rem)', position: 'relative' }}>
      <div className="chat-messages" style={{ height: 'calc(100% - 80px)' }}>
        {messages.length === 0 && (
          <div style={{ margin: 'auto', textAlign: 'center', color: 'var(--text-secondary)' }}>
            <Bot size={48} style={{ margin: '0 auto 1rem', opacity: 0.5 }} />
            <h3>Select an agent and start chatting</h3>
          </div>
        )}
        
        {messages.map(msg => (
          <div key={msg.id} className={`chat-message ${msg.role}`}>
            <div className={`avatar ${msg.role}`}>
              {msg.role === 'user' ? <User size={20} color="white" /> : <Bot size={20} color="white" />}
            </div>
            <div className="message-bubble">
              <div className={`markdown-body ${msg.role}`}>
                <ReactMarkdown 
                  remarkPlugins={[remarkGfm]}
                  components={{
                    a: CursorTrackingLink
                  }}
                >
                  {msg.content.replace(/```json[\s\S]*?```/g, '').trim()}
                </ReactMarkdown>
              </div>
              {msg.role === 'agent' && msg.status === 'streaming' && (
                <span style={{ display: 'inline-block', width: '8px', height: '16px', background: 'var(--primary)', marginLeft: '4px', animation: 'pulse 1s infinite' }} />
              )}
              {msg.parsedData && msg.parsedData.entities && msg.parsedData.entities.length > 0 && (
                <div style={{ marginTop: '1rem', padding: '0.75rem', background: 'rgba(0,0,0,0.2)', borderRadius: '8px', fontSize: '0.85rem' }}>
                  <strong>Extracted Entities:</strong>
                  <ul style={{ margin: '0.5rem 0 0 1.5rem' }}>
                    {msg.parsedData.entities.map((e: any, i: number) => (
                      <li key={i}>{e.label} <span style={{ color: 'var(--text-secondary)' }}>({e.type})</span></li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input-area" style={{ position: 'absolute', bottom: '2rem', left: '10%', right: '10%' }}>
        <input 
          type="text" 
          className="chat-input" 
          placeholder="Type your request here..." 
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && handleSend()}
          disabled={isProcessing}
        />
        <button 
          className="send-btn" 
          onClick={handleSend}
          disabled={isProcessing || !input.trim()}
        >
          <Send size={18} />
        </button>
      </div>
    </div>
  );
}
