"use client";

import { memo } from 'react';
import { Handle, Position, NodeProps } from 'reactflow';
import { FileOutput, Copy, CheckCircle } from 'lucide-react';

export default memo(({ data }: NodeProps) => {
  return (
    <div className="px-4 py-3 shadow-lg rounded-lg border-2 border-green-500 bg-card/80 backdrop-blur-sm min-w-[300px]">
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2">
          <FileOutput className="h-5 w-5 text-green-500" />
          <div className="font-bold text-sm">{data.label}</div>
        </div>
        {data.result && (
          <button
            onClick={() => navigator.clipboard.writeText(data.result || '')}
            className="p-1 hover:bg-muted rounded"
            title="Copy result"
          >
            <Copy className="h-4 w-4" />
          </button>
        )}
      </div>
      
      <div className="text-xs bg-background border border-border rounded p-2 max-h-[200px] overflow-y-auto">
        {data.result || 'No output yet. Run the workflow to see results.'}
      </div>

      {/* Handle at bottom */}
      <div className="flex justify-center items-center mt-3 pt-2 border-t border-green-500/30">
        <Handle
          type="target"
          position={Position.Bottom}
          id="input"
          className="!w-3 !h-3 !bg-green-500 !relative !transform-none"
          style={{ position: 'relative' }}
        />
        <div className="text-[10px] text-green-600 ml-2 flex items-center gap-1">
          <CheckCircle className="h-3 w-3" />
          End
        </div>
      </div>
    </div>
  );
});
