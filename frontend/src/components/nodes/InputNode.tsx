"use client";

import { memo, useState } from 'react';
import { Handle, Position, NodeProps, useReactFlow } from 'reactflow';
import { Keyboard } from 'lucide-react';

export default memo(({ data, id }: NodeProps) => {
  const [inputText, setInputText] = useState(data.userInput || '');
  const { setNodes } = useReactFlow();

  const handleTextChange = (text: string) => {
    setInputText(text);
    setNodes((nds) =>
      nds.map((node) => {
        if (node.id === id) {
          return {
            ...node,
            data: {
              ...node.data,
              userInput: text,
            },
          };
        }
        return node;
      })
    );
  };

  return (
    <div className="px-4 py-3 shadow-lg rounded-lg border-2 border-primary bg-card/80 backdrop-blur-sm min-w-[250px]">
      <div className="flex items-center gap-2 mb-2">
        <Keyboard className="h-5 w-5 text-primary" />
        <div className="font-bold text-sm">{data.label}</div>
      </div>
      
      <textarea
        value={inputText}
        onChange={(e) => handleTextChange(e.target.value)}
        className="w-full text-xs bg-background border border-border rounded p-2"
        placeholder="Enter your input here..."
        rows={4}
      />
      
      {/* Handle at bottom */}
      <div className="flex justify-center items-center mt-3 pt-2 border-t border-border">
        <Handle
          type="source"
          position={Position.Bottom}
          id="output"
          className="!w-3 !h-3 !bg-cyan-500 !relative !transform-none"
          style={{ position: 'relative' }}
        />
        <div className="text-[10px] text-muted-foreground ml-2">Start</div>
      </div>
    </div>
  );
});
