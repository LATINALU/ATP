"use client";

import { useState, useCallback, useRef } from 'react';
import ReactFlow, {
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  addEdge,
  Connection,
  Edge,
  BackgroundVariant,
  Panel,
} from 'reactflow';
import 'reactflow/dist/style.css';

import UserQueryNode from "@/components/nodes/UserQueryNode";
import LangGraphNode from "@/components/nodes/LangGraphNode";
import A2AMessageNode from "@/components/nodes/A2AMessageNode";
import AgentsClusterNode from "@/components/nodes/AgentsClusterNode";
import A2AResponsesNode from "@/components/nodes/A2AResponsesNode";
import SynthesisNode from "@/components/nodes/SynthesisNode";
import FinalResultNode from "@/components/nodes/FinalResultNode";

import {
  Bot,
  MessageSquare,
  Cpu,
  Keyboard,
  FileOutput,
  Play,
  Save,
  FolderOpen,
  LayoutGrid,
  Home,
  Trash2,
  Loader2,
  Upload,
  Download,
  Palette,
  Workflow,
  RadioTower,
  Layers3,
  Inbox,
  Sparkles,
  Trophy,
} from "lucide-react";
import Link from 'next/link';
import { WorkflowExecutor } from '@/lib/workflowExecutor';
import { ThemeSelector } from '@/components/ThemeSelector';
import { LanguageSelector } from '@/components/LanguageSelector';
import { getCurrentLanguage, getTranslation } from '@/lib/i18n';

const nodeTypes = {
  user_query: UserQueryNode,
  langgraph: LangGraphNode,
  a2a_message: A2AMessageNode,
  agents_cluster: AgentsClusterNode,
  a2a_responses: A2AResponsesNode,
  synthesis: SynthesisNode,
  final_result: FinalResultNode,
};

const initialNodes = [
  {
    id: "1",
    type: "user_query",
    data: { label: "User Query Intake", type: "user_query" },
    position: { x: 0, y: 80 },
  },
  {
    id: "2",
    type: "langgraph",
    data: { label: "LangGraph StateGraph", type: "langgraph" },
    position: { x: 0, y: 280 },
  },
  {
    id: "3",
    type: "a2a_message",
    data: { label: "A2A Message Broadcast", type: "a2a_message" },
    position: { x: 0, y: 480 },
  },
  {
    id: "4",
    type: "agents_cluster",
    data: { label: "Agents Cluster", type: "agents_cluster" },
    position: { x: 350, y: 480 },
  },
  {
    id: "5",
    type: "a2a_responses",
    data: { label: "A2A Responses Collector", type: "a2a_responses" },
    position: { x: 350, y: 680 },
  },
  {
    id: "6",
    type: "synthesis",
    data: { label: "Synthesis Engine", type: "synthesis" },
    position: { x: 350, y: 880 },
  },
  {
    id: "7",
    type: "final_result",
    data: { label: "Final Result", type: "final_result" },
    position: { x: 350, y: 1080 },
  },
];

const initialEdges: Edge[] = [];

export default function NodesPage() {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
  const [nodeIdCounter, setNodeIdCounter] = useState(initialNodes.length + 1);
  const [isRunning, setIsRunning] = useState(false);
  const [currentLang, setCurrentLang] = useState(getCurrentLanguage());
  const reactFlowWrapper = useRef<HTMLDivElement>(null);
  
  const t = (key: any) => getTranslation(currentLang, key);

  const onConnect = useCallback(
    (params: Connection) => {
      const sourceNode = nodes.find((n) => n.id === params.source);
      const targetNode = nodes.find((n) => n.id === params.target);
      if (!sourceNode || !targetNode) return;

      const flowRules = [
        {
          from: { type: "user_query", handle: "query-out" },
          to: { type: "langgraph", handle: "lg-input" },
          color: "#22d3ee",
        },
        {
          from: { type: "langgraph", handle: "lg-output" },
          to: { type: "a2a_message", handle: "a2a-in" },
          color: "#d946ef",
        },
        {
          from: { type: "a2a_message", handle: "a2a-out" },
          to: { type: "agents_cluster", handle: "agents-in" },
          color: "#fbbf24",
        },
        {
          from: { type: "agents_cluster", handle: "agents-out" },
          to: { type: "a2a_responses", handle: "responses-in" },
          color: "#38bdf8",
        },
        {
          from: { type: "a2a_responses", handle: "responses-out" },
          to: { type: "synthesis", handle: "synthesis-in" },
          color: "#818cf8",
        },
        {
          from: { type: "synthesis", handle: "synthesis-out" },
          to: { type: "final_result", handle: "final-in" },
          color: "#c084fc",
        },
      ];

      const isAllowed = flowRules.find(
        (rule) =>
          rule.from.type === sourceNode.type &&
          rule.from.handle === (params.sourceHandle || "") &&
          rule.to.type === targetNode.type &&
          rule.to.handle === (params.targetHandle || ""),
      );

      if (!isAllowed) {
        alert(
          "❌ Conexión no válida. Sigue el flujo:\n1. User Query (cyan) → LangGraph (fucsia)\n2. LangGraph → A2A Messages (ámbar)\n3. A2A Messages → Agents Cluster (azul)\n4. Agents → A2A Responses (índigo)\n5. Responses → Synthesis (violeta)\n6. Synthesis → Final Result (verde)\nVerifica los colores de los handles.",
        );
        return;
      }

      const newEdge = {
        ...params,
        style: { stroke: isAllowed.color, strokeWidth: 2 },
        animated: true,
      };

      setEdges((eds) => addEdge(newEdge, eds));
    },
    [nodes, setEdges],
  );

  const addNode = (type: string) => {
    const newNode = {
      id: `${nodeIdCounter}`,
      type,
      position: { x: Math.random() * 400 + 200, y: Math.random() * 300 + 100 },
      data: { 
        label: getNodeLabel(type),
        type: type as any,
      },
    };
    setNodes((nds) => nds.concat(newNode));
    setNodeIdCounter((prev) => prev + 1);
  };

  const getNodeLabel = (type: string) => {
    switch (type) {
      case "user_query":
        return "User Query Intake";
      case "langgraph":
        return "LangGraph StateGraph";
      case "a2a_message":
        return "A2A Message Dispatch";
      case "agents_cluster":
        return "Agents Cluster";
      case "a2a_responses":
        return "A2A Responses Collector";
      case "synthesis":
        return "Synthesis Engine";
      case "final_result":
        return "Final Result";
      default:
        return "Node";
    }
  };

  const clearWorkflow = () => {
    setNodes(initialNodes);
    setEdges([]);
    setNodeIdCounter(initialNodes.length + 1);
  };

  const validatePipeline = () => {
    const requiredSteps = [
      { type: "user_query", label: "User Query" },
      { type: "langgraph", label: "LangGraph StateGraph" },
      { type: "a2a_message", label: "A2A Message Dispatch" },
      { type: "agents_cluster", label: "Agents Cluster" },
      { type: "a2a_responses", label: "A2A Responses Collector" },
      { type: "synthesis", label: "Synthesis Engine" },
      { type: "final_result", label: "Final Result" },
    ];

    const missing = requiredSteps
      .filter((step) => !nodes.some((node) => node.type === step.type))
      .map((step) => step.label);

    const errors: string[] = [];
    if (missing.length > 0) {
      errors.push(`Faltan nodos obligatorios: ${missing.join(", ")}.`);
    }

    const agentsNode = nodes.find((node) => node.type === "agents_cluster");
    const agentsData = agentsNode?.data as { selectedAgents?: string[] } | undefined;
    const selectedAgents = Array.isArray(agentsData?.selectedAgents)
      ? agentsData?.selectedAgents
      : [];

    if (!selectedAgents || selectedAgents.length === 0) {
      errors.push("Configura al menos un agente en el nodo Agents Cluster.");
    }

    return { valid: errors.length === 0, errors };
  };

  const runWorkflow = async () => {
    const validation = validatePipeline();
    if (!validation.valid) {
      alert(`⚠️ Antes de ejecutar:\n${validation.errors.join("\n")}`);
      return;
    }

    setIsRunning(true);
    
    try {
      const executor = new WorkflowExecutor(nodes, edges);
      const result = await executor.execute();
      
      if (result.success) {
        // Actualizar nodos de output_base y output_final con los resultados
        setNodes((nds) =>
          nds.map((node) => {
            if (node.type === 'output_base' || node.type === 'output_final') {
              const output = result.outputs[node.id];
              return {
                ...node,
                data: {
                  ...node.data,
                  result: output || 'No output generated',
                },
              };
            }
            return node;
          })
        );
        alert('✅ Workflow executed successfully!');
      } else {
        alert(`❌ Workflow execution failed:\n${result.errors.join('\n')}`);
      }
    } catch (error) {
      alert(`❌ Error: ${error}`);
    } finally {
      setIsRunning(false);
    }
  };

  const saveWorkflow = () => {
    const workflow = {
      nodes,
      edges,
      timestamp: new Date().toISOString(),
    };
    localStorage.setItem('atp-workflow', JSON.stringify(workflow));
    alert('✅ Workflow saved to browser storage!');
  };

  const loadWorkflow = () => {
    const saved = localStorage.getItem('atp-workflow');
    if (saved) {
      const workflow = JSON.parse(saved);
      setNodes(workflow.nodes);
      setEdges(workflow.edges);
      alert('✅ Workflow loaded from browser storage!');
    } else {
      alert('⚠️ No saved workflow found in browser storage.');
    }
  };

  const exportWorkflow = () => {
    const workflow = {
      name: 'ATP Workflow',
      version: '1.0',
      nodes,
      edges,
      timestamp: new Date().toISOString(),
    };
    
    const dataStr = JSON.stringify(workflow, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `atp-workflow-${Date.now()}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  const importWorkflow = () => {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.json';
    input.onchange = (e: any) => {
      const file = e.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (event) => {
          try {
            const workflow = JSON.parse(event.target?.result as string);
            if (workflow.nodes && workflow.edges) {
              setNodes(workflow.nodes);
              setEdges(workflow.edges);
              alert('✅ Workflow imported successfully!');
            } else {
              alert('⚠️ Invalid workflow file format.');
            }
          } catch (error) {
            alert('❌ Error parsing workflow file.');
          }
        };
        reader.readAsText(file);
      }
    };
    input.click();
  };

  return (
    <div className="h-screen w-screen bg-background">
      {/* Top Bar */}
      <div className="h-14 bg-card border-b border-border flex items-center justify-between px-4">
        <div className="flex items-center gap-4">
          <Link href="/" className="flex items-center gap-2 hover:bg-muted px-3 py-2 rounded transition-colors">
            <Home className="h-5 w-5" />
            <span className="font-semibold">Chat Interface</span>
          </Link>
          <div className="flex items-center gap-2">
            <LayoutGrid className="h-5 w-5 text-primary" />
            <span className="font-bold text-lg">Node Workflow Editor</span>
          </div>
        </div>
        
        <div className="flex items-center gap-2">
          <LanguageSelector onLanguageChange={(lang) => setCurrentLang(lang)} />
          <ThemeSelector />
          
          <button
            onClick={importWorkflow}
            className="flex items-center gap-2 px-3 py-2 bg-card border border-border rounded hover:bg-muted transition-colors"
            title="Import Workflow"
          >
            <Upload className="h-4 w-4" />
            Import
          </button>
          <button
            onClick={exportWorkflow}
            className="flex items-center gap-2 px-3 py-2 bg-card border border-border rounded hover:bg-muted transition-colors"
            title="Export Workflow"
          >
            <Download className="h-4 w-4" />
            Export
          </button>
          <button
            onClick={saveWorkflow}
            className="flex items-center gap-2 px-3 py-2 bg-primary text-primary-foreground rounded hover:bg-primary/90 transition-colors"
            title="Save to Browser"
          >
            <Save className="h-4 w-4" />
            Save
          </button>
          <button
            onClick={loadWorkflow}
            className="flex items-center gap-2 px-3 py-2 bg-card border border-border rounded hover:bg-muted transition-colors"
            title="Load from Browser"
          >
            <FolderOpen className="h-4 w-4" />
            Load
          </button>
          <button
            onClick={clearWorkflow}
            className="flex items-center gap-2 px-3 py-2 bg-card border border-border rounded hover:bg-muted transition-colors"
            title="Clear Canvas"
          >
            <Trash2 className="h-4 w-4" />
            Clear
          </button>
          <button
            onClick={runWorkflow}
            disabled={isRunning}
            className="flex items-center gap-2 px-3 py-2 bg-green-600 text-white rounded hover:bg-green-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            title="Execute Workflow"
          >
            {isRunning ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" />
                Running...
              </>
            ) : (
              <>
                <Play className="h-4 w-4" />
                Run Workflow
              </>
            )}
          </button>
        </div>
      </div>

      {/* Main Canvas */}
      <div className="h-[calc(100vh-3.5rem)] flex">
        {/* Sidebar - Node Palette */}
        <div className="w-72 bg-card border-r border-border p-4 overflow-y-auto max-h-[calc(100vh-3.5rem)]">
          <h3 className="font-bold mb-4 text-sm uppercase text-muted-foreground">Add Workflow Nodes</h3>
          
          <div className="space-y-3 overflow-y-auto max-h-[calc(100vh-18rem)] pb-4">
            <button
              onClick={() => addNode("user_query")}
              className="w-full flex items-center gap-3 p-3 bg-background border-2 border-cyan-400/60 rounded-xl hover:bg-muted transition-colors"
            >
              <Keyboard className="h-5 w-5 text-cyan-400" />
              <div className="text-left">
                <div className="font-semibold text-sm">User Query Intake</div>
                <div className="text-xs text-muted-foreground">Contexto + Persona + Urgencia</div>
              </div>
            </button>

            <button
              onClick={() => addNode("langgraph")}
              className="w-full flex items-center gap-3 p-3 bg-background border-2 border-fuchsia-400/60 rounded-xl hover:bg-muted transition-colors"
            >
              <Workflow className="h-5 w-5 text-fuchsia-400" />
              <div className="text-left">
                <div className="font-semibold text-sm">LangGraph StateGraph</div>
                <div className="text-xs text-muted-foreground">Estrategia + Modelo + Paralelismo</div>
              </div>
            </button>

            <button
              onClick={() => addNode("a2a_message")}
              className="w-full flex items-center gap-3 p-3 bg-background border-2 border-amber-400/60 rounded-xl hover:bg-muted transition-colors"
            >
              <RadioTower className="h-5 w-5 text-amber-300" />
              <div className="text-left">
                <div className="font-semibold text-sm">A2A Message Dispatch</div>
                <div className="text-xs text-muted-foreground">Canal + Prioridad + Payload</div>
              </div>
            </button>

            <button
              onClick={() => addNode("agents_cluster")}
              className="w-full flex items-center gap-3 p-3 bg-background border-2 border-sky-400/60 rounded-xl hover:bg-muted transition-colors"
            >
              <Layers3 className="h-5 w-5 text-sky-300" />
              <div className="text-left">
                <div className="font-semibold text-sm">Agents Cluster</div>
                <div className="text-xs text-muted-foreground">Selección multi-nivel + Concurrencia</div>
              </div>
            </button>

            <button
              onClick={() => addNode("a2a_responses")}
              className="w-full flex items-center gap-3 p-3 bg-background border-2 border-indigo-400/60 rounded-xl hover:bg-muted transition-colors"
            >
              <Inbox className="h-5 w-5 text-indigo-300" />
              <div className="text-left">
                <div className="font-semibold text-sm">A2A Responses Collector</div>
                <div className="text-xs text-muted-foreground">Conteo de respuestas + Timeout</div>
              </div>
            </button>

            <button
              onClick={() => addNode("synthesis")}
              className="w-full flex items-center gap-3 p-3 bg-background border-2 border-violet-400/60 rounded-xl hover:bg-muted transition-colors"
            >
              <Sparkles className="h-5 w-5 text-violet-300" />
              <div className="text-left">
                <div className="font-semibold text-sm">Synthesis Engine</div>
                <div className="text-xs text-muted-foreground">Estrategia + Tono + Traza</div>
              </div>
            </button>

            <button
              onClick={() => addNode("final_result")}
              className="w-full flex items-center gap-3 p-3 bg-background border-2 border-emerald-400/60 rounded-xl hover:bg-muted transition-colors"
            >
              <Trophy className="h-5 w-5 text-emerald-300" />
              <div className="text-left">
                <div className="font-semibold text-sm">Final Result</div>
                <div className="text-xs text-muted-foreground">Output final + Export/Share</div>
              </div>
            </button>
          </div>

          <div className="mt-6 p-4 bg-muted/60 rounded-xl text-xs space-y-3 border border-border/60">
            <div>
              <p className="font-semibold mb-2">{t("howToUse")}:</p>
              <ul className="space-y-1 text-muted-foreground">
                <li>1. Añade los nodos en orden del flujo oficial.</li>
                <li>2. Configura cada etapa (inputs, estrategia, agentes).</li>
                <li>3. Conecta siguiendo los colores de los handles.</li>
                <li>4. Pulsa “Run Workflow” para ejecutar todo el pipeline.</li>
              </ul>
            </div>

            <div>
              <p className="font-semibold mb-2">🎨 Connection Colors</p>
              <ul className="space-y-1.5 text-muted-foreground">
                <li className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full" style={{ backgroundColor: "#22d3ee" }}></div>
                  <span className="text-[10px]">Cyan · User Query → LangGraph</span>
                </li>
                <li className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full" style={{ backgroundColor: "#d946ef" }}></div>
                  <span className="text-[10px]">Fuchsia · LangGraph → A2A Messages</span>
                </li>
                <li className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full" style={{ backgroundColor: "#fbbf24" }}></div>
                  <span className="text-[10px]">Amber · A2A Messages → Agents Cluster</span>
                </li>
                <li className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full" style={{ backgroundColor: "#38bdf8" }}></div>
                  <span className="text-[10px]">Sky · Agents → A2A Responses</span>
                </li>
                <li className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full" style={{ backgroundColor: "#818cf8" }}></div>
                  <span className="text-[10px]">Indigo · Responses → Synthesis</span>
                </li>
                <li className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full" style={{ backgroundColor: "#c084fc" }}></div>
                  <span className="text-[10px]">Violet · Synthesis → Final Result</span>
                </li>
              </ul>
            </div>

            <div>
              <p className="font-semibold mb-2">⚠️ Validaciones</p>
              <ul className="space-y-1 text-muted-foreground">
                <li>• Todos los nodos del flujo son obligatorios.</li>
                <li>• Debes seleccionar al menos un agente en el Agents Cluster.</li>
                <li>• Solo se permiten conexiones en el orden real del backend.</li>
              </ul>
            </div>
          </div>
        </div>

        {/* React Flow Canvas */}
        <div ref={reactFlowWrapper} className="flex-1">
          <ReactFlow
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onConnect={onConnect}
            nodeTypes={nodeTypes}
            fitView
          >
            <Controls />
            <MiniMap />
            <Background variant={BackgroundVariant.Dots} gap={12} size={1} />
          </ReactFlow>
        </div>
      </div>
    </div>
  );
}
