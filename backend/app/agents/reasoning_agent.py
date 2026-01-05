"""
Reasoning Agent - ATP v0.6.1
Maestro del Razonamiento Lógico y Pensamiento Crítico

Agente especializado en razonamiento riguroso, análisis lógico profundo,
y resolución de problemas complejos mediante múltiples paradigmas de pensamiento.

Capacidades únicas:
- Razonamiento deductivo, inductivo, abductivo y analógico
- Análisis de cadenas causales complejas
- Detección de falacias lógicas
- Construcción de argumentos sólidos
- Resolución de paradojas
- Pensamiento contrafactual
"""
from typing import Dict, Any, Optional, List
from app.agents.base_agent import BaseAgent
from app.a2a_protocol import AgentCapability


class ReasoningAgent(BaseAgent):
    """
    Agente Maestro de Razonamiento Lógico
    
    Este agente es una supercomputadora especializada en el arte del pensamiento
    riguroso. Aplica múltiples paradigmas de razonamiento para analizar problemas
    desde todos los ángulos posibles.
    
    Expertise:
    - Lógica formal y simbólica
    - Teoría de la argumentación
    - Análisis de sistemas complejos
    - Resolución de problemas mediante primeros principios
    - Pensamiento crítico avanzado
    """
    
    def __init__(self, model: str = None, api_config: Dict[str, Any] = None):
        super().__init__(
            agent_id="reasoning_master_001",
            name="Reasoning Master",
            primary_capability=AgentCapability.REASONING,
            secondary_capabilities=[
                AgentCapability.CRITICAL_THINKING,
                AgentCapability.ANALYSIS
            ],
            specialization="Advanced Logical Reasoning & Problem Solving",
            description="""
            Maestro del razonamiento lógico con expertise en múltiples paradigmas
            de pensamiento. Especializado en descomponer problemas complejos y
            aplicar razonamiento riguroso para llegar a conclusiones fundamentadas.
            """,
            backstory="""
            Soy el Agente de Razonamiento Maestro, entrenado en las tradiciones más
            rigurosas del pensamiento lógico desde Aristóteles hasta la lógica
            computacional moderna. Mi propósito es aplicar razonamiento sistemático
            y riguroso a cualquier problema, sin importar su complejidad.
            
            He sido diseñado para pensar en múltiples niveles simultáneamente:
            - Nivel superficial: Análisis directo del problema
            - Nivel estructural: Identificación de patrones y relaciones
            - Nivel fundamental: Reducción a primeros principios
            - Nivel meta: Análisis del proceso de razonamiento mismo
            
            Mi fortaleza radica en mi capacidad para aplicar diferentes tipos de
            razonamiento según la naturaleza del problema:
            - Deductivo: De lo general a lo específico
            - Inductivo: De lo específico a lo general
            - Abductivo: Inferencia a la mejor explicación
            - Analógico: Razonamiento por similitud
            - Causal: Análisis de causas y efectos
            - Contrafactual: Exploración de escenarios alternativos
            """,
            model_name="gpt-4",
            temperature=0.3,  # Baja temperatura para razonamiento preciso
            max_tokens=4000,
            model=model,
            api_config=api_config
        )
        
        # Estado especializado del agente
        self.reasoning_frameworks = [
            "deductive", "inductive", "abductive", "analogical",
            "causal", "counterfactual", "probabilistic"
        ]
        
        self.logical_tools = [
            "syllogism", "modus_ponens", "modus_tollens",
            "reductio_ad_absurdum", "proof_by_contradiction",
            "mathematical_induction", "case_analysis"
        ]
    
    def get_system_prompt(self) -> str:
        """System prompt especializado para razonamiento lógico"""
        return """Eres el Agente Maestro de Razonamiento Lógico, una supercomputadora especializada
en pensamiento riguroso y análisis lógico profundo.

TU MISIÓN:
Aplicar razonamiento sistemático y riguroso a cualquier problema, descomponiendo
la complejidad y construyendo argumentos sólidos basados en lógica impecable.

CAPACIDADES ÚNICAS:

1. RAZONAMIENTO MULTI-PARADIGMA:
   - Deductivo: Aplicar reglas generales a casos específicos
   - Inductivo: Generalizar desde observaciones específicas
   - Abductivo: Inferir la mejor explicación posible
   - Analógico: Razonar por similitud y transferencia
   - Causal: Analizar cadenas de causas y efectos
   - Contrafactual: Explorar escenarios "qué pasaría si"

2. ANÁLISIS LÓGICO PROFUNDO:
   - Identificar premisas implícitas y explícitas
   - Detectar falacias lógicas y errores de razonamiento
   - Construir cadenas argumentativas sólidas
   - Evaluar validez y solidez de argumentos
   - Resolver paradojas y contradicciones aparentes

3. RESOLUCIÓN DE PROBLEMAS:
   - Descomponer problemas complejos en componentes manejables
   - Aplicar pensamiento de primeros principios
   - Identificar patrones y estructuras subyacentes
   - Generar múltiples soluciones alternativas
   - Evaluar soluciones mediante criterios rigurosos

4. PENSAMIENTO CRÍTICO:
   - Cuestionar supuestos y creencias
   - Evaluar evidencia y su calidad
   - Distinguir entre correlación y causalidad
   - Identificar sesgos cognitivos
   - Mantener escepticismo saludable

METODOLOGÍA DE TRABAJO:

Cuando recibas una tarea, sigue este proceso:

1. COMPRENSIÓN:
   - Analiza el problema en profundidad
   - Identifica todas las premisas y supuestos
   - Clarifica términos ambiguos
   - Define el alcance del problema

2. DESCOMPOSICIÓN:
   - Divide el problema en sub-problemas
   - Identifica relaciones entre componentes
   - Establece jerarquía de elementos
   - Mapea dependencias

3. ANÁLISIS:
   - Aplica razonamiento apropiado al tipo de problema
   - Examina desde múltiples perspectivas
   - Identifica patrones y estructuras
   - Busca contraejemplos y casos límite

4. SÍNTESIS:
   - Construye argumentos sólidos
   - Integra conclusiones parciales
   - Verifica consistencia lógica
   - Evalúa robustez de conclusiones

5. VALIDACIÓN:
   - Revisa cada paso del razonamiento
   - Busca errores lógicos
   - Considera objeciones potenciales
   - Califica nivel de certeza

FORMATO DE RESPUESTA:

Estructura tus respuestas así:

**ANÁLISIS DEL PROBLEMA:**
[Comprensión profunda del problema]

**RAZONAMIENTO APLICADO:**
[Tipo(s) de razonamiento utilizados y por qué]

**PROCESO LÓGICO:**
[Pasos detallados del razonamiento]

**CONCLUSIONES:**
[Conclusiones fundamentadas con nivel de certeza]

**CONSIDERACIONES ADICIONALES:**
[Limitaciones, supuestos, y áreas de incertidumbre]

PRINCIPIOS FUNDAMENTALES:
- Rigor sobre rapidez
- Claridad sobre complejidad
- Evidencia sobre intuición
- Lógica sobre retórica
- Humildad intelectual sobre certeza dogmática

Eres un maestro del pensamiento, no un oráculo. Tu poder está en el proceso
de razonamiento, no solo en las conclusiones."""

    async def process_task(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Procesa una tarea aplicando razonamiento lógico riguroso
        
        Args:
            task: Problema o pregunta a analizar
            context: Contexto adicional (premisas, restricciones, etc.)
            
        Returns:
            Dict con análisis completo y conclusiones
        """
        context = context or {}
        
        # Preparar contexto de memoria
        memory_context = self.get_memory_context(limit=5)
        
        # Construir prompt con contexto
        user_message = f"""
TAREA: {task}

CONTEXTO ADICIONAL:
{self._format_context(context)}

MEMORIA RECIENTE:
{memory_context}

Por favor, aplica tu razonamiento lógico más riguroso para analizar esta tarea.
"""
        
        # Llamar al LLM
        response = await self.call_llm(
            messages=[{"role": "user", "content": user_message}],
            temperature=0.3  # Baja temperatura para precisión
        )
        
        # Extraer resultado
        result = {
            "analysis": response,
            "reasoning_type": self._identify_reasoning_type(task),
            "confidence": 0.85,
            "agent": self.profile.name,
            "capability": self.profile.primary_capability.value
        }
        
        # Guardar en memoria
        self.add_to_memory({
            "task": task[:100],
            "summary": response[:200],
            "reasoning_type": result["reasoning_type"]
        })
        
        return result
    
    def _format_context(self, context: Dict[str, Any]) -> str:
        """Formatea el contexto de manera legible"""
        if not context:
            return "No hay contexto adicional."
        
        formatted = []
        for key, value in context.items():
            formatted.append(f"- {key}: {value}")
        
        return "\n".join(formatted)
    
    def _identify_reasoning_type(self, task: str) -> List[str]:
        """Identifica qué tipos de razonamiento son más apropiados"""
        task_lower = task.lower()
        
        reasoning_types = []
        
        # Deductivo
        if any(word in task_lower for word in ["si", "entonces", "implica", "por lo tanto"]):
            reasoning_types.append("deductive")
        
        # Inductivo
        if any(word in task_lower for word in ["patrón", "generalizar", "observaciones", "ejemplos"]):
            reasoning_types.append("inductive")
        
        # Abductivo
        if any(word in task_lower for word in ["explicar", "por qué", "causa", "razón"]):
            reasoning_types.append("abductive")
        
        # Analógico
        if any(word in task_lower for word in ["similar", "como", "comparar", "analogía"]):
            reasoning_types.append("analogical")
        
        # Causal
        if any(word in task_lower for word in ["causa", "efecto", "resultado", "consecuencia"]):
            reasoning_types.append("causal")
        
        # Contrafactual
        if any(word in task_lower for word in ["qué pasaría si", "alternativa", "escenario"]):
            reasoning_types.append("counterfactual")
        
        # Default a deductivo si no se identifica ninguno
        if not reasoning_types:
            reasoning_types.append("deductive")
        
        return reasoning_types
    
    async def analyze_argument(self, argument: str) -> Dict[str, Any]:
        """
        Analiza un argumento para evaluar su validez y solidez
        
        Args:
            argument: Argumento a analizar
            
        Returns:
            Análisis detallado del argumento
        """
        return await self.process_task(
            f"Analiza la validez y solidez de este argumento: {argument}",
            context={"analysis_type": "argument_analysis"}
        )
    
    async def detect_fallacies(self, text: str) -> Dict[str, Any]:
        """
        Detecta falacias lógicas en un texto
        
        Args:
            text: Texto a analizar
            
        Returns:
            Lista de falacias detectadas
        """
        return await self.process_task(
            f"Identifica todas las falacias lógicas en este texto: {text}",
            context={"analysis_type": "fallacy_detection"}
        )
    
    async def solve_problem(self, problem: str, constraints: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Resuelve un problema aplicando razonamiento de primeros principios
        
        Args:
            problem: Problema a resolver
            constraints: Restricciones o limitaciones
            
        Returns:
            Solución fundamentada
        """
        context = {
            "analysis_type": "problem_solving",
            "approach": "first_principles"
        }
        
        if constraints:
            context["constraints"] = constraints
        
        return await self.process_task(problem, context=context)
