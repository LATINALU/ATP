export interface Agent {
  name: string;
  role: string;
  level: number;
}

export interface AgentDialogue {
  agentName: string;
  message: string;
  timestamp: Date;
}

export interface Message {
  id: string;
  role: "user" | "assistant" | "system";
  content: string;
  timestamp: Date;
  agents?: string[];
  status?: "pending" | "processing" | "completed" | "error";
  dialogues?: AgentDialogue[];
}
