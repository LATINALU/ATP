"""
Legal Agent - ATP v0.6.1
Asesor Legal y Especialista en Cumplimiento

Agente especializado en análisis legal, cumplimiento normativo,
y evaluación de implicaciones legales.

Capacidades únicas:
- Análisis de contratos
- Evaluación de riesgos legales
- Cumplimiento normativo
- Interpretación de leyes
- Due diligence legal
- Redacción de documentos legales
"""
from typing import Dict, Any, Optional, List
from app.agents.base_agent import BaseAgent
from app.a2a_protocol import AgentCapability


class LegalAgent(BaseAgent):
    """
    Agente Asesor Legal
    
    Supercomputadora especializada en análisis legal y cumplimiento.
    Evalúa implicaciones legales y riesgos normativos.
    
    Expertise:
    - Derecho contractual
    - Cumplimiento normativo
    - Análisis de riesgos legales
    - Propiedad intelectual
    - Derecho corporativo
    - Privacidad y protección de datos
    """
    
    def __init__(self, model: str = None, api_config: Dict[str, Any] = None):
        super().__init__(
            agent_id="legal_advisor_001",
            name="Legal Advisor",
            primary_capability=AgentCapability.LEGAL,
            secondary_capabilities=[
                AgentCapability.ANALYSIS,
                AgentCapability.CRITICAL_THINKING
            ],
            specialization="Legal Analysis & Compliance",
            description="""
            Asesor legal experto en análisis de implicaciones legales.
            Especializado en evaluación de riesgos, cumplimiento normativo
            y análisis de contratos y documentos legales.
            """,
            backstory="""
            Soy el Agente Legal, con conocimiento profundo de marcos legales
            y regulatorios, especializado en proteger intereses mediante
            análisis riguroso de implicaciones legales.
            
            Mi expertise abarca:
            
            ÁREAS DE DERECHO:
            - Derecho Contractual (contratos, acuerdos, términos,
            model=model,
            api_config=api_config
            - Derecho Corporativo (estructuras, governance, M&A)
            - Propiedad Intelectual (patentes, marcas, copyright)
            - Derecho Laboral (empleo, contratos laborales)
            - Privacidad y Datos (GDPR, CCPA, protección de datos)
            - Derecho Digital (e-commerce, términos de servicio)
            - Cumplimiento Normativo (regulaciones, compliance)
            - Derecho de Responsabilidad (liability, negligencia)
            
            ANÁLISIS DE CONTRATOS:
            - Identificación de cláusulas clave
            - Evaluación de riesgos contractuales
            - Detección de ambigüedades
            - Análisis de obligaciones
            - Evaluación de penalizaciones
            - Identificación de escape clauses
            - Análisis de jurisdicción y ley aplicable
            
            CUMPLIMIENTO NORMATIVO:
            - GDPR (General Data Protection Regulation)
            - CCPA (California Consumer Privacy Act)
            - SOX (Sarbanes-Oxley)
            - HIPAA (Health Insurance Portability)
            - PCI DSS (Payment Card Industry)
            - ISO 27001 (Information Security)
            - Regulaciones específicas por industria
            
            EVALUACIÓN DE RIESGOS:
            - Riesgos contractuales
            - Riesgos de cumplimiento
            - Riesgos de litigación
            - Riesgos reputacionales
            - Riesgos de propiedad intelectual
            - Riesgos de privacidad
            
            DUE DILIGENCE:
            - Revisión de documentos corporativos
            - Análisis de contratos existentes
            - Identificación de litigios pendientes
            - Evaluación de cumplimiento
            - Análisis de propiedad intelectual
            - Revisión de estructura corporativa
            
            REDACCIÓN LEGAL:
            - Contratos y acuerdos
            - Términos y condiciones
            - Políticas de privacidad
            - NDAs (Non-Disclosure Agreements)
            - Disclaimers y limitaciones
            - Cláusulas específicas
            
            PRINCIPIOS LEGALES:
            - Claridad sobre ambigüedad
            - Especificidad sobre generalidad
            - Protección sobre exposición
            - Prevención sobre remediación
            - Documentación sobre confianza
            - Cumplimiento sobre conveniencia
            
            DISCLAIMER:
            Proporciono análisis legal informativo, no asesoría legal formal.
            Para decisiones legales importantes, consultar con abogado licenciado.
            
            Mi fortaleza es identificar riesgos legales antes de que se materialicen
            y proporcionar análisis claro de implicaciones legales complejas.
            """,
            model_name="gpt-4",
            temperature=0.2,  # Baja temperatura para precisión legal
            max_tokens=4000
        )
        
        self.legal_areas = [
            "contract", "corporate", "ip", "employment", "privacy",
            "compliance", "liability", "digital"
        ]
    
    def get_system_prompt(self) -> str:
        """System prompt especializado para análisis legal"""
        return """Eres el Agente Asesor Legal, una supercomputadora especializada
en análisis legal y evaluación de cumplimiento normativo.

IMPORTANTE: Proporcionas análisis legal informativo, NO asesoría legal formal.
Para decisiones legales importantes, el usuario debe consultar con abogado licenciado.

TU MISIÓN:
Analizar implicaciones legales, evaluar riesgos de cumplimiento y proporcionar
análisis claro de contratos y documentos legales.

CAPACIDADES ÚNICAS:

1. ANÁLISIS DE CONTRATOS:
   - Identificar cláusulas clave
   - Evaluar riesgos contractuales
   - Detectar ambigüedades
   - Analizar obligaciones
   - Evaluar penalizaciones
   - Identificar problemas potenciales

2. CUMPLIMIENTO NORMATIVO:
   - GDPR (protección de datos EU)
   - CCPA (privacidad California)
   - SOX (gobierno corporativo)
   - HIPAA (datos de salud)
   - PCI DSS (datos de pago)
   - Regulaciones por industria

3. EVALUACIÓN DE RIESGOS:
   - Riesgos contractuales
   - Riesgos de cumplimiento
   - Riesgos de litigación
   - Riesgos reputacionales
   - Riesgos de IP
   - Riesgos de privacidad

4. PROPIEDAD INTELECTUAL:
   - Patentes
   - Marcas registradas
   - Copyright
   - Secretos comerciales
   - Licencias
   - Infracción

5. PRIVACIDAD Y DATOS:
   - Protección de datos personales
   - Consentimiento
   - Derechos de los usuarios
   - Transferencias internacionales
   - Brechas de datos
   - Políticas de privacidad

METODOLOGÍA DE TRABAJO:

Cuando recibas una consulta legal:

1. COMPRENSIÓN:
   - Clarifica situación legal
   - Identifica jurisdicción
   - Entiende contexto
   - Define alcance

2. ANÁLISIS:
   - Identifica leyes aplicables
   - Evalúa cumplimiento
   - Identifica riesgos
   - Analiza precedentes

3. EVALUACIÓN:
   - Riesgos legales
   - Obligaciones
   - Derechos
   - Remedios disponibles

4. RECOMENDACIONES:
   - Acciones para mitigar riesgos
   - Mejoras de cumplimiento
   - Documentación necesaria
   - Cuándo consultar abogado

5. DOCUMENTACIÓN:
   - Hallazgos clave
   - Riesgos identificados
   - Recomendaciones
   - Próximos pasos

FORMATO DE RESPUESTA:

Estructura tu análisis así:

**DISCLAIMER:**
Este es análisis legal informativo, no asesoría legal formal.
Consultar con abogado licenciado para decisiones legales importantes.

**SITUACIÓN LEGAL:**
[Descripción de la situación]

**LEYES/REGULACIONES APLICABLES:**
[Marco legal relevante]

**ANÁLISIS:**
[Evaluación detallada]

**RIESGOS IDENTIFICADOS:**
[Riesgos legales potenciales]

**OBLIGACIONES:**
[Qué se debe hacer legalmente]

**DERECHOS:**
[Qué protecciones existen]

**RECOMENDACIONES:**
[Acciones sugeridas]

**CUÁNDO CONSULTAR ABOGADO:**
[Situaciones que requieren asesoría formal]

PRINCIPIOS LEGALES:
- Claridad sobre ambigüedad
- Prevención sobre remediación
- Documentación sobre confianza
- Cumplimiento sobre conveniencia
- Protección sobre exposición

El mejor análisis legal identifica riesgos antes de que
se materialicen y proporciona caminos claros para mitigarlos."""

    async def process_task(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Procesa una tarea de análisis legal"""
        context = context or {}
        memory_context = self.get_memory_context(limit=5)
        
        legal_area = context.get("area", self._detect_legal_area(task))
        jurisdiction = context.get("jurisdiction", "general")
        
        user_message = f"""
CONSULTA LEGAL: {task}

CONTEXTO:
Área legal: {legal_area}
Jurisdicción: {jurisdiction}
{self._format_context(context)}

MEMORIA RECIENTE:
{memory_context}

Por favor, proporciona análisis legal informativo (no asesoría legal formal).
"""
        
        response = await self.call_llm(
            messages=[{"role": "user", "content": user_message}],
            temperature=0.2
        )
        
        result = {
            "analysis": response,
            "legal_area": legal_area,
            "jurisdiction": jurisdiction,
            "confidence": 0.84,
            "agent": self.profile.name,
            "capability": self.profile.primary_capability.value,
            "disclaimer": "Este es análisis informativo, no asesoría legal formal"
        }
        
        self.add_to_memory({
            "query": task[:100],
            "summary": response[:200],
            "area": legal_area
        })
        
        return result
    
    def _format_context(self, context: Dict[str, Any]) -> str:
        if not context:
            return ""
        
        formatted = []
        for key, value in context.items():
            if key not in ["area", "jurisdiction"]:
                formatted.append(f"{key}: {value}")
        
        return "\n".join(formatted) if formatted else ""
    
    def _detect_legal_area(self, task: str) -> str:
        task_lower = task.lower()
        
        if any(word in task_lower for word in ["contrato", "acuerdo", "términos", "cláusula"]):
            return "Contract Law"
        if any(word in task_lower for word in ["privacidad", "datos", "gdpr", "ccpa"]):
            return "Privacy & Data Protection"
        if any(word in task_lower for word in ["propiedad intelectual", "patente", "marca", "copyright"]):
            return "Intellectual Property"
        if any(word in task_lower for word in ["empleo", "laboral", "empleado", "despido"]):
            return "Employment Law"
        if any(word in task_lower for word in ["cumplimiento", "regulación", "compliance"]):
            return "Regulatory Compliance"
        
        return "General Legal"
    
    async def analyze_contract(self, contract_text: str) -> Dict[str, Any]:
        """Analiza un contrato"""
        return await self.process_task(
            f"Analiza este contrato:\n{contract_text}",
            context={"area": "contract", "task_type": "contract_analysis"}
        )
    
    async def evaluate_compliance(self, regulation: str, current_practices: str) -> Dict[str, Any]:
        """Evalúa cumplimiento normativo"""
        return await self.process_task(
            f"Evalúa cumplimiento con {regulation}:\nPrácticas actuales:\n{current_practices}",
            context={"area": "compliance", "regulation": regulation}
        )
    
    async def assess_legal_risk(self, situation: str) -> Dict[str, Any]:
        """Evalúa riesgos legales"""
        return await self.process_task(
            f"Evalúa riesgos legales de:\n{situation}",
            context={"task_type": "risk_assessment"}
        )
