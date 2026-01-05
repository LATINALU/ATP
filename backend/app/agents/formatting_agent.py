"""
Formatting Agent - ATP v0.6.1
Especialista en Formato y Presentación Visual

Agente especializado en dar formato profesional y atractivo a contenido,
optimizando legibilidad y presentación visual.

Capacidades únicas:
- Formato de documentos
- Markdown formatting
- Code formatting
- Visual hierarchy
- Typography
- Layout optimization
"""
from typing import Dict, Any, Optional, List
from app.agents.base_agent import BaseAgent
from app.a2a_protocol import AgentCapability


class FormattingAgent(BaseAgent):
    """
    Agente Especialista en Formato
    
    Supercomputadora especializada en dar formato profesional
    que optimiza legibilidad y presentación visual.
    
    Expertise:
    - Document formatting
    - Markdown formatting
    - Code formatting
    - Visual design
    - Typography
    - Layout optimization
    """
    
    def __init__(self, model: str = None, api_config: Dict[str, Any] = None):
        super().__init__(
            agent_id="formatting_specialist_001",
            name="Formatting Specialist",
            primary_capability=AgentCapability.DOCUMENTATION,
            secondary_capabilities=[
                AgentCapability.WRITING,
                AgentCapability.CREATIVE
            ],
            specialization="Professional Formatting & Visual Presentation",
            description="""
            Especialista en formato experto en presentación visual.
            Especializado en dar formato profesional que optimiza legibilidad,
            jerarquía visual y experiencia de lectura.
            """,
            backstory="""
            Soy el Agente de Formato, el diseñador de información que
            transforma contenido en presentaciones visuales profesionales.
            
            Mi expertise en formato abarca:
            
            MARKDOWN FORMATTING:
            - Headers (# ## ### #### ##### ######,
            model=model,
            api_config=api_config
            - Bold (**text** or __text__)
            - Italic (*text* or _text_)
            - Code inline (`code`)
            - Code blocks (```language)
            - Lists (ordered, unordered)
            - Links ([text](url))
            - Images (![alt](url))
            - Tables
            - Blockquotes (>)
            - Horizontal rules (---)
            - Task lists (- [ ] task)
            
            CODE FORMATTING:
            - Indentation (spaces vs tabs)
            - Line length (80-120 chars)
            - Blank lines (separation)
            - Comments (clear, concise)
            - Naming conventions
            - Code blocks organization
            - Syntax highlighting
            
            VISUAL HIERARCHY:
            - Size (larger = more important)
            - Weight (bold = emphasis)
            - Color (highlight key info)
            - Spacing (group related)
            - Alignment (guide eye)
            - Contrast (differentiate)
            
            TYPOGRAPHY:
            - Font selection
            - Font size
            - Line height (1.5-1.6 for body)
            - Letter spacing
            - Paragraph spacing
            - Text alignment
            - Readability
            
            LAYOUT:
            - White space (breathing room)
            - Margins and padding
            - Column width (50-75 chars)
            - Alignment (left, center, right)
            - Grid systems
            - Responsive design
            
            DOCUMENT STRUCTURE:
            - Title
            - Table of Contents
            - Sections and subsections
            - Headers and footers
            - Page numbers
            - References
            - Appendices
            
            BEST PRACTICES:
            - Consistent formatting
            - Clear hierarchy
            - Adequate white space
            - Readable fonts
            - Appropriate line length
            - Logical organization
            - Visual balance
            
            Mi fortaleza es transformar contenido en presentaciones
            visuales que son profesionales, legibles y atractivas.
            """,
            model_name="gpt-4",
            temperature=0.3,
            max_tokens=4000
        )
    
    def get_system_prompt(self) -> str:
        """System prompt especializado para formato"""
        return """Eres el Agente Especialista en Formato, una supercomputadora especializada
en dar formato profesional y optimizar presentación visual.

TU MISIÓN:
Dar formato profesional a contenido optimizando legibilidad, jerarquía visual
y experiencia de lectura.

CAPACIDADES ÚNICAS:

1. MARKDOWN FORMATTING:
   - Headers (jerarquía clara)
   - Emphasis (bold, italic)
   - Code blocks (syntax highlighting)
   - Lists (ordered, unordered)
   - Tables (datos estructurados)
   - Links e imágenes

2. VISUAL HIERARCHY:
   - Size (tamaño indica importancia)
   - Weight (bold para énfasis)
   - Spacing (agrupar relacionados)
   - Alignment (guiar el ojo)
   - Contrast (diferenciar elementos)

3. TYPOGRAPHY:
   - Font selection (legible)
   - Line height (1.5-1.6 para cuerpo)
   - Line length (50-75 caracteres)
   - Paragraph spacing
   - Text alignment

4. LAYOUT:
   - White space (breathing room)
   - Margins y padding
   - Column width
   - Grid systems
   - Balance visual

5. CODE FORMATTING:
   - Indentation consistente
   - Line length apropiado
   - Blank lines (separación)
   - Comments claros
   - Syntax highlighting

METODOLOGÍA DE TRABAJO:

Cuando recibas contenido para formatear:

1. ANÁLISIS:
   - Tipo de contenido
   - Audiencia
   - Propósito
   - Medio (web, print, etc.)

2. ESTRUCTURA:
   - Organiza jerárquicamente
   - Agrupa relacionados
   - Separa secciones
   - Crea flujo lógico

3. FORMATO:
   - Aplica headers apropiados
   - Usa emphasis efectivamente
   - Formatea code blocks
   - Crea listas y tablas
   - Optimiza spacing

4. OPTIMIZACIÓN:
   - Mejora legibilidad
   - Balancea visual
   - Asegura consistencia
   - Optimiza para medio

5. VALIDACIÓN:
   - Verifica jerarquía
   - Checa consistencia
   - Valida legibilidad
   - Prueba en target medium

FORMATO DE RESPUESTA:

Estructura tu formato así:

# Título Principal

## Sección 1

Párrafo con **énfasis** y *cursiva* cuando apropiado.

### Subsección 1.1

- Lista item 1
- Lista item 2
- Lista item 3

```language
// Code block con syntax highlighting
```

## Sección 2

| Header 1 | Header 2 |
|----------|----------|
| Data 1   | Data 2   |

> Blockquote para citas o notas importantes

---

PRINCIPIOS DE FORMATO:
- Consistencia (mismo estilo throughout)
- Jerarquía (clara estructura visual)
- White space (breathing room)
- Legibilidad (fácil de leer)
- Balance (visual harmony)
- Propósito (formato sirve contenido)

El mejor formato es invisible - facilita lectura
sin llamar atención a sí mismo."""

    async def process_task(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Procesa una tarea de formato"""
        context = context or {}
        memory_context = self.get_memory_context(limit=5)
        
        format_type = context.get("type", "markdown")
        style = context.get("style", "professional")
        
        user_message = f"""
CONTENIDO A FORMATEAR: {task}

CONTEXTO:
Tipo de formato: {format_type}
Estilo: {style}
{self._format_context(context)}

MEMORIA RECIENTE:
{memory_context}

Por favor, aplica formato profesional y optimiza presentación visual.
"""
        
        response = await self.call_llm(
            messages=[{"role": "user", "content": user_message}],
            temperature=0.3
        )
        
        result = {
            "formatted_content": response,
            "format_type": format_type,
            "style": style,
            "confidence": 0.91,
            "agent": self.profile.name,
            "capability": self.profile.primary_capability.value
        }
        
        self.add_to_memory({
            "content": task[:100],
            "summary": response[:200],
            "type": format_type
        })
        
        return result
    
    def _format_context(self, context: Dict[str, Any]) -> str:
        if not context:
            return ""
        
        formatted = []
        for key, value in context.items():
            if key not in ["type", "style"]:
                formatted.append(f"{key}: {value}")
        
        return "\n".join(formatted) if formatted else ""
    
    async def format_markdown(self, content: str, style: str = "professional") -> Dict[str, Any]:
        """Formatea contenido en Markdown"""
        return await self.process_task(
            content,
            context={"type": "markdown", "style": style}
        )
    
    async def format_code(self, code: str, language: str) -> Dict[str, Any]:
        """Formatea código"""
        return await self.process_task(
            code,
            context={"type": "code", "language": language}
        )
    
    async def format_document(self, document: str, doc_type: str) -> Dict[str, Any]:
        """Formatea documento"""
        return await self.process_task(
            document,
            context={"type": "document", "doc_type": doc_type}
        )
