"use client";

import { useState } from "react";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { AgentCard } from "@/components/AgentCard";
import { cn } from "@/lib/utils";
import {
  ChevronLeft,
  ChevronRight,
  Cpu,
  Layers,
  Settings,
  Zap,
} from "lucide-react";

interface Agent {
  name: string;
  role: string;
  level: number;
}

interface AvailableModel {
  id: string;
  name: string;
  provider: string;
}

interface SidebarProps {
  agents: Agent[];
  selectedAgents: string[];
  onAgentToggle: (agentName: string) => void;
  onSelectAll: (level?: number) => void;
  onClearAll: () => void;
  availableModels?: AvailableModel[];
  agentModels?: Record<string, string>;
  onAgentModelChange?: (agentName: string, modelId: string) => void;
  agentInstructions?: Record<string, string>;
  onAgentInstructionsChange?: (agentName: string, instructions: string) => void;
  onShowAgentDetails?: (agentName: string) => void;
}

const levelNames: Record<number, string> = {
  1: "Críticos",
  2: "Esenciales",
  3: "Especializados",
  4: "Soporte",
  5: "Auxiliares",
};

const levelDescriptions: Record<number, string> = {
  1: "Núcleo de razonamiento",
  2: "Capacidades fundamentales",
  3: "Dominios específicos",
  4: "Calidad y mantenimiento",
  5: "Funciones complementarias",
};

export function Sidebar({
  agents,
  selectedAgents,
  onAgentToggle,
  onSelectAll,
  onClearAll,
  availableModels = [],
  agentModels = {},
  onAgentModelChange,
  agentInstructions = {},
  onAgentInstructionsChange,
  onShowAgentDetails,
}: SidebarProps) {
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [activeLevel, setActiveLevel] = useState("all");

  const filteredAgents =
    activeLevel === "all"
      ? agents
      : agents.filter((a) => a.level === parseInt(activeLevel));

  const agentsByLevel = agents.reduce((acc, agent) => {
    if (!acc[agent.level]) acc[agent.level] = [];
    acc[agent.level].push(agent);
    return acc;
  }, {} as Record<number, Agent[]>);

  if (isCollapsed) {
    return (
      <div className="w-16 h-full bg-card/50 backdrop-blur-sm border-r border-primary/20 flex flex-col items-center py-4 gap-4">
        <Button
          variant="ghost"
          size="icon"
          onClick={() => setIsCollapsed(false)}
          className="text-primary"
        >
          <ChevronRight className="h-5 w-5" />
        </Button>
        <div className="flex flex-col gap-2">
          <div className="h-8 w-8 rounded-lg bg-primary/20 flex items-center justify-center">
            <Cpu className="h-4 w-4 text-primary" />
          </div>
          <Badge variant="outline" className="text-xs">
            {selectedAgents.length}
          </Badge>
        </div>
      </div>
    );
  }

  return (
    <div className="w-[340px] h-full bg-gradient-to-b from-card/80 to-card/50 backdrop-blur-md border-r-2 border-primary/30 flex flex-col shadow-2xl overflow-hidden">
      {/* Header - Mejorado */}
      <div className="p-4 border-b-2 border-primary/30 bg-gradient-to-r from-primary/10 to-transparent">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-xl bg-primary/20 border border-primary/40 shadow-lg">
              <Layers className="h-6 w-6 text-primary animate-pulse" />
            </div>
            <div>
              <span className="font-bold text-lg text-primary block leading-none">
                Agentes
              </span>
            </div>
          </div>
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setIsCollapsed(true)}
            className="text-muted-foreground hover:text-primary hover:bg-primary/10 transition-all"
          >
            <ChevronLeft className="h-5 w-5" />
          </Button>
        </div>

        <div className="flex items-center justify-between gap-2">
          <Badge variant="success" className="font-mono text-sm px-3 py-1.5 shadow-md">
            ✓ {selectedAgents.length} / {agents.length} activos
          </Badge>
          <div className="flex gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={() => onSelectAll()}
              className="text-xs font-semibold border-primary/40 hover:bg-primary/20 hover:border-primary transition-all"
            >
              <Zap className="h-3 w-3 mr-1" />
              Todos
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={onClearAll}
              className="text-xs font-semibold border-destructive/40 hover:bg-destructive/20 hover:border-destructive transition-all"
            >
              Limpiar
            </Button>
          </div>
        </div>
      </div>

      {/* Level Tabs - Mejorado */}
      <Tabs value={activeLevel} onValueChange={setActiveLevel} className="flex-1 flex flex-col overflow-hidden min-h-0">
        <TabsList className="mx-4 mt-4 grid grid-cols-6 bg-muted/40 p-1 rounded-xl border border-primary/20">
          <TabsTrigger value="all" className="text-xs font-bold data-[state=active]:bg-primary data-[state=active]:text-primary-foreground data-[state=active]:shadow-lg transition-all">
            Todos
          </TabsTrigger>
          {[1, 2, 3, 4, 5].map((level) => (
            <TabsTrigger 
              key={level} 
              value={level.toString()} 
              className="text-xs font-bold data-[state=active]:bg-primary data-[state=active]:text-primary-foreground data-[state=active]:shadow-lg transition-all"
            >
              L{level}
            </TabsTrigger>
          ))}
        </TabsList>

        <TabsContent value={activeLevel} className="flex-1 mt-0 overflow-hidden min-h-0">
          <div className="flex-1 h-full min-h-0 px-3 py-4">
            <ScrollArea className="h-full w-full flex-1 min-h-0 pr-1">
            {activeLevel === "all" ? (
              <div className="space-y-6">
                {Object.entries(agentsByLevel).map(([level, levelAgents]) => (
                  <div key={level}>
                    <div className="flex items-center justify-between mb-3 p-2 rounded-lg bg-gradient-to-r from-primary/10 to-transparent border-l-4 border-primary">
                      <div>
                        <h3 className="text-sm font-bold text-primary flex items-center gap-2">
                          <span className="inline-block w-2 h-2 rounded-full bg-primary animate-pulse"></span>
                          Nivel {level} - {levelNames[parseInt(level)]}
                        </h3>
                        <p className="text-xs text-muted-foreground mt-0.5">
                          {levelDescriptions[parseInt(level)]}
                        </p>
                      </div>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => onSelectAll(parseInt(level))}
                        className="text-xs h-7 font-semibold border-primary/40 hover:bg-primary/20 hover:border-primary transition-all"
                      >
                        <Zap className="h-3 w-3 mr-1" />
                        Todos
                      </Button>
                    </div>
                    <div className="flex flex-col gap-3">
                      {levelAgents.map((agent) => (
                        <AgentCard
                          key={agent.name}
                          name={agent.name}
                          role={agent.role}
                          level={agent.level}
                          isSelected={selectedAgents.includes(agent.name)}
                          onClick={() => onAgentToggle(agent.name)}
                          availableModels={availableModels}
                          selectedModel={agentModels[agent.name]}
                          onModelChange={onAgentModelChange}
                          customInstructions={agentInstructions[agent.name]}
                          onInstructionsChange={onAgentInstructionsChange}
                          onShowDetails={onShowAgentDetails}
                        />
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="flex flex-col gap-3">
                {filteredAgents.map((agent) => (
                  <AgentCard
                    key={agent.name}
                    name={agent.name}
                    role={agent.role}
                    level={agent.level}
                    isSelected={selectedAgents.includes(agent.name)}
                    onClick={() => onAgentToggle(agent.name)}
                    availableModels={availableModels}
                    selectedModel={agentModels[agent.name]}
                    onModelChange={onAgentModelChange}
                    customInstructions={agentInstructions[agent.name]}
                    onInstructionsChange={onAgentInstructionsChange}
                    onShowDetails={onShowAgentDetails}
                  />
                ))}
              </div>
            )}
            </ScrollArea>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}
