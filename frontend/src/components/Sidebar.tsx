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
    <div className="w-80 h-full bg-card/50 backdrop-blur-sm border-r border-primary/20 flex flex-col">
      {/* Header */}
      <div className="p-4 border-b border-primary/20">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <Layers className="h-5 w-5 text-primary" />
            <span className="font-semibold text-primary glow-text-subtle">
              Agentes
            </span>
          </div>
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setIsCollapsed(true)}
            className="text-muted-foreground hover:text-primary"
          >
            <ChevronLeft className="h-5 w-5" />
          </Button>
        </div>

        <div className="flex items-center justify-between">
          <Badge variant="success" className="font-mono">
            {selectedAgents.length} / {agents.length} activos
          </Badge>
          <div className="flex gap-1">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => onSelectAll()}
              className="text-xs"
            >
              Todos
            </Button>
            <Button
              variant="ghost"
              size="sm"
              onClick={onClearAll}
              className="text-xs"
            >
              Limpiar
            </Button>
          </div>
        </div>
      </div>

      {/* Level Tabs */}
      <Tabs value={activeLevel} onValueChange={setActiveLevel} className="flex-1 flex flex-col">
        <TabsList className="mx-4 mt-4 grid grid-cols-6">
          <TabsTrigger value="all" className="text-xs">
            All
          </TabsTrigger>
          {[1, 2, 3, 4, 5].map((level) => (
            <TabsTrigger key={level} value={level.toString()} className="text-xs">
              L{level}
            </TabsTrigger>
          ))}
        </TabsList>

        <TabsContent value={activeLevel} className="flex-1 mt-0">
          <ScrollArea className="h-full px-4 py-4">
            {activeLevel === "all" ? (
              <div className="space-y-6">
                {Object.entries(agentsByLevel).map(([level, levelAgents]) => (
                  <div key={level}>
                    <div className="flex items-center justify-between mb-2">
                      <div>
                        <h3 className="text-sm font-semibold text-primary">
                          Nivel {level} - {levelNames[parseInt(level)]}
                        </h3>
                        <p className="text-xs text-muted-foreground">
                          {levelDescriptions[parseInt(level)]}
                        </p>
                      </div>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => onSelectAll(parseInt(level))}
                        className="text-xs h-6"
                      >
                        <Zap className="h-3 w-3 mr-1" />
                        Todos
                      </Button>
                    </div>
                    <div className="grid gap-2">
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
                        />
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="grid gap-2">
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
                  />
                ))}
              </div>
            )}
          </ScrollArea>
        </TabsContent>
      </Tabs>
    </div>
  );
}
