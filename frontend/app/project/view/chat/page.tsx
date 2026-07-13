"use client";

import { useState, useEffect, useRef, use } from 'react';
import { Send, Bot, User, ArrowLeft } from 'lucide-react';
import { useRouter } from 'next/navigation';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import CursorTrackingLink from '@/app/components/CursorTrackingLink';

const API_BASE = 'http://127.0.0.1:8000';
const WS_BASE = 'ws://127.0.0.1:8000';

interface Agent {
  id: string;
  name: string;
  description: string;
}

interface Message {
  id: string;
  role: 'user' | 'agent';
  content: string;
  status?: 'streaming' | 'finished' | 'error';
  agentName?: string;
  parsedData?: any;
}

export default function ChatView() {
  const [projectId, setProjectId] = useState<string | null>(null);

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    setProjectId(params.get('id'));
  }, []);

  const router = useRouter();

  const [agents, setAgents] = useState<Agent[]>([]);
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoaded, setIsLoaded] = useState(false);

  if (!projectId) return null;

  const [input, setInput] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const storageKey = `ingot_chat_${projectId}`;

  useEffect(() => {
    const saved = localStorage.getItem(storageKey);
    if (saved) {
      try {
        // Clean up any streaming states that might have been interrupted by a page reload
        const parsed = JSON.parse(saved);
        const cleaned = parsed.map((m: Message) => 
          m.status === 'streaming' ? { ...m, status: 'error', content: m.content + '\n[Connection interrupted]' } : m
        );
        setMessages(cleaned);
      } catch (e) {
        console.error("Failed to parse saved chat history");
      }
    }
    setIsLoaded(true);
  }, [storageKey]);

  useEffect(() => {
    if (isLoaded) {
      localStorage.setItem(storageKey, JSON.stringify(messages));
    }
  }, [messages, isLoaded, storageKey]);

  useEffect(() => {
    fetch(`${API_BASE}/agents`)
      .then(res => res.json())
      .then(data => {
        setAgents(data);
      })
      .catch(err => console.error("Failed to load agents", err));
  }, []);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    const activeAgentsKey = `ingot_active_agents_${projectId}`;
    const savedAgents = localStorage.getItem(activeAgentsKey);
    let activeAgentsToRun: string[] = [];
    if (savedAgents) {
      try {
        activeAgentsToRun = JSON.parse(savedAgents);
      } catch (e) {}
    }
    
    if (activeAgentsToRun.length === 0) {
       if (agents.length > 0) {
         activeAgentsToRun = [agents[0].id];
       } else {
         alert("Cannot connect to the backend server. Please make sure your API server is running (uvicorn backend.main:app) and refresh the page.");
         return; // no agents available
       }
    }

    if (!input.trim() || isProcessing) return;

    const userMsgId = Date.now().toString();
    
    const newAgentMessages = activeAgentsToRun.map((agentId, index) => ({
      id: `${Date.now() + 1 + index}`,
      role: 'agent' as const,
      content: '',
      status: 'streaming' as const,
      agentName: agents.find(a => a.id === agentId)?.name || agentId
    }));

    setMessages(prev => [
      ...prev,
      { id: userMsgId, role: 'user', content: input },
      ...newAgentMessages
    ]);
    
    const currentInput = input;
    setInput('');
    setIsProcessing(true);

    let finishedCount = 0;
    const checkAllFinished = () => {
      finishedCount++;
      if (finishedCount === activeAgentsToRun.length) {
        setIsProcessing(false);
      }
    };

    activeAgentsToRun.forEach(async (agentId, index) => {
      const agentMsgId = newAgentMessages[index].id;
      try {
        const res = await fetch(`${API_BASE}/agents/run`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            agent_id: agentId,
            project_id: projectId,
            input: { query: currentInput } 
          })
        });

        if (!res.ok) {
          if (res.status === 403) throw new Error("API Key not configured. Please configure it in the Dashboard.");
          throw new Error(`Failed to start agent ${agentId}`);
        }

        const { run_id } = await res.json();
        
        const ws = new WebSocket(`${WS_BASE}/runs/${run_id}`);
        
        ws.onmessage = (event) => {
          const data = JSON.parse(event.data);
          if (data.type === 'run.token') {
            setMessages(prev => prev.map(msg => 
              msg.id === agentMsgId ? { ...msg, content: msg.content + data.data.token } : msg
            ));
          } else if (data.type === 'run.finished') {
            setMessages(prev => prev.map(msg => 
              msg.id === agentMsgId ? { 
                ...msg, 
                status: 'finished',
                parsedData: data.data.output
              } : msg
            ));
            ws.close();
            checkAllFinished();
          } else if (data.type === 'run.error') {
            setMessages(prev => prev.map(msg => 
              msg.id === agentMsgId ? { ...msg, status: 'error', content: `Error: ${data.data.error}` } : msg
            ));
            ws.close();
            checkAllFinished();
          }
        };
        
        ws.onerror = () => {
          setMessages(prev => prev.map(msg => 
            msg.id === agentMsgId && msg.status === 'streaming' ? { ...msg, status: 'error', content: 'WebSocket connection error' } : msg
          ));
        };
        
        ws.onclose = () => {
          // If it closed while still streaming, it was an unexpected drop
          setMessages(prev => {
            const isStillStreaming = prev.some(msg => msg.id === agentMsgId && msg.status === 'streaming');
            if (isStillStreaming) {
               checkAllFinished();
               return prev.map(msg => msg.id === agentMsgId && msg.status === 'streaming' ? { ...msg, status: 'error', content: msg.content + '\n\n[Connection closed unexpectedly]' } : msg);
            }
            return prev;
          });
        };

      } catch (error: any) {
        setMessages(prev => prev.map(msg => 
          msg.id === agentMsgId ? { ...msg, status: 'error', content: error.message } : msg
        ));
        checkAllFinished();
      }
    });
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%', width: '100%', paddingTop: '5rem' }}>
      <div className="chat-container" style={{ height: 'calc(100vh - 80px)' }}>
        <div className="chat-messages">
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

        <div className="chat-input-area">
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
    </div>
  );
}
