import { Handle, Position } from '@xyflow/react';
import { useState, useEffect } from 'react';
import { X } from 'lucide-react';

export default function TextNode({ id, data, isConnectable }: any) {
  const [isEditing, setIsEditing] = useState(false);
  const [text, setText] = useState(data.text || "Type your idea here...");

  // Sync internal state if data.text changes externally
  useEffect(() => {
    setText(data.text || "Type your idea here...");
  }, [data.text]);

  const handleChange = (e: any) => {
    const val = e.target.value;
    setText(val);
    if (data.onChange) {
      data.onChange(val);
    }
  };

  return (
    <div className="canvas-node text-node glass" style={{ position: 'relative' }}>
      <button 
        onClick={() => data.onDelete && data.onDelete(id)}
        className="node-delete-btn"
        title="Delete Note"
      >
        <X size={14} />
      </button>
      <Handle type="target" position={Position.Top} isConnectable={isConnectable} />
      <Handle type="target" position={Position.Left} isConnectable={isConnectable} />
      
      <div className="node-content" onClick={() => setIsEditing(true)}>
        {isEditing ? (
          <textarea 
            autoFocus
            className="node-input"
            value={text} 
            onChange={handleChange} 
            onBlur={() => setIsEditing(false)}
            placeholder="Type your idea here..."
          />
        ) : (
          <div className="node-text" style={{ whiteSpace: 'pre-wrap' }}>
            {text}
          </div>
        )}
      </div>
      
      <Handle type="source" position={Position.Bottom} isConnectable={isConnectable} />
      <Handle type="source" position={Position.Right} isConnectable={isConnectable} />
    </div>
  );
}
