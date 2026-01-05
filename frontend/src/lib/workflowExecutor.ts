import { Node, Edge } from 'reactflow';

export interface WorkflowExecutionResult {
  success: boolean;
  outputs: Record<string, any>;
  errors: string[];
}

export class WorkflowExecutor {
  private nodes: Node[];
  private edges: Edge[];

  constructor(nodes: Node[], edges: Edge[]) {
    this.nodes = nodes;
    this.edges = edges;
  }

  /**
   * Ejecuta el workflow completo siguiendo el grafo de nodos
   */
  async execute(): Promise<WorkflowExecutionResult> {
    const outputs: Record<string, any> = {};
    const errors: string[] = [];

    try {
      // 1. Encontrar nodos de inicio (Prompt)
      const startNodes = this.nodes.filter(n => n.type === 'prompt');
      if (startNodes.length === 0) {
        errors.push('No prompt nodes found in workflow. Add a Prompt node to start.');
        return { success: false, outputs, errors };
      }

      // 2. Construir el orden de ejecución (topological sort)
      const executionOrder = this.getExecutionOrder();
      if (!executionOrder) {
        errors.push('Workflow contains cycles or is invalid');
        return { success: false, outputs, errors };
      }

      // 3. Ejecutar nodos en orden
      for (const nodeId of executionOrder) {
        const node = this.nodes.find(n => n.id === nodeId);
        if (!node) continue;

        try {
          const result = await this.executeNode(node, outputs);
          outputs[nodeId] = result;
        } catch (error) {
          errors.push(`Error executing node ${nodeId}: ${error}`);
        }
      }

      return { success: errors.length === 0, outputs, errors };
    } catch (error) {
      errors.push(`Workflow execution failed: ${error}`);
      return { success: false, outputs, errors };
    }
  }

  /**
   * Ejecuta un nodo individual
   */
  private async executeNode(node: Node, previousOutputs: Record<string, any>): Promise<any> {
    const { type, data } = node;

    // Obtener inputs de nodos conectados
    const inputs = this.getNodeInputs(node.id, previousOutputs);

    switch (type) {
      case 'prompt':
        return this.executePromptNode(data, inputs);

      case 'agent_l1':
      case 'agent_l2':
      case 'agent_l3':
      case 'agent_l4':
      case 'agent_l5':
        return await this.executeAgentNode(data, inputs, node.id);

      case 'ai_provider':
        return data; // Provider config se pasa a otros nodos

      case 'output_base':
        return inputs[0] || 'No input received';

      case 'output_final':
        return inputs[0] || 'No final input received';

      default:
        return null;
    }
  }

  /**
   * Ejecuta un nodo de prompt (combina prompts positivos y negativos)
   */
  private executePromptNode(data: any, inputs: any[]): string {
    const basePrompt = inputs[0] || '';
    const positivePrompt = data.positivePrompt || '';
    const negativePrompt = data.negativePrompt || '';

    let finalPrompt = basePrompt;
    
    if (positivePrompt) {
      finalPrompt += `\n\nPOSITIVE INSTRUCTIONS:\n${positivePrompt}`;
    }
    
    if (negativePrompt) {
      finalPrompt += `\n\nNEGATIVE INSTRUCTIONS (avoid these):\n${negativePrompt}`;
    }

    return finalPrompt;
  }

  /**
   * Ejecuta un nodo de agente (llama al backend)
   */
  private async executeAgentNode(data: any, inputs: any[], nodeId: string): Promise<string> {
    const message = inputs[0] || '';
    const agentName = data.agentName || 'reasoning_agent';
    const additionalInstructions = data.additionalInstructions || '';

    // Buscar configuración de AI provider conectado
    const providerConfig = this.findConnectedProvider(nodeId);

    // Combinar mensaje con instrucciones adicionales
    let finalMessage = message;
    if (additionalInstructions) {
      finalMessage += `\n\nAdditional Instructions: ${additionalInstructions}`;
    }

    try {
      const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: finalMessage,
          agents: [agentName],
          provider: providerConfig?.provider || 'openai',
          model: providerConfig?.model || 'gpt-4',
          temperature: providerConfig?.temperature || 0.7,
          max_tokens: providerConfig?.maxTokens || 4096,
        }),
      });

      if (!response.ok) {
        throw new Error('API request failed');
      }

      const result = await response.json();
      return result.result || result.message || 'No response';
    } catch (error) {
      throw new Error(`Agent execution failed: ${error}`);
    }
  }

  /**
   * Encuentra el proveedor de IA conectado a un nodo
   */
  private findConnectedProvider(nodeId: string): any {
    // Buscar edges que conectan un ai_provider a este nodo
    const providerEdge = this.edges.find(e => {
      const sourceNode = this.nodes.find(n => n.id === e.source);
      return e.target === nodeId && sourceNode?.type === 'ai_provider';
    });

    if (providerEdge) {
      const providerNode = this.nodes.find(n => n.id === providerEdge.source);
      return providerNode?.data;
    }

    return null;
  }

  /**
   * Obtiene los inputs de un nodo desde nodos conectados
   */
  private getNodeInputs(nodeId: string, outputs: Record<string, any>): any[] {
    const inputs: any[] = [];
    
    // Encontrar edges que apuntan a este nodo
    const incomingEdges = this.edges.filter(e => e.target === nodeId);
    
    for (const edge of incomingEdges) {
      const sourceOutput = outputs[edge.source];
      if (sourceOutput !== undefined) {
        inputs.push(sourceOutput);
      }
    }

    return inputs;
  }

  /**
   * Obtiene el orden de ejecución usando topological sort
   */
  private getExecutionOrder(): string[] | null {
    const visited = new Set<string>();
    const temp = new Set<string>();
    const order: string[] = [];

    const visit = (nodeId: string): boolean => {
      if (temp.has(nodeId)) return false; // Ciclo detectado
      if (visited.has(nodeId)) return true;

      temp.add(nodeId);

      // Visitar dependencias (nodos de entrada)
      const incomingEdges = this.edges.filter(e => e.target === nodeId);
      for (const edge of incomingEdges) {
        if (!visit(edge.source)) return false;
      }

      temp.delete(nodeId);
      visited.add(nodeId);
      order.push(nodeId);
      return true;
    };

    // Visitar todos los nodos
    for (const node of this.nodes) {
      if (!visited.has(node.id)) {
        if (!visit(node.id)) return null;
      }
    }

    return order;
  }
}
