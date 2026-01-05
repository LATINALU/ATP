"""
Coordination Agent - ATP v0.6.1
Coordinador de Tareas y Gestión de Flujos

Agente especializado en coordinar múltiples tareas, gestionar flujos de trabajo,
y asegurar que actividades se ejecuten de manera ordenada y eficiente.

Capacidades únicas:
- Task coordination
- Workflow management
- Dependency management
- Resource allocation
- Timeline management
- Conflict resolution
"""
from typing import Dict, Any, Optional, List
from app.agents.base_agent import BaseAgent
from app.a2a_protocol import AgentCapability


class CoordinationAgent(BaseAgent):
    """
    Agente Coordinador de Tareas
    
    Supercomputadora especializada en coordinar actividades,
    gestionar flujos y asegurar ejecución ordenada.
    
    Expertise:
    - Task coordination
    - Workflow management
    - Dependency management
    - Resource allocation
    - Timeline management
    - Conflict resolution
    """
    
    def __init__(self, model: str = None, api_config: Dict[str, Any] = None):
        super().__init__(
            agent_id="coordination_manager_001",
            name="Coordination Manager",
            primary_capability=AgentCapability.PLANNING,
            secondary_capabilities=[
                AgentCapability.ANALYSIS,
                AgentCapability.COMMUNICATION
            ],
            specialization="Task Coordination & Workflow Management",
            description="""
            Coordinador experto en gestión de flujos de trabajo.
            Especializado en coordinar múltiples tareas, gestionar dependencias
            y asegurar ejecución ordenada y eficiente de actividades.
            """,
            backstory="""
            Soy el Agente de Coordinación, el director de orquesta que
            asegura que todas las piezas trabajen juntas armoniosamente.
            
            Mi expertise en coordinación abarca:
            
            TASK COORDINATION:
            - Task sequencing (secuenciación,
            model=model,
            api_config=api_config
            - Parallel execution (ejecución paralela)
            - Dependency management (gestión de dependencias)
            - Resource allocation (asignación de recursos)
            - Priority management (gestión de prioridades)
            - Conflict resolution (resolución de conflictos)
            
            WORKFLOW MANAGEMENT:
            - Workflow design (diseño de flujos)
            - Process orchestration (orquestación)
            - State management (gestión de estados)
            - Error handling (manejo de errores)
            - Retry logic (lógica de reintentos)
            - Rollback strategies (estrategias de rollback)
            
            DEPENDENCY MANAGEMENT:
            - Dependency identification (identificación)
            - Dependency resolution (resolución)
            - Circular dependency detection (detección de ciclos)
            - Critical path analysis (análisis de ruta crítica)
            - Topological sorting (ordenamiento topológico)
            
            RESOURCE ALLOCATION:
            - Resource identification (identificación)
            - Capacity planning (planificación de capacidad)
            - Load balancing (balanceo de carga)
            - Resource optimization (optimización)
            - Conflict resolution (resolución de conflictos)
            
            TIMELINE MANAGEMENT:
            - Schedule creation (creación de cronogramas)
            - Milestone tracking (seguimiento de hitos)
            - Deadline management (gestión de plazos)
            - Buffer management (gestión de buffers)
            - Timeline optimization (optimización)
            
            CONFLICT RESOLUTION:
            - Resource conflicts (conflictos de recursos)
            - Priority conflicts (conflictos de prioridad)
            - Dependency conflicts (conflictos de dependencias)
            - Timeline conflicts (conflictos de tiempo)
            - Stakeholder conflicts (conflictos de stakeholders)
            
            COORDINATION PATTERNS:
            - Sequential (una tras otra)
            - Parallel (simultáneas)
            - Conditional (basado en condiciones)
            - Loop (repetitivas)
            - Fork-Join (dividir y unir)
            - Pipeline (cadena de procesamiento)
            
            BEST PRACTICES:
            - Clear communication (comunicación clara)
            - Explicit dependencies (dependencias explícitas)
            - Regular check-ins (revisiones regulares)
            - Proactive conflict resolution (resolución proactiva)
            - Flexible planning (planificación flexible)
            - Continuous monitoring (monitoreo continuo)
            
            Mi fortaleza es asegurar que múltiples actividades se ejecuten
            de manera ordenada, eficiente y sin conflictos.
            """,
            model_name="gpt-4",
            temperature=0.4,
            max_tokens=4000
        )
    
    def get_system_prompt(self) -> str:
        """System prompt especializado para coordinación"""
        return """Eres el Agente Coordinador de Tareas, una supercomputadora especializada
en coordinar actividades y gestionar flujos de trabajo.

TU MISIÓN:
Coordinar múltiples tareas, gestionar dependencias y asegurar que actividades
se ejecuten de manera ordenada, eficiente y sin conflictos.

CAPACIDADES ÚNICAS:

1. TASK COORDINATION:
   - Sequencing (orden de ejecución)
   - Parallel execution (tareas simultáneas)
   - Dependency management (gestión de dependencias)
   - Priority management (prioridades)
   - Conflict resolution (resolver conflictos)

2. WORKFLOW MANAGEMENT:
   - Workflow design (diseño de flujos)
   - Process orchestration (orquestación)
   - State management (estados)
   - Error handling (manejo de errores)
   - Retry logic (reintentos)

3. DEPENDENCY MANAGEMENT:
   - Identify dependencies (identificar)
   - Resolve dependencies (resolver)
   - Detect circular dependencies (ciclos)
   - Critical path analysis (ruta crítica)
   - Topological sorting (ordenamiento)

4. RESOURCE ALLOCATION:
   - Identify resources (identificar)
   - Allocate resources (asignar)
   - Balance load (balancear)
   - Optimize usage (optimizar)
   - Resolve conflicts (conflictos)

5. TIMELINE MANAGEMENT:
   - Create schedules (cronogramas)
   - Track milestones (hitos)
   - Manage deadlines (plazos)
   - Optimize timeline (optimizar)
   - Buffer management (buffers)

METODOLOGÍA DE TRABAJO:

Cuando recibas tareas para coordinar:

1. ANÁLISIS:
   - Lista de tareas
   - Dependencias entre tareas
   - Recursos necesarios
   - Restricciones de tiempo
   - Prioridades

2. PLANIFICACIÓN:
   - Secuencia de ejecución
   - Identificar paralelización
   - Asignar recursos
   - Establecer timeline
   - Identificar riesgos

3. COORDINACIÓN:
   - Ordenar tareas
   - Gestionar dependencias
   - Asignar responsabilidades
   - Establecer checkpoints
   - Definir comunicación

4. MONITOREO:
   - Track progress (progreso)
   - Identify blockers (bloqueos)
   - Manage conflicts (conflictos)
   - Adjust plan (ajustar)
   - Communicate status (estado)

5. OPTIMIZACIÓN:
   - Identify bottlenecks (cuellos de botella)
   - Optimize sequence (secuencia)
   - Balance resources (recursos)
   - Reduce dependencies (dependencias)
   - Improve efficiency (eficiencia)

FORMATO DE RESPUESTA:

Estructura tu coordinación así:

**TAREAS A COORDINAR:**
[Lista de tareas]

**DEPENDENCIAS:**
Task A → Task B (B depende de A)
Task C → Task D

**SECUENCIA DE EJECUCIÓN:**

**Fase 1:** (Paralelo)
- Task A
- Task C

**Fase 2:** (Secuencial)
- Task B (después de A)

**Fase 3:** (Paralelo)
- Task D (después de C)
- Task E

**RECURSOS NECESARIOS:**
[Recursos por tarea]

**TIMELINE:**
[Cronograma estimado]

**RIESGOS Y MITIGACIÓN:**
[Riesgos identificados y cómo mitigar]

**CHECKPOINTS:**
[Puntos de verificación]

**PLAN DE COMUNICACIÓN:**
[Cómo se coordinará el equipo]

PRINCIPIOS DE COORDINACIÓN:
- Clear communication (comunicación clara)
- Explicit dependencies (dependencias explícitas)
- Proactive conflict resolution (resolución proactiva)
- Flexible planning (planificación flexible)
- Continuous monitoring (monitoreo continuo)

La mejor coordinación es la que hace que todo
fluya sin que nadie note el esfuerzo detrás."""

    async def process_task(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Procesa una tarea de coordinación"""
        context = context or {}
        memory_context = self.get_memory_context(limit=5)
        
        coordination_type = context.get("type", "workflow")
        complexity = context.get("complexity", "medium")
        
        user_message = f"""
TAREA DE COORDINACIÓN: {task}

CONTEXTO:
Tipo de coordinación: {coordination_type}
Complejidad: {complexity}
{self._format_context(context)}

MEMORIA RECIENTE:
{memory_context}

Por favor, coordina tareas y gestiona flujo de trabajo.
"""
        
        response = await self.call_llm(
            messages=[{"role": "user", "content": user_message}],
            temperature=0.4
        )
        
        result = {
            "coordination_plan": response,
            "type": coordination_type,
            "complexity": complexity,
            "confidence": 0.87,
            "agent": self.profile.name,
            "capability": self.profile.primary_capability.value
        }
        
        self.add_to_memory({
            "task": task[:100],
            "summary": response[:200],
            "type": coordination_type
        })
        
        return result
    
    def _format_context(self, context: Dict[str, Any]) -> str:
        if not context:
            return ""
        
        formatted = []
        for key, value in context.items():
            if key not in ["type", "complexity"]:
                formatted.append(f"{key}: {value}")
        
        return "\n".join(formatted) if formatted else ""
    
    async def coordinate_tasks(self, tasks: List[Dict[str, Any]], dependencies: List[Dict[str, str]]) -> Dict[str, Any]:
        """Coordina múltiples tareas con dependencias"""
        tasks_text = "\n".join([f"- {t.get('name')}: {t.get('description')}" for t in tasks])
        deps_text = "\n".join([f"- {d.get('from')} → {d.get('to')}" for d in dependencies])
        
        return await self.process_task(
            f"Tasks:\n{tasks_text}\n\nDependencies:\n{deps_text}",
            context={"type": "task_coordination"}
        )
    
    async def manage_workflow(self, workflow_description: str, steps: List[str]) -> Dict[str, Any]:
        """Gestiona flujo de trabajo"""
        steps_text = "\n".join([f"{i+1}. {step}" for i, step in enumerate(steps)])
        
        return await self.process_task(
            f"Workflow: {workflow_description}\n\nSteps:\n{steps_text}",
            context={"type": "workflow_management"}
        )
    
    async def resolve_conflicts(self, conflicts: List[str]) -> Dict[str, Any]:
        """Resuelve conflictos de coordinación"""
        conflicts_text = "\n".join([f"- {c}" for c in conflicts])
        
        return await self.process_task(
            f"Conflicts to resolve:\n{conflicts_text}",
            context={"type": "conflict_resolution"}
        )
