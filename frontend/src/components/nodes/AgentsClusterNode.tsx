"use client";

import { memo, useMemo, useState } from "react";
import { Handle, Position, NodeProps, useReactFlow } from "reactflow";
import { Layers3, Bot, Gauge, Users, Settings2 } from "lucide-react";
import { AGENT_DETAILS } from "@/data/agentDetails";

type AgentLevel = 1 | 2 | 3 | 4 | 5;

const LEVEL_LABELS: Record<AgentLevel, string> = {
  1: "Critical Reasoning",
  2: "Essential Builders",
  3: "Specialized Experts",
  4: "Quality & Support",
  5: "Auxiliary Boosters",
};

const LEVEL_COLORS: Record<AgentLevel, string> = {
  1: "text-red-300 border-red-400/60",
  2: "text-orange-300 border-orange-400/60",
  3: "text-amber-200 border-amber-300/60",
  4: "text-emerald-200 border-emerald-300/60",
  5: "text-sky-200 border-sky-300/60",
};

const AGENT_LEVEL_MAP: Record<string, AgentLevel> = {
  reasoning: 1,
  planning: 1,
  research: 1,
  analysis: 1,
  synthesis: 1,
  critical_thinking: 1,
  coding: 2,
  data: 2,
  writing: 2,
  communication: 2,
  decision: 2,
  problem_solving: 2,
  legal: 3,
  financial: 3,
  creative: 3,
  technical: 3,
  educational: 3,
  marketing: 3,
  qa: 4,
  documentation: 4,
  optimization: 4,
  security: 4,
  integration: 4,
  review: 4,
  translation: 5,
  summary: 5,
  formatting: 5,
  validation: 5,
  coordination: 5,
  explanation: 5,
};

const LEVEL_ORDER: AgentLevel[] = [1, 2, 3, 4, 5];

const AgentsClusterNode = memo(({ data, id }: NodeProps) => {
  const { setNodes } = useReactFlow();
  const initialAgents: string[] = data.selectedAgents || ["reasoning", "planning"];
  const [selectedAgents, setSelectedAgents] = useState<string[]>(initialAgents);
  const [maxParallel, setMaxParallel] = useState<number>(data.maxParallel || 2);
  const [cooldownMs, setCooldownMs] = useState<number>(data.cooldownMs || 1200);
  const [loadBalancing, setLoadBalancing] = useState(data.loadBalancing ?? true);

  const agentsByLevel = useMemo(() => {
    const grouped: Record<AgentLevel, string[]> = {
      1: [],
      2: [],
      3: [],
      4: [],
      5: [],
    };

    (Object.keys(AGENT_DETAILS) as Array<keyof typeof AGENT_DETAILS>).forEach(
      (key) => {
        const level = AGENT_LEVEL_MAP[key as string] ?? 5;
        grouped[level].push(key as string);
      },
    );

    return grouped;
  }, []);

  const updateNodeData = (payload: Record<string, unknown>) => {
    setNodes((nodes) =>
      nodes.map((node) =>
        node.id === id
          ? {
              ...node,
              data: {
                ...node.data,
                ...payload,
              },
            }
          : node,
      ),
    );
  };

  const toggleAgent = (agentId: string) => {
    setSelectedAgents((prev) => {
      const exists = prev.includes(agentId);
      const updated = exists ? prev.filter((a) => a !== agentId) : [...prev, agentId];
      updateNodeData({ selectedAgents: updated });
      return updated;
    });
  };

  return (
    <div className="px-4 py-3 shadow-xl rounded-2xl border-2 border-sky-400/70 bg-card/85 backdrop-blur min-w-[320px]">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <Layers3 className="h-5 w-5 text-sky-300" />
          <div className="font-bold text-sm uppercase tracking-widest text-sky-100">
            {data.label || "Agents Cluster"}
          </div>
        </div>
        <div className="text-[11px] text-muted-foreground flex items-center gap-1">
          <Users className="h-3.5 w-3.5" />
          {selectedAgents.length} selected
        </div>
      </div>

      <div className="max-h-48 overflow-y-auto pr-1 space-y-2">
        {LEVEL_ORDER.map((level) => (
          <div key={level} className="border border-border/60 rounded-lg p-2">
            <div
              className={`text-[11px] font-semibold uppercase tracking-wider mb-2 flex items-center gap-2 border-l-2 pl-2 ${LEVEL_COLORS[level]}`}
            >
              <Bot className="h-3.5 w-3.5" />
              {LEVEL_LABELS[level]}
            </div>
            <div className="flex flex-wrap gap-1.5">
              {agentsByLevel[level].map((agentId) => (
                <button
                  key={agentId}
                  onClick={() => toggleAgent(agentId)}
                  className={`px-2 py-1 rounded-full text-[11px] border transition-colors ${
                    selectedAgents.includes(agentId)
                      ? "bg-sky-500/20 border-sky-300 text-sky-100"
                      : "bg-background/40 border-border text-muted-foreground"
                  }`}
                >
                  {agentId.replace(/_/g, " ")}
                </button>
              ))}
            </div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-2 gap-2 mt-3 text-xs">
        <label className="flex flex-col gap-1">
          <span className="text-muted-foreground font-semibold uppercase tracking-wide flex items-center gap-1">
            <Gauge className="h-3.5 w-3.5 text-emerald-300" />
            Max Parallel
          </span>
          <input
            type="number"
            min={1}
            max={6}
            value={maxParallel}
            onChange={(e) => {
              const value = Number(e.target.value);
              setMaxParallel(value);
              updateNodeData({ maxParallel: value });
            }}
            className="bg-background/70 border border-border rounded px-2 py-1"
          />
        </label>

        <label className="flex flex-col gap-1">
          <span className="text-muted-foreground font-semibold uppercase tracking-wide flex items-center gap-1">
            <Settings2 className="h-3.5 w-3.5 text-amber-300" />
            Cooldown (ms)
          </span>
          <input
            type="number"
            min={200}
            value={cooldownMs}
            onChange={(e) => {
              const value = Number(e.target.value);
              setCooldownMs(value);
              updateNodeData({ cooldownMs: value });
            }}
            className="bg-background/70 border border-border rounded px-2 py-1"
          />
        </label>
      </div>

      <div className="mt-3 flex items-center justify-between text-[11px] bg-background/60 border border-border rounded px-2 py-1.5">
        <span className="uppercase tracking-wider text-muted-foreground">Load Balancing</span>
        <button
          onClick={() => {
            setLoadBalancing((prev: boolean) => {
              const next = !prev;
              updateNodeData({ loadBalancing: next });
              return next;
            });
          }}
          className={`px-2 py-0.5 rounded border ${
            loadBalancing
              ? "border-emerald-400/70 text-emerald-200"
              : "border-slate-500/60 text-slate-200"
          }`}
        >
          {loadBalancing ? "Enabled" : "Disabled"}
        </button>
      </div>

      <div className="flex justify-between items-center mt-4 pt-3 border-t border-border/70">
        <div className="flex flex-col items-center text-[10px] text-amber-100 font-semibold">
          <Handle
            type="target"
            position={Position.Top}
            id="agents-in"
            className="!w-4 !h-4 !bg-amber-400 !border-2 !border-white shadow-[0_0_12px_rgba(251,191,36,0.8)]"
          />
          A2A Message
        </div>
        <div className="flex flex-col items-center text-[10px] text-sky-100 font-semibold">
          <Handle
            type="source"
            position={Position.Bottom}
            id="agents-out"
            className="!w-4 !h-4 !bg-sky-400 !border-2 !border-white shadow-[0_0_12px_rgba(56,189,248,0.9)]"
          />
          Agent Output
        </div>
      </div>
    </div>
  );
});

export default AgentsClusterNode;
