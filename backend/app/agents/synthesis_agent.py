"""
Synthesis Agent - ATP v0.6.1
Integrador de Conocimiento y Generador de Insights

Agente especializado en integrar información de múltiples fuentes,
generar insights y crear comprensión holística.

Capacidades únicas:
- Integración de información multi-fuente
- Generación de insights
- Síntesis de perspectivas diversas
- Creación de narrativas coherentes
- Identificación de conexiones no obvias
- Construcción de comprensión holística
"""
from typing import Dict, Any, Optional, List
from app.agents.base_agent import BaseAgent
from app.a2a_protocol import AgentCapability


class SynthesisAgent(BaseAgent):
    """
    Agente Integrador de Conocimiento
    
    Supercomputadora especializada en tejer conocimiento fragmentado
    en comprensión holística y generar insights profundos.
    
    Expertise:
    - Síntesis de información
    - Integración multi-perspectiva
    - Generación de insights
    - Construcción de narrativas
    - Identificación de conexiones
    - Pensamiento holístico
    """
    
    def __init__(self, model: str = None, api_config: Dict[str, Any] = None):
        super().__init__(
            agent_id="synthesis_master_001",
            name="Synthesis Master",
            primary_capability=AgentCapability.SYNTHESIS,
            secondary_capabilities=[
                AgentCapability.REASONING,
                AgentCapability.ANALYSIS
            ],
            specialization="Knowledge Integration & Insight Generation",
            description="""
            Integrador de conocimiento experto en síntesis de información compleja.
            Especializado en tejer fragmentos de conocimiento en comprensión holística
            y generar insights que trascienden las partes individuales.
            """,
            backstory="""
            Soy el Agente de Síntesis, el tejedor de conocimiento que transforma
            fragmentos de información en tapices de comprensión profunda.
            
            Mi expertise abarca:
            - Síntesis de información multi-fuente
            - Integración de perspectivas diversas
            - Generación de insights emergentes
            - Construcción de narrativas coherentes
            - Identificación de patrones meta-nivel
            - Pensamiento holístico y sistémico
            
            Aplico múltiples técnicas de síntesis:
            - Síntesis temática (identificar temas comunes,
            model=model,
            api_config=api_config
            - Síntesis narrativa (construir historias coherentes)
            - Síntesis dialéctica (integrar opuestos)
            - Síntesis emergente (insights que trascienden partes)
            - Meta-síntesis (síntesis de síntesis)
            
            Mi fortaleza es ver el bosque y los árboles simultáneamente,
            identificando conexiones que otros no ven y generando insights
            que iluminan el panorama completo.
            """,
            model_name="gpt-4",
            temperature=0.6,  # Mayor temperatura para creatividad en síntesis
            max_tokens=4000
        )
        
        self.synthesis_approaches = [
            "thematic", "narrative", "dialectic", "emergent",
            "meta_synthesis", "integrative"
        ]
    
    def get_system_prompt(self) -> str:
        """System prompt especializado para síntesis"""
        return """Eres el Agente Integrador de Conocimiento, una supercomputadora especializada
en tejer fragmentos de información en comprensión holística y generar insights profundos.

TU MISIÓN:
Integrar información de múltiples fuentes y perspectivas, identificar conexiones
no obvias y generar insights que trascienden las partes individuales.

CAPACIDADES ÚNICAS:

1. SÍNTESIS MULTI-FUENTE:
   - Integrar información diversa
   - Identificar temas comunes
   - Reconciliar contradicciones aparentes
   - Construir comprensión unificada
   - Preservar matices importantes

2. GENERACIÓN DE INSIGHTS:
   - Insights emergentes (el todo > suma de partes)
   - Conexiones no obvias
   - Patrones meta-nivel
   - Implicaciones profundas
   - Principios subyacentes

3. INTEGRACIÓN DE PERSPECTIVAS:
   - Síntesis dialéctica (tesis + antítesis = síntesis)
   - Integración de opuestos
   - Perspectivas complementarias
   - Visión 360 grados
   - Comprensión multi-dimensional

4. CONSTRUCCIÓN DE NARRATIVAS:
   - Historias coherentes
   - Flujo lógico
   - Conexiones causales
   - Arcos narrativos
   - Significado profundo

5. PENSAMIENTO HOLÍSTICO:
   - Ver el panorama completo
   - Identificar emergencias
   - Comprender interdependencias
   - Apreciar complejidad
   - Mantener simplicidad esencial

METODOLOGÍA DE TRABAJO:

Cuando recibas información para sintetizar:

1. RECOLECCIÓN:
   - Reúne todas las piezas de información
   - Identifica fuentes y perspectivas
   - Nota contradicciones y complementos
   - Mapea el territorio de conocimiento

2. ANÁLISIS INICIAL:
   - Identifica temas principales
   - Agrupa información relacionada
   - Nota patrones y outliers
   - Evalúa calidad y relevancia

3. INTEGRACIÓN:
   - Conecta piezas relacionadas
   - Reconcilia contradicciones
   - Identifica complementariedades
   - Construye estructura coherente

4. GENERACIÓN DE INSIGHTS:
   - Busca patrones emergentes
   - Identifica conexiones no obvias
   - Genera hipótesis integradoras
   - Descubre principios subyacentes

5. SÍNTESIS FINAL:
   - Construye narrativa coherente
   - Articula insights clave
   - Preserva matices importantes
   - Comunica con claridad

FORMATO DE RESPUESTA:

Estructura tus síntesis así:

**PANORAMA GENERAL:**
[Visión holística de la información]

**TEMAS PRINCIPALES:**
[Temas comunes identificados]

**PERSPECTIVAS INTEGRADAS:**
[Cómo diferentes perspectivas se complementan]

**INSIGHTS EMERGENTES:**
[Comprensiones que trascienden las partes]

**CONEXIONES CLAVE:**
[Relaciones importantes identificadas]

**SÍNTESIS NARRATIVA:**
[Historia coherente que integra todo]

**IMPLICACIONES:**
[Qué significa esto en el panorama mayor]

**ÁREAS DE TENSIÓN:**
[Contradicciones o paradojas que persisten]

PRINCIPIOS DE SÍNTESIS:
- Integración sobre fragmentación
- Insights sobre información
- Coherencia sobre caos
- Profundidad sobre superficialidad
- Claridad sobre confusión

La verdadera síntesis no solo junta piezas, sino que revela
un nivel de comprensión que no existía antes."""

    async def process_task(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Procesa una tarea de síntesis
        
        Args:
            task: Información a sintetizar o pregunta sobre síntesis
            context: Contexto (fuentes, perspectivas, enfoque)
            
        Returns:
            Síntesis completa con insights
        """
        context = context or {}
        
        # Preparar contexto de memoria
        memory_context = self.get_memory_context(limit=5)
        
        # Determinar enfoque de síntesis
        approach = context.get("approach", "integrative")
        
        # Construir prompt
        user_message = f"""
INFORMACIÓN A SINTETIZAR: {task}

CONTEXTO:
{self._format_context(context)}

ENFOQUE DE SÍNTESIS: {approach}

MEMORIA RECIENTE:
{memory_context}

Por favor, realiza una síntesis profunda e integradora de esta información.
"""
        
        # Llamar al LLM
        response = await self.call_llm(
            messages=[{"role": "user", "content": user_message}],
            temperature=0.6  # Mayor temperatura para creatividad
        )
        
        # Extraer resultado
        result = {
            "synthesis": response,
            "approach": approach,
            "confidence": 0.87,
            "agent": self.profile.name,
            "capability": self.profile.primary_capability.value
        }
        
        # Guardar en memoria
        self.add_to_memory({
            "subject": task[:100],
            "summary": response[:200],
            "approach": approach
        })
        
        return result
    
    def _format_context(self, context: Dict[str, Any]) -> str:
        """Formatea el contexto de síntesis"""
        if not context:
            return "No hay contexto adicional."
        
        formatted = []
        
        if "sources" in context:
            formatted.append(f"Fuentes: {context['sources']}")
        
        if "perspectives" in context:
            formatted.append(f"Perspectivas: {context['perspectives']}")
        
        if "focus" in context:
            formatted.append(f"Enfoque: {context['focus']}")
        
        if "contradictions" in context:
            formatted.append(f"Contradicciones a reconciliar: {context['contradictions']}")
        
        for key, value in context.items():
            if key not in ["sources", "perspectives", "focus", "contradictions", "approach"]:
                formatted.append(f"{key}: {value}")
        
        return "\n".join(formatted) if formatted else "No hay contexto adicional."
    
    async def integrate_perspectives(self, perspectives: List[str]) -> Dict[str, Any]:
        """
        Integra múltiples perspectivas
        
        Args:
            perspectives: Lista de perspectivas diferentes
            
        Returns:
            Síntesis integradora
        """
        perspectives_text = "\n\n".join([f"Perspectiva {i+1}:\n{p}" for i, p in enumerate(perspectives)])
        
        return await self.process_task(
            f"Integra estas perspectivas:\n\n{perspectives_text}",
            context={"approach": "dialectic", "synthesis_type": "multi_perspective"}
        )
    
    async def generate_insights(self, information: str) -> Dict[str, Any]:
        """
        Genera insights de información
        
        Args:
            information: Información base
            
        Returns:
            Insights emergentes
        """
        return await self.process_task(
            f"Genera insights profundos de esta información:\n{information}",
            context={"approach": "emergent", "synthesis_type": "insight_generation"}
        )
    
    async def create_narrative(self, fragments: List[str]) -> Dict[str, Any]:
        """
        Crea narrativa coherente de fragmentos
        
        Args:
            fragments: Fragmentos de información
            
        Returns:
            Narrativa coherente
        """
        fragments_text = "\n".join([f"- {f}" for f in fragments])
        
        return await self.process_task(
            f"Crea una narrativa coherente de estos fragmentos:\n{fragments_text}",
            context={"approach": "narrative", "synthesis_type": "narrative_construction"}
        )
