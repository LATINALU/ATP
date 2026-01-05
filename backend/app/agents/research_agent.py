"""
Research Agent - ATP v0.6.1
Investigador Senior y Analista de Información

Agente especializado en investigación exhaustiva con rigor académico,
análisis de fuentes, y síntesis de información compleja.

Capacidades únicas:
- Investigación profunda multi-fuente
- Evaluación crítica de fuentes
- Metodología de investigación científica
- Análisis de literatura académica
- Síntesis de hallazgos
- Identificación de gaps de conocimiento
"""
from typing import Dict, Any, Optional, List
from app.agents.base_agent import BaseAgent
from app.a2a_protocol import AgentCapability


class ResearchAgent(BaseAgent):
    """
    Agente Investigador Senior
    
    Supercomputadora especializada en investigación exhaustiva y análisis de información.
    Aplica metodología científica para explorar temas en profundidad.
    
    Expertise:
    - Metodología de investigación
    - Análisis de fuentes primarias y secundarias
    - Evaluación de credibilidad
    - Síntesis de literatura
    - Identificación de tendencias
    - Meta-análisis
    """
    
    def __init__(self, model: str = None, api_config: Dict[str, Any] = None):
        super().__init__(
            agent_id="research_senior_001",
            name="Research Senior",
            primary_capability=AgentCapability.SCIENTIFIC,
            secondary_capabilities=[
                AgentCapability.ANALYSIS,
                AgentCapability.CRITICAL_THINKING
            ],
            specialization="Academic Research & Information Analysis",
            description="""
            Investigador senior con expertise en metodología científica y análisis
            de información. Especializado en investigación exhaustiva, evaluación
            crítica de fuentes y síntesis de hallazgos complejos.
            """,
            backstory="""
            Soy el Agente de Investigación Profunda, con la curiosidad insaciable de un
            científico y la meticulosidad de un detective académico.
            
            Mi formación abarca:
            - Metodología de investigación científica
            - Análisis crítico de fuentes
            - Revisión sistemática de literatura
            - Meta-análisis y síntesis de evidencia
            - Identificación de sesgos y limitaciones
            
            Aplico el método científico rigurosamente:
            1. Formular preguntas de investigación claras
            2. Diseñar estrategia de búsqueda
            3. Evaluar calidad de fuentes
            4. Analizar evidencia sistemáticamente
            5. Sintetizar hallazgos
            6. Identificar gaps de conocimiento
            
            Mi fortaleza es transformar preguntas vagas en investigaciones estructuradas
            que producen insights accionables basados en evidencia sólida.
            """,
            model_name="gpt-4",
            temperature=0.4,
            max_tokens=4000,
            model=model,
            api_config=api_config
        )
        
        self.research_methodologies = [
            "systematic_review", "meta_analysis", "case_study",
            "comparative_analysis", "longitudinal_study", "exploratory"
        ]
        
        self.source_types = [
            "academic_papers", "books", "reports", "datasets",
            "expert_opinions", "primary_sources", "secondary_sources"
        ]
    
    def get_system_prompt(self) -> str:
        """System prompt especializado para investigación"""
        return """Eres el Agente Investigador Senior, una supercomputadora especializada
en investigación exhaustiva y análisis de información con rigor académico.

TU MISIÓN:
Investigar cualquier tema en profundidad, evaluando críticamente fuentes,
sintetizando hallazgos y produciendo insights basados en evidencia sólida.

CAPACIDADES ÚNICAS:

1. METODOLOGÍA DE INVESTIGACIÓN:
   - Diseño de estrategias de búsqueda
   - Revisión sistemática de literatura
   - Meta-análisis de estudios
   - Análisis comparativo
   - Estudios de caso
   - Investigación exploratoria

2. EVALUACIÓN DE FUENTES:
   - Credibilidad y autoridad
   - Actualidad y relevancia
   - Objetividad y sesgo
   - Cobertura y profundidad
   - Verificación cruzada
   - Jerarquía de evidencia

3. ANÁLISIS DE INFORMACIÓN:
   - Identificación de patrones
   - Detección de contradicciones
   - Evaluación de consenso científico
   - Análisis de limitaciones
   - Identificación de gaps
   - Síntesis de hallazgos

4. PENSAMIENTO CRÍTICO:
   - Evaluación de metodología
   - Identificación de sesgos
   - Análisis de validez
   - Consideración de alternativas
   - Evaluación de implicaciones

METODOLOGÍA DE TRABAJO:

Cuando recibas una pregunta de investigación:

1. CLARIFICACIÓN:
   - Define alcance de la investigación
   - Identifica preguntas específicas
   - Establece criterios de éxito
   - Determina profundidad necesaria

2. ESTRATEGIA:
   - Diseña plan de búsqueda
   - Identifica fuentes relevantes
   - Establece criterios de inclusión/exclusión
   - Define metodología apropiada

3. RECOLECCIÓN:
   - Busca información sistemáticamente
   - Evalúa calidad de fuentes
   - Documenta hallazgos
   - Identifica gaps

4. ANÁLISIS:
   - Sintetiza información
   - Identifica patrones y tendencias
   - Evalúa consenso y controversias
   - Analiza limitaciones

5. SÍNTESIS:
   - Integra hallazgos
   - Responde preguntas de investigación
   - Identifica implicaciones
   - Sugiere áreas para investigación futura

FORMATO DE RESPUESTA:

Estructura tus investigaciones así:

**PREGUNTA DE INVESTIGACIÓN:**
[Pregunta clara y específica]

**METODOLOGÍA:**
[Enfoque y estrategia de investigación]

**HALLAZGOS PRINCIPALES:**
[Síntesis de información clave]

**ANÁLISIS CRÍTICO:**
[Evaluación de evidencia y limitaciones]

**CONSENSO Y CONTROVERSIAS:**
[Áreas de acuerdo y desacuerdo]

**CONCLUSIONES:**
[Respuestas basadas en evidencia]

**GAPS DE CONOCIMIENTO:**
[Áreas que requieren más investigación]

**FUENTES CLAVE:**
[Referencias principales consultadas]

PRINCIPIOS DE INVESTIGACIÓN:
- Rigor sobre rapidez
- Evidencia sobre opinión
- Objetividad sobre sesgo
- Profundidad sobre superficialidad
- Transparencia sobre opacidad

Eres un investigador, no un oráculo. Tu poder está en la metodología
rigurosa y la evaluación crítica de evidencia."""

    async def process_task(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Procesa una tarea de investigación
        
        Args:
            task: Pregunta o tema de investigación
            context: Contexto (profundidad, fuentes preferidas, etc.)
            
        Returns:
            Investigación completa con hallazgos y análisis
        """
        context = context or {}
        
        # Preparar contexto de memoria
        memory_context = self.get_memory_context(limit=5)
        
        # Determinar metodología apropiada
        methodology = context.get("methodology", self._suggest_methodology(task))
        depth = context.get("depth", "comprehensive")
        
        # Construir prompt
        user_message = f"""
PREGUNTA DE INVESTIGACIÓN: {task}

CONTEXTO:
{self._format_context(context)}

METODOLOGÍA SUGERIDA: {methodology}
PROFUNDIDAD: {depth}

MEMORIA RECIENTE:
{memory_context}

Por favor, realiza una investigación exhaustiva sobre este tema.
"""
        
        # Llamar al LLM
        response = await self.call_llm(
            messages=[{"role": "user", "content": user_message}],
            temperature=0.4
        )
        
        # Extraer resultado
        result = {
            "research": response,
            "methodology": methodology,
            "depth": depth,
            "confidence": 0.85,
            "agent": self.profile.name,
            "capability": self.profile.primary_capability.value
        }
        
        # Guardar en memoria
        self.add_to_memory({
            "question": task[:100],
            "summary": response[:200],
            "methodology": methodology
        })
        
        return result
    
    def _format_context(self, context: Dict[str, Any]) -> str:
        """Formatea el contexto de investigación"""
        if not context:
            return "No hay contexto adicional."
        
        formatted = []
        
        if "depth" in context:
            formatted.append(f"Profundidad: {context['depth']}")
        
        if "sources" in context:
            formatted.append(f"Fuentes preferidas: {context['sources']}")
        
        if "time_period" in context:
            formatted.append(f"Período de tiempo: {context['time_period']}")
        
        if "focus_areas" in context:
            formatted.append(f"Áreas de enfoque: {context['focus_areas']}")
        
        for key, value in context.items():
            if key not in ["depth", "sources", "time_period", "focus_areas", "methodology"]:
                formatted.append(f"{key}: {value}")
        
        return "\n".join(formatted) if formatted else "No hay contexto adicional."
    
    def _suggest_methodology(self, task: str) -> str:
        """Sugiere metodología apropiada basada en la tarea"""
        task_lower = task.lower()
        
        # Revisión sistemática para temas amplios
        if any(word in task_lower for word in ["estado del arte", "revisión", "panorama", "overview"]):
            return "Systematic Review"
        
        # Meta-análisis para estudios cuantitativos
        if any(word in task_lower for word in ["efectividad", "impacto", "resultados", "evidencia"]):
            return "Meta-Analysis"
        
        # Estudio de caso para situaciones específicas
        if any(word in task_lower for word in ["caso", "ejemplo", "específico", "particular"]):
            return "Case Study"
        
        # Análisis comparativo
        if any(word in task_lower for word in ["comparar", "diferencias", "vs", "versus"]):
            return "Comparative Analysis"
        
        # Exploratoria para temas nuevos
        if any(word in task_lower for word in ["explorar", "nuevo", "emergente", "tendencias"]):
            return "Exploratory Research"
        
        return "Comprehensive Research"
    
    async def systematic_review(self, topic: str, criteria: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Realiza una revisión sistemática de literatura
        
        Args:
            topic: Tema de revisión
            criteria: Criterios de inclusión/exclusión
            
        Returns:
            Revisión sistemática completa
        """
        context = {
            "methodology": "systematic_review",
            "depth": "comprehensive"
        }
        
        if criteria:
            context["criteria"] = criteria
        
        return await self.process_task(topic, context=context)
    
    async def evaluate_sources(self, sources: List[str]) -> Dict[str, Any]:
        """
        Evalúa la credibilidad de fuentes
        
        Args:
            sources: Lista de fuentes a evaluar
            
        Returns:
            Evaluación de cada fuente
        """
        sources_text = "\n".join([f"- {s}" for s in sources])
        
        return await self.process_task(
            f"Evalúa la credibilidad y calidad de estas fuentes:\n{sources_text}",
            context={"analysis_type": "source_evaluation"}
        )
    
    async def identify_gaps(self, topic: str, current_knowledge: str) -> Dict[str, Any]:
        """
        Identifica gaps de conocimiento
        
        Args:
            topic: Tema de investigación
            current_knowledge: Conocimiento actual
            
        Returns:
            Gaps identificados y áreas para investigación futura
        """
        return await self.process_task(
            f"Identifica gaps de conocimiento en: {topic}\n\nConocimiento actual:\n{current_knowledge}",
            context={"analysis_type": "gap_analysis"}
        )
