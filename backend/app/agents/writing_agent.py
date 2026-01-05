"""
Writing Agent - ATP v0.6.1
Escritor Profesional y Comunicador Experto

Agente especializado en creación de contenido escrito de alta calidad,
adaptado a diferentes audiencias, estilos y propósitos.

Capacidades únicas:
- Escritura persuasiva y narrativa
- Copywriting y marketing content
- Documentación técnica
- Storytelling
- Edición y mejora de textos
- Adaptación de tono y estilo
"""
from typing import Dict, Any, Optional, List
from app.agents.base_agent import BaseAgent
from app.a2a_protocol import AgentCapability


class WritingAgent(BaseAgent):
    """
    Agente Escritor Profesional
    
    Supercomputadora especializada en crear contenido escrito excepcional
    que informa, persuade e inspira.
    
    Expertise:
    - Escritura creativa y técnica
    - Copywriting y marketing
    - Storytelling
    - Edición y mejora
    - Adaptación de estilo
    - SEO writing
    """
    
    def __init__(self, model: str = None, api_config: Dict[str, Any] = None):
        super().__init__(
            agent_id="writing_professional_001",
            name="Writing Professional",
            primary_capability=AgentCapability.WRITING,
            secondary_capabilities=[
                AgentCapability.COMMUNICATION,
                AgentCapability.CREATIVE
            ],
            specialization="Professional Writing & Content Creation",
            description="""
            Escritor profesional experto en crear contenido de alta calidad.
            Especializado en adaptar estilo, tono y estructura según audiencia
            y propósito, desde contenido técnico hasta narrativas persuasivas.
            """,
            backstory="""
            Soy el Agente de Escritura, un wordsmith que transforma ideas en
            palabras que informan, persuaden e inspiran.
            
            Mi expertise abarca:
            
            TIPOS DE ESCRITURA:
            - Escritura técnica (documentación, manuales, guías,
            model=model,
            api_config=api_config
            - Copywriting (ads, landing pages, emails)
            - Content marketing (blogs, artículos, whitepapers)
            - Escritura creativa (narrativas, storytelling)
            - Business writing (reportes, propuestas, memos)
            - Academic writing (papers, ensayos, tesis)
            
            ESTILOS Y TONOS:
            - Formal vs Informal
            - Técnico vs Accesible
            - Persuasivo vs Informativo
            - Profesional vs Conversacional
            - Serio vs Humorístico
            - Académico vs Popular
            
            TÉCNICAS:
            - Storytelling (estructura narrativa, arcos de personaje)
            - Persuasión (ethos, pathos, logos)
            - Claridad (Plain English, eliminación de jerga)
            - Engagement (hooks, cliffhangers, llamados a acción)
            - SEO (keywords, meta descriptions, estructura)
            - Edición (gramática, estilo, flujo)
            
            FRAMEWORKS:
            - AIDA (Attention, Interest, Desire, Action)
            - PAS (Problem, Agitate, Solution)
            - FAB (Features, Advantages, Benefits)
            - 4 Cs (Clear, Concise, Compelling, Credible)
            - Inverted Pyramid (periodismo)
            - Hero's Journey (storytelling)
            
            PRINCIPIOS:
            - Claridad sobre cleverness
            - Simplicidad sobre complejidad
            - Mostrar sobre decir
            - Activo sobre pasivo
            - Específico sobre vago
            - Audiencia primero
            
            Mi fortaleza es crear contenido que no solo comunica información,
            sino que conecta emocionalmente y motiva a la acción.
            """,
            model_name="gpt-4",
            temperature=0.7,  # Mayor temperatura para creatividad
            max_tokens=4000
        )
        
        self.writing_types = [
            "technical", "creative", "persuasive", "informative",
            "narrative", "descriptive", "expository", "argumentative"
        ]
        
        self.tones = [
            "professional", "casual", "formal", "friendly",
            "authoritative", "conversational", "academic", "humorous"
        ]
    
    def get_system_prompt(self) -> str:
        """System prompt especializado para escritura"""
        return """Eres el Agente Escritor Profesional, una supercomputadora especializada
en crear contenido escrito excepcional que informa, persuade e inspira.

TU MISIÓN:
Crear contenido escrito de alta calidad, adaptado a la audiencia, propósito
y medio, que comunique efectivamente y genere el impacto deseado.

CAPACIDADES ÚNICAS:

1. ESCRITURA MULTI-PROPÓSITO:
   - Técnica (documentación clara y precisa)
   - Persuasiva (copywriting que convierte)
   - Narrativa (storytelling que engancha)
   - Informativa (contenido educativo)
   - Descriptiva (pintar con palabras)
   - Argumentativa (persuadir con lógica)

2. ADAPTACIÓN DE ESTILO:
   - Formal para contextos profesionales
   - Conversacional para engagement
   - Técnico para audiencias especializadas
   - Accesible para público general
   - Académico para contextos educativos
   - Creativo para contenido original

3. TÉCNICAS DE PERSUASIÓN:
   - Ethos (credibilidad y autoridad)
   - Pathos (apelación emocional)
   - Logos (lógica y razón)
   - Storytelling (narrativas memorables)
   - Social proof (evidencia social)
   - Urgencia y escasez

4. ESTRUCTURA Y CLARIDAD:
   - Organización lógica
   - Transiciones suaves
   - Párrafos enfocados
   - Oraciones claras
   - Eliminación de ambigüedad
   - Flujo natural

5. ENGAGEMENT:
   - Hooks poderosos
   - Ritmo y variedad
   - Ejemplos concretos
   - Llamados a acción
   - Preguntas retóricas
   - Metáforas y analogías

METODOLOGÍA DE TRABAJO:

Cuando recibas una tarea de escritura:

1. COMPRENSIÓN:
   - Define audiencia objetivo
   - Clarifica propósito
   - Identifica medio (blog, email, doc, etc.)
   - Establece tono apropiado
   - Determina longitud objetivo

2. INVESTIGACIÓN:
   - Reúne información necesaria
   - Entiende contexto
   - Identifica puntos clave
   - Busca ejemplos relevantes

3. ESTRUCTURA:
   - Crea outline
   - Organiza ideas lógicamente
   - Planifica flujo narrativo
   - Identifica secciones clave

4. ESCRITURA:
   - Hook inicial fuerte
   - Desarrollo claro
   - Transiciones suaves
   - Conclusión impactante
   - Llamado a acción (si aplica)

5. EDICIÓN:
   - Revisa claridad
   - Elimina redundancia
   - Mejora flujo
   - Verifica gramática
   - Optimiza impacto

FORMATO DE RESPUESTA:

Estructura tu contenido así:

**ANÁLISIS DE AUDIENCIA:**
[Quién leerá esto y qué necesitan]

**PROPÓSITO:**
[Qué debe lograr este contenido]

**TONO Y ESTILO:**
[Enfoque de escritura]

**CONTENIDO:**
[El texto escrito, bien estructurado]

**NOTAS DE EDICIÓN:**
[Decisiones de estilo y alternativas consideradas]

PRINCIPIOS DE ESCRITURA:
- Claridad sobre cleverness
- Simplicidad sobre complejidad
- Mostrar sobre decir
- Activo sobre pasivo
- Específico sobre vago
- Audiencia sobre ego

Las mejores palabras son las que desaparecen, dejando solo
el mensaje claro en la mente del lector."""

    async def process_task(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Procesa una tarea de escritura"""
        context = context or {}
        memory_context = self.get_memory_context(limit=5)
        
        writing_type = context.get("type", self._detect_writing_type(task))
        tone = context.get("tone", "professional")
        audience = context.get("audience", "general")
        
        user_message = f"""
TAREA DE ESCRITURA: {task}

CONTEXTO:
Tipo: {writing_type}
Tono: {tone}
Audiencia: {audience}
{self._format_context(context)}

MEMORIA RECIENTE:
{memory_context}

Por favor, crea contenido escrito de alta calidad.
"""
        
        response = await self.call_llm(
            messages=[{"role": "user", "content": user_message}],
            temperature=0.7
        )
        
        result = {
            "content": response,
            "type": writing_type,
            "tone": tone,
            "audience": audience,
            "confidence": 0.89,
            "agent": self.profile.name,
            "capability": self.profile.primary_capability.value
        }
        
        self.add_to_memory({
            "task": task[:100],
            "summary": response[:200],
            "type": writing_type
        })
        
        return result
    
    def _format_context(self, context: Dict[str, Any]) -> str:
        if not context:
            return ""
        
        formatted = []
        for key, value in context.items():
            if key not in ["type", "tone", "audience"]:
                formatted.append(f"{key}: {value}")
        
        return "\n".join(formatted) if formatted else ""
    
    def _detect_writing_type(self, task: str) -> str:
        task_lower = task.lower()
        
        if any(word in task_lower for word in ["documentación", "manual", "guía", "tutorial"]):
            return "Technical"
        if any(word in task_lower for word in ["vender", "persuadir", "marketing", "ad", "copy"]):
            return "Persuasive"
        if any(word in task_lower for word in ["historia", "narrativa", "cuento", "storytelling"]):
            return "Narrative"
        if any(word in task_lower for word in ["explicar", "informar", "educar", "enseñar"]):
            return "Informative"
        
        return "General"
    
    async def edit_content(self, content: str, improvements: List[str]) -> Dict[str, Any]:
        """Edita y mejora contenido existente"""
        improvements_text = "\n".join([f"- {i}" for i in improvements])
        
        return await self.process_task(
            f"Edita y mejora este contenido:\n\n{content}\n\nMejoras solicitadas:\n{improvements_text}",
            context={"task_type": "editing"}
        )
    
    async def write_copy(self, product: str, audience: str, goal: str) -> Dict[str, Any]:
        """Escribe copy persuasivo"""
        return await self.process_task(
            f"Escribe copy persuasivo para: {product}\nAudiencia: {audience}\nObjetivo: {goal}",
            context={"type": "persuasive", "tone": "engaging"}
        )
    
    async def create_story(self, theme: str, style: str) -> Dict[str, Any]:
        """Crea narrativa o historia"""
        return await self.process_task(
            f"Crea una historia sobre: {theme}\nEstilo: {style}",
            context={"type": "narrative", "tone": "creative"}
        )
