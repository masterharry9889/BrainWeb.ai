import { Handle, Position } from '@xyflow/react';
import { Globe, X } from 'lucide-react';
import { useState } from 'react';

import { NodeProps, Node } from '@xyflow/react';
import { CustomNodeData } from '@/lib/types';

export default function WebNode({ id, data, isConnectable }: NodeProps<Node<CustomNodeData>>) {
  const [url, setUrl] = useState(data.url || "");
  const [isEditing, setIsEditing] = useState(!data.url);

  const handleSave = () => {
    setIsEditing(false);
    if (data.onChange) data.onChange(url);
  };

  return (
    <div className="canvas-node web-node glass" style={{ position: 'relative' }}>
      <button 
        onClick={() => data.onDelete && data.onDelete(id)}
        className="node-delete-btn"
        title="Delete Node"
      >
        <X size={14} />
      </button>
      <Handle type="target" position={Position.Top} isConnectable={isConnectable} />
      <Handle type="target" position={Position.Left} isConnectable={isConnectable} />
      
      <div className="node-header" onDoubleClick={() => setIsEditing(true)}>
        <Globe size={14} /> <span style={{ flex: 1, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{url || "Interactive Web View"}</span>
      </div>
      
      <div className="node-content" style={{ padding: 0 }}>
        {isEditing ? (
           <div style={{ padding: '1rem', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
           <input 
             type="text" 
             placeholder="Enter website URL (e.g. https://wikipedia.org)" 
             value={url} 
             onChange={e => setUrl(e.target.value)}
             className="input-field"
             autoFocus
           />
           <button className="btn btn-primary" style={{ padding: '0.25rem' }} onClick={handleSave}>Embed</button>
         </div>
        ) : (
          url ? (
            <iframe src={url} className="node-iframe" title="Web Embed" />
          ) : (
            <div className="node-placeholder" style={{ padding: '2rem', textAlign: 'center' }} onClick={() => setIsEditing(true)}>
              Click to embed a website
            </div>
          )
        )}
      </div>
      
      <Handle type="source" position={Position.Bottom} isConnectable={isConnectable} />
      <Handle type="source" position={Position.Right} isConnectable={isConnectable} />
    </div>
  );
}
