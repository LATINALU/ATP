"""
Analysis Agent - ATP v0.6.1
Analista Experto en Descomposición de Problemas

Agente especializado en análisis profundo, descomposición de sistemas complejos,
identificación de patrones y relaciones causales.

Capacidades únicas:
- Descomposición de problemas complejos
- Análisis de sistemas y subsistemas
- Identificación de patrones y estructuras
- Análisis de relaciones causales
- Modelado de sistemas
- Análisis de impacto y dependencias
"""
from typing import Dict, Any, Optional, List
from app.agents.base_agent import BaseAgent
from app.a2a_protocol import AgentCapability


class AnalysisAgent(BaseAgent):
    """
    Agente Analista Experto
    
    Supercomputadora especializada en descomponer la complejidad y revelar
    estructura, patrones y relaciones subyacentes.
    
    Expertise:
    - Análisis de sistemas complejos
    - Descomposición estructurada
    - Identificación de patrones
    - Análisis causal
    - Modelado conceptual
    - Análisis de dependencias
    """
    
    def __init__(self, model: str = None, api_config: Dict[str, Any] = None):
        super().__init__(
            agent_id="analysis_expert_001",
            name="Analysis Expert",
            primary_capability=AgentCapability.ANALYSIS,
            secondary_capabilities=[
                AgentCapability.REASONING,
                AgentCapability.SYSTEM_ARCHITECTURE
            ],
            specialization="Complex Systems Analysis & Problem Decomposition",
            description="""
            Analista experto en descomposición de problemas complejos. Especializado
            en revelar estructura, identificar patrones y analizar relaciones causales
            en sistemas de cualquier complejidad.
            """,
            backstory="""
            Soy el Agente de Análisis Profundo, especializado en diseccionar la complejidad
            para revelar estructura y significado oculto.
            
            Mi expertise abarca:
            - Análisis de sistemas complejos (Systems Thinking,
            model=model,
            api_config=api_config
            - Descomposición estructurada (MECE framework)
            - Análisis de causa raíz (5 Whys, Ishikawa)
            - Identificación de patrones y arquetipos
            - Modelado conceptual y diagramación
            - Análisis de impacto y dependencias
            
            Aplico múltiples frameworks analíticos:
            - MECE (Mutually Exclusive, Collectively Exhaustive)
            - 5 Whys para análisis causal
            - Diagrama de Ishikawa (espina de pescado)
            - Análisis SWOT
            - Análisis de Pareto (80/20)
            - Análisis de árbol de decisión
            - Análisis de sistemas dinámicos
            
            Mi fortaleza es tomar situaciones complejas y opacas, y transformarlas
            en estructuras claras y comprensibles que revelan insights accionables.
            """,
            model_name="gpt-4",
            temperature=0.3,
            max_tokens=4000
        )
        
        self.analysis_frameworks = [
            "mece", "five_whys", "ishikawa", "swot", "pareto",
            "decision_tree", "systems_thinking", "root_cause"
        ]
        
        self.decomposition_methods = [
            "hierarchical", "functional", "temporal", "spatial",
            "causal", "component_based"
        ]
    
    def get_system_prompt(self) -> str:
        """System prompt especializado para análisis"""
        return """Eres el Agente Analista Experto, una supercomputadora especializada
en descomponer la complejidad y revelar estructura, patrones y relaciones subyacentes.

TU MISIÓN:
Analizar situaciones complejas de manera sistemática, descomponiendo problemas
en componentes manejables e identificando patrones, relaciones y causas raíz.

CAPACIDADES ÚNICAS:

1. DESCOMPOSICIÓN ESTRUCTURADA:
   - MECE (Mutually Exclusive, Collectively Exhaustive)
   - Descomposición jerárquica
   - Análisis funcional
   - Separación de concerns
   - Identificación de componentes clave

2. ANÁLISIS CAUSAL:
   - 5 Whys para causa raíz
   - Diagrama de Ishikawa
   - Análisis de cadenas causales
   - Identificación de factores contribuyentes
   - Distinción entre correlación y causalidad

3. IDENTIFICACIÓN DE PATRONES:
   - Patrones estructurales
   - Patrones de comportamiento
   - Arquetipos de sistemas
   - Tendencias y ciclos
   - Anomalías y outliers

4. ANÁLISIS DE SISTEMAS:
   - Pensamiento sistémico
   - Identificación de feedback loops
   - Análisis de dependencias
   - Puntos de apalancamiento
   - Efectos de segundo y tercer orden

5. MODELADO CONCEPTUAL:
   - Diagramas de flujo
   - Mapas conceptuales
   - Modelos mentales
   - Representaciones visuales
   - Abstracciones útiles

METODOLOGÍA DE TRABAJO:

Cuando recibas un problema o situación:

1. COMPRENSIÓN:
   - Entiende el problema en su totalidad
   - Identifica stakeholders y contexto
   - Clarifica objetivos del análisis
   - Define alcance y límites

2. DESCOMPOSICIÓN:
   - Divide en componentes lógicos
   - Aplica framework MECE
   - Identifica jerarquías
   - Mapea relaciones

3. ANÁLISIS PROFUNDO:
   - Examina cada componente
   - Identifica patrones
   - Analiza causas y efectos
   - Evalúa interdependencias

4. SÍNTESIS:
   - Integra hallazgos
   - Identifica insights clave
   - Construye modelo conceptual
   - Prioriza elementos

5. RECOMENDACIONES:
   - Sugiere áreas de enfoque
   - Identifica puntos de apalancamiento
   - Propone próximos pasos
   - Destaca riesgos y oportunidades

FORMATO DE RESPUESTA:

Estructura tus análisis así:

**PROBLEMA/SITUACIÓN:**
[Descripción clara del objeto de análisis]

**DESCOMPOSICIÓN:**
[Componentes principales identificados]
├─ Componente 1
│  ├─ Sub-componente 1.1
│  └─ Sub-componente 1.2
├─ Componente 2
...

**PATRONES IDENTIFICADOS:**
[Patrones estructurales y de comportamiento]

**ANÁLISIS CAUSAL:**
[Causas raíz y factores contribuyentes]

**RELACIONES Y DEPENDENCIAS:**
[Cómo los componentes se relacionan]

**INSIGHTS CLAVE:**
[Hallazgos principales del análisis]

**PUNTOS DE APALANCAMIENTO:**
[Áreas de mayor impacto potencial]

**RECOMENDACIONES:**
[Próximos pasos sugeridos]

PRINCIPIOS DE ANÁLISIS:
- Estructura sobre caos
- Claridad sobre complejidad
- Profundidad sobre superficialidad
- Evidencia sobre suposición
- Simplicidad sobre complicación

Un buen análisis no solo descompone, sino que revela insights
que no eran evidentes en la superficie."""

    async def process_task(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Procesa una tarea de análisis
        
        Args:
            task: Problema o situación a analizar
            context: Contexto (framework preferido, profundidad, etc.)
            
        Returns:
            Análisis completo con descomposición e insights
        """
        context = context or {}
        
        # Preparar contexto de memoria
        memory_context = self.get_memory_context(limit=5)
        
        # Determinar framework apropiado
        framework = context.get("framework", self._suggest_framework(task))
        
        # Construir prompt
        user_message = f"""
OBJETO DE ANÁLISIS: {task}

CONTEXTO:
{self._format_context(context)}

FRAMEWORK SUGERIDO: {framework}

MEMORIA RECIENTE:
{memory_context}

Por favor, realiza un análisis profundo y estructurado de esta situación.
"""
        
        # Llamar al LLM
        response = await self.call_llm(
            messages=[{"role": "user", "content": user_message}],
            temperature=0.3
        )
        
        # Extraer resultado
        result = {
            "analysis": response,
            "framework": framework,
            "confidence": 0.88,
            "agent": self.profile.name,
            "capability": self.profile.primary_capability.value
        }
        
        # Guardar en memoria
        self.add_to_memory({
            "subject": task[:100],
            "summary": response[:200],
            "framework": framework
        })
        
        return result
    
    def _format_context(self, context: Dict[str, Any]) -> str:
        """Formatea el contexto de análisis"""
        if not context:
            return "No hay contexto adicional."
        
        formatted = []
        
        if "focus" in context:
            formatted.append(f"Enfoque: {context['focus']}")
        
        if "depth" in context:
            formatted.append(f"Profundidad: {context['depth']}")
        
        if "stakeholders" in context:
            formatted.append(f"Stakeholders: {context['stakeholders']}")
        
        if "constraints" in context:
            formatted.append(f"Restricciones: {context['constraints']}")
        
        for key, value in context.items():
            if key not in ["focus", "depth", "stakeholders", "constraints", "framework"]:
                formatted.append(f"{key}: {value}")
        
        return "\n".join(formatted) if formatted else "No hay contexto adicional."
    
    def _suggest_framework(self, task: str) -> str:
        """Sugiere framework apropiado basado en la tarea"""
        task_lower = task.lower()
        
        # MECE para descomposición estructurada
        if any(word in task_lower for word in ["descomponer", "dividir", "componentes", "estructura"]):
            return "MECE Framework"
        
        # 5 Whys para causa raíz
        if any(word in task_lower for word in ["por qué", "causa", "raíz", "origen"]):
            return "5 Whys / Root Cause Analysis"
        
        # Ishikawa para problemas complejos
        if any(word in task_lower for word in ["problema", "fallo", "issue", "defecto"]):
            return "Ishikawa Diagram"
        
        # SWOT para análisis estratégico
        if any(word in task_lower for word in ["fortalezas", "debilidades", "estrategia", "competitivo"]):
            return "SWOT Analysis"
        
        # Systems Thinking para sistemas complejos
        if any(word in task_lower for word in ["sistema", "complejo", "interdependencias", "dinámico"]):
            return "Systems Thinking"
        
        # Pareto para priorización
        if any(word in task_lower for word in ["priorizar", "importante", "impacto", "80/20"]):
            return "Pareto Analysis"
        
        return "Comprehensive Analysis"
    
    async def root_cause_analysis(self, problem: str) -> Dict[str, Any]:
        """
        Realiza análisis de causa raíz
        
        Args:
            problem: Problema a analizar
            
        Returns:
            Análisis de causa raíz con 5 Whys
        """
        return await self.process_task(
            f"Realiza un análisis de causa raíz para: {problem}",
            context={"framework": "five_whys", "analysis_type": "root_cause"}
        )
    
    async def swot_analysis(self, subject: str) -> Dict[str, Any]:
        """
        Realiza análisis SWOT
        
        Args:
            subject: Sujeto del análisis SWOT
            
        Returns:
            Análisis SWOT completo
        """
        return await self.process_task(
            f"Realiza un análisis SWOT de: {subject}",
            context={"framework": "swot", "analysis_type": "strategic"}
        )
    
    async def identify_patterns(self, data: str) -> Dict[str, Any]:
        """
        Identifica patrones en datos o situaciones
        
        Args:
            data: Datos o descripción de situación
            
        Returns:
            Patrones identificados
        """
        return await self.process_task(
            f"Identifica patrones en: {data}",
            context={"analysis_type": "pattern_recognition"}
        )
    
    async def dependency_analysis(self, system: str) -> Dict[str, Any]:
        """
        Analiza dependencias en un sistema
        
        Args:
            system: Sistema a analizar
            
        Returns:
            Mapa de dependencias
        """
        return await self.process_task(
            f"Analiza las dependencias en: {system}",
            context={"analysis_type": "dependency_mapping"}
        )
