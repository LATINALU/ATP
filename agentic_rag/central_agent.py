"""
Agente Central para Agentic RAG
El "jefe de proyecto" que coordina todo el sistema:
- Recibe consultas del usuario
- Consulta memoria y planificación
- Delega tareas a sub-agentes
- Coordina con MCP Servers
- Sintetiza respuestas finales
"""

import asyncio
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
import json

from .memory import MemorySystem
from .planning import PlanningEngine, ExecutionPlan, PlanStatus, ActionType
from .mcp_servers import MCPServerManager, MCPResponse
from .sub_agents import SubAgentManager, AgentTask


@dataclass
class QueryResult:
    """Resultado de una consulta procesada"""
    query: str
    response: str
    plan_id: str
    agents_used: List[str]
    sources_consulted: List[str]
    reasoning_trace: List[str]
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            "query": self.query,
            "response": self.response,
            "plan_id": self.plan_id,
            "agents_used": self.agents_used,
            "sources_consulted": self.sources_consulted,
            "reasoning_trace": self.reasoning_trace,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata
        }


class CentralAgent:
    """
    Agente Central - Coordinador del Sistema Agentic RAG
    
    Flujo de trabajo:
    1. Recibe consulta del usuario
    2. Consulta memoria (corto y largo plazo)
    3. Crea plan de ejecución (ReACT + CoT)
    4. Delega tareas a sub-agentes
    5. Coordina con MCP Servers para datos externos
    6. Sintetiza respuesta final
    """
    
    def __init__(self, data_path: str = "./data"):
        # Componentes del sistema
        self.memory = MemorySystem(data_path)
        self.planning = PlanningEngine()
        self.mcp_servers = MCPServerManager(data_path)
        self.sub_agents = SubAgentManager()
        
        # Configuración
        self.api_callback: Optional[Callable] = None
        self.model_id: str = ""
        self.is_initialized = False
        
        # Historial
        self.query_history: List[QueryResult] = []
        
    async def initialize(self) -> bool:
        """Inicializar todos los componentes"""
        try:
            # Conectar servidores MCP
            await self.mcp_servers.connect_all()
            self.is_initialized = True
            return True
        except Exception as e:
            print(f"Error initializing Central Agent: {e}")
            return False
    
    def set_api_callback(self, callback: Callable):
        """
        Establecer callback para llamadas a API de LLM
        
        El callback debe tener la firma:
        async def callback(prompt: str, model_id: str = None, **kwargs) -> str
        """
        self.api_callback = callback
        self.sub_agents.set_api_callback(callback)
    
    def set_model(self, model_id: str):
        """Establecer modelo principal del orquestador"""
        self.model_id = model_id
    
    def configure_agent_model(self, agent_name: str, model_id: str):
        """Configurar modelo para un agente específico"""
        self.sub_agents.set_agent_model(agent_name, model_id)
    
    def configure_agent_instructions(self, agent_name: str, instructions: str):
        """Configurar instrucciones para un agente específico"""
        self.sub_agents.set_agent_instructions(agent_name, instructions)
    
    async def process_query(self, query: str, 
                           selected_agents: List[str] = None) -> QueryResult:
        """
        Procesar una consulta del usuario
        
        Args:
            query: Consulta del usuario
            selected_agents: Lista de agentes seleccionados (opcional)
        
        Returns:
            QueryResult con la respuesta y metadatos
        """
        if not self.is_initialized:
            await self.initialize()
        
        # Tracking
        agents_used = []
        sources_consulted = []
        reasoning_trace = []
        
        reasoning_trace.append(f"[INICIO] Procesando consulta: {query}")
        
        # CAPA 1: Recepción de consulta
        self.memory.remember_query(query)
        reasoning_trace.append("[CAPA 1] Consulta recibida y almacenada en memoria")
        
        # CAPA 2: Consultar memoria y crear plan
        reasoning_trace.append("[CAPA 2] Consultando memoria y planificando...")
        
        # Obtener contexto relevante
        context = self.memory.get_full_context_for_llm(query)
        reasoning_trace.append(f"[MEMORIA] Contexto recuperado: {len(context)} caracteres")
        
        # Crear plan de ejecución
        plan = self.planning.create_plan(query, {"context": context})
        reasoning_trace.extend(plan.reasoning_trace)
        
        # CAPA 3: Delegación de tareas
        reasoning_trace.append("[CAPA 3] Delegando tareas a sub-agentes...")
        
        # Determinar agentes a usar
        if selected_agents:
            target_agents = selected_agents
        else:
            # Encontrar mejor agente automáticamente
            best_agent = self.sub_agents.find_best_agent(query)
            target_agents = [best_agent.name] if best_agent else ["reasoning_agent"]
        
        agents_used = target_agents
        reasoning_trace.append(f"[AGENTES] Seleccionados: {', '.join(target_agents)}")
        
        # CAPA 4: Conexión con MCP Servers
        reasoning_trace.append("[CAPA 4] Consultando fuentes externas...")
        
        # Buscar en datos locales
        local_response = await self.mcp_servers.query_server("local_data", {
            "action": "search",
            "query": query
        })
        if local_response.success and local_response.data:
            sources_consulted.append("local_data")
            reasoning_trace.append(f"[MCP] Datos locales: {len(local_response.data)} resultados")
        
        # Buscar en motor de búsqueda (si está configurado)
        search_response = await self.mcp_servers.query_server("search_engine", {
            "action": "search",
            "query": query,
            "max_results": 5
        })
        if search_response.success and search_response.data:
            sources_consulted.append("search_engine")
            reasoning_trace.append(f"[MCP] Búsqueda web: {len(search_response.data)} resultados")
        
        # CAPA 5: Procesamiento y síntesis
        reasoning_trace.append("[CAPA 5] Sintetizando respuesta final...")
        
        # Ejecutar tareas con agentes
        agent_responses = []
        for agent_name in target_agents:
            task = await self.sub_agents.delegate_task(
                agent_name,
                query,
                {"context": context, "sources": sources_consulted}
            )
            executed_task = await self.sub_agents.execute_task(task, context)
            if executed_task.result:
                agent_responses.append({
                    "agent": agent_name,
                    "response": executed_task.result.get("response", "")
                })
        
        # Generar respuesta final
        final_response = await self._synthesize_response(
            query=query,
            context=context,
            agent_responses=agent_responses,
            mcp_data={
                "local": local_response.data if local_response.success else None,
                "search": search_response.data if search_response.success else None
            }
        )
        
        reasoning_trace.append("[SÍNTESIS] Respuesta final generada")
        
        # Almacenar en memoria
        self.memory.remember_response(final_response)
        
        # Crear resultado
        result = QueryResult(
            query=query,
            response=final_response,
            plan_id=plan.id,
            agents_used=agents_used,
            sources_consulted=sources_consulted,
            reasoning_trace=reasoning_trace,
            metadata={
                "model_id": self.model_id,
                "plan_steps": len(plan.steps)
            }
        )
        
        self.query_history.append(result)
        
        return result
    
    async def _synthesize_response(self, query: str, context: str,
                                   agent_responses: List[Dict],
                                   mcp_data: Dict) -> str:
        """Sintetizar respuesta final usando el LLM"""
        
        # Construir prompt de síntesis
        synthesis_prompt = self._build_synthesis_prompt(
            query, context, agent_responses, mcp_data
        )
        
        # Llamar a API si está disponible
        if self.api_callback:
            try:
                response = await self.api_callback(
                    prompt=synthesis_prompt,
                    model_id=self.model_id
                )
                return response
            except Exception as e:
                return f"Error al generar respuesta: {str(e)}"
        
        # Respuesta por defecto si no hay API
        if agent_responses:
            return agent_responses[0].get("response", "No se pudo generar respuesta")
        
        return "Sistema inicializado. Configure una API para obtener respuestas completas."
    
    def _build_synthesis_prompt(self, query: str, context: str,
                                agent_responses: List[Dict],
                                mcp_data: Dict) -> str:
        """Construir prompt para síntesis final"""
        
        prompt_parts = [
            "Eres el Agente Central del sistema ATP (Agentes de Tareas Polivalentes).",
            "Tu trabajo es sintetizar toda la información recopilada en una respuesta coherente.",
            "",
            f"CONSULTA DEL USUARIO: {query}",
            ""
        ]
        
        if context:
            prompt_parts.extend([
                "CONTEXTO DE SESIÓN:",
                context,
                ""
            ])
        
        if agent_responses:
            prompt_parts.append("RESPUESTAS DE AGENTES ESPECIALIZADOS:")
            for resp in agent_responses:
                prompt_parts.append(f"- [{resp['agent']}]: {resp['response']}")
            prompt_parts.append("")
        
        if mcp_data.get("local"):
            prompt_parts.extend([
                "DATOS LOCALES ENCONTRADOS:",
                json.dumps(mcp_data["local"][:3], ensure_ascii=False, indent=2),
                ""
            ])
        
        if mcp_data.get("search"):
            prompt_parts.extend([
                "RESULTADOS DE BÚSQUEDA:",
                json.dumps(mcp_data["search"][:3], ensure_ascii=False, indent=2),
                ""
            ])
        
        prompt_parts.extend([
            "INSTRUCCIONES:",
            "1. Analiza toda la información proporcionada",
            "2. Sintetiza una respuesta completa y coherente",
            "3. Cita las fuentes cuando sea relevante",
            "4. Mantén un tono profesional pero accesible",
            "5. Si hay información conflictiva, menciona las diferentes perspectivas",
            "",
            "Genera tu respuesta:"
        ])
        
        return "\n".join(prompt_parts)
    
    def store_knowledge(self, fact: str, category: str = "general"):
        """Almacenar conocimiento en memoria a largo plazo"""
        return self.memory.store_fact(fact, category)
    
    def clear_session(self):
        """Limpiar sesión actual"""
        self.memory.clear_session()
    
    def get_system_status(self) -> Dict:
        """Obtener estado del sistema"""
        return {
            "is_initialized": self.is_initialized,
            "model_id": self.model_id,
            "memory": {
                "short_term_entries": len(self.memory.short_term.entries),
                "long_term_entries": len(self.memory.long_term.entries)
            },
            "mcp_servers": self.mcp_servers.get_all_status(),
            "agents": {
                "total": len(self.sub_agents.agents),
                "by_level": {
                    level: len(self.sub_agents.get_agents_by_level(level))
                    for level in range(1, 6)
                }
            },
            "query_history_count": len(self.query_history)
        }
    
    def get_available_agents(self) -> List[Dict]:
        """Obtener lista de agentes disponibles"""
        return [
            agent.to_dict() 
            for agent in self.sub_agents.agents.values()
        ]
    
    def get_query_history(self, limit: int = 20) -> List[Dict]:
        """Obtener historial de consultas"""
        return [q.to_dict() for q in self.query_history[-limit:]]


# Función de utilidad para crear instancia global
_central_agent_instance: Optional[CentralAgent] = None

def get_central_agent(data_path: str = "./data") -> CentralAgent:
    """Obtener instancia singleton del Agente Central"""
    global _central_agent_instance
    if _central_agent_instance is None:
        _central_agent_instance = CentralAgent(data_path)
    return _central_agent_instance
