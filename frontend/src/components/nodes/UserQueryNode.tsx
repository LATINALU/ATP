"use client";

import { memo, useState } from "react";
import { Handle, Position, NodeProps, useReactFlow } from "reactflow";
import { Keyboard, Target, Sparkles } from "lucide-react";

const UserQueryNode = memo(({ data, id }: NodeProps) => {
  const [inputText, setInputText] = useState(data.userInput || "");
  const [persona, setPersona] = useState(data.persona || "Executive");
  const [urgency, setUrgency] = useState(data.urgency || "normal");
  const { setNodes } = useReactFlow();

  const updateNodeData = (updates: Record<string, unknown>) => {
    setNodes((nodes) =>
      nodes.map((node) =>
        node.id === id
          ? {
              ...node,
              data: {
                ...node.data,
                ...updates,
              },
            }
          : node
      )
    );
  };

  const handleTextChange = (text: string) => {
    setInputText(text);
    updateNodeData({ userInput: text });
  };

  return (
    <div className="px-4 py-3 shadow-lg rounded-lg border-2 border-cyan-400 bg-card/80 backdrop-blur-lg min-w-[260px]">
      <div className="flex items-center gap-2 mb-3">
        <Keyboard className="h-5 w-5 text-cyan-400" />
        <div className="font-bold text-sm uppercase tracking-wide text-cyan-200">
          {data.label || "User Query"}
        </div>
      </div>

      <textarea
        value={inputText}
        onChange={(e) => handleTextChange(e.target.value)}
        className="w-full text-xs bg-background/70 border border-border rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-cyan-400"
        placeholder="Describe la intención del usuario..."
        rows={4}
      />

      <div className="grid grid-cols-2 gap-2 mt-3">
        <label className="text-[10px] text-muted-foreground flex flex-col gap-1">
          <span className="flex items-center gap-1 font-semibold uppercase tracking-wide">
            <Sparkles className="h-3 w-3 text-amber-400" />
            Persona
          </span>
          <select
            value={persona}
            onChange={(e) => {
              setPersona(e.target.value);
              updateNodeData({ persona: e.target.value });
            }}
            className="text-xs bg-background/60 border border-border rounded px-2 py-1"
          >
            <option>Executive</option>
            <option>Technical</option>
            <option>Creative</option>
            <option>Research</option>
          </select>
        </label>

        <label className="text-[10px] text-muted-foreground flex flex-col gap-1">
          <span className="flex items-center gap-1 font-semibold uppercase tracking-wide">
            <Target className="h-3 w-3 text-rose-400" />
            Urgency
          </span>
          <select
            value={urgency}
            onChange={(e) => {
              setUrgency(e.target.value);
              updateNodeData({ urgency: e.target.value });
            }}
            className="text-xs bg-background/60 border border-border rounded px-2 py-1"
          >
            <option value="normal">Normal</option>
            <option value="priority">Priority</option>
            <option value="critical">Critical</option>
          </select>
        </label>
      </div>

      <div className="flex justify-center items-center mt-4 pt-3 border-t border-border/70">
        <Handle
          type="source"
          position={Position.Bottom}
          id="query-out"
          className="!w-4 !h-4 !bg-cyan-400 !border-2 !border-white shadow-[0_0_12px_rgba(34,211,238,0.6)]"
        />
        <div className="text-[10px] text-cyan-200 font-semibold ml-2">
          User Query
        </div>
      </div>
    </div>
  );
});

export default UserQueryNode;
