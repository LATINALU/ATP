"use client";

import { memo, useMemo, useState } from "react";
import { Handle, Position, NodeProps, useReactFlow } from "reactflow";
import { Inbox, Activity, BarChart3, Shield } from "lucide-react";

type ResponseBucket = "success" | "warning" | "error";

const STATUS_COLORS: Record<ResponseBucket, string> = {
  success: "text-emerald-300 border-emerald-400/60",
  warning: "text-amber-300 border-amber-400/60",
  error: "text-rose-300 border-rose-400/60",
};

const A2AResponsesNode = memo(({ data, id }: NodeProps) => {
  const { setNodes } = useReactFlow();
  const [expectedAgents, setExpectedAgents] = useState<number>(
    data.expectedAgents || 3,
  );
  const [timeoutMs, setTimeoutMs] = useState<number>(data.timeoutMs || 8000);
  const [autoRetry, setAutoRetry] = useState<boolean>(
    data.autoRetry ?? true,
  );
  const [statusBuckets, setStatusBuckets] = useState<Record<ResponseBucket, number>>({
    success: data.successCount || 0,
    warning: data.warningCount || 0,
    error: data.errorCount || 0,
  });

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

  const buckets = useMemo(
    () => [
      { label: "Success", key: "success" as ResponseBucket, icon: Shield },
      { label: "Warning", key: "warning" as ResponseBucket, icon: Activity },
      { label: "Error", key: "error" as ResponseBucket, icon: BarChart3 },
    ],
    [],
  );

  return (
    <div className="px-4 py-3 shadow-xl rounded-2xl border-2 border-indigo-400/70 bg-card/90 backdrop-blur min-w-[300px]">
      <div className="flex items-center gap-2 mb-3">
        <Inbox className="h-5 w-5 text-indigo-300" />
        <div className="font-bold text-sm uppercase tracking-wider text-indigo-100">
          {data.label || "A2A Responses Collector"}
        </div>
      </div>

      <div className="grid grid-cols-3 gap-2 text-xs">
        {buckets.map(({ label, key, icon: Icon }) => (
          <button
            key={key}
            onClick={() => {
              setStatusBuckets((prev) => {
                const updated = {
                  ...prev,
                  [key]: prev[key] + 1,
                };
                updateNodeData({
                  [`${key}Count`]: updated[key],
                });
                return updated;
              });
            }}
            className={`flex flex-col gap-1 border rounded-lg p-2 text-center ${STATUS_COLORS[key]}`}
          >
            <span className="text-[10px] uppercase tracking-wider">
              {label}
            </span>
            <div className="flex justify-center gap-1 items-center text-sm font-semibold">
              <Icon className="h-3.5 w-3.5" />
              {statusBuckets[key]}
            </div>
          </button>
        ))}
      </div>

      <div className="grid grid-cols-2 gap-2 mt-3 text-xs">
        <label className="flex flex-col gap-1">
          <span className="text-muted-foreground font-semibold uppercase tracking-wide">
            Expected Agents
          </span>
          <input
            type="number"
            min={1}
            value={expectedAgents}
            onChange={(e) => {
              const val = Number(e.target.value);
              setExpectedAgents(val);
              updateNodeData({ expectedAgents: val });
            }}
            className="bg-background/70 border border-border rounded px-2 py-1"
          />
        </label>
        <label className="flex flex-col gap-1">
          <span className="text-muted-foreground font-semibold uppercase tracking-wide">
            Timeout (ms)
          </span>
          <input
            type="number"
            min={1000}
            value={timeoutMs}
            onChange={(e) => {
              const val = Number(e.target.value);
              setTimeoutMs(val);
              updateNodeData({ timeoutMs: val });
            }}
            className="bg-background/70 border border-border rounded px-2 py-1"
          />
        </label>
      </div>

      <div className="mt-3 flex items-center justify-between text-[11px] bg-background/60 border border-border rounded px-2 py-1.5">
        <span className="uppercase tracking-wider text-muted-foreground">
          Auto Retry
        </span>
        <button
          onClick={() => {
            setAutoRetry((prev: boolean) => {
              const next = !prev;
              updateNodeData({ autoRetry: next });
              return next;
            });
          }}
          className={`px-2 py-0.5 rounded border ${
            autoRetry
              ? "border-emerald-400/70 text-emerald-200"
              : "border-slate-500/60 text-slate-200"
          }`}
        >
          {autoRetry ? "Enabled" : "Disabled"}
        </button>
      </div>

      <div className="flex justify-between items-center mt-4 pt-3 border-t border-border/70">
        <div className="flex flex-col items-center text-[10px] text-sky-100 font-semibold">
          <Handle
            type="target"
            position={Position.Top}
            id="responses-in"
            className="!w-4 !h-4 !bg-sky-400 !border-2 !border-white shadow-[0_0_12px_rgba(56,189,248,0.9)]"
          />
          Agent Output
        </div>
        <div className="flex flex-col items-center text-[10px] text-indigo-100 font-semibold">
          <Handle
            type="source"
            position={Position.Bottom}
            id="responses-out"
            className="!w-4 !h-4 !bg-indigo-400 !border-2 !border-white shadow-[0_0_12px_rgba(129,140,248,0.9)]"
          />
          A2A Responses
        </div>
      </div>
    </div>
  );
});

export default A2AResponsesNode;
