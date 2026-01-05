"use client";

import { memo } from 'react';
import { Handle, Position, NodeProps } from 'reactflow';
import { ArrowRight, Copy } from 'lucide-react';

export default memo(({ data }: NodeProps) => {
  return (
    <div className="px-4 py-3 shadow-lg rounded-lg border-2 border-blue-500 bg-card/80 backdrop-blur-sm min-w-[280px]">
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2">
          <ArrowRight className="h-5 w-5 text-blue-500" />
          <div className="font-bold text-sm">{data.label}</div>
        </div>
        {data.result && (
          <button
            onClick={() => navigator.clipboard.writeText(data.result || '')}
            className="p-1 hover:bg-muted rounded"
            title="Copy result"
          >
            <Copy className="h-3 w-3" />
          </button>
        )}
      </div>
      
      <div className="text-xs bg-background border border-border rounded p-2 min-h-[60px] max-h-[120px] overflow-y-auto">
        {data.result || (
          <span className="text-muted-foreground italic">
            Intermediate output. Can connect to another agent.
          </span>
        )}
      </div>

      {/* Handles: 1 entrada azul (arriba) + 1 salida morada (abajo) */}
      <div className="mt-3 pt-2 border-t border-border">
        {/* Entrada azul */}
        <div className="flex justify-center items-center mb-2">
          <div className="flex flex-col items-center gap-1">
            <Handle
              type="target"
              position={Position.Top}
              id="input"
              className="!w-4 !h-4 !bg-blue-500 !relative !transform-none !border-2 !border-white"
              style={{ position: 'relative' }}
            />
            <div className="text-[9px] text-blue-500 font-semibold">Data In</div>
          </div>
        </div>
        
        {/* Salida morada */}
        <div className="flex justify-center items-center">
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
    </div>
  );
});
