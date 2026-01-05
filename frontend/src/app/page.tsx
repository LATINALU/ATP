"use client";

import { useState, useEffect } from "react";
import { Header } from "@/components/Header";
import { Sidebar } from "@/components/Sidebar";
import { ChatInterface } from "@/components/ChatInterface";
import { ThemeSelector } from "@/components/ThemeSelector";
import { LiveReasoning } from "@/components/AgentReasoning";
import { MemoryPanel } from "@/components/MemoryPanel";
import { ApiSettings, ApiProvider } from "@/components/ApiSettings";
import { Settings, Plus, LayoutGrid } from "lucide-react";
import Link from "next/link";
import { LanguageSelector } from "@/components/LanguageSelector";
import { Agent, Message } from "@/types";
import { AgentDetailPanel } from "@/components/AgentDetailPanel";

const AGENTS_DATA: Agent[] = [
  // Level 1 - Critical (6 agentes)
  { name: "reasoning", role: "Maestro de Razonamiento Lógico y Pensamiento Crítico", level: 1 },
  { name: "planning", role: "Estratega de Planificación y Gestión de Proyectos", level: 1 },
  { name: "research", role: "Investigador Senior y Analista de Información", level: 1 },
  { name: "analysis", role: "Analista Experto en Descomposición de Problemas", level: 1 },
  { name: "synthesis", role: "Integrador de Conocimiento y Generador de Insights", level: 1 },
  { name: "critical_thinking", role: "Evaluador Crítico y Detector de Falacias", level: 1 },
  // Level 2 - Essential (6 agentes)
  { name: "coding", role: "Ingeniero de Software Senior y Arquitecto de Código", level: 2 },
  { name: "data", role: "Científico de Datos y Analista Cuantitativo", level: 2 },
  { name: "writing", role: "Escritor Profesional y Comunicador Experto", level: 2 },
  { name: "communication", role: "Especialista en Comunicación y Relaciones", level: 2 },
  { name: "decision", role: "Estratega de Decisiones y Análisis de Opciones", level: 2 },
  { name: "problem_solving", role: "Solucionador Creativo de Problemas", level: 2 },
  // Level 3 - Specialized (6 agentes)
  { name: "legal", role: "Asesor Legal y Especialista en Cumplimiento", level: 3 },
  { name: "financial", role: "Analista Financiero y Estratega Económico", level: 3 },
  { name: "creative", role: "Director Creativo y Generador de Ideas", level: 3 },
  { name: "technical", role: "Arquitecto Técnico y Especialista en Sistemas", level: 3 },
  { name: "educational", role: "Educador Experto y Diseñador Instruccional", level: 3 },
  { name: "marketing", role: "Estratega de Marketing y Especialista en Branding", level: 3 },
  // Level 4 - Support (6 agentes)
  { name: "qa", role: "Ingeniero de Calidad y Testing", level: 4 },
  { name: "documentation", role: "Especialista en Documentación Técnica", level: 4 },
  { name: "optimization", role: "Ingeniero de Optimización y Performance", level: 4 },
  { name: "security", role: "Especialista en Seguridad de la Información", level: 4 },
  { name: "integration", role: "Arquitecto de Integraciones y APIs", level: 4 },
  { name: "review", role: "Revisor Experto y Coach de Mejora", level: 4 },
  // Level 5 - Auxiliary (6 agentes)
  { name: "translation", role: "Traductor Profesional y Especialista en Localización", level: 5 },
  { name: "summary", role: "Especialista en Síntesis y Resumen", level: 5 },
  { name: "formatting", role: "Especialista en Formato y Presentación Visual", level: 5 },
  { name: "validation", role: "Verificador de Exactitud y Consistencia", level: 5 },
  { name: "coordination", role: "Coordinador de Equipos y Flujos de Trabajo", level: 5 },
  { name: "explanation", role: "Explicador Experto y Clarificador", level: 5 },
];

const DEFAULT_MODEL = "openai/gpt-oss-120b";
const GROQ_FALLBACK_MODELS = [
  { id: "openai/gpt-oss-120b", name: "openai/gpt-oss-120b", provider: "Groq" },
  { id: "llama-3.3-70b-versatile", name: "llama-3.3-70b-versatile", provider: "Groq" },
  { id: "mixtral-8x7b-32768", name: "mixtral-8x7b-32768", provider: "Groq" },
];

interface AgentProgress {
  agent_id: string;
  agent_name: string;
  status: "pending" | "processing" | "completed" | "error";
  progress?: number;
  current_step?: string;
  result?: string;
}

export default function Home() {
  const [selectedAgents, setSelectedAgents] = useState<string[]>([
    "reasoning",
    "analysis",
    "synthesis",
  ]);
  const [messages, setMessages] = useState<Message[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [isConnected, setIsConnected] = useState(false);
  const [model, setModel] = useState(DEFAULT_MODEL);
  const [showApiSettings, setShowApiSettings] = useState(false);
  const [apiProviders, setApiProviders] = useState<ApiProvider[]>([]);
  const [availableModels, setAvailableModels] = useState<{id: string; name: string; provider: string}[]>([]);
  const [agentModels, setAgentModels] = useState<Record<string, string>>({});
  const [agentInstructions, setAgentInstructions] = useState<Record<string, string>>({});
  const [currentAgentProgress, setCurrentAgentProgress] = useState<AgentProgress[]>([]);
  const [activeAgentDetail, setActiveAgentDetail] = useState<string | null>(null);

  useEffect(() => {
    // Check backend connection
    const checkConnection = async () => {
      try {
        const response = await fetch("/api/health");
        setIsConnected(response.ok);
      } catch {
        setIsConnected(false);
      }
    };
    checkConnection();
    const interval = setInterval(checkConnection, 30000);
    return () => clearInterval(interval);
  }, []);

  // Load API providers from localStorage
  useEffect(() => {
    const saved = localStorage.getItem("atp-api-providers");
    if (saved) {
      try {
        const providers = JSON.parse(saved);
        setApiProviders(providers);
        
        // Get models from ALL active providers with API keys (SOLO enabledModels)
        const activeProviders = providers.filter((p: ApiProvider) => p.isActive && p.apiKey);
        if (activeProviders.length > 0) {
          const allModels = activeProviders.flatMap((p: ApiProvider) => 
            (p.enabledModels || p.models).map((m: string) => ({ 
              id: m, 
              name: m,
              provider: p.name 
            }))
          );
          setAvailableModels(allModels);
          
          // Si el modelo actual no está en los disponibles, seleccionar el primero
          if (allModels.length > 0 && !allModels.find((m: {id: string}) => m.id === model)) {
            setModel(allModels[0].id);
          }
        } else {
          // No hay providers activos con API keys
          setAvailableModels(GROQ_FALLBACK_MODELS);
          setModel(DEFAULT_MODEL);
        }
      } catch (e) {
        console.error("Error loading API providers:", e);
        setAvailableModels(GROQ_FALLBACK_MODELS);
        setModel(DEFAULT_MODEL);
      }
    } else {
      // No hay providers guardados
      setAvailableModels(GROQ_FALLBACK_MODELS);
      setModel(DEFAULT_MODEL);
    }
    
    // Load agent models config
    const savedAgentModels = localStorage.getItem("atp-agent-models");
    if (savedAgentModels) {
      try {
        setAgentModels(JSON.parse(savedAgentModels));
      } catch (e) {
        console.error("Error loading agent models:", e);
      }
    }
    
    // Load agent instructions
    const savedInstructions = localStorage.getItem("atp-agent-instructions");
    if (savedInstructions) {
      try {
        setAgentInstructions(JSON.parse(savedInstructions));
      } catch (e) {
        console.error("Error loading agent instructions:", e);
      }
    }
  }, []);

  const handleAgentToggle = (agentName: string) => {
    setSelectedAgents((prev) =>
      prev.includes(agentName)
        ? prev.filter((a) => a !== agentName)
        : [...prev, agentName]
    );
  };

  const handleSelectAll = (level?: number) => {
    if (level) {
      const levelAgents = AGENTS_DATA.filter((a) => a.level === level).map(
        (a) => a.name
      );
      setSelectedAgents((prev) => {
        const otherAgents = prev.filter(
          (a) => !levelAgents.includes(a)
        );
        return [...otherAgents, ...levelAgents];
      });
    } else {
      setSelectedAgents(AGENTS_DATA.map((a) => a.name));
    }
  };

  const handleClearAll = () => {
    setSelectedAgents([]);
  };

  const handleAgentModelChange = (agentName: string, modelId: string) => {
    const newAgentModels = { ...agentModels, [agentName]: modelId };
    setAgentModels(newAgentModels);
    localStorage.setItem("atp-agent-models", JSON.stringify(newAgentModels));
  };

  const handleAgentInstructionsChange = (agentName: string, instructions: string) => {
    const newInstructions = { ...agentInstructions, [agentName]: instructions };
    setAgentInstructions(newInstructions);
    localStorage.setItem("atp-agent-instructions", JSON.stringify(newInstructions));
  };

  const handleShowAgentDetails = (agentName: string) => {
    setActiveAgentDetail(agentName);
  };

  const activeAgentMeta = activeAgentDetail
    ? AGENTS_DATA.find((agent) => agent.name === activeAgentDetail)
    : undefined;

  const handleProvidersChange = (providers: ApiProvider[]) => {
    setApiProviders(providers);
    // Update available models from ALL active providers with API keys (SOLO enabledModels)
    const activeProviders = providers.filter(p => p.isActive && p.apiKey);
    if (activeProviders.length > 0) {
      const allModels = activeProviders.flatMap(p => 
        (p.enabledModels || p.models).map(m => ({ 
          id: m, 
          name: m,
          provider: p.name 
        }))
      );
      setAvailableModels(allModels);
      
      // Si el modelo actual no está disponible, seleccionar el primero
      if (allModels.length > 0 && !allModels.find((m: {id: string}) => m.id === model)) {
        setModel(allModels[0].id);
      }
    } else {
      setAvailableModels(GROQ_FALLBACK_MODELS);
      setModel(DEFAULT_MODEL); // Mantener modelo predeterminado Groq
    }
  };

  const handleSendMessage = async (content: string) => {
    if (!content.trim() || selectedAgents.length === 0) return;

    const effectiveModel = model || DEFAULT_MODEL;
    const activeGroqProvider = apiProviders.find(
      (p) => p.isActive && p.apiKey && p.type === "groq"
    );

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsProcessing(true);
    
    // Inicializar progreso de agentes
    const initialProgress: AgentProgress[] = selectedAgents.map(agentId => ({
      agent_id: agentId,
      agent_name: AGENTS_DATA.find(a => a.name === agentId)?.role || agentId,
      status: "pending",
      progress: 0,
      current_step: "Esperando..."
    }));
    setCurrentAgentProgress(initialProgress);

    try {
      // Timeout de 5 minutos para procesamiento largo
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 300000); // 5 minutos
      
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: content,
          agents: selectedAgents,
          model: effectiveModel,
          // Only send API config if the user added one; otherwise backend uses server defaults
          apiConfig: activeGroqProvider && activeGroqProvider.apiKey ? activeGroqProvider : undefined,
          // Enviar configuraciones personalizadas de agentes
          agentModels,
          agentInstructions,
        }),
        signal: controller.signal,
      });
      
      clearTimeout(timeoutId);

      if (!response.ok) {
        throw new Error("Error en la respuesta del servidor");
      }

      const data = await response.json();

      // Check if there's an error in the response
      let responseContent = "";
      if (data.error) {
        responseContent = `⚠️ **Error del backend:** ${data.error}`;
      } else if (data.result && data.result.trim()) {
        responseContent = data.result;
      } else if (data.message) {
        responseContent = data.message;
      } else {
        responseContent = "⚠️ No se recibió respuesta del servidor. Verifica que hayas configurado una API key válida en ⚙️ Configuración.";
      }

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: responseContent,
        timestamp: new Date(),
        agents: selectedAgents,
        status: data.success ? "completed" : "error",
        a2a_messages_count: data.a2a_messages_count,
        a2a_responses_count: data.a2a_responses_count,
      };

      setMessages((prev) => [...prev, assistantMessage]);
      
      // Actualizar progreso final de agentes
      if (data.agents_used) {
        const finalProgress: AgentProgress[] = data.agents_used.map((agentId: string) => ({
          agent_id: agentId,
          agent_name: AGENTS_DATA.find(a => a.name === agentId)?.role || agentId,
          status: "completed" as const,
          progress: 100,
          current_step: "Completado"
        }));
        setCurrentAgentProgress(finalProgress);
      }
    } catch (error) {
      let errorContent = "Error desconocido";
      
      if (error instanceof Error) {
        if (error.name === "AbortError") {
          errorContent = "⚠️ **Timeout:** El procesamiento tomó más de 5 minutos. Los agentes pueden estar procesando tareas muy complejas. Intenta con una tarea más simple o menos agentes.";
        } else {
          errorContent = `Error: ${error.message}. Asegúrate de que el backend esté ejecutándose.`;
        }
      }
      
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: errorContent,
        timestamp: new Date(),
        status: "error",
      };
      setMessages((prev) => [...prev, errorMessage]);
      
      // Marcar agentes como error
      setCurrentAgentProgress(prev => prev.map(agent => ({
        ...agent,
        status: "error" as const,
        current_step: "Error en procesamiento"
      })));
    } finally {
      setIsProcessing(false);
      // Limpiar progreso después de 3 segundos
      setTimeout(() => setCurrentAgentProgress([]), 3000);
    }
  };

  const handleNewChat = () => {
    setMessages([]);
    setIsProcessing(false);
  };

  const handleLoadMemory = (memory: any) => {
    setMessages(memory.messages);
    setSelectedAgents(memory.agents);
  };

  return (
    <div className="h-screen flex flex-col bg-background">
      {/* Theme Selector & API Settings & New Chat - Fixed Position */}
      <div className="fixed top-4 right-4 z-[100] flex items-center gap-2">
        <Link
          href="/nodes"
          className="flex items-center gap-2 px-3 py-2 rounded-lg bg-card border border-border hover:bg-muted transition-colors"
          title="Switch to Node Workflow Editor"
        >
          <LayoutGrid className="h-4 w-4 text-primary" />
          <span className="text-sm font-medium hidden md:inline">Node Workflow Editor</span>
        </Link>
        <button
          onClick={handleNewChat}
          className="p-2 rounded-lg bg-card border border-border hover:bg-muted transition-colors"
          title="Nuevo Chat"
        >
          <Plus className="h-4 w-4 text-primary" />
        </button>
        <button
          onClick={() => setShowApiSettings(true)}
          className="p-2 rounded-lg bg-card border border-border hover:bg-muted transition-colors"
          title="Configurar APIs"
        >
          <Settings className="h-4 w-4 text-primary" />
        </button>
        <LanguageSelector />
        <ThemeSelector />
      </div>

      {/* API Settings Modal */}
      <ApiSettings
        isOpen={showApiSettings}
        onClose={() => setShowApiSettings(false)}
        onProvidersChange={handleProvidersChange}
      />

      <Header
        model={model}
        onModelChange={setModel}
        isConnected={isConnected}
        availableModels={availableModels}
      />

      <div className="flex-1 flex overflow-hidden">
        <Sidebar
          agents={AGENTS_DATA}
          selectedAgents={selectedAgents}
          onAgentToggle={handleAgentToggle}
          onSelectAll={handleSelectAll}
          onClearAll={handleClearAll}
          availableModels={availableModels}
          agentModels={agentModels}
          onAgentModelChange={handleAgentModelChange}
          agentInstructions={agentInstructions}
          onAgentInstructionsChange={handleAgentInstructionsChange}
          onShowAgentDetails={handleShowAgentDetails}
        />

        <main className="flex-1 p-4 overflow-hidden flex flex-col gap-4">
          {/* Live Reasoning Display */}
          {isProcessing && (
            <LiveReasoning 
              agents={selectedAgents} 
              isProcessing={isProcessing} 
            />
          )}
          
          <div className="flex-1 overflow-hidden">
            <ChatInterface
              selectedAgents={selectedAgents}
              onSendMessage={handleSendMessage}
              messages={messages}
              isProcessing={isProcessing}
              currentAgentProgress={currentAgentProgress}
              totalAgents={AGENTS_DATA.length}
            />
          </div>
        </main>

        {/* Memory Panel - Right Side */}
        <MemoryPanel
          messages={messages}
          currentAgents={selectedAgents}
          onSaveMemory={() => {}}
          onLoadMemory={handleLoadMemory}
        />
      </div>

      {activeAgentDetail && activeAgentMeta && (
        <AgentDetailPanel
          agentName={activeAgentDetail}
          role={activeAgentMeta.role}
          level={activeAgentMeta.level}
          selectedModel={agentModels[activeAgentDetail]}
          availableModels={availableModels}
          instructions={agentInstructions[activeAgentDetail]}
          onModelChange={handleAgentModelChange}
          onInstructionsChange={handleAgentInstructionsChange}
          onClose={() => setActiveAgentDetail(null)}
        />
      )}
    </div>
  );
}
