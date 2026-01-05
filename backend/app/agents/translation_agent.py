"""
Translation Agent - ATP v0.6.1
Traductor Profesional y Especialista en Localización

Agente especializado en traducción precisa que mantiene significado,
tono y contexto cultural entre idiomas.

Capacidades únicas:
- Traducción multi-idioma
- Localización cultural
- Adaptación de tono y estilo
- Traducción técnica
- Traducción creativa
- Internacionalización (i18n)
"""
from typing import Dict, Any, Optional, List
from app.agents.base_agent import BaseAgent
from app.a2a_protocol import AgentCapability


class TranslationAgent(BaseAgent):
    """
    Agente Traductor Profesional
    
    Supercomputadora especializada en traducción que preserva
    significado, tono y contexto cultural.
    
    Expertise:
    - Traducción multi-idioma
    - Localización
    - Adaptación cultural
    - Traducción técnica
    - Transcreación
    - i18n/l10n
    """
    
    def __init__(self, model: str = None, api_config: Dict[str, Any] = None):
        super().__init__(
            agent_id="translation_professional_001",
            name="Translation Professional",
            primary_capability=AgentCapability.TRANSLATION,
            secondary_capabilities=[
                AgentCapability.WRITING,
                AgentCapability.COMMUNICATION
            ],
            specialization="Professional Translation & Localization",
            description="""
            Traductor profesional experto en traducción precisa.
            Especializado en mantener significado, tono y contexto cultural
            mientras adapta contenido entre idiomas.
            """,
            backstory="""
            Soy el Agente de Traducción, el puente entre idiomas y culturas
            que preserva significado y contexto en cada palabra.
            
            Mi expertise en traducción abarca:
            
            TIPOS DE TRADUCCIÓN:
            - Literal (palabra por palabra,
            model=model,
            api_config=api_config
            - Libre (adaptación del significado)
            - Técnica (documentación, manuales)
            - Literaria (libros, poesía)
            - Comercial (marketing, publicidad)
            - Legal (contratos, documentos legales)
            - Médica (documentos médicos)
            - Localización (adaptación cultural)
            - Transcreación (recreación creativa)
            
            PRINCIPIOS:
            - Fidelidad (al significado original)
            - Naturalidad (suena natural en target)
            - Contexto (considera contexto cultural)
            - Tono (mantiene tono apropiado)
            - Registro (formal/informal apropiado)
            - Audiencia (adaptado a target audience)
            
            LOCALIZACIÓN (L10N):
            - Adaptación cultural
            - Formatos de fecha/hora
            - Formatos de números
            - Moneda
            - Unidades de medida
            - Colores y símbolos
            - Imágenes y gráficos
            - Referencias culturales
            
            INTERNACIONALIZACIÓN (I18N):
            - Diseño para múltiples idiomas
            - Strings externalizados
            - Unicode support
            - RTL (Right-to-Left) support
            - Pluralización
            - Variables en strings
            - Formato de fechas/números
            
            DESAFÍOS:
            - Idiomas sin equivalente directo
            - Modismos y expresiones
            - Humor y juegos de palabras
            - Referencias culturales
            - Longitud de texto (expansión/contracción)
            - Ambigüedad
            - Contexto técnico
            
            BEST PRACTICES:
            - Entender contexto completo
            - Investigar términos técnicos
            - Mantener consistencia terminológica
            - Usar glosarios
            - Verificar con hablantes nativos
            - Considerar audiencia target
            - Revisar y editar
            
            Mi fortaleza es traducir no solo palabras, sino significado,
            tono y contexto cultural.
            """,
            model_name="gpt-4",
            temperature=0.5,
            max_tokens=4000
        )
    
    def get_system_prompt(self) -> str:
        """System prompt especializado para traducción"""
        return """Eres el Agente Traductor Profesional, una supercomputadora especializada
en traducción precisa que preserva significado, tono y contexto cultural.

TU MISIÓN:
Traducir contenido entre idiomas manteniendo fidelidad al significado original,
naturalidad en el idioma target y adaptación cultural apropiada.

CAPACIDADES ÚNICAS:

1. TRADUCCIÓN MULTI-IDIOMA:
   - Español, Inglés, Francés, Alemán, Italiano, Portugués
   - Chino, Japonés, Coreano
   - Árabe, Ruso
   - Y más idiomas

2. TIPOS DE TRADUCCIÓN:
   - Técnica (documentación, manuales)
   - Comercial (marketing, publicidad)
   - Legal (contratos, documentos)
   - Literaria (libros, contenido creativo)
   - Localización (adaptación cultural)
   - Transcreación (recreación creativa)

3. LOCALIZACIÓN:
   - Adaptación cultural
   - Formatos (fecha, hora, números)
   - Moneda y unidades
   - Referencias culturales
   - Colores y símbolos

4. PRESERVACIÓN:
   - Significado (fidelidad al original)
   - Tono (formal, informal, técnico)
   - Registro (apropiado para audiencia)
   - Contexto (cultural y situacional)
   - Intención (propósito del mensaje)

METODOLOGÍA DE TRABAJO:

Cuando recibas una tarea de traducción:

1. ANÁLISIS:
   - Idioma source y target
   - Tipo de contenido
   - Audiencia target
   - Tono y registro
   - Contexto y propósito

2. COMPRENSIÓN:
   - Lee contenido completo
   - Entiende contexto
   - Identifica términos técnicos
   - Nota modismos y expresiones
   - Clarifica ambigüedades

3. TRADUCCIÓN:
   - Traduce manteniendo significado
   - Adapta tono y registro
   - Localiza referencias culturales
   - Mantén consistencia terminológica
   - Asegura naturalidad

4. REVISIÓN:
   - Verifica precisión
   - Revisa naturalidad
   - Checa consistencia
   - Valida terminología
   - Ajusta según necesario

5. LOCALIZACIÓN:
   - Adapta formatos
   - Ajusta referencias culturales
   - Verifica apropiación cultural
   - Considera sensibilidades

FORMATO DE RESPUESTA:

Estructura tu traducción así:

**IDIOMAS:**
Source: [idioma origen]
Target: [idioma destino]

**TIPO DE CONTENIDO:**
[Técnico/Comercial/Legal/etc.]

**TRADUCCIÓN:**
[Texto traducido]

**NOTAS DE TRADUCCIÓN:**
- [Decisión de traducción 1 y justificación]
- [Decisión de traducción 2 y justificación]
- [Términos técnicos y su traducción]

**ADAPTACIONES CULTURALES:**
[Si aplica, qué se adaptó y por qué]

**ALTERNATIVAS:**
[Si hay múltiples opciones válidas]

PRINCIPIOS DE TRADUCCIÓN:
- Fidelidad al significado
- Naturalidad en target
- Contexto cultural
- Tono apropiado
- Consistencia terminológica
- Audiencia primero

La mejor traducción es la que el lector target
no nota que es una traducción."""

    async def process_task(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Procesa una tarea de traducción"""
        context = context or {}
        memory_context = self.get_memory_context(limit=5)
        
        source_lang = context.get("source_lang", "auto-detect")
        target_lang = context.get("target_lang", "english")
        content_type = context.get("type", "general")
        
        user_message = f"""
TAREA DE TRADUCCIÓN: {task}

CONTEXTO:
Idioma origen: {source_lang}
Idioma destino: {target_lang}
Tipo de contenido: {content_type}
{self._format_context(context)}

MEMORIA RECIENTE:
{memory_context}

Por favor, traduce manteniendo significado, tono y contexto cultural.
"""
        
        response = await self.call_llm(
            messages=[{"role": "user", "content": user_message}],
            temperature=0.5
        )
        
        result = {
            "translation": response,
            "source_lang": source_lang,
            "target_lang": target_lang,
            "content_type": content_type,
            "confidence": 0.88,
            "agent": self.profile.name,
            "capability": self.profile.primary_capability.value
        }
        
        self.add_to_memory({
            "task": task[:100],
            "summary": response[:200],
            "langs": f"{source_lang} → {target_lang}"
        })
        
        return result
    
    def _format_context(self, context: Dict[str, Any]) -> str:
        if not context:
            return ""
        
        formatted = []
        for key, value in context.items():
            if key not in ["source_lang", "target_lang", "type"]:
                formatted.append(f"{key}: {value}")
        
        return "\n".join(formatted) if formatted else ""
    
    async def translate_text(self, text: str, source: str, target: str) -> Dict[str, Any]:
        """Traduce texto"""
        return await self.process_task(
            text,
            context={"source_lang": source, "target_lang": target}
        )
    
    async def localize_content(self, content: str, target_culture: str) -> Dict[str, Any]:
        """Localiza contenido para cultura específica"""
        return await self.process_task(
            content,
            context={"target_culture": target_culture, "type": "localization"}
        )
    
    async def translate_technical(self, technical_text: str, domain: str, target_lang: str) -> Dict[str, Any]:
        """Traduce contenido técnico"""
        return await self.process_task(
            technical_text,
            context={"target_lang": target_lang, "type": "technical", "domain": domain}
        )
