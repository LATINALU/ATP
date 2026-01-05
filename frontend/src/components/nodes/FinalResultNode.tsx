"use client";

import { memo, useEffect, useState } from "react";
import { Handle, Position, NodeProps, useReactFlow } from "reactflow";
import {
  Trophy,
  Copy,
  Download,
  Share2,
  BookCheck,
  ExternalLink,
} from "lucide-react";

const FinalResultNode = memo(({ data, id }: NodeProps) => {
  const { setNodes } = useReactFlow();
  const [title, setTitle] = useState(data.title || "Final ATP Output");
  const [result, setResult] = useState(data.result || "");
  const [format, setFormat] = useState(data.format || "markdown");

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

  useEffect(() => {
    if (typeof data.result === "string" && data.result !== result) {
      setResult(data.result);
    }
  }, [data.result, result]);

  const handleCopy = () => {
    if (result) {
      navigator.clipboard.writeText(result);
    }
  };

  const handleDownload = () => {
    if (result) {
      const blob = new Blob([result], { type: "text/plain" });
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = `atp-final-output.${format === "markdown" ? "md" : "txt"}`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
    }
  };

  return (
    <div className="px-4 py-3 shadow-2xl rounded-3xl border-2 border-emerald-400/80 bg-gradient-to-br from-slate-950/85 to-slate-900/85 backdrop-blur min-w-[320px]">
      <div className="flex items-center gap-2 mb-3">
        <Trophy className="h-6 w-6 text-emerald-300" />
        <input
          value={title}
          onChange={(e) => {
            setTitle(e.target.value);
            updateNode({ title: e.target.value });
          }}
          className="bg-transparent border-b border-dashed border-emerald-400/50 text-sm font-bold uppercase tracking-widest text-emerald-100 focus:outline-none"
        />
      </div>

      <textarea
        value={result}
        onChange={(e) => {
          setResult(e.target.value);
          updateNode({ result: e.target.value });
        }}
        placeholder="La síntesis final aparecerá aquí..."
        rows={6}
        className="w-full text-xs bg-black/30 border border-white/10 rounded-xl p-3 text-slate-100 font-mono focus:outline-none focus:ring-2 focus:ring-emerald-400/60 min-h-[120px]"
      />

      <div className="grid grid-cols-2 gap-2 mt-3 text-xs">
        <label className="flex flex-col gap-1">
          <span className="uppercase tracking-wide text-muted-foreground font-semibold flex items-center gap-1">
            <BookCheck className="h-3.5 w-3.5 text-emerald-200" />
            Format
          </span>
          <select
            value={format}
            onChange={(e) => {
              setFormat(e.target.value);
              updateNode({ format: e.target.value });
            }}
            className="bg-black/30 border border-white/10 rounded px-2 py-1 text-slate-100"
          >
            <option value="markdown">Markdown</option>
            <option value="plain">Plain Text</option>
            <option value="json">JSON</option>
          </select>
        </label>
        <label className="flex flex-col gap-1">
          <span className="uppercase tracking-wide text-muted-foreground font-semibold flex items-center gap-1">
            <Share2 className="h-3.5 w-3.5 text-sky-200" />
            Share URL
          </span>
          <input
            value={data.shareUrl || ""}
            onChange={(e) => updateNode({ shareUrl: e.target.value })}
            placeholder="https://..."
            className="bg-black/30 border border-white/10 rounded px-2 py-1 text-slate-100"
          />
        </label>
      </div>

      <div className="flex gap-2 mt-3">
          <button
            onClick={handleCopy}
            className="flex-1 flex items-center justify-center gap-1.5 px-3 py-1.5 rounded-xl border border-emerald-400/50 text-emerald-200 hover:bg-emerald-400/10 transition-colors"
          >
            <Copy className="h-3.5 w-3.5" />
            Copy
          </button>
          <button
            onClick={handleDownload}
            className="flex-1 flex items-center justify-center gap-1.5 px-3 py-1.5 rounded-xl border border-sky-400/50 text-sky-200 hover:bg-sky-400/10 transition-colors"
          >
            <Download className="h-3.5 w-3.5" />
            Download
          </button>
          <button
            onClick={() => data.shareUrl && window.open(data.shareUrl, "_blank")}
            className="flex-1 flex items-center justify-center gap-1.5 px-3 py-1.5 rounded-xl border border-purple-400/50 text-purple-200 hover:bg-purple-400/10 transition-colors"
          >
            <ExternalLink className="h-3.5 w-3.5" />
            Open
          </button>
      </div>

      <div className="flex justify-center items-center mt-4 pt-3 border-t border-white/10">
        <div className="flex flex-col items-center text-[10px] text-emerald-200 font-semibold">
          <Handle
            type="target"
            position={Position.Top}
            id="final-in"
            className="!w-4 !h-4 !bg-violet-400 !border-2 !border-white shadow-[0_0_12px_rgba(196,181,253,0.9)]"
          />
          Synthesized Draft
        </div>
      </div>
    </div>
  );
});

export default FinalResultNode;
