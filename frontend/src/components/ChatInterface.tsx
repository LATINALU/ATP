"use client";

import { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import { Send, Bot, User, Loader2, Terminal, Sparkles, Paperclip, X, FileText, Image, File } from "lucide-react";
import ReactMarkdown from "react-markdown";

interface AttachedFile {
  name: string;
  type: string;
  size: number;
  content: string;
}

interface Message {
  id: string;
  role: "user" | "assistant" | "system";
  content: string;
  timestamp: Date;
  agents?: string[];
  status?: "pending" | "processing" | "completed" | "error";
}

interface ChatInterfaceProps {
  selectedAgents: string[];
  onSendMessage: (message: string) => Promise<void>;
  messages: Message[];
  isProcessing: boolean;
}

export function ChatInterface({
  selectedAgents,
  onSendMessage,
  messages,
  isProcessing,
}: ChatInterfaceProps) {
  const [input, setInput] = useState("");
  const [attachedFiles, setAttachedFiles] = useState<AttachedFile[]>([]);
  const scrollRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isProcessing) return;

    // Build message with attached files
    let message = input.trim();
    if (attachedFiles.length > 0) {
      const filesInfo = attachedFiles.map(f => 
        `\n\n--- Archivo adjunto: ${f.name} (${f.type}) ---\n${f.content}`
      ).join("\n");
      message += filesInfo;
    }

    setInput("");
    setAttachedFiles([]);
    await onSendMessage(message);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (!files) return;

    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      
      // Limit file size to 1MB
      if (file.size > 1024 * 1024) {
        alert(`El archivo ${file.name} es muy grande. Máximo 1MB.`);
        continue;
      }

      try {
        const content = await readFileContent(file);
        setAttachedFiles(prev => [...prev, {
          name: file.name,
          type: file.type || 'text/plain',
          size: file.size,
          content
        }]);
      } catch (err) {
        console.error('Error reading file:', err);
      }
    }

    // Reset input
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const readFileContent = (file: globalThis.File): Promise<string> => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      
      reader.onload = (e) => {
        const result = e.target?.result;
        if (typeof result === 'string') {
          resolve(result);
        } else {
          reject(new Error('Failed to read file'));
        }
      };
      
      reader.onerror = () => reject(reader.error);
      
      // Read as text for text files, base64 for others
      if (file.type.startsWith('text/') || 
          file.name.endsWith('.json') || 
          file.name.endsWith('.md') ||
          file.name.endsWith('.py') ||
          file.name.endsWith('.js') ||
          file.name.endsWith('.ts') ||
          file.name.endsWith('.tsx') ||
          file.name.endsWith('.css') ||
          file.name.endsWith('.html')) {
        reader.readAsText(file);
      } else {
        reader.readAsDataURL(file);
      }
    });
  };

  const removeFile = (index: number) => {
    setAttachedFiles(prev => prev.filter((_, i) => i !== index));
  };

  const getFileIcon = (type: string) => {
    if (type.startsWith('image/')) return Image;
    if (type.startsWith('text/') || type.includes('json')) return FileText;
    return File;
  };

  return (
    <div className="flex flex-col h-full bg-background/50 backdrop-blur-sm rounded-xl border border-primary/20 overflow-hidden">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-primary/20 bg-card/50">
        <div className="flex items-center gap-2">
          <Terminal className="h-5 w-5 text-primary" />
          <span className="font-mono text-sm text-primary glow-text-subtle">
            ATP_TERMINAL v1.0
          </span>
        </div>
        <div className="flex items-center gap-2">
          <div className="h-2 w-2 rounded-full bg-green-500 animate-pulse" />
          <span className="text-xs text-muted-foreground">
            {selectedAgents.length} agentes activos
          </span>
        </div>
      </div>

      {/* Messages */}
      <ScrollArea className="flex-1 p-4" ref={scrollRef}>
        <div className="space-y-4">
          {messages.length === 0 && (
            <div className="flex flex-col items-center justify-center h-64 text-center">
              <Sparkles className="h-12 w-12 text-primary/50 mb-4" />
              <h3 className="text-lg font-semibold text-primary glow-text-subtle">
                Sistema ATP Listo
              </h3>
              <p className="text-sm text-muted-foreground mt-2 max-w-md">
                Selecciona agentes y escribe tu tarea. Los agentes colaborarán
                para resolver cualquier problema con razonamiento profundo.
              </p>
            </div>
          )}

          {messages.map((message) => (
            <div
              key={message.id}
              className={cn(
                "flex gap-3 animate-in fade-in slide-in-from-bottom-2 duration-300",
                message.role === "user" ? "justify-end" : "justify-start"
              )}
            >
              {message.role !== "user" && (
                <div className="flex-shrink-0 h-8 w-8 rounded-lg bg-primary/20 border border-primary/30 flex items-center justify-center">
                  <Bot className="h-4 w-4 text-primary" />
                </div>
              )}

              <div
                className={cn(
                  "max-w-[80%] rounded-xl px-4 py-3",
                  message.role === "user"
                    ? "bg-primary/20 border border-primary/30 text-foreground"
                    : "bg-card border border-primary/20 text-foreground"
                )}
              >
                {message.agents && message.agents.length > 0 && (
                  <div className="flex flex-wrap gap-1 mb-2">
                    {message.agents.map((agent) => (
                      <Badge key={agent} variant="outline" className="text-xs">
                        {agent.replace(/_/g, " ")}
                      </Badge>
                    ))}
                  </div>
                )}

                <div className="prose prose-invert prose-sm max-w-none">
                  <ReactMarkdown>{message.content}</ReactMarkdown>
                </div>

                <div className="flex items-center justify-between mt-2 pt-2 border-t border-primary/10">
                  <span className="text-xs text-muted-foreground font-mono">
                    {message.timestamp.toLocaleTimeString()}
                  </span>
                  {message.status === "processing" && (
                    <div className="flex items-center gap-1">
                      <Loader2 className="h-3 w-3 animate-spin text-primary" />
                      <span className="text-xs text-primary">Procesando...</span>
                    </div>
                  )}
                </div>
              </div>

              {message.role === "user" && (
                <div className="flex-shrink-0 h-8 w-8 rounded-lg bg-secondary/20 border border-secondary/30 flex items-center justify-center">
                  <User className="h-4 w-4 text-secondary" />
                </div>
              )}
            </div>
          ))}

          {isProcessing && (
            <div className="flex gap-3 animate-in fade-in">
              <div className="flex-shrink-0 h-8 w-8 rounded-lg bg-primary/20 border border-primary/30 flex items-center justify-center">
                <Bot className="h-4 w-4 text-primary animate-pulse" />
              </div>
              <div className="bg-card border border-primary/20 rounded-xl px-4 py-3">
                <div className="flex items-center gap-2">
                  <div className="flex gap-1">
                    <div className="h-2 w-2 rounded-full bg-primary animate-bounce" />
                    <div className="h-2 w-2 rounded-full bg-primary animate-bounce delay-100" />
                    <div className="h-2 w-2 rounded-full bg-primary animate-bounce delay-200" />
                  </div>
                  <span className="text-sm text-muted-foreground">
                    Agentes procesando...
                  </span>
                </div>
              </div>
            </div>
          )}
        </div>
      </ScrollArea>

      {/* Input */}
      <form onSubmit={handleSubmit} className="p-4 border-t border-primary/20">
        {/* Attached Files Preview */}
        {attachedFiles.length > 0 && (
          <div className="flex flex-wrap gap-2 mb-3">
            {attachedFiles.map((file, index) => {
              const FileIcon = getFileIcon(file.type);
              return (
                <div
                  key={index}
                  className="flex items-center gap-2 px-3 py-1.5 bg-primary/10 border border-primary/30 rounded-lg text-xs"
                >
                  <FileIcon className="h-4 w-4 text-primary" />
                  <span className="text-foreground max-w-[150px] truncate">{file.name}</span>
                  <span className="text-muted-foreground">
                    ({(file.size / 1024).toFixed(1)}KB)
                  </span>
                  <button
                    type="button"
                    onClick={() => removeFile(index)}
                    className="p-0.5 hover:bg-destructive/20 rounded"
                  >
                    <X className="h-3 w-3 text-destructive" />
                  </button>
                </div>
              );
            })}
          </div>
        )}

        <div className="flex gap-2">
          {/* Hidden file input */}
          <input
            ref={fileInputRef}
            type="file"
            multiple
            onChange={handleFileSelect}
            className="hidden"
            accept=".txt,.md,.json,.py,.js,.ts,.tsx,.css,.html,.csv,.xml,.yaml,.yml,.log,.sql,.sh,.bat,.ps1,.env,.gitignore,.dockerfile,image/*"
          />
          
          {/* Attach button */}
          <Button
            type="button"
            variant="outline"
            size="icon"
            className="h-[60px] w-[50px] shrink-0"
            onClick={() => fileInputRef.current?.click()}
            disabled={isProcessing}
            title="Adjuntar archivo"
          >
            <Paperclip className="h-5 w-5" />
          </Button>

          <Textarea
            ref={textareaRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Escribe tu tarea en lenguaje natural..."
            className="min-h-[60px] max-h-[200px] resize-none font-mono text-sm"
            disabled={isProcessing}
          />
          <Button
            type="submit"
            size="icon"
            className="h-[60px] w-[60px]"
            disabled={!input.trim() || isProcessing}
          >
            {isProcessing ? (
              <Loader2 className="h-5 w-5 animate-spin" />
            ) : (
              <Send className="h-5 w-5" />
            )}
          </Button>
        </div>
        {/* Quick Instructions */}
        <div className="mt-3 flex flex-wrap gap-2">
          <span className="text-xs text-muted-foreground">Instrucciones rápidas:</span>
          {[
            { label: "📝 Analiza", prompt: "Analiza en detalle: " },
            { label: "💡 Explica", prompt: "Explica de forma simple: " },
            { label: "🔍 Investiga", prompt: "Investiga a fondo sobre: " },
            { label: "📋 Planifica", prompt: "Crea un plan detallado para: " },
            { label: "💻 Código", prompt: "Escribe código para: " },
            { label: "✍️ Redacta", prompt: "Redacta un texto profesional sobre: " },
            { label: "🧠 Razona", prompt: "Razona paso a paso: " },
            { label: "📊 Compara", prompt: "Compara y contrasta: " },
          ].map((item) => (
            <button
              key={item.label}
              type="button"
              onClick={() => setInput(item.prompt)}
              className="px-2 py-1 text-xs bg-primary/10 hover:bg-primary/20 border border-primary/30 rounded-md text-primary transition-colors"
              disabled={isProcessing}
            >
              {item.label}
            </button>
          ))}
        </div>
        
        <p className="text-xs text-muted-foreground mt-2 font-mono">
          Enter para enviar • Shift+Enter nueva línea • 📎 Adjuntar archivos
        </p>
      </form>
    </div>
  );
}
