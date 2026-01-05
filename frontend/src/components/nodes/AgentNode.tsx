"use client";

import { memo, useState, useEffect } from 'react';
import { Handle, Position, NodeProps, useReactFlow } from 'reactflow';
import { Bot, ChevronDown, Info } from 'lucide-react';

const AGENTS_DATA = [
  // Level 1 - Critical (6 agentes)
  { name: "reasoning", role: "Maestro de Razonamiento Lógico", level: 1, skills: ["Deducción", "Inducción", "Análisis lógico"], color: "#ef4444" },
  { name: "planning", role: "Estratega de Planificación", level: 1, skills: ["Gestión de proyectos", "Planificación estratégica"], color: "#ef4444" },
  { name: "research", role: "Investigador Senior", level: 1, skills: ["Investigación profunda", "Síntesis de información"], color: "#ef4444" },
  { name: "analysis", role: "Analista Experto", level: 1, skills: ["Descomposición de problemas", "Análisis de datos"], color: "#ef4444" },
  { name: "synthesis", role: "Integrador de Conocimiento", level: 1, skills: ["Integración de información", "Generación de insights"], color: "#ef4444" },
  { name: "critical_thinking", role: "Evaluador Crítico", level: 1, skills: ["Evaluación de argumentos", "Detección de falacias"], color: "#ef4444" },
  
  // Level 2 - Essential (6 agentes)
  { name: "coding", role: "Ingeniero de Software Senior", level: 2, skills: ["Programación", "Arquitectura", "Debug"], color: "#f97316" },
  { name: "data", role: "Científico de Datos", level: 2, skills: ["Análisis de datos", "Estadística", "ML"], color: "#f97316" },
  { name: "writing", role: "Escritor Profesional", level: 2, skills: ["Redacción", "Copywriting", "Storytelling"], color: "#f97316" },
  { name: "communication", role: "Especialista en Comunicación", level: 2, skills: ["Comunicación efectiva", "Negociación"], color: "#f97316" },
  { name: "decision", role: "Estratega de Decisiones", level: 2, skills: ["Toma de decisiones", "Análisis de riesgos"], color: "#f97316" },
  { name: "problem_solving", role: "Solucionador Creativo", level: 2, skills: ["Resolución creativa", "Pensamiento lateral"], color: "#f97316" },
  
  // Level 3 - Specialized (6 agentes)
  { name: "legal", role: "Asesor Legal", level: 3, skills: ["Análisis legal", "Cumplimiento", "Contratos"], color: "#eab308" },
  { name: "financial", role: "Analista Financiero", level: 3, skills: ["Finanzas", "Valoración", "Inversiones"], color: "#eab308" },
  { name: "creative", role: "Director Creativo", level: 3, skills: ["Creatividad", "Innovación", "Diseño"], color: "#eab308" },
  { name: "technical", role: "Arquitecto Técnico", level: 3, skills: ["Arquitectura", "Sistemas", "Cloud"], color: "#eab308" },
  { name: "educational", role: "Educador Experto", level: 3, skills: ["Pedagogía", "Enseñanza", "Diseño instruccional"], color: "#eab308" },
  { name: "marketing", role: "Estratega de Marketing", level: 3, skills: ["Marketing digital", "SEO", "Branding"], color: "#eab308" },
  
  // Level 4 - Support (6 agentes)
  { name: "qa", role: "Ingeniero de Calidad", level: 4, skills: ["Testing", "QA", "Calidad"], color: "#22c55e" },
  { name: "documentation", role: "Documentador Técnico", level: 4, skills: ["Documentación", "Tutoriales", "Guías"], color: "#22c55e" },
  { name: "optimization", role: "Optimizador de Performance", level: 4, skills: ["Optimización", "Eficiencia", "Performance"], color: "#22c55e" },
  { name: "security", role: "Experto en Seguridad", level: 4, skills: ["Seguridad", "Auditoría", "Protección"], color: "#22c55e" },
  { name: "integration", role: "Arquitecto de Integraciones", level: 4, skills: ["APIs", "Integraciones", "ETL"], color: "#22c55e" },
  { name: "review", role: "Revisor Experto", level: 4, skills: ["Revisión", "Feedback", "Mejora"], color: "#22c55e" },
  
  // Level 5 - Auxiliary (6 agentes)
  { name: "translation", role: "Traductor Profesional", level: 5, skills: ["Traducción", "Localización", "Idiomas"], color: "#3b82f6" },
  { name: "summary", role: "Especialista en Resumen", level: 5, skills: ["Resumen", "Síntesis", "Compresión"], color: "#3b82f6" },
  { name: "formatting", role: "Especialista en Formato", level: 5, skills: ["Formato", "Estilo", "Presentación"], color: "#3b82f6" },
  { name: "validation", role: "Validador de Datos", level: 5, skills: ["Validación", "Verificación", "Chequeo"], color: "#3b82f6" },
  { name: "coordination", role: "Coordinador de Flujos", level: 5, skills: ["Coordinación", "Gestión", "Workflows"], color: "#3b82f6" },
  { name: "explanation", role: "Explicador Experto", level: 5, skills: ["Explicación", "Clarificación", "Enseñanza"], color: "#3b82f6" },
];

export default memo(({ data, id, selected }: NodeProps) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const [selectedAgent, setSelectedAgent] = useState(data.agentName || '');
  const [additionalText, setAdditionalText] = useState(data.additionalInstructions || '');
  const { setNodes } = useReactFlow();

  // Determinar el nivel del nodo basado en el tipo
  const nodeLevel = data.agentLevel || (() => {
    const type = data.type;
    if (type === 'agent_l1') return 1;
    if (type === 'agent_l2') return 2;
    if (type === 'agent_l3') return 3;
    if (type === 'agent_l4') return 4;
    if (type === 'agent_l5') return 5;
    return 1; // Default
  })();

  // Filtrar agentes solo del nivel correspondiente
  const availableAgents = AGENTS_DATA.filter(a => a.level === nodeLevel);
  const currentAgent = AGENTS_DATA.find(a => a.name === selectedAgent);

  const handleAgentChange = (agentName: string) => {
    setSelectedAgent(agentName);
    const agent = AGENTS_DATA.find(a => a.name === agentName);
    
    setNodes((nds) =>
      nds.map((node) => {
        if (node.id === id) {
          return {
            ...node,
            data: {
              ...node.data,
              agentName,
              agentRole: agent?.role || '',
              agentSkills: agent?.skills || [],
            },
          };
        }
        return node;
      })
    );
  };

  const handleTextChange = (text: string) => {
    setAdditionalText(text);
    setNodes((nds) =>
      nds.map((node) => {
        if (node.id === id) {
          return {
            ...node,
            data: {
              ...node.data,
              additionalInstructions: text,
            },
          };
        }
        return node;
      })
    );
  };

  const getLevelColor = (level: number) => {
    switch(level) {
      case 1: return { border: '#ef4444', bg: '#ef4444/10', text: '#ef4444' }; // Red
      case 2: return { border: '#f97316', bg: '#f97316/10', text: '#f97316' }; // Orange
      case 3: return { border: '#eab308', bg: '#eab308/10', text: '#eab308' }; // Yellow
      case 4: return { border: '#22c55e', bg: '#22c55e/10', text: '#22c55e' }; // Green
      case 5: return { border: '#3b82f6', bg: '#3b82f6/10', text: '#3b82f6' }; // Blue
      default: return { border: '#6b7280', bg: '#6b7280/10', text: '#6b7280' };
    }
  };

  const levelColors = currentAgent ? getLevelColor(currentAgent.level) : getLevelColor(0);

  return (
    <div 
      className={`px-4 py-3 shadow-lg rounded-lg border-2 bg-card/80 backdrop-blur-sm min-w-[280px] relative overflow-hidden ${
        selected ? 'border-primary' : 'border-border'
      }`}
      style={{ 
        borderColor: currentAgent ? levelColors.border : undefined,
      }}
    >
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <Bot className="h-5 w-5" style={{ color: currentAgent ? levelColors.text : undefined }} />
          <div className="font-bold text-sm">{data.label}</div>
          {/* Level Badge - movido aquí para evitar conflicto */}
          {currentAgent && (
            <div 
              className="px-2 py-0.5 rounded-full text-[10px] font-bold ml-1"
              style={{ 
                backgroundColor: levelColors.bg,
                color: levelColors.text,
                border: `1px solid ${levelColors.border}`
              }}
            >
              L{currentAgent.level}
            </div>
          )}
        </div>
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="p-1 hover:bg-muted rounded transition-colors"
        >
          <ChevronDown className={`h-4 w-4 transition-transform ${isExpanded ? 'rotate-180' : ''}`} />
        </button>
      </div>
      
      {/* Agent Selector */}
      <div className="mb-2">
        <label className="text-xs text-muted-foreground mb-1 block">
          Select Agent (Level {nodeLevel} - {availableAgents.length} available)
        </label>
        <select
          value={selectedAgent}
          onChange={(e) => handleAgentChange(e.target.value)}
          className="w-full text-xs bg-background border border-border rounded p-2"
        >
          <option value="">-- Select Agent --</option>
          {availableAgents.map((agent) => (
            <option key={agent.name} value={agent.name}>
              {agent.role}
            </option>
          ))}
        </select>
      </div>

      {/* Agent Info */}
      {currentAgent && (
        <div className="mb-2 p-2 bg-muted/50 rounded text-xs">
          <div className="font-semibold text-primary mb-1">{currentAgent.role}</div>
          <div className="flex items-start gap-1 text-muted-foreground">
            <Info className="h-3 w-3 mt-0.5 flex-shrink-0" />
            <div className="flex flex-wrap gap-1">
              {currentAgent.skills.map((skill, idx) => (
                <span key={idx} className="px-1.5 py-0.5 bg-primary/10 rounded text-[10px]">
                  {skill}
                </span>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Additional Instructions */}
      {isExpanded && (
        <div className="mb-2">
          <label className="text-xs text-muted-foreground mb-1 block">Additional Instructions</label>
          <textarea
            value={additionalText}
            onChange={(e) => handleTextChange(e.target.value)}
            placeholder="Add specific instructions for this agent..."
            className="w-full text-xs bg-background border border-border rounded p-2"
            rows={3}
          />
        </div>
      )}

      {/* Handles: 3 entradas (morada, naranja, azul) + 1 salida azul */}
      <div className="mt-3 pt-2 border-t border-border">
        {/* Entradas */}
        <div className="flex justify-around items-center mb-2">
          <div className="flex flex-col items-center gap-1">
            <div className="text-[9px] text-purple-500 font-semibold">Prompt</div>
            <Handle
              type="target"
              position={Position.Top}
              id="input-prompt"
              className="!w-4 !h-4 !bg-purple-500 !relative !transform-none !border-2 !border-white"
              style={{ position: 'relative' }}
            />
          </div>
          <div className="flex flex-col items-center gap-1">
            <div className="text-[9px] text-orange-500 font-semibold">AI</div>
            <Handle
              type="target"
              position={Position.Top}
              id="input-ai"
              className="!w-4 !h-4 !bg-orange-500 !relative !transform-none !border-2 !border-white"
              style={{ position: 'relative' }}
            />
          </div>
          <div className="flex flex-col items-center gap-1">
            <div className="text-[9px] text-blue-500 font-semibold">Data</div>
            <Handle
              type="target"
              position={Position.Top}
              id="input-data"
              className="!w-4 !h-4 !bg-blue-500 !relative !transform-none !border-2 !border-white"
              style={{ position: 'relative' }}
            />
          </div>
        </div>
        
        {/* Salida */}
        <div className="flex justify-center items-center">
          <div className="flex items-center gap-2">
            <div className="text-[10px] text-blue-500 font-semibold">Output</div>
            <Handle
              type="source"
              position={Position.Bottom}
              id="output"
              className="!w-4 !h-4 !bg-blue-500 !relative !transform-none !border-2 !border-white"
              style={{ position: 'relative' }}
            />
          </div>
        </div>
      </div>
    </div>
  );
});
