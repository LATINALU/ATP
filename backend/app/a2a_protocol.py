"""
A2A Protocol (Agent-to-Agent Communication Protocol)
Version: 0.6.1

Protocolo de comunicación estructurado para agentes especializados.
Proporciona una capa aislada de comunicación entre agentes, evitando enredos
y manteniendo la integridad del sistema.

Arquitectura diseñada por desarrollador senior con 30+ años de experiencia.
"""
from typing import Dict, Any, List, Optional, Literal
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
import uuid


class MessageType(str, Enum):
    """Tipos de mensajes en el protocolo A2A"""
    REQUEST = "request"           # Solicitud de procesamiento
    RESPONSE = "response"         # Respuesta a solicitud
    BROADCAST = "broadcast"       # Mensaje a múltiples agentes
    QUERY = "query"              # Consulta de información
    COMMAND = "command"          # Comando directo
    EVENT = "event"              # Notificación de evento
    ERROR = "error"              # Reporte de error
    ACKNOWLEDGMENT = "ack"       # Confirmación de recepción


class AgentCapability(str, Enum):
    """Capacidades especializadas de agentes"""
    # Cognitive Capabilities
    REASONING = "reasoning"
    PLANNING = "planning"
    ANALYSIS = "analysis"
    SYNTHESIS = "synthesis"
    CRITICAL_THINKING = "critical_thinking"
    
    # Technical Capabilities
    CODING = "coding"
    DATA_ANALYSIS = "data_analysis"
    SYSTEM_ARCHITECTURE = "system_architecture"
    OPTIMIZATION = "optimization"
    SECURITY = "security"
    
    # Communication Capabilities
    WRITING = "writing"
    TRANSLATION = "translation"
    DOCUMENTATION = "documentation"
    PRESENTATION = "presentation"
    
    # Domain Expertise
    LEGAL = "legal"
    FINANCIAL = "financial"
    MEDICAL = "medical"
    SCIENTIFIC = "scientific"
    CREATIVE = "creative"
    EDUCATIONAL = "educational"
    MARKETING = "marketing"


class Priority(str, Enum):
    """Niveles de prioridad de mensajes"""
    CRITICAL = "critical"    # Requiere procesamiento inmediato
    HIGH = "high"           # Alta prioridad
    NORMAL = "normal"       # Prioridad normal
    LOW = "low"            # Baja prioridad
    BACKGROUND = "background"  # Procesamiento en segundo plano


class AgentStatus(str, Enum):
    """Estados de agente"""
    IDLE = "idle"              # Disponible
    PROCESSING = "processing"  # Procesando tarea
    WAITING = "waiting"        # Esperando respuesta
    ERROR = "error"           # Estado de error
    OFFLINE = "offline"       # No disponible


class A2AMessage(BaseModel):
    """Mensaje estructurado del protocolo A2A"""
    
    # Metadata del mensaje
    message_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    message_type: MessageType
    priority: Priority = Priority.NORMAL
    
    # Routing
    sender_id: str
    sender_capability: AgentCapability
    recipient_id: Optional[str] = None  # None para broadcast
    recipient_capabilities: Optional[List[AgentCapability]] = None
    
    # Contenido
    subject: str
    payload: Dict[str, Any]
    context: Optional[Dict[str, Any]] = None
    
    # Tracking
    conversation_id: Optional[str] = None
    parent_message_id: Optional[str] = None
    requires_response: bool = True
    timeout_seconds: Optional[int] = 30
    
    # Metadata adicional
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class A2AResponse(BaseModel):
    """Respuesta estructurada del protocolo A2A"""
    
    response_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    # Referencia al mensaje original
    original_message_id: str
    conversation_id: str
    
    # Agente respondiente
    responder_id: str
    responder_capability: AgentCapability
    
    # Estado de la respuesta
    success: bool
    status_code: int = 200  # HTTP-like status codes
    
    # Contenido de la respuesta
    result: Any
    reasoning: Optional[str] = None  # Explicación del razonamiento
    confidence: float = Field(ge=0.0, le=1.0, default=1.0)
    
    # Información adicional
    processing_time_ms: Optional[float] = None
    tokens_used: Optional[int] = None
    error_message: Optional[str] = None
    suggestions: Optional[List[str]] = None
    
    # Metadata
    metadata: Dict[str, Any] = Field(default_factory=dict)


class AgentProfile(BaseModel):
    """Perfil completo de un agente especializado"""
    
    # Identificación
    agent_id: str
    name: str
    version: str = "0.6.1"
    
    # Capacidades
    primary_capability: AgentCapability
    secondary_capabilities: List[AgentCapability] = Field(default_factory=list)
    
    # Especialización
    specialization: str
    expertise_level: Literal["junior", "mid", "senior", "expert", "master"] = "expert"
    domain_knowledge: List[str] = Field(default_factory=list)
    
    # Características operacionales
    max_concurrent_tasks: int = 3
    average_response_time_ms: float = 1000.0
    reliability_score: float = Field(ge=0.0, le=1.0, default=0.95)
    
    # Estado actual
    status: AgentStatus = AgentStatus.IDLE
    current_load: int = 0
    
    # Configuración
    model_name: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 4000
    
    # Metadata
    description: str
    backstory: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_active: datetime = Field(default_factory=datetime.utcnow)


class A2AProtocol:
    """
    Implementación del protocolo A2A
    
    Proporciona métodos para:
    - Crear mensajes estructurados
    - Validar comunicaciones
    - Enrutar mensajes entre agentes
    - Gestionar conversaciones
    - Tracking y logging
    """
    
    def __init__(self):
        self.active_conversations: Dict[str, List[A2AMessage]] = {}
        self.agent_registry: Dict[str, AgentProfile] = {}
        
    def register_agent(self, profile: AgentProfile) -> bool:
        """Registrar un agente en el protocolo"""
        self.agent_registry[profile.agent_id] = profile
        return True
    
    def create_message(
        self,
        sender_id: str,
        sender_capability: AgentCapability,
        subject: str,
        payload: Dict[str, Any],
        message_type: MessageType = MessageType.REQUEST,
        recipient_id: Optional[str] = None,
        recipient_capabilities: Optional[List[AgentCapability]] = None,
        priority: Priority = Priority.NORMAL,
        conversation_id: Optional[str] = None,
        **kwargs
    ) -> A2AMessage:
        """Crear un mensaje A2A estructurado"""
        
        if conversation_id is None:
            conversation_id = str(uuid.uuid4())
        
        message = A2AMessage(
            message_type=message_type,
            priority=priority,
            sender_id=sender_id,
            sender_capability=sender_capability,
            recipient_id=recipient_id,
            recipient_capabilities=recipient_capabilities,
            subject=subject,
            payload=payload,
            conversation_id=conversation_id,
            **kwargs
        )
        
        # Almacenar en conversación activa
        if conversation_id not in self.active_conversations:
            self.active_conversations[conversation_id] = []
        self.active_conversations[conversation_id].append(message)
        
        return message
    
    def create_response(
        self,
        original_message: A2AMessage,
        responder_id: str,
        responder_capability: AgentCapability,
        result: Any,
        success: bool = True,
        **kwargs
    ) -> A2AResponse:
        """Crear una respuesta A2A estructurada"""
        
        response = A2AResponse(
            original_message_id=original_message.message_id,
            conversation_id=original_message.conversation_id,
            responder_id=responder_id,
            responder_capability=responder_capability,
            success=success,
            result=result,
            **kwargs
        )
        
        return response
    
    def find_capable_agents(
        self,
        required_capability: AgentCapability,
        exclude_agents: Optional[List[str]] = None
    ) -> List[AgentProfile]:
        """Encontrar agentes con una capacidad específica"""
        
        exclude_agents = exclude_agents or []
        capable_agents = []
        
        for agent_id, profile in self.agent_registry.items():
            if agent_id in exclude_agents:
                continue
            
            if (profile.primary_capability == required_capability or
                required_capability in profile.secondary_capabilities):
                if profile.status == AgentStatus.IDLE or profile.current_load < profile.max_concurrent_tasks:
                    capable_agents.append(profile)
        
        # Ordenar por carga actual (menor carga primero)
        capable_agents.sort(key=lambda x: x.current_load)
        
        return capable_agents
    
    def get_conversation_history(self, conversation_id: str) -> List[A2AMessage]:
        """Obtener historial de una conversación"""
        return self.active_conversations.get(conversation_id, [])
    
    def validate_message(self, message: A2AMessage) -> tuple[bool, Optional[str]]:
        """Validar un mensaje A2A"""
        
        # Validar sender existe
        if message.sender_id not in self.agent_registry:
            return False, f"Sender agent {message.sender_id} not registered"
        
        # Validar recipient si es específico
        if message.recipient_id and message.recipient_id not in self.agent_registry:
            return False, f"Recipient agent {message.recipient_id} not registered"
        
        # Validar payload no está vacío
        if not message.payload:
            return False, "Message payload cannot be empty"
        
        return True, None


# Instancia global del protocolo
a2a_protocol = A2AProtocol()
