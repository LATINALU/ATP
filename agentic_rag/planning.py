"""
Sistema de Planificación para Agentic RAG
- ReACT (Reasoning + Acting): Razonamiento paso a paso con acciones
- Chain of Thought (CoT): Descomposición lógica de problemas
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import json


class PlanStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ActionType(Enum):
    SEARCH = "search"           # Buscar información
    RETRIEVE = "retrieve"       # Recuperar datos
    ANALYZE = "analyze"         # Analizar información
    SYNTHESIZE = "synthesize"   # Sintetizar resultados
    DELEGATE = "delegate"       # Delegar a sub-agente
    RESPOND = "respond"         # Generar respuesta
    STORE = "store"             # Almacenar en memoria


@dataclass
class PlanStep:
    """Paso individual en un plan"""
    id: str
    description: str
    action_type: ActionType
    status: PlanStatus = PlanStatus.PENDING
    dependencies: List[str] = field(default_factory=list)  # IDs de pasos previos requeridos
    assigned_agent: Optional[str] = None
    input_data: Dict[str, Any] = field(default_factory=dict)
    output_data: Dict[str, Any] = field(default_factory=dict)
    reasoning: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "description": self.description,
            "action_type": self.action_type.value,
            "status": self.status.value,
            "dependencies": self.dependencies,
            "assigned_agent": self.assigned_agent,
            "input_data": self.input_data,
            "output_data": self.output_data,
            "reasoning": self.reasoning,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }


@dataclass
class ExecutionPlan:
    """Plan de ejecución completo"""
    id: str
    query: str
    steps: List[PlanStep] = field(default_factory=list)
    status: PlanStatus = PlanStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    reasoning_trace: List[str] = field(default_factory=list)
    
    def add_step(self, step: PlanStep):
        self.steps.append(step)
        
    def get_next_step(self) -> Optional[PlanStep]:
        """Obtener el siguiente paso ejecutable"""
        for step in self.steps:
            if step.status == PlanStatus.PENDING:
                # Verificar dependencias
                deps_completed = all(
                    self.get_step(dep_id).status == PlanStatus.COMPLETED
                    for dep_id in step.dependencies
                    if self.get_step(dep_id)
                )
                if deps_completed:
                    return step
        return None
    
    def get_step(self, step_id: str) -> Optional[PlanStep]:
        for step in self.steps:
            if step.id == step_id:
                return step
        return None
    
    def is_complete(self) -> bool:
        return all(step.status in [PlanStatus.COMPLETED, PlanStatus.CANCELLED] 
                   for step in self.steps)
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "query": self.query,
            "steps": [s.to_dict() for s in self.steps],
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "reasoning_trace": self.reasoning_trace
        }


class ReACTPlanner:
    """
    Planificador ReACT (Reasoning + Acting)
    Genera planes usando el patrón: Thought -> Action -> Observation
    """
    
    def __init__(self):
        self.action_templates = {
            ActionType.SEARCH: "Buscar información sobre: {topic}",
            ActionType.RETRIEVE: "Recuperar datos de: {source}",
            ActionType.ANALYZE: "Analizar: {data}",
            ActionType.SYNTHESIZE: "Sintetizar resultados de: {sources}",
            ActionType.DELEGATE: "Delegar tarea a {agent}: {task}",
            ActionType.RESPOND: "Generar respuesta final",
            ActionType.STORE: "Almacenar en memoria: {data}"
        }
    
    def create_plan(self, query: str, context: Dict = None) -> ExecutionPlan:
        """
        Crear plan de ejecución usando ReACT
        """
        import hashlib
        plan_id = hashlib.md5(f"{query}{datetime.now()}".encode()).hexdigest()[:12]
        
        plan = ExecutionPlan(
            id=f"plan_{plan_id}",
            query=query
        )
        
        # Análisis inicial de la consulta
        plan.reasoning_trace.append(f"[THOUGHT] Analizando consulta: {query}")
        
        # Determinar tipo de tarea y crear pasos
        steps = self._decompose_query(query, context)
        
        for i, step_info in enumerate(steps):
            step = PlanStep(
                id=f"step_{i}",
                description=step_info["description"],
                action_type=step_info["action_type"],
                dependencies=step_info.get("dependencies", []),
                assigned_agent=step_info.get("agent"),
                reasoning=step_info.get("reasoning", "")
            )
            plan.add_step(step)
            plan.reasoning_trace.append(
                f"[ACTION] Paso {i+1}: {step.description} ({step.action_type.value})"
            )
        
        return plan
    
    def _decompose_query(self, query: str, context: Dict = None) -> List[Dict]:
        """Descomponer consulta en pasos ejecutables"""
        steps = []
        query_lower = query.lower()
        
        # Paso 1: Siempre buscar contexto relevante
        steps.append({
            "description": "Buscar información relevante en memoria y fuentes",
            "action_type": ActionType.SEARCH,
            "reasoning": "Primero necesito obtener contexto relevante"
        })
        
        # Paso 2: Determinar si necesita búsqueda externa
        needs_search = any(word in query_lower for word in [
            "busca", "encuentra", "investiga", "qué es", "cómo", "por qué",
            "search", "find", "what", "how", "why", "explain"
        ])
        
        if needs_search:
            steps.append({
                "description": "Buscar información en fuentes externas",
                "action_type": ActionType.RETRIEVE,
                "dependencies": ["step_0"],
                "reasoning": "La consulta requiere información externa"
            })
        
        # Paso 3: Determinar si necesita análisis
        needs_analysis = any(word in query_lower for word in [
            "analiza", "compara", "evalúa", "diferencia", "ventajas",
            "analyze", "compare", "evaluate", "difference", "advantages"
        ])
        
        if needs_analysis:
            steps.append({
                "description": "Analizar información recopilada",
                "action_type": ActionType.ANALYZE,
                "dependencies": [f"step_{len(steps)-1}"],
                "reasoning": "Se requiere análisis de la información"
            })
        
        # Paso 4: Determinar si necesita delegación a agentes especializados
        agent_keywords = {
            "coding_agent": ["código", "programa", "función", "code", "program"],
            "writing_agent": ["escribe", "redacta", "email", "write", "draft"],
            "data_agent": ["datos", "estadísticas", "gráfico", "data", "statistics"],
            "research_agent": ["investiga", "research", "estudia"],
            "analysis_agent": ["analiza", "analyze", "evalúa"]
        }
        
        for agent, keywords in agent_keywords.items():
            if any(kw in query_lower for kw in keywords):
                steps.append({
                    "description": f"Delegar tarea especializada a {agent}",
                    "action_type": ActionType.DELEGATE,
                    "agent": agent,
                    "dependencies": [f"step_{len(steps)-1}"] if steps else [],
                    "reasoning": f"Tarea requiere especialización de {agent}"
                })
                break
        
        # Paso 5: Sintetizar resultados
        steps.append({
            "description": "Sintetizar toda la información recopilada",
            "action_type": ActionType.SYNTHESIZE,
            "dependencies": [f"step_{len(steps)-1}"] if steps else [],
            "reasoning": "Combinar todos los resultados obtenidos"
        })
        
        # Paso 6: Generar respuesta final
        steps.append({
            "description": "Generar respuesta coherente para el usuario",
            "action_type": ActionType.RESPOND,
            "dependencies": [f"step_{len(steps)-1}"],
            "reasoning": "Formular respuesta final"
        })
        
        return steps


class ChainOfThoughtPlanner:
    """
    Planificador Chain of Thought (CoT)
    Descompone problemas en pasos lógicos de razonamiento
    """
    
    def __init__(self):
        self.thought_patterns = {
            "problem_solving": [
                "Identificar el problema principal",
                "Descomponer en sub-problemas",
                "Resolver cada sub-problema",
                "Integrar soluciones",
                "Verificar resultado"
            ],
            "analysis": [
                "Recopilar información relevante",
                "Identificar patrones y relaciones",
                "Evaluar desde múltiples perspectivas",
                "Extraer conclusiones",
                "Formular recomendaciones"
            ],
            "creative": [
                "Explorar el espacio de posibilidades",
                "Generar ideas diversas",
                "Evaluar viabilidad",
                "Refinar las mejores opciones",
                "Desarrollar solución final"
            ]
        }
    
    def create_thought_chain(self, query: str, pattern: str = "problem_solving") -> List[Dict]:
        """Crear cadena de pensamiento para una consulta"""
        thoughts = []
        template = self.thought_patterns.get(pattern, self.thought_patterns["problem_solving"])
        
        for i, thought_template in enumerate(template):
            thoughts.append({
                "step": i + 1,
                "thought": thought_template,
                "applied_to": query,
                "status": "pending"
            })
        
        return thoughts
    
    def generate_reasoning_prompt(self, query: str, context: str = "") -> str:
        """Generar prompt con instrucciones de razonamiento CoT"""
        prompt = f"""Piensa paso a paso para resolver esta consulta.

CONSULTA: {query}

{f"CONTEXTO: {context}" if context else ""}

Sigue estos pasos de razonamiento:

1. COMPRENSIÓN: ¿Qué se está pidiendo exactamente?
2. DESCOMPOSICIÓN: ¿Cuáles son los componentes del problema?
3. ANÁLISIS: ¿Qué información necesito y de dónde la obtengo?
4. RAZONAMIENTO: ¿Cómo conecto la información para llegar a una conclusión?
5. SÍNTESIS: ¿Cuál es la respuesta final integrada?

Muestra tu razonamiento en cada paso antes de dar la respuesta final."""
        
        return prompt


class PlanningEngine:
    """
    Motor de Planificación Unificado
    Combina ReACT y CoT para planificación óptima
    """
    
    def __init__(self):
        self.react_planner = ReACTPlanner()
        self.cot_planner = ChainOfThoughtPlanner()
        self.active_plans: Dict[str, ExecutionPlan] = {}
    
    def create_plan(self, query: str, context: Dict = None, 
                    use_cot: bool = True) -> ExecutionPlan:
        """Crear plan de ejecución combinando ReACT y CoT"""
        
        # Crear plan base con ReACT
        plan = self.react_planner.create_plan(query, context)
        
        # Enriquecer con razonamiento CoT si está habilitado
        if use_cot:
            thought_chain = self.cot_planner.create_thought_chain(query)
            plan.reasoning_trace.insert(0, "=== CHAIN OF THOUGHT ===")
            for thought in thought_chain:
                plan.reasoning_trace.append(
                    f"[CoT Step {thought['step']}] {thought['thought']}"
                )
        
        self.active_plans[plan.id] = plan
        return plan
    
    def execute_step(self, plan_id: str, step_id: str, 
                     result: Dict = None) -> Optional[PlanStep]:
        """Marcar paso como ejecutado y obtener siguiente"""
        plan = self.active_plans.get(plan_id)
        if not plan:
            return None
        
        step = plan.get_step(step_id)
        if step:
            step.status = PlanStatus.COMPLETED
            step.completed_at = datetime.now()
            if result:
                step.output_data = result
            
            plan.reasoning_trace.append(
                f"[OBSERVATION] Paso {step_id} completado: {step.description}"
            )
        
        return plan.get_next_step()
    
    def get_plan_status(self, plan_id: str) -> Dict:
        """Obtener estado actual del plan"""
        plan = self.active_plans.get(plan_id)
        if not plan:
            return {"error": "Plan not found"}
        
        completed = sum(1 for s in plan.steps if s.status == PlanStatus.COMPLETED)
        total = len(plan.steps)
        
        return {
            "plan_id": plan_id,
            "query": plan.query,
            "progress": f"{completed}/{total}",
            "percentage": (completed / total * 100) if total > 0 else 0,
            "current_step": plan.get_next_step().to_dict() if plan.get_next_step() else None,
            "is_complete": plan.is_complete(),
            "reasoning_trace": plan.reasoning_trace
        }
    
    def get_cot_prompt(self, query: str, context: str = "") -> str:
        """Obtener prompt con instrucciones CoT"""
        return self.cot_planner.generate_reasoning_prompt(query, context)
