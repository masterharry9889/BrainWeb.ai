import { Handle, Position } from '@xyflow/react';
import { Image as ImageIcon, X } from 'lucide-react';
import { useState } from 'react';

export default function ImageNode({ id, data, isConnectable }: any) {
  const [url, setUrl] = useState(data.url || "");
  const [isEditing, setIsEditing] = useState(!data.url);

  const handleSave = () => {
    setIsEditing(false);
    if (data.onChange) data.onChange(url);
  };

  return (
    <div className="canvas-node media-node glass" style={{ position: 'relative' }}>
      <button 
        onClick={() => data.onDelete && data.onDelete(id)}
        className="node-delete-btn"
        title="Delete Node"
      >
        <X size={14} />
      </button>
      <Handle type="target" position={Position.Top} isConnectable={isConnectable} />
      <Handle type="target" position={Position.Left} isConnectable={isConnectable} />
      
      {isEditing ? (
        <div className="node-content" style={{ padding: '1rem', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
          <input 
            type="text" 
            placeholder="Enter image URL..." 
            value={url} 
            onChange={e => setUrl(e.target.value)}
            className="input-field"
            autoFocus
          />
          <button className="btn btn-primary" style={{ padding: '0.25rem' }} onClick={handleSave}>Save</button>
        </div>
      ) : (
        <div className="node-media-container" onClick={() => setIsEditing(true)}>
          {url ? (
             <img src={url} alt="Canvas Media" className="node-media" />
          ) : (
            <div className="node-placeholder" style={{ padding: '2rem', textAlign: 'center' }}>
              <ImageIcon size={32} opacity={0.5} style={{ margin: '0 auto 0.5rem' }} />
              <div>Click to add image URL</div>
            </div>
          )}
        </div>
      )}
      
      <Handle type="source" position={Position.Bottom} isConnectable={isConnectable} />
      <Handle type="source" position={Position.Right} isConnectable={isConnectable} />
    </div>
  );
}
