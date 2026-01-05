"""
Planning Agent - ATP v0.6.1
Estratega de Planificación y Gestión de Proyectos

Agente especializado en crear planes de acción detallados, realistas y ejecutables.
Experto en descomposición de objetivos, gestión de recursos y optimización de rutas críticas.

Capacidades únicas:
- Planificación estratégica multi-nivel
- Análisis de dependencias y rutas críticas
- Gestión de recursos y restricciones
- Optimización de cronogramas
- Análisis de riesgos y contingencias
- Metodologías ágiles y tradicionales
"""
from typing import Dict, Any, Optional, List
from app.agents.base_agent import BaseAgent
from app.a2a_protocol import AgentCapability


class PlanningAgent(BaseAgent):
    """
    Agente Estratega de Planificación
    
    Supercomputadora especializada en transformar objetivos complejos en planes
    de acción ejecutables. Aplica metodologías de gestión de proyectos de clase mundial.
    
    Expertise:
    - Planificación estratégica y táctica
    - Descomposición de objetivos (WBS)
    - Análisis de camino crítico (CPM)
    - Gestión de recursos y capacidades
    - Análisis de riesgos y mitigación
    - Metodologías: Agile, Waterfall, Hybrid
    """
    
    def __init__(self, model: str = None, api_config: Dict[str, Any] = None):
        super().__init__(
            agent_id="planning_strategist_001",
            name="Planning Strategist",
            primary_capability=AgentCapability.PLANNING,
            secondary_capabilities=[
                AgentCapability.ANALYSIS,
                AgentCapability.OPTIMIZATION
            ],
            specialization="Strategic Planning & Project Management",
            description="""
            Estratega de planificación con expertise en metodologías de gestión de proyectos.
            Especializado en crear planes detallados, realistas y ejecutables que consideran
            recursos, restricciones y riesgos.
            """,
            backstory="""
            Soy el Agente de Planificación Estratégica, formado en las mejores prácticas
            de gestión de proyectos desde PMI hasta metodologías ágiles modernas.
            
            Mi expertise abarca:
            - Planificación estratégica a largo plazo
            - Planificación táctica a medio plazo
            - Planificación operativa a corto plazo
            
            Aplico múltiples frameworks según el contexto:
            - SMART goals para objetivos claros
            - OKRs para alineación organizacional
            - WBS para descomposición de trabajo
            - Gantt para visualización temporal
            - Kanban para flujo continuo
            - Scrum para iteraciones ágiles
            
            Mi fortaleza es transformar visiones ambiciosas en pasos concretos y alcanzables,
            considerando siempre recursos disponibles, restricciones reales y riesgos potenciales.
            """,
            model_name="gpt-4",
            temperature=0.4,
            max_tokens=4000,
            model=model,
            api_config=api_config
        )
        
        self.planning_methodologies = [
            "waterfall", "agile", "scrum", "kanban", "lean",
            "prince2", "pmbok", "hybrid"
        ]
        
        self.planning_tools = [
            "wbs", "gantt", "pert", "cpm", "risk_matrix",
            "resource_leveling", "earned_value"
        ]
    
    def get_system_prompt(self) -> str:
        """System prompt especializado para planificación estratégica"""
        return """Eres el Agente Estratega de Planificación, una supercomputadora especializada
en transformar objetivos complejos en planes de acción ejecutables.

TU MISIÓN:
Crear planes detallados, realistas y ejecutables que guíen desde la visión inicial
hasta la implementación exitosa, considerando recursos, restricciones y riesgos.

CAPACIDADES ÚNICAS:

1. PLANIFICACIÓN MULTI-NIVEL:
   - Estratégica: Visión a largo plazo (1-5 años)
   - Táctica: Objetivos a medio plazo (3-12 meses)
   - Operativa: Acciones a corto plazo (días-semanas)
   
2. DESCOMPOSICIÓN DE OBJETIVOS:
   - Work Breakdown Structure (WBS)
   - Identificación de entregables
   - Definición de hitos clave
   - Establecimiento de criterios de éxito
   
3. ANÁLISIS DE DEPENDENCIAS:
   - Identificar relaciones entre tareas
   - Determinar ruta crítica
   - Optimizar secuencia de ejecución
   - Identificar paralelización posible
   
4. GESTIÓN DE RECURSOS:
   - Estimación de esfuerzo y duración
   - Asignación de recursos
   - Nivelación de carga
   - Identificación de cuellos de botella
   
5. ANÁLISIS DE RIESGOS:
   - Identificar riesgos potenciales
   - Evaluar probabilidad e impacto
   - Desarrollar estrategias de mitigación
   - Crear planes de contingencia

METODOLOGÍA DE TRABAJO:

Cuando recibas un objetivo o proyecto:

1. COMPRENSIÓN:
   - Clarificar el objetivo final
   - Identificar stakeholders
   - Entender restricciones y recursos
   - Definir criterios de éxito

2. DESCOMPOSICIÓN:
   - Dividir en fases principales
   - Descomponer en tareas específicas
   - Identificar entregables por fase
   - Establecer hitos de control

3. SECUENCIACIÓN:
   - Determinar orden lógico
   - Identificar dependencias
   - Calcular ruta crítica
   - Optimizar paralelización

4. ESTIMACIÓN:
   - Estimar duración de tareas
   - Calcular esfuerzo requerido
   - Identificar recursos necesarios
   - Considerar buffers realistas

5. VALIDACIÓN:
   - Verificar viabilidad
   - Revisar restricciones
   - Evaluar riesgos
   - Ajustar según feedback

FORMATO DE RESPUESTA:

Estructura tus planes así:

**RESUMEN EJECUTIVO:**
[Objetivo, alcance, duración estimada]

**FASES DEL PROYECTO:**
[Fases principales con objetivos]

**PLAN DETALLADO:**
Fase 1: [Nombre]
├─ Tarea 1.1: [Descripción]
│  ├─ Duración: [X días/horas]
│  ├─ Recursos: [Necesarios]
│  └─ Dependencias: [Tareas previas]
├─ Tarea 1.2: [Descripción]
...

**HITOS CLAVE:**
[Puntos de control importantes]

**RUTA CRÍTICA:**
[Secuencia de tareas críticas]

**RECURSOS NECESARIOS:**
[Recursos humanos, técnicos, materiales]

**RIESGOS Y MITIGACIÓN:**
[Riesgos identificados y planes de contingencia]

**CRONOGRAMA:**
[Timeline con fechas estimadas]

PRINCIPIOS DE PLANIFICACIÓN:
- Realismo sobre optimismo
- Claridad sobre complejidad
- Flexibilidad sobre rigidez
- Medible sobre abstracto
- Accionable sobre teórico

Un buen plan es como un mapa: te muestra el camino, pero permite ajustes
cuando encuentras obstáculos inesperados."""

    async def process_task(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Procesa una tarea de planificación
        
        Args:
            task: Objetivo o proyecto a planificar
            context: Contexto (recursos, restricciones, metodología preferida)
            
        Returns:
            Plan detallado y ejecutable
        """
        context = context or {}
        
        # Preparar contexto de memoria
        memory_context = self.get_memory_context(limit=5)
        
        # Determinar metodología apropiada
        methodology = context.get("methodology", self._suggest_methodology(task))
        
        # Construir prompt
        user_message = f"""
OBJETIVO/PROYECTO: {task}

CONTEXTO:
{self._format_context(context)}

METODOLOGÍA SUGERIDA: {methodology}

MEMORIA RECIENTE:
{memory_context}

Por favor, crea un plan detallado, realista y ejecutable para este objetivo.
"""
        
        # Llamar al LLM
        response = await self.call_llm(
            messages=[{"role": "user", "content": user_message}],
            temperature=0.4
        )
        
        # Extraer resultado
        result = {
            "plan": response,
            "methodology": methodology,
            "confidence": 0.88,
            "agent": self.profile.name,
            "capability": self.profile.primary_capability.value,
            "estimated_complexity": self._estimate_complexity(task)
        }
        
        # Guardar en memoria
        self.add_to_memory({
            "objective": task[:100],
            "summary": response[:200],
            "methodology": methodology
        })
        
        return result
    
    def _format_context(self, context: Dict[str, Any]) -> str:
        """Formatea el contexto de planificación"""
        if not context:
            return "No hay contexto adicional."
        
        formatted = []
        
        # Recursos
        if "resources" in context:
            formatted.append(f"Recursos disponibles: {context['resources']}")
        
        # Restricciones
        if "constraints" in context:
            formatted.append(f"Restricciones: {context['constraints']}")
        
        # Timeline
        if "deadline" in context:
            formatted.append(f"Fecha límite: {context['deadline']}")
        
        # Prioridades
        if "priorities" in context:
            formatted.append(f"Prioridades: {context['priorities']}")
        
        # Otros
        for key, value in context.items():
            if key not in ["resources", "constraints", "deadline", "priorities", "methodology"]:
                formatted.append(f"{key}: {value}")
        
        return "\n".join(formatted) if formatted else "No hay contexto adicional."
    
    def _suggest_methodology(self, task: str) -> str:
        """Sugiere metodología apropiada basada en la tarea"""
        task_lower = task.lower()
        
        # Agile/Scrum para desarrollo iterativo
        if any(word in task_lower for word in ["desarrollo", "software", "app", "iterativo", "mvp"]):
            return "Agile/Scrum"
        
        # Waterfall para proyectos con requisitos claros
        if any(word in task_lower for word in ["construcción", "manufactura", "secuencial", "fases"]):
            return "Waterfall"
        
        # Kanban para flujo continuo
        if any(word in task_lower for word in ["mantenimiento", "soporte", "continuo", "flujo"]):
            return "Kanban"
        
        # Lean para optimización
        if any(word in task_lower for word in ["optimizar", "eficiencia", "reducir", "lean"]):
            return "Lean"
        
        # Hybrid por defecto
        return "Hybrid (Agile + Waterfall)"
    
    def _estimate_complexity(self, task: str) -> str:
        """Estima la complejidad del proyecto"""
        task_length = len(task)
        task_lower = task.lower()
        
        complexity_indicators = [
            "múltiple", "complejo", "integración", "sistema", "arquitectura",
            "escalable", "distribuido", "varios", "muchos"
        ]
        
        complexity_score = sum(1 for indicator in complexity_indicators if indicator in task_lower)
        
        if complexity_score >= 3 or task_length > 500:
            return "High"
        elif complexity_score >= 1 or task_length > 200:
            return "Medium"
        else:
            return "Low"
    
    async def create_wbs(self, objective: str, levels: int = 3) -> Dict[str, Any]:
        """
        Crea una Work Breakdown Structure
        
        Args:
            objective: Objetivo principal
            levels: Niveles de descomposición
            
        Returns:
            WBS estructurada
        """
        return await self.process_task(
            f"Crea una Work Breakdown Structure de {levels} niveles para: {objective}",
            context={"analysis_type": "wbs", "levels": levels}
        )
    
    async def identify_critical_path(self, tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Identifica la ruta crítica de un conjunto de tareas
        
        Args:
            tasks: Lista de tareas con duraciones y dependencias
            
        Returns:
            Ruta crítica identificada
        """
        tasks_description = "\n".join([
            f"- {t.get('name')}: {t.get('duration')} días, depende de: {t.get('dependencies', 'ninguna')}"
            for t in tasks
        ])
        
        return await self.process_task(
            f"Identifica la ruta crítica de estas tareas:\n{tasks_description}",
            context={"analysis_type": "critical_path"}
        )
    
    async def analyze_risks(self, project_description: str) -> Dict[str, Any]:
        """
        Analiza riesgos de un proyecto
        
        Args:
            project_description: Descripción del proyecto
            
        Returns:
            Análisis de riesgos con mitigación
        """
        return await self.process_task(
            f"Analiza los riesgos de este proyecto: {project_description}",
            context={"analysis_type": "risk_analysis"}
        )
