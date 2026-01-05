"use client";

import { memo, useState } from "react";
import { Handle, Position, NodeProps, useReactFlow } from "reactflow";
import { Share2, Workflow, ShieldCheck } from "lucide-react";

const LangGraphNode = memo(({ data, id }: NodeProps) => {
  const [strategy, setStrategy] = useState(data.strategy || "deterministic");
  const [maxAgents, setMaxAgents] = useState(data.maxAgents || 3);
  const [model, setModel] = useState(data.model || "openai/gpt-oss-120b");
  const [allowParallel, setAllowParallel] = useState(
    data.allowParallel ?? true,
  );
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
    <div className="px-4 py-3 shadow-lg rounded-xl border-2 border-fuchsia-500/70 bg-card/85 backdrop-blur min-w-[280px]">
      <div className="flex items-center gap-2 mb-3">
        <Workflow className="h-5 w-5 text-fuchsia-400" />
        <div className="font-bold text-sm uppercase tracking-wider text-fuchsia-100">
          {data.label || "LangGraph StateGraph"}
        </div>
      </div>

      <div className="space-y-3 text-xs">
        <label className="flex flex-col gap-1">
          <span className="text-muted-foreground font-semibold uppercase tracking-wide">
            Execution Strategy
          </span>
          <select
            value={strategy}
            onChange={(e) => {
              setStrategy(e.target.value);
              updateNode({ strategy: e.target.value });
            }}
            className="bg-background/70 border border-border rounded px-2 py-1"
          >
            <option value="deterministic">Deterministic</option>
            <option value="adaptive">Adaptive</option>
            <option value="cybernetic">Cybernetic</option>
          </select>
        </label>

        <div className="grid grid-cols-2 gap-2">
          <label className="flex flex-col gap-1">
            <span className="text-muted-foreground font-semibold uppercase tracking-wide">
              Max Agents
            </span>
            <input
              type="number"
              min={1}
              max={10}
              value={maxAgents}
              onChange={(e) => {
                const value = Number(e.target.value);
                setMaxAgents(value);
                updateNode({ maxAgents: value });
              }}
              className="bg-background/70 border border-border rounded px-2 py-1"
            />
          </label>

          <label className="flex flex-col gap-1">
            <span className="text-muted-foreground font-semibold uppercase tracking-wide">
              Parallel
            </span>
            <button
              onClick={() => {
                setAllowParallel((prev: boolean) => {
                  const next = !prev;
                  updateNode({ allowParallel: next });
                  return next;
                });
              }}
              className={`px-2 py-1 rounded border text-[11px] ${
                allowParallel
                  ? "bg-emerald-500/20 text-emerald-300 border-emerald-400/60"
                  : "bg-slate-800/50 text-slate-200 border-border"
              }`}
            >
              {allowParallel ? "Enabled" : "Disabled"}
            </button>
          </label>
        </div>

        <label className="flex flex-col gap-1">
          <span className="text-muted-foreground font-semibold uppercase tracking-wide">
            Primary Model
          </span>
          <input
            value={model}
            onChange={(e) => {
              setModel(e.target.value);
              updateNode({ model: e.target.value });
            }}
            className="bg-background/70 border border-border rounded px-2 py-1"
            placeholder="openai/gpt-oss-120b"
          />
        </label>

        <div className="flex items-center gap-2 text-[11px] text-muted-foreground bg-background/60 border border-border rounded p-2">
          <ShieldCheck className="h-4 w-4 text-emerald-400" />
          Validates DAG, controls concurrency y delega a A2A.
        </div>
      </div>

      <div className="flex justify-between items-center mt-4 pt-3 border-t border-border/70">
        <div className="flex flex-col items-center text-[10px] text-fuchsia-300 font-semibold">
          <Handle
            type="target"
            position={Position.Top}
            id="lg-input"
            className="!w-4 !h-4 !bg-cyan-400 !border-2 !border-white shadow-[0_0_12px_rgba(6,182,212,0.7)]"
          />
          User Query
        </div>
        <div className="flex flex-col items-center text-[10px] text-fuchsia-300 font-semibold">
          <Handle
            type="source"
            position={Position.Bottom}
            id="lg-output"
            className="!w-4 !h-4 !bg-fuchsia-500 !border-2 !border-white shadow-[0_0_12px_rgba(232,121,249,0.8)]"
          />
          LangGraph Plan
        </div>
      </div>
    </div>
  );
});

export default LangGraphNode;
