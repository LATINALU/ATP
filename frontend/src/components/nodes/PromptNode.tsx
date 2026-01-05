"use client";

import { memo, useState } from 'react';
import { Handle, Position, NodeProps } from 'reactflow';
import { MessageSquare, Plus, Minus } from 'lucide-react';

export default memo(({ data, id }: NodeProps) => {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <div className="px-4 py-3 shadow-lg rounded-lg border-2 border-border bg-card min-w-[250px]">
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2">
          <MessageSquare className="h-5 w-5 text-primary" />
          <div className="font-bold text-sm">{data.label}</div>
        </div>
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="p-1 hover:bg-muted rounded"
        >
          {isExpanded ? <Minus className="h-4 w-4" /> : <Plus className="h-4 w-4" />}
        </button>
      </div>
      
      {isExpanded && (
        <div className="space-y-2">
          <div>
            <label className="text-xs text-green-500 font-semibold">✓ Positive Prompt</label>
            <textarea
              className="w-full text-xs bg-background border border-border rounded p-2 mt-1"
              placeholder="What you want..."
              rows={3}
              defaultValue={data.positivePrompt || ''}
            />
          </div>
          
          <div>
            <label className="text-xs text-red-500 font-semibold">✗ Negative Prompt</label>
            <textarea
              className="w-full text-xs bg-background border border-border rounded p-2 mt-1"
              placeholder="What you don't want..."
              rows={3}
              defaultValue={data.negativePrompt || ''}
            />
          </div>
        </div>
      )}
      
      {!isExpanded && (
        <div className="text-xs text-muted-foreground">
          Click + to edit prompts
        </div>
      )}
      
      {/* Handle: 1 salida morada en la parte inferior */}
      <div className="flex justify-center items-center mt-3 pt-2 border-t border-border">
        <div className="flex items-center gap-2">
          <div className="text-[10px] text-purple-500 font-semibold">Output</div>
          <Handle
            type="source"
            position={Position.Bottom}
            id="output"
            className="!w-4 !h-4 !bg-purple-500 !relative !transform-none !border-2 !border-white"
            style={{ position: 'relative' }}
          />
        </div>
      </div>
    </div>
  );
});
