"use client";

import { memo, useState, useEffect } from 'react';
import { Handle, Position, NodeProps, useReactFlow } from 'reactflow';
import { Cpu, Settings } from 'lucide-react';

export default memo(({ data, id }: NodeProps) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const [selectedProvider, setSelectedProvider] = useState(data.provider || 'openai');
  const [selectedModel, setSelectedModel] = useState(data.model || '');
  const [temperature, setTemperature] = useState(data.temperature || 0.7);
  const [maxTokens, setMaxTokens] = useState(data.maxTokens || 4096);
  const [availableModels, setAvailableModels] = useState<string[]>([]);
  const { setNodes } = useReactFlow();

  // Cargar modelos habilitados desde localStorage
  useEffect(() => {
    const savedProviders = localStorage.getItem('atp-api-providers');
    if (savedProviders) {
      try {
        const providers = JSON.parse(savedProviders);
        const activeProvider = providers.find((p: any) => p.type === selectedProvider && p.isActive);
        if (activeProvider && activeProvider.enabledModels) {
          setAvailableModels(activeProvider.enabledModels);
        } else if (activeProvider && activeProvider.models) {
          setAvailableModels(activeProvider.models);
        }
      } catch (e) {
        console.error('Error loading models:', e);
      }
    }
  }, [selectedProvider]);

  const updateNodeData = (updates: any) => {
    setNodes((nds) =>
      nds.map((node) => {
        if (node.id === id) {
          return {
            ...node,
            data: {
              ...node.data,
              ...updates,
            },
          };
        }
        return node;
      })
    );
  };

  const handleProviderChange = (provider: string) => {
    setSelectedProvider(provider);
    updateNodeData({ provider });
  };

  const handleModelChange = (model: string) => {
    setSelectedModel(model);
    updateNodeData({ model });
  };

  return (
    <div className="px-4 py-3 shadow-lg rounded-lg border-2 border-border bg-card min-w-[240px]">
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2">
          <Cpu className="h-5 w-5 text-primary" />
          <div className="font-bold text-sm">{data.label}</div>
        </div>
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="p-1 hover:bg-muted rounded"
        >
          <Settings className="h-4 w-4" />
        </button>
      </div>
      
      <div className="space-y-2">
        <div className="text-xs">
          <label className="text-muted-foreground">Provider</label>
          <select 
            value={selectedProvider}
            onChange={(e) => handleProviderChange(e.target.value)}
            className="w-full bg-background border border-border rounded p-1 mt-1"
          >
            <option value="openai">OpenAI</option>
            <option value="deepseek">DeepSeek</option>
            <option value="groq">Groq</option>
            <option value="anthropic">Anthropic</option>
            <option value="ollama">Ollama</option>
            <option value="together">Together AI</option>
            <option value="openrouter">OpenRouter</option>
          </select>
        </div>
        
        <div className="text-xs">
          <label className="text-muted-foreground">Model</label>
          {availableModels.length > 0 ? (
            <select
              value={selectedModel}
              onChange={(e) => handleModelChange(e.target.value)}
              className="w-full bg-background border border-border rounded p-1 mt-1"
            >
              <option value="">-- Select Model --</option>
              {availableModels.map((model) => (
                <option key={model} value={model}>
                  {model}
                </option>
              ))}
            </select>
          ) : (
            <input
              type="text"
              value={selectedModel}
              onChange={(e) => handleModelChange(e.target.value)}
              className="w-full bg-background border border-border rounded p-1 mt-1"
              placeholder="Enter model name"
            />
          )}
        </div>
        
        {isExpanded && (
          <>
            <div className="text-xs">
              <label className="text-muted-foreground">Temperature</label>
              <input
                type="number"
                min="0"
                max="2"
                step="0.1"
                value={temperature}
                onChange={(e) => {
                  setTemperature(parseFloat(e.target.value));
                  updateNodeData({ temperature: parseFloat(e.target.value) });
                }}
                className="w-full bg-background border border-border rounded p-1 mt-1"
              />
            </div>
            
            <div className="text-xs">
              <label className="text-muted-foreground">Max Tokens</label>
              <input
                type="number"
                value={maxTokens}
                onChange={(e) => {
                  setMaxTokens(parseInt(e.target.value));
                  updateNodeData({ maxTokens: parseInt(e.target.value) });
                }}
                className="w-full bg-background border border-border rounded p-1 mt-1"
              />
            </div>
          </>
        )}
      </div>
      
      {/* Handle: Solo 1 salida naranja */}
      <div className="flex justify-center items-center mt-3 pt-2 border-t border-border">
        <div className="flex items-center gap-2">
          <div className="text-[10px] text-orange-500 font-semibold">AI Output</div>
          <Handle
            type="source"
            position={Position.Bottom}
            id="output"
            className="!w-4 !h-4 !bg-orange-500 !relative !transform-none !border-2 !border-white"
            style={{ position: 'relative' }}
          />
        </div>
      </div>
    </div>
  );
});
