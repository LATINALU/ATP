"""
Sistema de Sub-Agentes para Agentic RAG
Gestiona la delegación de tareas a agentes especializados
"""

import asyncio
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json


class AgentStatus(Enum):
    IDLE = "idle"
    BUSY = "busy"
    ERROR = "error"
    OFFLINE = "offline"


@dataclass
class AgentTask:
    """Tarea asignada a un agente"""
    id: str
    agent_name: str
    description: str
    input_data: Dict[str, Any]
    status: str = "pending"
    result: Optional[Dict] = None
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    error: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "agent_name": self.agent_name,
            "description": self.description,
            "input_data": self.input_data,
            "status": self.status,
            "result": self.result,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "error": self.error
        }


@dataclass
class SubAgentConfig:
    """Configuración de un sub-agente"""
    name: str
    role: str
    level: int
    capabilities: List[str]
    model_id: Optional[str] = None
    custom_instructions: str = ""
    status: AgentStatus = AgentStatus.IDLE
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "role": self.role,
            "level": self.level,
            "capabilities": self.capabilities,
            "model_id": self.model_id,
            "custom_instructions": self.custom_instructions,
            "status": self.status.value
        }


class SubAgentManager:
    """
    Gestor de Sub-Agentes
    Coordina la delegación de tareas a los 30 agentes especializados
    """
    
    def __init__(self):
        self.agents: Dict[str, SubAgentConfig] = {}
        self.task_queue: List[AgentTask] = []
        self.completed_tasks: List[AgentTask] = []
        self.api_callback: Optional[Callable] = None
        
        # Inicializar agentes por defecto
        self._init_default_agents()
    
    def _init_default_agents(self):
        """Inicializar los 30 agentes del sistema ATP"""
        
        # Nivel 1 - CRÍTICOS
        level1_agents = [
            ("reasoning_agent", "Agente de Razonamiento", ["logic", "deduction", "inference"]),
            ("planning_agent", "Agente de Planificación", ["strategy", "project_management", "scheduling"]),
            ("research_agent", "Agente de Investigación", ["research", "synthesis", "information_gathering"]),
            ("analysis_agent", "Agente de Análisis", ["analysis", "decomposition", "evaluation"]),
            ("synthesis_agent", "Agente de Síntesis", ["integration", "knowledge_synthesis", "insights"]),
            ("critical_thinking_agent", "Agente de Pensamiento Crítico", ["critical_evaluation", "fallacy_detection", "argumentation"]),
        ]
        
        # Nivel 2 - ESENCIALES
        level2_agents = [
            ("coding_agent", "Agente de Programación", ["coding", "debugging", "software_development"]),
            ("writing_agent", "Agente de Escritura", ["writing", "editing", "communication"]),
            ("data_agent", "Agente de Datos", ["data_analysis", "statistics", "visualization"]),
            ("communication_agent", "Agente de Comunicación", ["interpersonal", "stakeholder_management", "presentation"]),
            ("decision_agent", "Agente de Decisiones", ["decision_making", "risk_assessment", "prioritization"]),
            ("problem_solving_agent", "Agente de Resolución de Problemas", ["problem_solving", "creativity", "innovation"]),
        ]
        
        # Nivel 3 - ESPECIALIZADOS
        level3_agents = [
            ("legal_agent", "Agente Legal", ["legal", "compliance", "contracts"]),
            ("financial_agent", "Agente Financiero", ["finance", "economics", "budgeting"]),
            ("creative_agent", "Agente Creativo", ["creativity", "design", "brainstorming"]),
            ("technical_agent", "Agente Técnico", ["architecture", "systems", "infrastructure"]),
            ("educational_agent", "Agente Educativo", ["teaching", "instructional_design", "learning"]),
            ("marketing_agent", "Agente de Marketing", ["marketing", "branding", "strategy"]),
        ]
        
        # Nivel 4 - SOPORTE
        level4_agents = [
            ("qa_agent", "Agente de QA", ["testing", "quality_assurance", "validation"]),
            ("documentation_agent", "Agente de Documentación", ["documentation", "technical_writing", "manuals"]),
            ("optimization_agent", "Agente de Optimización", ["optimization", "performance", "efficiency"]),
            ("security_agent", "Agente de Seguridad", ["security", "privacy", "compliance"]),
            ("integration_agent", "Agente de Integración", ["integration", "apis", "systems"]),
            ("review_agent", "Agente de Revisión", ["review", "feedback", "quality_control"]),
        ]
        
        # Nivel 5 - AUXILIARES
        level5_agents = [
            ("translation_agent", "Agente de Traducción", ["translation", "localization", "languages"]),
            ("summary_agent", "Agente de Resumen", ["summarization", "condensation", "extraction"]),
            ("formatting_agent", "Agente de Formato", ["formatting", "presentation", "styling"]),
            ("validation_agent", "Agente de Validación", ["validation", "verification", "checking"]),
            ("coordination_agent", "Agente de Coordinación", ["coordination", "team_management", "scheduling"]),
            ("explanation_agent", "Agente de Explicación", ["explanation", "teaching", "simplification"]),
        ]
        
        # Registrar todos los agentes
        all_agents = [
            (1, level1_agents),
            (2, level2_agents),
            (3, level3_agents),
            (4, level4_agents),
            (5, level5_agents)
        ]
        
        for level, agents in all_agents:
            for name, role, capabilities in agents:
                self.register_agent(SubAgentConfig(
                    name=name,
                    role=role,
                    level=level,
                    capabilities=capabilities
                ))
    
    def register_agent(self, config: SubAgentConfig):
        """Registrar un nuevo agente"""
        self.agents[config.name] = config
    
    def get_agent(self, name: str) -> Optional[SubAgentConfig]:
        """Obtener configuración de un agente"""
        return self.agents.get(name)
    
    def get_agents_by_level(self, level: int) -> List[SubAgentConfig]:
        """Obtener agentes por nivel"""
        return [a for a in self.agents.values() if a.level == level]
    
    def get_agents_by_capability(self, capability: str) -> List[SubAgentConfig]:
        """Obtener agentes que tienen una capacidad específica"""
        return [
            a for a in self.agents.values() 
            if capability.lower() in [c.lower() for c in a.capabilities]
        ]
    
    def find_best_agent(self, task_description: str) -> Optional[SubAgentConfig]:
        """Encontrar el mejor agente para una tarea"""
        task_lower = task_description.lower()
        
        # Mapeo de palabras clave a agentes
        keyword_mapping = {
            "reasoning_agent": ["razona", "lógica", "deduce", "infiere", "reason", "logic"],
            "planning_agent": ["planifica", "estrategia", "proyecto", "plan", "strategy"],
            "research_agent": ["investiga", "busca", "research", "find", "search"],
            "analysis_agent": ["analiza", "evalúa", "analyze", "evaluate", "assess"],
            "synthesis_agent": ["sintetiza", "integra", "combina", "synthesize", "integrate"],
            "critical_thinking_agent": ["critica", "evalúa", "argumenta", "critical", "argue"],
            "coding_agent": ["código", "programa", "función", "code", "program", "script"],
            "writing_agent": ["escribe", "redacta", "email", "write", "draft", "compose"],
            "data_agent": ["datos", "estadísticas", "gráfico", "data", "statistics", "chart"],
            "communication_agent": ["comunica", "presenta", "communicate", "present"],
            "decision_agent": ["decide", "elige", "prioriza", "decide", "choose", "prioritize"],
            "problem_solving_agent": ["resuelve", "soluciona", "solve", "fix", "solution"],
            "legal_agent": ["legal", "contrato", "ley", "contract", "law", "compliance"],
            "financial_agent": ["financiero", "dinero", "presupuesto", "financial", "money", "budget"],
            "creative_agent": ["creativo", "diseña", "innova", "creative", "design", "innovate"],
            "technical_agent": ["técnico", "arquitectura", "sistema", "technical", "architecture"],
            "educational_agent": ["enseña", "explica", "aprende", "teach", "learn", "educate"],
            "marketing_agent": ["marketing", "marca", "ventas", "brand", "sales"],
            "qa_agent": ["prueba", "test", "calidad", "quality", "testing"],
            "documentation_agent": ["documenta", "manual", "guía", "document", "guide"],
            "optimization_agent": ["optimiza", "mejora", "rendimiento", "optimize", "improve"],
            "security_agent": ["seguridad", "protege", "security", "protect", "secure"],
            "integration_agent": ["integra", "conecta", "api", "integrate", "connect"],
            "review_agent": ["revisa", "feedback", "review", "check"],
            "translation_agent": ["traduce", "idioma", "translate", "language"],
            "summary_agent": ["resume", "condensa", "summarize", "summary"],
            "formatting_agent": ["formato", "presenta", "format", "style"],
            "validation_agent": ["valida", "verifica", "validate", "verify"],
            "coordination_agent": ["coordina", "equipo", "coordinate", "team"],
            "explanation_agent": ["explica", "simplifica", "explain", "simplify"],
        }
        
        # Buscar coincidencias
        best_match = None
        best_score = 0
        
        for agent_name, keywords in keyword_mapping.items():
            score = sum(1 for kw in keywords if kw in task_lower)
            if score > best_score:
                best_score = score
                best_match = agent_name
        
        if best_match:
            return self.agents.get(best_match)
        
        # Si no hay coincidencia, usar agente de razonamiento por defecto
        return self.agents.get("reasoning_agent")
    
    def set_agent_model(self, agent_name: str, model_id: str):
        """Asignar modelo a un agente"""
        if agent_name in self.agents:
            self.agents[agent_name].model_id = model_id
    
    def set_agent_instructions(self, agent_name: str, instructions: str):
        """Asignar instrucciones personalizadas a un agente"""
        if agent_name in self.agents:
            self.agents[agent_name].custom_instructions = instructions
    
    def set_api_callback(self, callback: Callable):
        """Establecer callback para llamadas a API"""
        self.api_callback = callback
    
    async def delegate_task(self, agent_name: str, task_description: str, 
                           input_data: Dict = None) -> AgentTask:
        """Delegar tarea a un agente específico"""
        import hashlib
        
        task_id = hashlib.md5(f"{agent_name}{task_description}{datetime.now()}".encode()).hexdigest()[:12]
        
        task = AgentTask(
            id=f"task_{task_id}",
            agent_name=agent_name,
            description=task_description,
            input_data=input_data or {}
        )
        
        self.task_queue.append(task)
        
        # Marcar agente como ocupado
        if agent_name in self.agents:
            self.agents[agent_name].status = AgentStatus.BUSY
        
        return task
    
    async def execute_task(self, task: AgentTask, context: str = "") -> AgentTask:
        """Ejecutar una tarea delegada"""
        agent = self.agents.get(task.agent_name)
        if not agent:
            task.status = "error"
            task.error = f"Agent {task.agent_name} not found"
            return task
        
        try:
            task.status = "in_progress"
            
            # Construir prompt para el agente
            prompt = self._build_agent_prompt(agent, task, context)
            
            # Ejecutar con callback de API si está disponible
            if self.api_callback:
                result = await self.api_callback(
                    prompt=prompt,
                    model_id=agent.model_id,
                    agent_name=agent.name
                )
                task.result = {"response": result}
            else:
                # Resultado simulado si no hay callback
                task.result = {
                    "response": f"[{agent.role}] Tarea procesada: {task.description}",
                    "simulated": True
                }
            
            task.status = "completed"
            task.completed_at = datetime.now()
            
        except Exception as e:
            task.status = "error"
            task.error = str(e)
        
        finally:
            # Marcar agente como disponible
            if task.agent_name in self.agents:
                self.agents[task.agent_name].status = AgentStatus.IDLE
            
            # Mover a tareas completadas
            if task in self.task_queue:
                self.task_queue.remove(task)
            self.completed_tasks.append(task)
        
        return task
    
    def _build_agent_prompt(self, agent: SubAgentConfig, task: AgentTask, 
                           context: str = "") -> str:
        """Construir prompt para el agente"""
        prompt_parts = [
            f"Eres {agent.role}, un agente especializado de nivel {agent.level}.",
            f"Tus capacidades principales son: {', '.join(agent.capabilities)}.",
        ]
        
        if agent.custom_instructions:
            prompt_parts.append(f"\nInstrucciones especiales: {agent.custom_instructions}")
        
        if context:
            prompt_parts.append(f"\nContexto relevante:\n{context}")
        
        prompt_parts.append(f"\nTarea asignada: {task.description}")
        
        if task.input_data:
            prompt_parts.append(f"\nDatos de entrada: {json.dumps(task.input_data, ensure_ascii=False)}")
        
        prompt_parts.append("\nProporciona una respuesta detallada y profesional.")
        
        return "\n".join(prompt_parts)
    
    def get_all_agents_status(self) -> Dict[str, Dict]:
        """Obtener estado de todos los agentes"""
        return {
            name: agent.to_dict()
            for name, agent in self.agents.items()
        }
    
    def get_task_history(self, limit: int = 50) -> List[Dict]:
        """Obtener historial de tareas"""
        return [t.to_dict() for t in self.completed_tasks[-limit:]]
    
    def get_pending_tasks(self) -> List[Dict]:
        """Obtener tareas pendientes"""
        return [t.to_dict() for t in self.task_queue]
