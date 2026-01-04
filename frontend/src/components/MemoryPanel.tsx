"use client";

import { useState, useEffect } from "react";
import { Brain, Trash2, Save, Search, Clock, MessageSquare, Users } from "lucide-react";
import { Message } from "@/types";

interface MemoryEntry {
  id: string;
  timestamp: Date;
  messages: Message[];
  agents: string[];
  summary: string;
  tags: string[];
}

interface MemoryPanelProps {
  messages: Message[];
  currentAgents: string[];
  onSaveMemory?: (entry: MemoryEntry) => void;
  onLoadMemory?: (entry: MemoryEntry) => void;
}

export function MemoryPanel({ messages, currentAgents, onSaveMemory, onLoadMemory }: MemoryPanelProps) {
  const [memories, setMemories] = useState<MemoryEntry[]>([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [isExpanded, setIsExpanded] = useState(false);
  const [summary, setSummary] = useState("");
  const [tags, setTags] = useState("");

  // Load memories from localStorage
  useEffect(() => {
    const saved = localStorage.getItem("atp-memories");
    if (saved) {
      try {
        const parsedMemories = JSON.parse(saved).map((m: any) => ({
          ...m,
          timestamp: new Date(m.timestamp)
        }));
        setMemories(parsedMemories);
      } catch (e) {
        console.error("Error loading memories:", e);
      }
    }
  }, []);

  // Save memories to localStorage
  useEffect(() => {
    if (memories.length > 0) {
      localStorage.setItem("atp-memories", JSON.stringify(memories));
    }
  }, [memories]);

  const handleSaveMemory = () => {
    if (messages.length === 0) return;

    const newMemory: MemoryEntry = {
      id: Date.now().toString(),
      timestamp: new Date(),
      messages: [...messages],
      agents: [...currentAgents],
      summary: summary || generateAutoSummary(),
      tags: tags ? tags.split(",").map(t => t.trim()).filter(t => t) : generateAutoTags()
    };

    const updatedMemories = [newMemory, ...memories];
    setMemories(updatedMemories);
    setSummary("");
    setTags("");
    
    if (onSaveMemory) {
      onSaveMemory(newMemory);
    }
  };

  const handleDeleteMemory = (id: string) => {
    setMemories(prev => prev.filter(m => m.id !== id));
  };

  const handleLoadMemory = (memory: MemoryEntry) => {
    if (onLoadMemory) {
      onLoadMemory(memory);
    }
  };

  const generateAutoSummary = (): string => {
    if (messages.length === 0) return "";
    const userMessage = messages.find(m => m.role === "user");
    return userMessage ? userMessage.content.substring(0, 100) + "..." : "Conversación sin título";
  };

  const generateAutoTags = (): string[] => {
    const tags = new Set<string>();
    currentAgents.forEach(agent => {
      tags.add(agent.replace("_agent", ""));
    });
    if (messages.some(m => m.content.toLowerCase().includes("codigo"))) tags.add("programación");
    if (messages.some(m => m.content.toLowerCase().includes("análisis"))) tags.add("análisis");
    if (messages.some(m => m.content.toLowerCase().includes("plan"))) tags.add("planificación");
    return Array.from(tags);
  };

  const filteredMemories = memories.filter(memory => 
    memory.summary.toLowerCase().includes(searchTerm.toLowerCase()) ||
    memory.tags.some(tag => tag.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  return (
    <div className={`bg-card border-l border-border transition-all duration-300 ${isExpanded ? "w-80" : "w-12"}`}>
      {/* Toggle Button */}
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full p-3 hover:bg-muted transition-colors border-b border-border"
        title="Panel de Memoria"
      >
        <Brain className={`h-5 w-5 text-primary transition-transform ${isExpanded ? "rotate-180" : ""}`} />
      </button>

      {isExpanded && (
        <div className="p-4 h-full overflow-y-auto">
          <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <Brain className="h-5 w-5" />
            Memoria Conversacional
          </h3>

          {/* Save Current Memory */}
          {messages.length > 0 && (
            <div className="mb-6 p-3 bg-muted rounded-lg">
              <h4 className="font-medium mb-2">Guardar Conversación Actual</h4>
              <input
                type="text"
                placeholder="Resumen (opcional)"
                value={summary}
                onChange={(e) => setSummary(e.target.value)}
                className="w-full p-2 mb-2 text-sm bg-background border border-border rounded"
              />
              <input
                type="text"
                placeholder="Tags (separados por comas)"
                value={tags}
                onChange={(e) => setTags(e.target.value)}
                className="w-full p-2 mb-2 text-sm bg-background border border-border rounded"
              />
              <button
                onClick={handleSaveMemory}
                className="w-full p-2 bg-primary text-primary-foreground rounded hover:bg-primary/90 transition-colors flex items-center justify-center gap-2"
              >
                <Save className="h-4 w-4" />
                Guardar Memoria
              </button>
            </div>
          )}

          {/* Search */}
          <div className="mb-4">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <input
                type="text"
                placeholder="Buscar memorias..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full p-2 pl-10 bg-background border border-border rounded"
              />
            </div>
          </div>

          {/* Memories List */}
          <div className="space-y-3">
            {filteredMemories.map((memory) => (
              <div key={memory.id} className="p-3 bg-muted rounded-lg hover:bg-muted/80 transition-colors">
                <div className="flex justify-between items-start mb-2">
                  <div className="flex-1">
                    <h5 className="font-medium text-sm truncate">{memory.summary}</h5>
                    <div className="flex items-center gap-2 text-xs text-muted-foreground mt-1">
                      <Clock className="h-3 w-3" />
                      {memory.timestamp.toLocaleDateString()}
                    </div>
                  </div>
                  <div className="flex gap-1">
                    <button
                      onClick={() => handleLoadMemory(memory)}
                      className="p-1 hover:bg-background rounded transition-colors"
                      title="Cargar memoria"
                    >
                      <MessageSquare className="h-3 w-3" />
                    </button>
                    <button
                      onClick={() => handleDeleteMemory(memory.id)}
                      className="p-1 hover:bg-background rounded transition-colors"
                      title="Eliminar memoria"
                    >
                      <Trash2 className="h-3 w-3" />
                    </button>
                  </div>
                </div>
                
                <div className="flex items-center gap-2 text-xs text-muted-foreground mb-2">
                  <Users className="h-3 w-3" />
                  {memory.agents.length} agentes
                </div>

                {memory.tags.length > 0 && (
                  <div className="flex flex-wrap gap-1">
                    {memory.tags.map((tag, index) => (
                      <span
                        key={index}
                        className="px-2 py-1 bg-primary/10 text-primary text-xs rounded-full"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>

          {filteredMemories.length === 0 && (
            <div className="text-center text-muted-foreground py-8">
              <Brain className="h-12 w-12 mx-auto mb-2 opacity-50" />
              <p className="text-sm">No hay memorias guardadas</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
