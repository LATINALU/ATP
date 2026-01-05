"""
Base Agent Architecture - ATP v0.6.1
Sistema de agentes especializados usando LangGraph

Arquitectura diseñada por desarrollador senior con 30+ años de experiencia.
Cada agente es una supercomputadora única con capacidades especializadas.
"""
from typing import Dict, Any, List, Optional, Callable
from abc import ABC, abstractmethod
from datetime import datetime
import asyncio
import time

from app.a2a_protocol import (
    A2AMessage, A2AResponse, AgentProfile, AgentCapability,
    AgentStatus, a2a_protocol, MessageType, Priority
)
from app.llm_providers import chat_completion


class BaseAgent(ABC):
    """
    Clase base abstracta para todos los agentes especializados.
    
    Cada agente hereda de esta clase y debe implementar:
    - process_task: Lógica principal de procesamiento
    - get_system_prompt: Prompt especializado del agente
    
    Características:
    - Comunicación vía protocolo A2A
    - Gestión de estado interno
    - Tracking de métricas
    - Manejo de errores robusto
    - Capacidad de delegación a otros agentes
    """
    
    def __init__(
        self,
        agent_id: str,
        name: str,
        primary_capability: AgentCapability,
        specialization: str,
        description: str,
        backstory: str,
        model_name: str = "gpt-4",
        temperature: float = 0.7,
        max_tokens: int = 4000,
        secondary_capabilities: Optional[List[AgentCapability]] = None,
        model: Optional[str] = None,
        api_config: Optional[Dict[str, Any]] = None
    ):
        # Usar model proporcionado o default
        actual_model = model or model_name
        
        # Perfil del agente
        self.profile = AgentProfile(
            agent_id=agent_id,
            name=name,
            primary_capability=primary_capability,
            secondary_capabilities=secondary_capabilities or [],
            specialization=specialization,
            description=description,
            backstory=backstory,
            model_name=actual_model,
            temperature=temperature,
            max_tokens=max_tokens,
            expertise_level="master"
        )
        
        # Estado interno
        self.state: Dict[str, Any] = {}
        self.memory: List[Dict[str, Any]] = []
        self.active_tasks: Dict[str, A2AMessage] = {}
        
        # Configuración de modelo y API
        self.model = actual_model
        self.api_config = api_config
        
        # Métricas
        self.metrics = {
            "total_tasks": 0,
            "successful_tasks": 0,
            "failed_tasks": 0,
            "total_processing_time_ms": 0.0,
            "average_response_time_ms": 0.0,
            "total_tokens_used": 0
        }
        
        # Registrar en el protocolo A2A
        a2a_protocol.register_agent(self.profile)
    
    @abstractmethod
    def get_system_prompt(self) -> str:
        """
        Retorna el system prompt especializado del agente.
        Debe ser implementado por cada agente concreto.
        """
        pass
    
    @abstractmethod
    async def process_task(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Procesa una tarea específica del agente.
        Debe ser implementado por cada agente concreto.
        
        Args:
            task: Descripción de la tarea a realizar
            context: Contexto adicional para la tarea
            
        Returns:
            Dict con el resultado del procesamiento
        """
        pass
    
    async def handle_message(self, message: A2AMessage) -> A2AResponse:
        """
        Maneja un mensaje A2A recibido.
        
        Este es el punto de entrada principal para la comunicación entre agentes.
        """
        start_time = time.time()
        
        try:
            # Actualizar estado
            self.profile.status = AgentStatus.PROCESSING
            self.profile.current_load += 1
            self.active_tasks[message.message_id] = message
            
            # Validar mensaje
            is_valid, error = a2a_protocol.validate_message(message)
            if not is_valid:
                return self._create_error_response(message, error)
            
            # Procesar según tipo de mensaje
            if message.message_type == MessageType.REQUEST:
                result = await self._handle_request(message)
            elif message.message_type == MessageType.QUERY:
                result = await self._handle_query(message)
            elif message.message_type == MessageType.COMMAND:
                result = await self._handle_command(message)
            else:
                result = {"error": f"Message type {message.message_type} not supported"}
            
            # Calcular tiempo de procesamiento
            processing_time = (time.time() - start_time) * 1000
            
            # Actualizar métricas
            self._update_metrics(processing_time, success=True)
            
            # Crear respuesta exitosa
            response = a2a_protocol.create_response(
                original_message=message,
                responder_id=self.profile.agent_id,
                responder_capability=self.profile.primary_capability,
                result=result,
                success=True,
                processing_time_ms=processing_time,
                confidence=result.get("confidence", 0.9)
            )
            
            return response
            
        except Exception as e:
            # Manejar error
            processing_time = (time.time() - start_time) * 1000
            self._update_metrics(processing_time, success=False)
            
            return self._create_error_response(
                message,
                f"Error processing message: {str(e)}"
            )
            
        finally:
            # Limpiar estado
            self.profile.current_load -= 1
            if message.message_id in self.active_tasks:
                del self.active_tasks[message.message_id]
            
            if self.profile.current_load == 0:
                self.profile.status = AgentStatus.IDLE
            
            self.profile.last_active = datetime.utcnow()
    
    async def _handle_request(self, message: A2AMessage) -> Dict[str, Any]:
        """Maneja una solicitud de procesamiento"""
        task = message.payload.get("task", "")
        context = message.payload.get("context", {})
        
        if not task:
            raise ValueError("Task is required in payload")
        
        result = await self.process_task(task, context)
        return result
    
    async def _handle_query(self, message: A2AMessage) -> Dict[str, Any]:
        """Maneja una consulta de información"""
        query = message.payload.get("query", "")
        
        if not query:
            raise ValueError("Query is required in payload")
        
        # Usar el agente para responder la consulta
        result = await self.process_task(f"Responde esta consulta: {query}", message.context)
        return result
    
    async def _handle_command(self, message: A2AMessage) -> Dict[str, Any]:
        """Maneja un comando directo"""
        command = message.payload.get("command", "")
        params = message.payload.get("params", {})
        
        if not command:
            raise ValueError("Command is required in payload")
        
        # Ejecutar comando específico
        if command == "get_status":
            return self._get_status()
        elif command == "get_metrics":
            return self._get_metrics()
        elif command == "reset_metrics":
            return self._reset_metrics()
        else:
            raise ValueError(f"Unknown command: {command}")
    
    def _create_error_response(self, message: A2AMessage, error: str) -> A2AResponse:
        """Crea una respuesta de error"""
        return a2a_protocol.create_response(
            original_message=message,
            responder_id=self.profile.agent_id,
            responder_capability=self.profile.primary_capability,
            result={"error": error},
            success=False,
            status_code=400,
            error_message=error
        )
    
    async def call_llm(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Llama al LLM con el system prompt del agente.
        
        Args:
            messages: Lista de mensajes para el LLM
            temperature: Temperatura para la generación (usa default del agente si None)
            max_tokens: Máximo de tokens (usa default del agente si None)
            
        Returns:
            Respuesta del LLM
        """
        # Preparar mensajes con system prompt
        full_messages = [
            {"role": "system", "content": self.get_system_prompt()}
        ] + messages
        
        # Usar configuración del agente si no se especifica
        temp = temperature if temperature is not None else self.profile.temperature
        max_tok = max_tokens if max_tokens is not None else self.profile.max_tokens
        
        # Llamar al LLM con configuración del agente
        response = await chat_completion(
            messages=full_messages,
            model=self.model,
            temperature=temp,
            max_tokens=max_tok,
            api_config=self.api_config
        )
        
        # Actualizar métricas de tokens (si está disponible)
        if hasattr(response, 'usage'):
            self.metrics["total_tokens_used"] += response.usage.total_tokens
        
        return response
    
    async def delegate_to_agent(
        self,
        capability: AgentCapability,
        task: str,
        context: Optional[Dict[str, Any]] = None,
        priority: Priority = Priority.NORMAL
    ) -> A2AResponse:
        """
        Delega una tarea a otro agente con la capacidad especificada.
        
        Args:
            capability: Capacidad requerida del agente
            task: Tarea a delegar
            context: Contexto adicional
            priority: Prioridad del mensaje
            
        Returns:
            Respuesta del agente delegado
        """
        # Encontrar agente capaz
        capable_agents = a2a_protocol.find_capable_agents(
            required_capability=capability,
            exclude_agents=[self.profile.agent_id]
        )
        
        if not capable_agents:
            raise ValueError(f"No agent found with capability: {capability}")
        
        # Seleccionar el mejor agente (menor carga)
        target_agent = capable_agents[0]
        
        # Crear mensaje A2A
        message = a2a_protocol.create_message(
            sender_id=self.profile.agent_id,
            sender_capability=self.profile.primary_capability,
            subject=f"Delegation: {task[:50]}...",
            payload={"task": task, "context": context or {}},
            message_type=MessageType.REQUEST,
            recipient_id=target_agent.agent_id,
            priority=priority
        )
        
        # Aquí se enviaría el mensaje al agente target
        # Por ahora retornamos un placeholder
        # En la implementación completa, esto iría a través del orquestador
        
        return A2AResponse(
            original_message_id=message.message_id,
            conversation_id=message.conversation_id,
            responder_id=target_agent.agent_id,
            responder_capability=target_agent.primary_capability,
            success=True,
            result={"delegated": True, "target_agent": target_agent.agent_id}
        )
    
    def _update_metrics(self, processing_time_ms: float, success: bool):
        """Actualiza las métricas del agente"""
        self.metrics["total_tasks"] += 1
        
        if success:
            self.metrics["successful_tasks"] += 1
        else:
            self.metrics["failed_tasks"] += 1
        
        self.metrics["total_processing_time_ms"] += processing_time_ms
        self.metrics["average_response_time_ms"] = (
            self.metrics["total_processing_time_ms"] / self.metrics["total_tasks"]
        )
        
        # Actualizar perfil
        self.profile.average_response_time_ms = self.metrics["average_response_time_ms"]
        self.profile.reliability_score = (
            self.metrics["successful_tasks"] / self.metrics["total_tasks"]
            if self.metrics["total_tasks"] > 0 else 1.0
        )
    
    def _get_status(self) -> Dict[str, Any]:
        """Obtiene el estado actual del agente"""
        return {
            "agent_id": self.profile.agent_id,
            "name": self.profile.name,
            "status": self.profile.status.value,
            "current_load": self.profile.current_load,
            "max_concurrent_tasks": self.profile.max_concurrent_tasks,
            "active_tasks": len(self.active_tasks),
            "last_active": self.profile.last_active.isoformat()
        }
    
    def _get_metrics(self) -> Dict[str, Any]:
        """Obtiene las métricas del agente"""
        return {
            **self.metrics,
            "reliability_score": self.profile.reliability_score,
            "success_rate": (
                self.metrics["successful_tasks"] / self.metrics["total_tasks"]
                if self.metrics["total_tasks"] > 0 else 1.0
            )
        }
    
    def _reset_metrics(self) -> Dict[str, Any]:
        """Resetea las métricas del agente"""
        self.metrics = {
            "total_tasks": 0,
            "successful_tasks": 0,
            "failed_tasks": 0,
            "total_processing_time_ms": 0.0,
            "average_response_time_ms": 0.0,
            "total_tokens_used": 0
        }
        return {"message": "Metrics reset successfully"}
    
    def add_to_memory(self, entry: Dict[str, Any]):
        """Agrega una entrada a la memoria del agente"""
        entry["timestamp"] = datetime.utcnow().isoformat()
        self.memory.append(entry)
        
        # Limitar memoria a últimas 100 entradas
        if len(self.memory) > 100:
            self.memory = self.memory[-100:]
    
    def get_memory_context(self, limit: int = 10) -> str:
        """Obtiene contexto de memoria reciente"""
        recent_memory = self.memory[-limit:]
        
        if not recent_memory:
            return "No hay memoria previa."
        
        context_parts = []
        for entry in recent_memory:
            context_parts.append(f"- {entry.get('summary', str(entry))}")
        
        return "\n".join(context_parts)
