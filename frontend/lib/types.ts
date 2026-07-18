export interface Project {
  id: string;
  name: string;
  date: string;
  type: 'conversation' | 'upload';
}

export interface Chat {
  id: string;
  name: string;
}

export interface Entity {
  label: string;
  type: string;
  [key: string]: unknown;
}

export interface Agent {
  id: string;
  name: string;
  description?: string;
  system_prompt?: string;
}

export interface Setting {
  provider: string;
  model_name: string;
  api_key_masked?: string;
}

export interface CustomNodeData {
  url?: string;
  text?: string;
  onChange?: (val: string) => void;
  onDelete?: (id: string) => void;
  [key: string]: unknown;
}

export interface ParsedMessageData {
  entities?: Entity[];
  [key: string]: unknown;
}

export interface Message {
  id: string;
  role: 'user' | 'agent';
  content: string;
  status?: 'streaming' | 'finished' | 'error';
  agentName?: string;
  parsedData?: ParsedMessageData;
}

export interface GraphNode {
  id: string;
  label: string;
  type: string;
  val?: number;
  mention_count?: number;
  x?: number;
  y?: number;
  action?: string;
  [key: string]: unknown;
}

export interface GraphEdge {
  id: string;
  source: string | GraphNode;
  target: string | GraphNode;
  label: string;
  type?: string;
  action?: string;
  [key: string]: unknown;
}

export interface GraphData {
  nodes: GraphNode[];
  links: GraphEdge[];
}
