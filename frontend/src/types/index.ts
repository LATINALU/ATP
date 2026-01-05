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

export interface AgentProgress {
  agent_id: string;
  agent_name: string;
  status: "pending" | "processing" | "completed" | "error";
  progress?: number;
  current_step?: string;
  result?: string;
}

export interface Message {
  id: string;
  role: "user" | "assistant" | "system";
  content: string;
  timestamp: Date;
  agents?: string[];
  status?: "pending" | "processing" | "completed" | "error";
  dialogues?: AgentDialogue[];
  agentProgress?: AgentProgress[];
  a2a_messages_count?: number;
  a2a_responses_count?: number;
}
