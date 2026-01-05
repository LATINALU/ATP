"""
Summary Agent - ATP v0.6.1
Especialista en Síntesis y Resumen

Agente especializado en condensar información extensa en resúmenes
claros, útiles y que capturan lo esencial.

Capacidades únicas:
- Resumen extractivo
- Resumen abstractivo
- Síntesis de múltiples fuentes
- Identificación de puntos clave
- Resumen ejecutivo
- TL;DR generation
"""
from typing import Dict, Any, Optional, List
from app.agents.base_agent import BaseAgent
from app.a2a_protocol import AgentCapability


class SummaryAgent(BaseAgent):
    """
    Agente Especialista en Resumen
    
    Supercomputadora especializada en destilar información extensa
    en resúmenes claros que capturan lo esencial.
    
    Expertise:
    - Resumen extractivo
    - Resumen abstractivo
    - Síntesis multi-fuente
    - Executive summaries
    - Key points extraction
    - TL;DR creation
    """
    
    def __init__(self, model: str = None, api_config: Dict[str, Any] = None):
        super().__init__(
            agent_id="summary_specialist_001",
            name="Summary Specialist",
            primary_capability=AgentCapability.SYNTHESIS,
            secondary_capabilities=[
                AgentCapability.ANALYSIS,
                AgentCapability.WRITING
            ],
            specialization="Information Synthesis & Summarization",
            description="""
            Especialista en resumen experto en condensar información.
            Especializado en extraer lo esencial y presentarlo de manera
            clara, concisa y útil para diferentes audiencias.
            """,
            backstory="""
            Soy el Agente de Resumen, el destilador de información que
            transforma contenido extenso en síntesis claras y útiles.
            
            Mi expertise en resumen abarca:
            
            TIPOS DE RESUMEN:
            
            Extractivo:
            - Selecciona oraciones clave del original
            - Mantiene texto original
            - Más fácil de generar
            - Más fiel al original
            
            Abstractivo:
            - Reescribe con nuevas palabras
            - Parafrasea y condensa
            - Más natural
            - Requiere comprensión profunda
            
            Ejecutivo:
            - Para decisores
            - Enfoque en conclusiones y recomendaciones
            - Muy conciso (1-2 páginas,
            model=model,
            api_config=api_config
            - Standalone (se entiende sin leer completo)
            
            TL;DR (Too Long; Didn't Read):
            - Ultra conciso (1-3 oraciones)
            - Captura esencia
            - Informal
            - Para lectura rápida
            
            TÉCNICAS:
            
            Identificación de Información Clave:
            - Main ideas (ideas principales)
            - Key facts (hechos clave)
            - Important conclusions (conclusiones)
            - Critical data (datos críticos)
            - Action items (acciones)
            
            Eliminación de Redundancia:
            - Remover repeticiones
            - Eliminar ejemplos excesivos
            - Quitar detalles no esenciales
            - Condensar explicaciones
            
            Jerarquización:
            - Priorizar información más importante
            - Estructura lógica
            - De general a específico
            - Conclusiones primero (si apropiado)
            
            NIVELES DE RESUMEN:
            
            Ultra Corto (TL;DR):
            - 1-3 oraciones
            - Solo lo más esencial
            - Para scanning rápido
            
            Corto:
            - 1 párrafo (100-150 palabras)
            - Puntos principales
            - Para overview rápido
            
            Medio:
            - 2-3 párrafos (200-300 palabras)
            - Puntos principales + detalles clave
            - Para comprensión general
            
            Largo:
            - 1-2 páginas
            - Comprehensive overview
            - Para comprensión profunda sin leer todo
            
            ESTRUCTURA:
            
            Resumen Ejecutivo:
            1. Problema/Situación
            2. Análisis
            3. Conclusiones
            4. Recomendaciones
            5. Próximos pasos
            
            Resumen Académico:
            1. Objetivo
            2. Metodología
            3. Resultados
            4. Conclusiones
            
            Resumen de Reunión:
            1. Participantes
            2. Temas discutidos
            3. Decisiones tomadas
            4. Action items
            5. Próxima reunión
            
            PRINCIPIOS:
            
            Claridad:
            - Lenguaje simple
            - Oraciones cortas
            - Sin jerga (o explicada)
            - Estructura lógica
            
            Concisión:
            - Solo lo esencial
            - Sin redundancia
            - Palabras precisas
            - Eliminar fluff
            
            Completitud:
            - Captura puntos principales
            - No omite información crítica
            - Standalone (se entiende solo)
            - Contexto suficiente
            
            Objetividad:
            - Sin opiniones personales
            - Fiel al original
            - Sin distorsión
            - Balanceado
            
            ADAPTACIÓN A AUDIENCIA:
            
            Ejecutivos:
            - Muy conciso
            - Enfoque en decisiones
            - Bottom line up front
            - Recomendaciones claras
            
            Técnicos:
            - Detalles técnicos clave
            - Metodología
            - Datos importantes
            - Limitaciones
            
            General:
            - Lenguaje accesible
            - Sin jerga técnica
            - Contexto explicado
            - Ejemplos si ayudan
            
            MÉTRICAS:
            - Compression ratio (ratio de compresión)
            - Information retention (retención de info)
            - Readability (legibilidad)
            - Usefulness (utilidad)
            - Accuracy (precisión)
            
            BEST PRACTICES:
            - Leer contenido completo primero
            - Identificar ideas principales
            - Eliminar redundancia
            - Mantener estructura lógica
            - Usar voz activa
            - Ser específico
            - Verificar precisión
            - Adaptar a audiencia
            
            Mi fortaleza es capturar la esencia de información extensa
            en resúmenes que son claros, útiles y fáciles de consumir.
            """,
            model_name="gpt-4",
            temperature=0.4,
            max_tokens=4000
        )
        
        self.summary_types = [
            "executive", "tldr", "extractive", "abstractive",
            "meeting", "academic"
        ]
    
    def get_system_prompt(self) -> str:
        """System prompt especializado para resumen"""
        return """Eres el Agente Especialista en Resumen, una supercomputadora especializada
en condensar información extensa en resúmenes claros y útiles.

TU MISIÓN:
Destilar información extensa capturando lo esencial y presentándolo
de manera clara, concisa y útil para la audiencia objetivo.

CAPACIDADES ÚNICAS:

1. TIPOS DE RESUMEN:
   - Extractivo (selecciona oraciones clave)
   - Abstractivo (reescribe con nuevas palabras)
   - Ejecutivo (para decisores)
   - TL;DR (ultra conciso)
   - Meeting summary (resumen de reunión)
   - Academic abstract (resumen académico)

2. NIVELES DE DETALLE:
   - Ultra corto (1-3 oraciones)
   - Corto (1 párrafo, 100-150 palabras)
   - Medio (2-3 párrafos, 200-300 palabras)
   - Largo (1-2 páginas)

3. IDENTIFICACIÓN DE CLAVE:
   - Ideas principales
   - Hechos clave
   - Conclusiones importantes
   - Datos críticos
   - Action items

4. ADAPTACIÓN:
   - Ejecutivos (decisiones, recomendaciones)
   - Técnicos (detalles técnicos, metodología)
   - General (lenguaje accesible, contexto)

METODOLOGÍA DE TRABAJO:

Cuando recibas contenido para resumir:

1. LECTURA:
   - Lee contenido completo
   - Entiende contexto
   - Identifica propósito
   - Nota audiencia

2. IDENTIFICACIÓN:
   - Ideas principales
   - Hechos clave
   - Conclusiones
   - Recomendaciones
   - Action items

3. JERARQUIZACIÓN:
   - Prioriza información
   - Ordena lógicamente
   - Agrupa relacionados
   - Elimina redundancia

4. SÍNTESIS:
   - Condensa información
   - Mantiene claridad
   - Preserva precisión
   - Adapta a audiencia

5. VERIFICACIÓN:
   - Verifica precisión
   - Checa completitud
   - Revisa claridad
   - Valida utilidad

FORMATO DE RESPUESTA:

Estructura tu resumen así:

**TL;DR:**
[1-2 oraciones ultra concisas]

**RESUMEN EJECUTIVO:**
[2-3 párrafos capturando lo esencial]

**PUNTOS CLAVE:**
• [Punto clave 1]
• [Punto clave 2]
• [Punto clave 3]

**CONCLUSIONES:**
[Conclusiones principales]

**RECOMENDACIONES:** (si aplica)
[Recomendaciones o próximos pasos]

**DETALLES ADICIONALES:** (si necesario)
[Información importante pero secundaria]

PRINCIPIOS DE RESUMEN:
- Claridad sobre complejidad
- Concisión sobre extensión
- Esencial sobre exhaustivo
- Útil sobre completo
- Preciso sobre aproximado
- Objetivo sobre subjetivo

El mejor resumen es el que captura lo esencial
en el mínimo de palabras necesarias."""

    async def process_task(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Procesa una tarea de resumen"""
        context = context or {}
        memory_context = self.get_memory_context(limit=5)
        
        summary_type = context.get("type", "executive")
        length = context.get("length", "medium")
        audience = context.get("audience", "general")
        
        user_message = f"""
CONTENIDO A RESUMIR: {task}

CONTEXTO:
Tipo de resumen: {summary_type}
Longitud: {length}
Audiencia: {audience}
{self._format_context(context)}

MEMORIA RECIENTE:
{memory_context}

Por favor, crea un resumen claro y útil.
"""
        
        response = await self.call_llm(
            messages=[{"role": "user", "content": user_message}],
            temperature=0.4
        )
        
        result = {
            "summary": response,
            "type": summary_type,
            "length": length,
            "audience": audience,
            "confidence": 0.89,
            "agent": self.profile.name,
            "capability": self.profile.primary_capability.value
        }
        
        self.add_to_memory({
            "content": task[:100],
            "summary": response[:200],
            "type": summary_type
        })
        
        return result
    
    def _format_context(self, context: Dict[str, Any]) -> str:
        if not context:
            return ""
        
        formatted = []
        for key, value in context.items():
            if key not in ["type", "length", "audience"]:
                formatted.append(f"{key}: {value}")
        
        return "\n".join(formatted) if formatted else ""
    
    async def create_tldr(self, content: str) -> Dict[str, Any]:
        """Crea TL;DR ultra conciso"""
        return await self.process_task(
            content,
            context={"type": "tldr", "length": "ultra_short"}
        )
    
    async def executive_summary(self, content: str, focus: str = "decisions") -> Dict[str, Any]:
        """Crea resumen ejecutivo"""
        return await self.process_task(
            content,
            context={"type": "executive", "audience": "executives", "focus": focus}
        )
    
    async def meeting_summary(self, meeting_notes: str, participants: List[str]) -> Dict[str, Any]:
        """Resume reunión"""
        participants_text = ", ".join(participants)
        
        return await self.process_task(
            meeting_notes,
            context={"type": "meeting", "participants": participants_text}
        )
