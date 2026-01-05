"use client";

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { cn } from "@/lib/utils";
import {
  Terminal,
  Settings,
  Cpu,
  Activity,
  Wifi,
} from "lucide-react";

interface AvailableModel {
  id: string;
  name: string;
  provider: string;
}

interface HeaderProps {
  model: string;
  onModelChange: (model: string) => void;
  isConnected: boolean;
  availableModels?: AvailableModel[];
}

export function Header({ model, onModelChange, isConnected, availableModels = [] }: HeaderProps) {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  return (
    <header className="min-h-16 border-b border-primary/20 bg-card/50 backdrop-blur-sm px-4 py-2 flex flex-wrap items-center justify-between gap-4">
      {/* Logo */}
      <div className="flex items-center gap-3">
        <div className="relative">
          <div className="h-10 w-10 rounded-xl bg-gradient-to-br from-primary/30 to-cyber-blue/30 border border-primary/50 flex items-center justify-center">
            <Terminal className="h-5 w-5 text-primary" />
          </div>
          <div className="absolute -bottom-1 -right-1 h-3 w-3 rounded-full bg-green-500 border-2 border-background animate-pulse" />
        </div>
        <div>
          <h1 className="text-lg md:text-xl font-bold tracking-tight">
            <span className="text-primary glow-text-subtle">Agentic Task Platform</span>
          </h1>
          <div className="flex items-center gap-2 mt-0.5">
            <Badge variant="outline" className="text-xs font-mono">
              v2.0.0
            </Badge>
            <div className="flex items-center gap-1">
              <Wifi
                className={cn(
                  "h-3 w-3",
                  isConnected ? "text-green-500" : "text-red-500"
                )}
              />
              <span className="text-xs text-muted-foreground">
                {isConnected ? "Conectado" : "Desconectado"}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Center - Model Selector */}
      <div className="flex flex-wrap items-center gap-2 md:gap-4">
        <div className="flex items-center gap-2">
          <Cpu className="h-4 w-4 text-muted-foreground" />
          <span className="text-xs text-muted-foreground hidden md:inline">Orquestador:</span>
          <Select value={model} onValueChange={onModelChange}>
            <SelectTrigger className="w-[180px] md:w-[280px] bg-background/50 border-primary/30">
              <SelectValue placeholder="Seleccionar modelo orquestador" />
            </SelectTrigger>
            <SelectContent>
              {availableModels.length > 0 ? (
                availableModels.map((m) => (
                  <SelectItem key={m.id} value={m.id}>
                    <div className="flex items-center gap-2">
                      <span className="truncate">{m.name.split("/").pop()}</span>
                      {m.provider && (
                        <Badge variant="outline" className="text-xs">
                          {m.provider}
                        </Badge>
                      )}
                    </div>
                  </SelectItem>
                ))
              ) : (
                <SelectItem value="none" disabled>
                  ⚠️ Configura una API primero
                </SelectItem>
              )}
            </SelectContent>
          </Select>
        </div>

        <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-muted/50 border border-primary/20">
          <Activity className={cn("h-4 w-4", availableModels.length > 0 ? "text-green-500" : "text-yellow-500")} />
          <span className="text-xs text-muted-foreground font-mono">
            {availableModels.length > 0 ? `${availableModels.length} modelos` : "Sin API"}
          </span>
        </div>
      </div>

      {/* Right - Actions */}
      <div className="flex items-center gap-2">
      </div>
    </header>
  );
}
