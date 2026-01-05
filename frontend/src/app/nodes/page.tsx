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

import AgentNode from '@/components/nodes/AgentNode';
import PromptNode from '@/components/nodes/PromptNode';
import AIProviderNode from '@/components/nodes/AIProviderNode';
import OutputBaseNode from '@/components/nodes/OutputBaseNode';
import OutputFinalNode from '@/components/nodes/OutputFinalNode';

import { Bot, MessageSquare, Cpu, Keyboard, FileOutput, Play, Save, FolderOpen, LayoutGrid, Home, Trash2, Loader2, Upload, Download, Palette } from 'lucide-react';
import Link from 'next/link';
import { WorkflowExecutor } from '@/lib/workflowExecutor';
import { ThemeSelector } from '@/components/ThemeSelector';
import { LanguageSelector } from '@/components/LanguageSelector';
import { getCurrentLanguage, getTranslation } from '@/lib/i18n';

const nodeTypes = {
  prompt: PromptNode,
  agent_l1: AgentNode,
  agent_l2: AgentNode,
  agent_l3: AgentNode,
  agent_l4: AgentNode,
  agent_l5: AgentNode,
  ai_provider: AIProviderNode,
  output_base: OutputBaseNode,
  output_final: OutputFinalNode,
};

const initialNodes = [
  {
    id: '1',
    type: 'prompt',
    data: { label: 'Prompt Principal', type: 'prompt' },
    position: { x: 50, y: 100 },
  },
];

const initialEdges: Edge[] = [];

export default function NodesPage() {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
  const [nodeIdCounter, setNodeIdCounter] = useState(3);
  const [isRunning, setIsRunning] = useState(false);
  const [currentLang, setCurrentLang] = useState(getCurrentLanguage());
  const reactFlowWrapper = useRef<HTMLDivElement>(null);
  
  const t = (key: any) => getTranslation(currentLang, key);

  const onConnect = useCallback(
    (params: Connection) => {
      const sourceNode = nodes.find(n => n.id === params.source);
      const targetNode = nodes.find(n => n.id === params.target);
      
      if (!sourceNode || !targetNode) return;

      // Validación de conexiones con handles específicos
      const sourceHandle = params.sourceHandle || '';
      const targetHandle = params.targetHandle || '';
      
      // Reglas de validación por tipo y handle
      const isValidConnection = () => {
        // Prompt (salida morada) → Agent (entrada morada)
        if (sourceNode.type === 'prompt' && sourceHandle === 'output') {
          return ['agent_l1', 'agent_l2', 'agent_l3', 'agent_l4', 'agent_l5'].includes(targetNode.type || '') 
                 && targetHandle === 'input-prompt';
        }
        
        // Agent (salida azul) → Output Base (entrada azul)
        if (['agent_l1', 'agent_l2', 'agent_l3', 'agent_l4', 'agent_l5'].includes(sourceNode.type || '') 
            && sourceHandle === 'output') {
          return targetNode.type === 'output_base' && targetHandle === 'input';
        }
        
        // AI Provider (salida naranja) → Agent (entrada naranja)
        if (sourceNode.type === 'ai_provider' && sourceHandle === 'output') {
          return ['agent_l1', 'agent_l2', 'agent_l3', 'agent_l4', 'agent_l5'].includes(targetNode.type || '')
                 && targetHandle === 'input-ai';
        }
        
        // Output Base (salida morada) → Agent (entrada morada) o Output Final (entrada azul)
        if (sourceNode.type === 'output_base' && sourceHandle === 'output') {
          if (['agent_l1', 'agent_l2', 'agent_l3', 'agent_l4', 'agent_l5'].includes(targetNode.type || '')) {
            return targetHandle === 'input-prompt';
          }
          if (targetNode.type === 'output_final') {
            return targetHandle === 'input';
          }
        }
        
        return false;
      };
      
      if (!isValidConnection()) {
        alert(`❌ Conexión no válida\n\nReglas de conexión:\n🟣 Prompt (morado) → Agent entrada morada\n🔵 Agent (azul) → Output Base entrada azul\n🟠 AI Provider (naranja) → Agent entrada naranja\n🟣 Output Base (morado) → Agent entrada morada o Output Final\n\nVerifica los colores de los handles!`);
        return;
      }

      // Asignar colores según el tipo de conexión
      let edgeStyle = { stroke: '#10b981', strokeWidth: 2 };
      
      if (sourceNode.type === 'prompt') {
        edgeStyle = { stroke: '#a855f7', strokeWidth: 2 }; // Purple
      } else if (sourceNode.type === 'ai_provider') {
        edgeStyle = { stroke: '#f97316', strokeWidth: 2 }; // Orange
      } else if (sourceNode.type?.startsWith('agent_')) {
        edgeStyle = { stroke: '#10b981', strokeWidth: 2 }; // Green
      } else if (sourceNode.type === 'output_base') {
        edgeStyle = { stroke: '#3b82f6', strokeWidth: 2 }; // Blue
      }
      
      const newEdge = {
        ...params,
        style: edgeStyle,
        animated: true,
      };
      
      setEdges((eds) => addEdge(newEdge, eds));
    },
    [setEdges, nodes]
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
    setNodeIdCounter(nodeIdCounter + 1);
  };

  const getNodeLabel = (type: string) => {
    switch (type) {
      case 'prompt': return 'Prompt Principal';
      case 'agent_l1': return 'Agent Level 1';
      case 'agent_l2': return 'Agent Level 2';
      case 'agent_l3': return 'Agent Level 3';
      case 'agent_l4': return 'Agent Level 4';
      case 'agent_l5': return 'Agent Level 5';
      case 'ai_provider': return 'AI Provider';
      case 'output_base': return 'Output Base';
      case 'output_final': return 'Output Final';
      default: return 'Node';
    }
  };

  const clearWorkflow = () => {
    setNodes(initialNodes);
    setEdges([]);
    setNodeIdCounter(3);
  };

  const runWorkflow = async () => {
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
        <div className="w-64 bg-card border-r border-border p-4 overflow-y-auto max-h-[calc(100vh-3.5rem)]">
          <h3 className="font-bold mb-4 text-sm uppercase text-muted-foreground">Add Nodes</h3>
          
          <div className="space-y-2 overflow-y-auto max-h-[calc(100vh-20rem)] pb-4">
            <button
              onClick={() => addNode('prompt')}
              className="w-full flex items-center gap-3 p-3 bg-background border-2 border-purple-500/50 rounded hover:bg-muted transition-colors"
            >
              <MessageSquare className="h-5 w-5 text-purple-500" />
              <div className="text-left">
                <div className="font-semibold text-sm">Prompt Principal</div>
                <div className="text-xs text-muted-foreground">+/- prompts</div>
              </div>
            </button>

            <button
              onClick={() => addNode('agent_l1')}
              className="w-full flex items-center gap-3 p-3 bg-background border-2 border-red-500/50 rounded hover:bg-muted transition-colors"
            >
              <Bot className="h-5 w-5 text-red-500" />
              <div className="text-left">
                <div className="font-semibold text-sm">Agent LVL 1</div>
                <div className="text-xs text-muted-foreground">Critical (6 agentes)</div>
              </div>
            </button>

            <button
              onClick={() => addNode('agent_l2')}
              className="w-full flex items-center gap-3 p-3 bg-background border-2 border-orange-500/50 rounded hover:bg-muted transition-colors"
            >
              <Bot className="h-5 w-5 text-orange-500" />
              <div className="text-left">
                <div className="font-semibold text-sm">Agent LVL 2</div>
                <div className="text-xs text-muted-foreground">Professional (6 agentes)</div>
              </div>
            </button>

            <button
              onClick={() => addNode('agent_l3')}
              className="w-full flex items-center gap-3 p-3 bg-background border-2 border-yellow-500/50 rounded hover:bg-muted transition-colors"
            >
              <Bot className="h-5 w-5 text-yellow-500" />
              <div className="text-left">
                <div className="font-semibold text-sm">Agent LVL 3</div>
                <div className="text-xs text-muted-foreground">Specialized (6 agentes)</div>
              </div>
            </button>

            <button
              onClick={() => addNode('agent_l4')}
              className="w-full flex items-center gap-3 p-3 bg-background border-2 border-green-500/50 rounded hover:bg-muted transition-colors"
            >
              <Bot className="h-5 w-5 text-green-500" />
              <div className="text-left">
                <div className="font-semibold text-sm">Agent LVL 4</div>
                <div className="text-xs text-muted-foreground">Support (6 agentes)</div>
              </div>
            </button>

            <button
              onClick={() => addNode('agent_l5')}
              className="w-full flex items-center gap-3 p-3 bg-background border-2 border-blue-500/50 rounded hover:bg-muted transition-colors"
            >
              <Bot className="h-5 w-5 text-blue-500" />
              <div className="text-left">
                <div className="font-semibold text-sm">Agent LVL 5</div>
                <div className="text-xs text-muted-foreground">Auxiliary (6 agentes)</div>
              </div>
            </button>

            <button
              onClick={() => addNode('ai_provider')}
              className="w-full flex items-center gap-3 p-3 bg-background border border-border rounded hover:bg-muted transition-colors"
            >
              <Cpu className="h-5 w-5 text-orange-500" />
              <div className="text-left">
                <div className="font-semibold text-sm">AI Provider</div>
                <div className="text-xs text-muted-foreground">Model config</div>
              </div>
            </button>

            <button
              onClick={() => addNode('output_base')}
              className="w-full flex items-center gap-3 p-3 bg-background border-2 border-blue-500/50 rounded hover:bg-muted transition-colors"
            >
              <FileOutput className="h-5 w-5 text-blue-500" />
              <div className="text-left">
                <div className="font-semibold text-sm">Output Base</div>
                <div className="text-xs text-muted-foreground">Intermediate result</div>
              </div>
            </button>

            <button
              onClick={() => addNode('output_final')}
              className="w-full flex items-center gap-3 p-3 bg-background border-2 border-green-500/50 rounded hover:bg-muted transition-colors"
            >
              <FileOutput className="h-5 w-5 text-green-500" />
              <div className="text-left">
                <div className="font-semibold text-sm">Output Final</div>
                <div className="text-xs text-muted-foreground">Final result</div>
              </div>
            </button>
          </div>

          <div className="mt-6 p-3 bg-muted rounded text-xs">
            <p className="font-semibold mb-2">{t('howToUse')}:</p>
            <ul className="space-y-1 text-muted-foreground">
              <li>• {t('clickNodesToAdd')}</li>
              <li>• {t('dragToConnect')}</li>
              <li>• {t('clickToConfig')}</li>
              <li>• {t('runToExecute')}</li>
            </ul>
            
            <p className="font-semibold mb-2 mt-4">🎨 Connection Colors:</p>
            <ul className="space-y-1.5">
              <li className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full" style={{ backgroundColor: '#a855f7' }}></div>
                <span className="text-[10px]">Prompt → Agent (Purple)</span>
              </li>
              <li className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full" style={{ backgroundColor: '#10b981' }}></div>
                <span className="text-[10px]">Agent → AI/Output (Green)</span>
              </li>
              <li className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full" style={{ backgroundColor: '#f97316' }}></div>
                <span className="text-[10px]">AI Provider → Agent (Orange)</span>
              </li>
              <li className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full" style={{ backgroundColor: '#3b82f6' }}></div>
                <span className="text-[10px]">Output Base → Agent/Final (Blue)</span>
              </li>
            </ul>
            
            <p className="font-semibold mb-2 mt-4">📊 Agent Levels:</p>
            <ul className="space-y-1">
              <li className="flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-red-500"></div>
                <span className="text-[10px]">L1 - Critical (6)</span>
              </li>
              <li className="flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-orange-500"></div>
                <span className="text-[10px]">L2 - Professional (6)</span>
              </li>
              <li className="flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-yellow-500"></div>
                <span className="text-[10px]">L3 - Specialized (6)</span>
              </li>
              <li className="flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-green-500"></div>
                <span className="text-[10px]">L4 - Support (6)</span>
              </li>
              <li className="flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-blue-500"></div>
                <span className="text-[10px]">L5 - Auxiliary (6)</span>
              </li>
            </ul>
            
            <p className="text-[10px] text-muted-foreground mt-3 italic">
              ⚠️ {currentLang === 'es' ? 'Solo se permiten conexiones válidas' : 'Only valid connections are allowed'}
            </p>
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
