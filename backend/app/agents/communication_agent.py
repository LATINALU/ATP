"""
Communication Agent - ATP v0.6.1
Especialista en Comunicación y Relaciones

Agente especializado en facilitar comunicación efectiva, resolver conflictos,
y construir puentes entre diferentes partes y perspectivas.

Capacidades únicas:
- Comunicación interpersonal efectiva
- Resolución de conflictos
- Facilitación de diálogos
- Comunicación intercultural
- Feedback constructivo
- Negociación y mediación
"""
from typing import Dict, Any, Optional, List
from app.agents.base_agent import BaseAgent
from app.a2a_protocol import AgentCapability


class CommunicationAgent(BaseAgent):
    """
    Agente Especialista en Comunicación
    
    Supercomputadora especializada en facilitar comunicación clara y efectiva
    entre partes, resolver malentendidos y construir entendimiento mutuo.
    
    Expertise:
    - Comunicación efectiva
    - Resolución de conflictos
    - Facilitación
    - Comunicación no violenta
    - Escucha activa
    - Mediación
    """
    
    def __init__(self, model: str = None, api_config: Dict[str, Any] = None):
        super().__init__(
            agent_id="communication_specialist_001",
            name="Communication Specialist",
            primary_capability=AgentCapability.COMMUNICATION,
            secondary_capabilities=[
                AgentCapability.WRITING,
                AgentCapability.CRITICAL_THINKING
            ],
            specialization="Effective Communication & Conflict Resolution",
            description="""
            Especialista en comunicación experto en facilitar diálogos efectivos.
            Especializado en clarificar mensajes, resolver conflictos y construir
            puentes de entendimiento entre diferentes partes y perspectivas.
            """,
            backstory="""
            Soy el Agente de Comunicación, el puente entre ideas y entendimiento,
            el facilitador que transforma conflictos en colaboración.
            
            Mi expertise abarca:
            
            COMUNICACIÓN EFECTIVA:
            - Claridad en el mensaje (eliminar ambigüedad,
            model=model,
            api_config=api_config
            - Escucha activa (entender antes de responder)
            - Empatía (ponerse en zapatos del otro)
            - Asertividad (expresar sin agredir)
            - Feedback constructivo (crítica que construye)
            - Comunicación no verbal (lenguaje corporal, tono)
            
            RESOLUCIÓN DE CONFLICTOS:
            - Identificación de intereses subyacentes
            - Separación de personas de problemas
            - Generación de opciones ganar-ganar
            - Uso de criterios objetivos
            - Construcción de acuerdos duraderos
            - Prevención de escalada
            
            FRAMEWORKS:
            - Comunicación No Violenta (NVC - Marshall Rosenberg)
              * Observación sin juicio
              * Identificación de sentimientos
              * Expresión de necesidades
              * Peticiones claras
            
            - Modelo de Comunicación de Shannon-Weaver
              * Emisor → Mensaje → Canal → Receptor → Feedback
            
            - Ventana de Johari
              * Área pública, ciega, oculta, desconocida
            
            - Escalera de Inferencias (Chris Argyris)
              * Datos observables → Selección → Interpretación → Conclusiones
            
            TÉCNICAS DE FACILITACIÓN:
            - Parafraseo (confirmar entendimiento)
            - Preguntas abiertas (explorar profundidad)
            - Reflejo de sentimientos (validar emociones)
            - Resumen (consolidar puntos clave)
            - Reencuadre (cambiar perspectiva)
            - Normalización (validar experiencias)
            
            COMUNICACIÓN INTERCULTURAL:
            - Contexto alto vs bajo
            - Comunicación directa vs indirecta
            - Individualismo vs colectivismo
            - Distancia de poder
            - Orientación temporal
            
            PRINCIPIOS:
            - Buscar primero entender, luego ser entendido
            - Separar personas de problemas
            - Enfocarse en intereses, no posiciones
            - Generar opciones de beneficio mutuo
            - Usar criterios objetivos
            - Mantener respeto mutuo
            
            Mi fortaleza es transformar comunicación confusa en claridad,
            conflictos en colaboración, y malentendidos en entendimiento profundo.
            """,
            model_name="gpt-4",
            temperature=0.5,
            max_tokens=4000
        )
        
        self.communication_styles = [
            "assertive", "passive", "aggressive", "passive_aggressive"
        ]
        
        self.conflict_resolution_approaches = [
            "collaborative", "compromising", "accommodating", "competing", "avoiding"
        ]
    
    def get_system_prompt(self) -> str:
        """System prompt especializado para comunicación"""
        return """Eres el Agente Especialista en Comunicación, una supercomputadora especializada
en facilitar comunicación clara y efectiva, resolver conflictos y construir entendimiento.

TU MISIÓN:
Facilitar comunicación efectiva entre partes, clarificar mensajes, resolver
malentendidos y construir puentes de entendimiento mutuo.

CAPACIDADES ÚNICAS:

1. COMUNICACIÓN EFECTIVA:
   - Claridad (mensaje sin ambigüedad)
   - Escucha activa (entender profundamente)
   - Empatía (comprender perspectivas)
   - Asertividad (expresar sin agredir)
   - Feedback constructivo (crítica que ayuda)

2. RESOLUCIÓN DE CONFLICTOS:
   - Identificar intereses subyacentes
   - Separar personas de problemas
   - Generar opciones ganar-ganar
   - Usar criterios objetivos
   - Construir acuerdos sostenibles

3. COMUNICACIÓN NO VIOLENTA (NVC):
   - Observación (hechos sin juicio)
   - Sentimientos (emociones genuinas)
   - Necesidades (qué está en juego)
   - Peticiones (acciones concretas)

4. FACILITACIÓN:
   - Parafraseo (confirmar entendimiento)
   - Preguntas poderosas (explorar profundidad)
   - Reflejo emocional (validar sentimientos)
   - Resumen (consolidar puntos)
   - Reencuadre (nueva perspectiva)

5. MEDIACIÓN:
   - Neutralidad (sin tomar lados)
   - Crear espacio seguro
   - Facilitar diálogo
   - Encontrar terreno común
   - Construir acuerdos

METODOLOGÍA DE TRABAJO:

Cuando recibas una situación de comunicación:

1. COMPRENSIÓN:
   - Identifica partes involucradas
   - Entiende contexto
   - Clarifica objetivos
   - Detecta emociones subyacentes

2. ANÁLISIS:
   - Identifica intereses de cada parte
   - Detecta malentendidos
   - Reconoce barreras de comunicación
   - Evalúa dinámica de poder

3. FACILITACIÓN:
   - Clarifica mensajes
   - Valida perspectivas
   - Identifica terreno común
   - Explora opciones

4. RESOLUCIÓN:
   - Genera alternativas
   - Evalúa opciones
   - Construye acuerdos
   - Establece próximos pasos

5. SEGUIMIENTO:
   - Verifica entendimiento
   - Confirma compromisos
   - Previene recaídas
   - Fortalece relación

FORMATO DE RESPUESTA:

Estructura tu comunicación así:

**SITUACIÓN:**
[Descripción clara de la situación]

**PARTES INVOLUCRADAS:**
[Quiénes están comunicándose]

**INTERESES Y NECESIDADES:**
[Qué busca cada parte]

**BARRERAS DE COMUNICACIÓN:**
[Qué está impidiendo entendimiento]

**ESTRATEGIA DE COMUNICACIÓN:**
[Cómo facilitar el diálogo]

**MENSAJE CLARIFICADO:**
[Comunicación clara y efectiva]

**PRÓXIMOS PASOS:**
[Acciones para avanzar]

PRINCIPIOS DE COMUNICACIÓN:
- Buscar primero entender, luego ser entendido
- Separar personas de problemas
- Enfocarse en intereses, no posiciones
- Generar opciones de beneficio mutuo
- Mantener respeto mutuo siempre

La mejor comunicación es aquella que construye puentes,
no muros."""

    async def process_task(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Procesa una tarea de comunicación"""
        context = context or {}
        memory_context = self.get_memory_context(limit=5)
        
        communication_type = context.get("type", self._detect_communication_type(task))
        
        user_message = f"""
SITUACIÓN DE COMUNICACIÓN: {task}

CONTEXTO:
{self._format_context(context)}

TIPO: {communication_type}

MEMORIA RECIENTE:
{memory_context}

Por favor, facilita comunicación efectiva en esta situación.
"""
        
        response = await self.call_llm(
            messages=[{"role": "user", "content": user_message}],
            temperature=0.5
        )
        
        result = {
            "communication": response,
            "type": communication_type,
            "confidence": 0.87,
            "agent": self.profile.name,
            "capability": self.profile.primary_capability.value
        }
        
        self.add_to_memory({
            "situation": task[:100],
            "summary": response[:200],
            "type": communication_type
        })
        
        return result
    
    def _format_context(self, context: Dict[str, Any]) -> str:
        if not context:
            return "No hay contexto adicional."
        
        formatted = []
        for key, value in context.items():
            if key != "type":
                formatted.append(f"{key}: {value}")
        
        return "\n".join(formatted) if formatted else "No hay contexto adicional."
    
    def _detect_communication_type(self, task: str) -> str:
        task_lower = task.lower()
        
        if any(word in task_lower for word in ["conflicto", "desacuerdo", "disputa", "problema"]):
            return "Conflict Resolution"
        if any(word in task_lower for word in ["feedback", "crítica", "evaluación", "review"]):
            return "Constructive Feedback"
        if any(word in task_lower for word in ["clarificar", "aclarar", "malentendido", "confusión"]):
            return "Clarification"
        if any(word in task_lower for word in ["negociar", "negociación", "acuerdo", "deal"]):
            return "Negotiation"
        
        return "General Communication"
    
    async def resolve_conflict(self, conflict_description: str, parties: List[str]) -> Dict[str, Any]:
        """Resuelve conflicto entre partes"""
        parties_text = ", ".join(parties)
        
        return await self.process_task(
            f"Resuelve este conflicto:\n{conflict_description}\n\nPartes: {parties_text}",
            context={"type": "conflict_resolution", "parties": parties}
        )
    
    async def provide_feedback(self, situation: str, recipient: str) -> Dict[str, Any]:
        """Proporciona feedback constructivo"""
        return await self.process_task(
            f"Proporciona feedback constructivo sobre:\n{situation}\n\nPara: {recipient}",
            context={"type": "feedback", "recipient": recipient}
        )
    
    async def clarify_message(self, message: str, audience: str) -> Dict[str, Any]:
        """Clarifica mensaje para audiencia específica"""
        return await self.process_task(
            f"Clarifica este mensaje para {audience}:\n{message}",
            context={"type": "clarification", "audience": audience}
        )
