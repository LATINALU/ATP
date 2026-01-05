"use client";

import { memo, useState } from "react";
import { Handle, Position, NodeProps, useReactFlow } from "reactflow";
import { Sparkles, BookOpenCheck, ListChecks, PenSquare } from "lucide-react";

const SynthesisNode = memo(({ data, id }: NodeProps) => {
  const { setNodes } = useReactFlow();
  const [strategy, setStrategy] = useState(data.strategy || "hierarchical");
  const [tone, setTone] = useState(data.tone || "executive");
  const [maxSections, setMaxSections] = useState(data.maxSections || 4);
  const [includeTrace, setIncludeTrace] = useState(data.includeTrace ?? true);

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

  const handleStrategyChange = (value: string) => {
    setStrategy(value);
    updateNode({ strategy: value });
  };

  return (
    <div className="px-4 py-3 shadow-xl rounded-2xl border-2 border-violet-400/70 bg-card/90 backdrop-blur min-w-[260px]">
      <div className="flex items-center gap-2 mb-3">
        <Sparkles className="h-5 w-5 text-violet-300" />
        <div className="font-bold text-sm uppercase tracking-widest text-violet-100">
          {data.label || "Synthesis Engine"}
        </div>
      </div>

      <div className="space-y-3 text-xs">
        <label className="flex flex-col gap-1">
          <span className="text-muted-foreground font-semibold uppercase tracking-wide flex items-center gap-1">
            <ListChecks className="h-3.5 w-3.5 text-emerald-300" />
            Strategy
          </span>
          <select
            value={strategy}
            onChange={(e) => handleStrategyChange(e.target.value)}
            className="bg-background/70 border border-border rounded px-2 py-1"
          >
            <option value="hierarchical">Hierarchical Merge</option>
            <option value="chronological">Chronological</option>
            <option value="evidence">Evidence-Weighted</option>
            <option value="conflict">Conflict Resolution</option>
          </select>
        </label>

        <label className="flex flex-col gap-1">
          <span className="text-muted-foreground font-semibold uppercase tracking-wide flex items-center gap-1">
            <PenSquare className="h-3.5 w-3.5 text-sky-300" />
            Tone
          </span>
          <select
            value={tone}
            onChange={(e) => {
              setTone(e.target.value);
              updateNode({ tone: e.target.value });
            }}
            className="bg-background/70 border border-border rounded px-2 py-1"
          >
            <option value="executive">Executive</option>
            <option value="technical">Technical</option>
            <option value="creative">Creative</option>
            <option value="analytical">Analytical</option>
          </select>
        </label>

        <label className="flex flex-col gap-1">
          <span className="text-muted-foreground font-semibold uppercase tracking-wide flex items-center gap-1">
            <BookOpenCheck className="h-3.5 w-3.5 text-amber-300" />
            Max Sections
          </span>
          <input
            type="number"
            min={1}
            max={8}
            value={maxSections}
            onChange={(e) => {
              const value = Number(e.target.value);
              setMaxSections(value);
              updateNode({ maxSections: value });
            }}
            className="bg-background/70 border border-border rounded px-2 py-1"
          />
        </label>

        <div className="flex items-center justify-between text-[11px] bg-background/60 border border-border rounded px-2 py-1.5">
          <span className="uppercase tracking-wider text-muted-foreground">
            Include Traceability
          </span>
          <button
            onClick={() => {
              setIncludeTrace((prev: boolean) => {
                const next = !prev;
                updateNode({ includeTrace: next });
                return next;
              });
            }}
            className={`px-2 py-0.5 rounded border ${
              includeTrace
                ? "border-emerald-400/70 text-emerald-200"
                : "border-slate-500/60 text-slate-200"
            }`}
          >
            {includeTrace ? "Enabled" : "Disabled"}
          </button>
        </div>
      </div>

      <div className="flex justify-between items-center mt-4 pt-3 border-t border-border/70">
        <div className="flex flex-col items-center text-[10px] text-indigo-100 font-semibold">
          <Handle
            type="target"
            position={Position.Top}
            id="synthesis-in"
            className="!w-4 !h-4 !bg-indigo-400 !border-2 !border-white shadow-[0_0_12px_rgba(129,140,248,0.9)]"
          />
          A2A Responses
        </div>
        <div className="flex flex-col items-center text-[10px] text-violet-100 font-semibold">
          <Handle
            type="source"
            position={Position.Bottom}
            id="synthesis-out"
            className="!w-4 !h-4 !bg-violet-400 !border-2 !border-white shadow-[0_0_12px_rgba(196,181,253,0.9)]"
          />
          Synthesized Draft
        </div>
      </div>
    </div>
  );
});

export default SynthesisNode;
