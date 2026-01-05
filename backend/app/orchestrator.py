"""
Agent Orchestrator - ATP v0.6.8
Orquestador Central usando LangGraph directamente con A2A Protocol

Usa LangGraph como motor de orquestación y A2A Protocol como capa aislada
de comunicación entre agentes. Esto evita enredos y mantiene la integridad
del sistema mediante mensajes estructurados.

Arquitectura:
- LangGraph: Gestión de flujo y estado (StateGraph)
- A2A Protocol: Comunicación aislada entre agentes (capa de mensajería)
- Groq: Proveedor LLM obligatorio
- Sin comunicación directa entre agentes

Diseñado para escalabilidad y mantenibilidad.
"""
from typing import Dict, Any, List, Optional, TypedDict
from langgraph.graph import StateGraph, END
from datetime import datetime
import uuid

from app.a2a_protocol import (
    A2AMessage, A2AResponse, AgentCapability, MessageType,
    Priority, a2a_protocol, AgentStatus
)


class AgentState(TypedDict):
    """
    Estado compartido en el grafo de LangGraph
    
    Todos los agentes se comunican SOLO a través de A2A Protocol.
    El estado mantiene el historial de mensajes A2A y coordina el flujo.
    """
    # Input original del usuario
    user_query: str
    context: Dict[str, Any]
    
    # Comunicación A2A (capa aislada)
    a2a_messages: List[A2AMessage]
    a2a_responses: List[A2AResponse]
    
    # Control de flujo LangGraph
    current_step: str
    next_agent: Optional[str]
    agents_to_execute: List[str]
    agents_completed: List[str]
    
    # Resultados
    intermediate_results: Dict[str, Any]
    final_result: Optional[str]
    
    # Metadata
    conversation_id: str
    start_time: datetime
    is_complete: bool
    error: Optional[str]


class AgentOrchestrator:
    """
    Orquestador Central usando LangGraph + A2A Protocol
    
    ARQUITECTURA:
    1. LangGraph gestiona el flujo de ejecución (StateGraph)
    2. A2A Protocol maneja TODA la comunicación entre agentes (capa aislada)
    3. Los agentes NUNCA se comunican directamente entre sí
    4. Todos los mensajes pasan por el protocolo A2A
    
    BENEFICIOS:
    - Sin enredos: comunicación estructurada y validada
    - Trazabilidad: todos los mensajes son rastreables
    - Escalabilidad: fácil agregar nuevos agentes
    - Mantenibilidad: capa de comunicación aislada
    
    FLUJO:
    User Query -> LangGraph -> A2A Messages -> Agents -> A2A Responses -> LangGraph -> Final Result
    """
    
    def __init__(self):
        # Registro de agentes disponibles (se llenarán dinámicamente)
        self.agents: Dict[str, Any] = {}
        
        # Instancia del protocolo A2A (capa de comunicación aislada)
        self.protocol = a2a_protocol
        
        # Grafo de LangGraph (se construye dinámicamente)
        self.graph = None
        
        # Estadísticas
        self.stats = {
            "total_queries": 0,
            "successful_queries": 0,
            "failed_queries": 0,
            "total_a2a_messages": 0,
            "average_response_time_ms": 0.0
        }
    
    def register_agents(self, agents: List[Any]) -> None:
        """
        Registra agentes en el orchestrator y en el protocolo A2A
        
        Args:
            agents: Lista de instancias de agentes
        """
        self.agents = {}
        
        for agent in agents:
            agent_id = agent.profile.agent_id
            self.agents[agent_id] = agent
            
            # Registrar en el protocolo A2A
            self.protocol.register_agent(agent.profile)
        
        # Construir grafo con los agentes registrados
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """
        Construye el grafo de LangGraph con los agentes registrados
        
        El grafo define:
        1. analyze_query: Analiza la consulta y determina agentes necesarios
        2. execute_agents: Ejecuta agentes usando A2A Protocol
        3. synthesize: Combina resultados de todos los agentes
        4. finalize: Prepara respuesta final
        """
        workflow = StateGraph(AgentState)
        
        # Nodos del grafo
        workflow.add_node("analyze_query", self._analyze_query)
        workflow.add_node("execute_agents", self._execute_agents)
        workflow.add_node("synthesize", self._synthesize_results)
        workflow.add_node("finalize", self._finalize_result)
        
        # Punto de entrada
        workflow.set_entry_point("analyze_query")
        
        # Flujo lineal con decisión condicional
        workflow.add_edge("analyze_query", "execute_agents")
        workflow.add_conditional_edges(
            "execute_agents",
            self._should_continue,
            {
                "continue": "execute_agents",  # Ejecutar más agentes
                "synthesize": "synthesize"      # Todos completados
            }
        )
        workflow.add_edge("synthesize", "finalize")
        workflow.add_edge("finalize", END)
        
        return workflow.compile()
    
    async def execute(
        self,
        task: str,
        agents: List[Any],
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Ejecuta una tarea con los agentes seleccionados
        
        Args:
            task: Tarea a ejecutar
            agents: Lista de agentes a usar
            context: Contexto adicional
            
        Returns:
            Resultado de la ejecución con metadata
        """
        try:
            # Registrar agentes
            self.register_agents(agents)
            
            # Preparar estado inicial
            conversation_id = str(uuid.uuid4())
            start_time = datetime.utcnow()
            
            initial_state: AgentState = {
                "user_query": task,
                "context": context or {},
                "a2a_messages": [],
                "a2a_responses": [],
                "current_step": "init",
                "next_agent": None,
                "agents_to_execute": [agent.profile.agent_id for agent in agents],
                "agents_completed": [],
                "intermediate_results": {},
                "final_result": None,
                "conversation_id": conversation_id,
                "start_time": start_time,
                "is_complete": False,
                "error": None
            }
            
            # Ejecutar grafo de LangGraph
            final_state = await self.graph.ainvoke(initial_state)
            
            # Calcular tiempo de procesamiento
            processing_time = (datetime.utcnow() - start_time).total_seconds() * 1000
            
            # Actualizar estadísticas
            self.stats["total_queries"] += 1
            self.stats["successful_queries"] += 1
            self.stats["total_a2a_messages"] += len(final_state["a2a_messages"])
            
            return {
                "success": True,
                "final_result": final_state["final_result"],
                "conversation_id": conversation_id,
                "agents_used": final_state["agents_completed"],
                "processing_time_ms": processing_time,
                "a2a_messages_count": len(final_state["a2a_messages"]),
                "a2a_responses_count": len(final_state["a2a_responses"]),
                "intermediate_results": final_state["intermediate_results"]
            }
            
        except Exception as e:
            self.stats["total_queries"] += 1
            self.stats["failed_queries"] += 1
            
            return {
                "success": False,
                "error": str(e),
                "final_result": None
            }
    
    async def _analyze_query(self, state: AgentState) -> AgentState:
        """
        Analiza la consulta del usuario y prepara el contexto
        
        Crea el mensaje A2A inicial que se enviará a los agentes.
        """
        # Crear mensaje A2A inicial para broadcast a todos los agentes
        initial_message = self.protocol.create_message(
            sender_id="orchestrator",
            sender_capability=AgentCapability.REASONING,
            subject="User Query Processing",
            payload={
                "query": state["user_query"],
                "context": state["context"],
                "task_type": "analysis"
            },
            message_type=MessageType.BROADCAST,
            priority=Priority.NORMAL,
            conversation_id=state["conversation_id"]
        )
        
        state.setdefault("a2a_messages", []).append(initial_message)
        state["current_step"] = "analyzed"
        
        return state
    
    async def _execute_agents(self, state: AgentState) -> AgentState:
        """
        Ejecuta agentes usando A2A Protocol como capa de comunicación
        
        Cada agente recibe un mensaje A2A y responde con A2AResponse.
        """
        # Obtener agentes pendientes
        pending_agents = [
            agent_id for agent_id in state["agents_to_execute"]
            if agent_id not in state["agents_completed"]
        ]
        
        if not pending_agents:
            state["current_step"] = "all_agents_completed"
            return state
        
        # Ejecutar el siguiente agente
        agent_id = pending_agents[0]
        agent = self.agents.get(agent_id)
        
        if not agent:
            state["error"] = f"Agent {agent_id} not found"
            return state
        
        try:
            # Crear mensaje A2A para este agente específico
            agent_message = self.protocol.create_message(
                sender_id="orchestrator",
                sender_capability=AgentCapability.REASONING,
                subject=f"Task Execution Request for {agent_id}",
                payload={
                    "query": state["user_query"],
                    "context": state["context"],
                    "previous_results": state["intermediate_results"]
                },
                message_type=MessageType.REQUEST,
                recipient_id=agent_id,
                priority=Priority.NORMAL,
                conversation_id=state["conversation_id"]
            )
            
            # Ejecutar agente (el agente procesa el mensaje A2A)
            result = await agent.execute(state["user_query"])
            
            # Crear respuesta A2A
            agent_response = self.protocol.create_response(
                original_message=agent_message,
                responder_id=agent_id,
                responder_capability=agent.profile.primary_capability,
                result=result,
                success=True,
                reasoning=f"Processed by {agent.profile.name}"
            )
            
            # Almacenar resultados
            state.setdefault("a2a_messages", []).append(agent_message)
            state.setdefault("a2a_responses", []).append(agent_response)
            state["intermediate_results"][agent_id] = result
            state["agents_completed"].append(agent_id)
            state["current_step"] = f"executed_{agent_id}"
            
        except Exception as e:
            # Crear respuesta de error
            error_response = A2AResponse(
                original_message_id=agent_message.message_id if 'agent_message' in locals() else "error",
                conversation_id=state["conversation_id"],
                responder_id=agent_id,
                responder_capability=AgentCapability.REASONING,
                success=False,
                result=None,
                error_message=str(e)
            )
            
            state.setdefault("a2a_responses", []).append(error_response)
            state["error"] = f"Error executing {agent_id}: {str(e)}"
        
        return state
    
    def _should_continue(self, state: AgentState) -> str:
        """
        Decide si continuar ejecutando agentes o pasar a síntesis
        """
        pending = [
            agent_id for agent_id in state["agents_to_execute"]
            if agent_id not in state["agents_completed"]
        ]
        
        if pending and not state.get("error"):
            return "continue"
        return "synthesize"
    
    async def _synthesize_results(self, state: AgentState) -> AgentState:
        """
        Sintetiza los resultados de todos los agentes
        
        Combina las respuestas A2A de todos los agentes en un resultado coherente.
        """
        results = []
        
        for agent_id, result in state["intermediate_results"].items():
            agent = self.agents.get(agent_id)
            if agent:
                results.append(f"**{agent.profile.name}:**\n{result}\n")
        
        # Combinar resultados
        if results:
            state["final_result"] = "\n".join(results)
        else:
            state["final_result"] = "No se pudieron obtener resultados de los agentes."
        
        state["current_step"] = "synthesized"
        
        return state
    
    async def _finalize_result(self, state: AgentState) -> AgentState:
        """
        Finaliza el procesamiento y marca como completo
        """
        state["is_complete"] = True
        state["current_step"] = "finalized"
        
        return state
    
    def get_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas del orchestrator"""
        return self.stats.copy()
    
    def get_agent_status(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Obtiene el estado de un agente específico"""
        agent = self.agents.get(agent_id)
        if not agent:
            return None
        
        status = getattr(agent.profile, "status", AgentStatus.IDLE)
        current_load = getattr(agent.profile, "current_load", 0)
        max_tasks = getattr(agent.profile, "max_concurrent_tasks", 1)
        
        return {
            "agent_id": agent.profile.agent_id,
            "name": agent.profile.name,
            "status": status.value if isinstance(status, AgentStatus) else status,
            "current_load": current_load,
            "max_concurrent_tasks": max_tasks
        }


# Instancia global del orchestrator
orchestrator = AgentOrchestrator()
