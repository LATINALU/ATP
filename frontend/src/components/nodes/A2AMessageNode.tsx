"use client";

import { memo, useState } from "react";
import { Handle, Position, NodeProps, useReactFlow } from "reactflow";
import { RadioTower, Waves, AlertTriangle, Lock } from "lucide-react";

const A2AMessageNode = memo(({ data, id }: NodeProps) => {
  const [channel, setChannel] = useState(data.channel || "broadcast");
  const [priority, setPriority] = useState(data.priority || "normal");
  const [messageType, setMessageType] = useState(data.messageType || "analysis");
  const [subject, setSubject] = useState(data.subject || "");
  const [encrypted, setEncrypted] = useState(data.encrypted ?? true);
  const { setNodes } = useReactFlow();

  const updateNode = (updates: Record<string, unknown>) => {
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
          : node,
      ),
    );
  };

  return (
    <div className="px-4 py-3 shadow-xl rounded-xl border-2 border-amber-400/70 bg-card/85 backdrop-blur min-w-[270px]">
      <div className="flex items-center gap-2 mb-2">
        <RadioTower className="h-5 w-5 text-amber-300" />
        <div className="font-bold text-sm uppercase tracking-wider text-amber-100">
          {data.label || "A2A Message Dispatch"}
        </div>
      </div>

      <div className="space-y-2 text-xs">
        <label className="flex flex-col gap-1">
          <span className="text-muted-foreground font-semibold uppercase tracking-wide">
            Channel
          </span>
          <select
            value={channel}
            onChange={(e) => {
              setChannel(e.target.value);
              updateNode({ channel: e.target.value });
            }}
            className="bg-background/70 border border-border rounded px-2 py-1"
          >
            <option value="broadcast">Broadcast</option>
            <option value="directed">Directed</option>
            <option value="multicast">Multicast</option>
          </select>
        </label>

        <label className="flex flex-col gap-1">
          <span className="text-muted-foreground font-semibold uppercase tracking-wide">
            Priority
          </span>
          <select
            value={priority}
            onChange={(e) => {
              setPriority(e.target.value);
              updateNode({ priority: e.target.value });
            }}
            className="bg-background/70 border border-border rounded px-2 py-1"
          >
            <option value="normal">Normal</option>
            <option value="high">High</option>
            <option value="critical">Critical</option>
          </select>
        </label>

        <label className="flex flex-col gap-1">
          <span className="text-muted-foreground font-semibold uppercase tracking-wide">
            Message Type
          </span>
          <select
            value={messageType}
            onChange={(e) => {
              setMessageType(e.target.value);
              updateNode({ messageType: e.target.value });
            }}
            className="bg-background/70 border border-border rounded px-2 py-1"
          >
            <option value="analysis">Analysis</option>
            <option value="tasking">Tasking</option>
            <option value="alert">Alert</option>
          </select>
        </label>

        <label className="flex flex-col gap-1">
          <span className="text-muted-foreground font-semibold uppercase tracking-wide">
            Subject / Payload Focus
          </span>
          <input
            value={subject}
            onChange={(e) => {
              setSubject(e.target.value);
              updateNode({ subject: e.target.value });
            }}
            className="bg-background/70 border border-border rounded px-2 py-1"
            placeholder="LangGraph orchestration request..."
          />
        </label>

        <div className="flex items-center justify-between text-[11px] bg-background/60 border border-border rounded px-2 py-1.5">
          <div className="flex items-center gap-1 text-muted-foreground">
            {encrypted ? (
              <Lock className="h-3.5 w-3.5 text-emerald-400" />
            ) : (
              <AlertTriangle className="h-3.5 w-3.5 text-amber-400" />
            )}
            <span className="font-semibold uppercase tracking-wider">
              Encryption
            </span>
          </div>
          <button
            onClick={() => {
              setEncrypted((prev: boolean) => {
                const next = !prev;
                updateNode({ encrypted: next });
                return next;
              });
            }}
            className={`px-2 py-0.5 rounded border ${
              encrypted
                ? "border-emerald-400/60 text-emerald-200"
                : "border-amber-300/60 text-amber-200"
            }`}
          >
            {encrypted ? "Enabled" : "Disabled"}
          </button>
        </div>

        {data.statusMessage && (
          <div className="text-[11px] text-amber-100 bg-amber-500/10 border border-amber-400/40 rounded px-2 py-1">
            {data.statusMessage}
          </div>
        )}
      </div>

      <div className="flex justify-between items-center mt-3 pt-3 border-t border-border/70">
        <div className="flex flex-col items-center text-[10px] text-fuchsia-200 font-semibold">
          <Handle
            type="target"
            position={Position.Top}
            id="a2a-in"
            className="!w-4 !h-4 !bg-fuchsia-500 !border-2 !border-white shadow-[0_0_10px_rgba(217,70,239,0.7)]"
          />
          LangGraph
        </div>
        <div className="flex flex-col items-center text-[10px] text-amber-200 font-semibold">
          <Handle
            type="source"
            position={Position.Bottom}
            id="a2a-out"
            className="!w-4 !h-4 !bg-amber-400 !border-2 !border-white shadow-[0_0_10px_rgba(251,191,36,0.8)]"
          />
          A2A Message
        </div>
      </div>
    </div>
  );
});

export default A2AMessageNode;
