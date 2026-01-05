import { Node, Edge } from "reactflow";

export interface WorkflowExecutionResult {
  success: boolean;
  outputs: Record<string, any>;
  errors: string[];
  rawResponse?: any;
}

interface PipelineNodes {
  userQuery: Node | undefined;
  langgraph: Node | undefined;
  a2aMessage: Node | undefined;
  agentsCluster: Node | undefined;
  a2aResponses: Node | undefined;
  synthesis: Node | undefined;
  finalResult: Node | undefined;
}

export class WorkflowExecutor {
  private nodes: Node[];
  private edges: Edge[];

  constructor(nodes: Node[], edges: Edge[]) {
    this.nodes = nodes;
    this.edges = edges;
  }

  async execute(): Promise<WorkflowExecutionResult> {
    const outputs: Record<string, any> = {};
    const errors: string[] = [];

    const pipeline = this.getPipelineNodes();
    const missingNodes = Object.entries(pipeline)
      .filter(([, node]) => !node)
      .map(([key]) => key);

    if (missingNodes.length > 0) {
      errors.push(
        `Faltan nodos requeridos: ${missingNodes
          .map((n) => n.replace(/([A-Z])/g, " $1"))
          .join(", ")}.`,
      );
      return { success: false, outputs, errors };
    }

    const userInput = String(pipeline.userQuery?.data?.userInput || "").trim();
    const selectedAgents = Array.isArray(pipeline.agentsCluster?.data?.selectedAgents)
      ? pipeline.agentsCluster?.data?.selectedAgents
      : [];
    const chosenModel =
      pipeline.langgraph?.data?.model?.trim() || "openai/gpt-oss-120b";

    if (!userInput) {
      errors.push("La consulta del usuario no puede estar vacía.");
    }

    if (!selectedAgents || selectedAgents.length === 0) {
      errors.push("Selecciona al menos un agente en el nodo Agents Cluster.");
    }

    if (errors.length > 0) {
      return { success: false, outputs, errors };
    }

    const contextPayload = {
      persona: pipeline.userQuery?.data?.persona,
      urgency: pipeline.userQuery?.data?.urgency,
      langgraph: {
        strategy: pipeline.langgraph?.data?.strategy,
        maxAgents: pipeline.langgraph?.data?.maxAgents,
        allowParallel: pipeline.langgraph?.data?.allowParallel,
        model: chosenModel,
      },
      a2aMessage: {
        channel: pipeline.a2aMessage?.data?.channel,
        priority: pipeline.a2aMessage?.data?.priority,
        messageType: pipeline.a2aMessage?.data?.messageType,
        subject: pipeline.a2aMessage?.data?.subject,
        encrypted: pipeline.a2aMessage?.data?.encrypted,
      },
      agentsCluster: {
        selectedAgents,
        maxParallel: pipeline.agentsCluster?.data?.maxParallel,
        cooldownMs: pipeline.agentsCluster?.data?.cooldownMs,
        loadBalancing: pipeline.agentsCluster?.data?.loadBalancing,
      },
      a2aResponsesCollector: {
        expectedAgents: pipeline.a2aResponses?.data?.expectedAgents,
        timeoutMs: pipeline.a2aResponses?.data?.timeoutMs,
        autoRetry: pipeline.a2aResponses?.data?.autoRetry,
      },
      synthesis: {
        strategy: pipeline.synthesis?.data?.strategy,
        tone: pipeline.synthesis?.data?.tone,
        maxSections: pipeline.synthesis?.data?.maxSections,
        includeTrace: pipeline.synthesis?.data?.includeTrace,
      },
      generatedAt: new Date().toISOString(),
    };

    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: userInput,
          agents: selectedAgents,
          model: chosenModel,
          context: contextPayload,
        }),
      });

      if (!response.ok) {
        errors.push("El backend devolvió un estado no exitoso.");
        return { success: false, outputs, errors };
      }

      const data = await response.json();

      if (!data.success) {
        errors.push(data.error || "El backend no pudo completar la ejecución.");
        return { success: false, outputs, errors, rawResponse: data };
      }

      const finalText =
        data.result ||
        data.final_result ||
        data.message ||
        "No se obtuvo resultado.";

      if (pipeline.synthesis) {
        outputs[pipeline.synthesis.id] = finalText;
      }

      if (pipeline.finalResult) {
        outputs[pipeline.finalResult.id] = finalText;
      }

      if (pipeline.a2aResponses) {
        outputs[pipeline.a2aResponses.id] = {
          agentsUsed: data.agents_used || [],
          modelUsed: data.model_used,
        };
      }

      return { success: true, outputs, errors, rawResponse: data };
    } catch (error) {
      errors.push(
        error instanceof Error
          ? `Error conectando con el backend: ${error.message}`
          : "Error desconocido ejecutando el workflow.",
      );
      return { success: false, outputs, errors };
    }
  }

  private getPipelineNodes(): PipelineNodes {
    const findNode = (type: string) => this.nodes.find((node) => node.type === type);

    return {
      userQuery: findNode("user_query"),
      langgraph: findNode("langgraph"),
      a2aMessage: findNode("a2a_message"),
      agentsCluster: findNode("agents_cluster"),
      a2aResponses: findNode("a2a_responses"),
      synthesis: findNode("synthesis"),
      finalResult: findNode("final_result"),
    };
  }
}
