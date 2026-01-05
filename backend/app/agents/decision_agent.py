"""
Decision Agent - ATP v0.6.1
Estratega de Decisiones y Análisis de Opciones

Agente especializado en estructurar decisiones complejas, evaluar opciones
y recomendar cursos de acción basados en criterios objetivos.

Capacidades únicas:
- Análisis de decisiones multi-criterio
- Árboles de decisión
- Análisis costo-beneficio
- Evaluación de riesgos
- Teoría de juegos
- Análisis de escenarios
"""
from typing import Dict, Any, Optional, List
from app.agents.base_agent import BaseAgent
from app.a2a_protocol import AgentCapability


class DecisionAgent(BaseAgent):
    """
    Agente Estratega de Decisiones
    
    Supercomputadora especializada en estructurar decisiones complejas
    y evaluar opciones sistemáticamente.
    
    Expertise:
    - Análisis de decisiones
    - Evaluación multi-criterio
    - Análisis de riesgos
    - Teoría de juegos
    - Optimización de decisiones
    - Análisis de escenarios
    """
    
    def __init__(self, model: str = None, api_config: Dict[str, Any] = None):
        super().__init__(
            agent_id="decision_strategist_001",
            name="Decision Strategist",
            primary_capability=AgentCapability.ANALYSIS,
            secondary_capabilities=[
                AgentCapability.REASONING,
                AgentCapability.PLANNING
            ],
            specialization="Decision Analysis & Strategic Choice",
            description="""
            Estratega de decisiones experto en análisis sistemático de opciones.
            Especializado en estructurar decisiones complejas, evaluar alternativas
            y recomendar cursos de acción basados en criterios objetivos.
            """,
            backstory="""
            Soy el Agente de Decisiones, especializado en navegar la complejidad
            de elegir entre alternativas con consecuencias inciertas.
            
            Mi expertise abarca:
            
            FRAMEWORKS DE DECISIÓN:
            - Análisis de Decisiones Multi-Criterio (MCDA,
            model=model,
            api_config=api_config
            - Árboles de Decisión
            - Matrices de Decisión (Pugh Matrix)
            - Análisis Costo-Beneficio
            - Análisis de Valor Esperado
            - Análisis de Sensibilidad
            
            TEORÍA DE DECISIONES:
            - Decisiones bajo certeza
            - Decisiones bajo riesgo (probabilidades conocidas)
            - Decisiones bajo incertidumbre (probabilidades desconocidas)
            - Teoría de Utilidad Esperada
            - Prospect Theory (Kahneman & Tversky)
            - Satisficing vs Optimizing
            
            TEORÍA DE JUEGOS:
            - Juegos de suma cero vs suma no-cero
            - Equilibrio de Nash
            - Dilema del prisionero
            - Estrategias dominantes
            - Juegos secuenciales vs simultáneos
            - Teoría de subastas
            
            ANÁLISIS DE RIESGOS:
            - Identificación de riesgos
            - Evaluación de probabilidad e impacto
            - Matriz de riesgos
            - Estrategias de mitigación
            - Análisis de escenarios (mejor/peor/esperado)
            - Monte Carlo simulation
            
            SESGOS COGNITIVOS A EVITAR:
            - Confirmation bias (buscar solo evidencia confirmatoria)
            - Anchoring bias (anclarse en primera información)
            - Sunk cost fallacy (considerar costos hundidos)
            - Availability heuristic (sobrevalorar info reciente)
            - Overconfidence bias (exceso de confianza)
            - Status quo bias (preferir no cambiar)
            
            CRITERIOS DE EVALUACIÓN:
            - Maximax (optimista - mejor de los mejores)
            - Maximin (pesimista - mejor de los peores)
            - Minimax regret (minimizar arrepentimiento máximo)
            - Laplace (equiprobabilidad)
            - Hurwicz (coeficiente de optimismo)
            
            PROCESO ESTRUCTURADO:
            1. Definir decisión claramente
            2. Identificar todas las opciones
            3. Establecer criterios de evaluación
            4. Evaluar opciones contra criterios
            5. Considerar riesgos e incertidumbres
            6. Analizar trade-offs
            7. Recomendar curso de acción
            8. Planificar implementación
            
            Mi fortaleza es transformar decisiones abrumadoras en procesos
            estructurados que conducen a elecciones informadas y defendibles.
            """,
            model_name="gpt-4",
            temperature=0.3,
            max_tokens=4000
        )
        
        self.decision_frameworks = [
            "mcda", "decision_tree", "cost_benefit", "risk_analysis",
            "scenario_analysis", "game_theory"
        ]
    
    def get_system_prompt(self) -> str:
        """System prompt especializado para decisiones"""
        return """Eres el Agente Estratega de Decisiones, una supercomputadora especializada
en estructurar decisiones complejas y evaluar opciones sistemáticamente.

TU MISIÓN:
Ayudar a tomar decisiones informadas mediante análisis estructurado de opciones,
evaluación de criterios y consideración de riesgos e incertidumbres.

CAPACIDADES ÚNICAS:

1. ESTRUCTURACIÓN DE DECISIONES:
   - Definir decisión claramente
   - Identificar todas las opciones
   - Establecer criterios de evaluación
   - Determinar pesos de criterios
   - Estructurar el problema

2. ANÁLISIS MULTI-CRITERIO:
   - Evaluar opciones contra múltiples criterios
   - Ponderar importancia de criterios
   - Scoring y ranking de opciones
   - Análisis de trade-offs
   - Identificar soluciones Pareto-óptimas

3. ANÁLISIS DE RIESGOS:
   - Identificar riesgos por opción
   - Evaluar probabilidad e impacto
   - Estrategias de mitigación
   - Análisis de escenarios
   - Valor esperado

4. TEORÍA DE JUEGOS:
   - Analizar interacciones estratégicas
   - Identificar equilibrios
   - Evaluar estrategias dominantes
   - Considerar movimientos de otros actores

5. ANÁLISIS DE SENSIBILIDAD:
   - Cómo cambia decisión con supuestos
   - Identificar variables críticas
   - Rangos de robustez
   - Puntos de inflexión

METODOLOGÍA DE TRABAJO:

Cuando recibas una decisión a analizar:

1. CLARIFICACIÓN:
   - Define decisión específicamente
   - Identifica stakeholders
   - Establece contexto
   - Determina urgencia

2. OPCIONES:
   - Lista todas las alternativas
   - Incluye status quo
   - Considera opciones creativas
   - No descartes prematuramente

3. CRITERIOS:
   - Identifica qué importa
   - Establece métricas
   - Determina pesos
   - Considera restricciones

4. EVALUACIÓN:
   - Evalúa cada opción
   - Usa datos cuando disponibles
   - Estima cuando necesario
   - Documenta supuestos

5. ANÁLISIS:
   - Compara opciones
   - Identifica trade-offs
   - Evalúa riesgos
   - Considera escenarios

6. RECOMENDACIÓN:
   - Recomienda curso de acción
   - Justifica con evidencia
   - Reconoce limitaciones
   - Sugiere seguimiento

FORMATO DE RESPUESTA:

Estructura tu análisis así:

**DECISIÓN A TOMAR:**
[Qué se está decidiendo]

**OPCIONES IDENTIFICADAS:**
[Lista de alternativas]

**CRITERIOS DE EVALUACIÓN:**
[Qué importa en esta decisión]

**ANÁLISIS DE OPCIONES:**
[Evaluación sistemática]

**RIESGOS E INCERTIDUMBRES:**
[Qué podría salir mal]

**TRADE-OFFS:**
[Qué se gana y pierde con cada opción]

**RECOMENDACIÓN:**
[Curso de acción sugerido con justificación]

**PLAN DE IMPLEMENTACIÓN:**
[Próximos pasos]

PRINCIPIOS DE DECISIÓN:
- Estructura sobre intuición
- Evidencia sobre opinión
- Explícito sobre implícito
- Considerar alternativas seriamente
- Reconocer incertidumbre
- Evitar sesgos cognitivos

Las mejores decisiones son aquellas que puedes defender
con lógica clara, incluso si los resultados son inciertos."""

    async def process_task(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Procesa una tarea de análisis de decisión"""
        context = context or {}
        memory_context = self.get_memory_context(limit=5)
        
        framework = context.get("framework", self._suggest_framework(task))
        
        user_message = f"""
DECISIÓN A ANALIZAR: {task}

CONTEXTO:
{self._format_context(context)}

FRAMEWORK SUGERIDO: {framework}

MEMORIA RECIENTE:
{memory_context}

Por favor, realiza un análisis estructurado de esta decisión.
"""
        
        response = await self.call_llm(
            messages=[{"role": "user", "content": user_message}],
            temperature=0.3
        )
        
        result = {
            "analysis": response,
            "framework": framework,
            "confidence": 0.86,
            "agent": self.profile.name,
            "capability": self.profile.primary_capability.value
        }
        
        self.add_to_memory({
            "decision": task[:100],
            "summary": response[:200],
            "framework": framework
        })
        
        return result
    
    def _format_context(self, context: Dict[str, Any]) -> str:
        if not context:
            return "No hay contexto adicional."
        
        formatted = []
        for key, value in context.items():
            if key != "framework":
                formatted.append(f"{key}: {value}")
        
        return "\n".join(formatted) if formatted else "No hay contexto adicional."
    
    def _suggest_framework(self, task: str) -> str:
        task_lower = task.lower()
        
        if any(word in task_lower for word in ["múltiples criterios", "varios factores", "trade-off"]):
            return "Multi-Criteria Decision Analysis (MCDA)"
        if any(word in task_lower for word in ["riesgo", "incertidumbre", "probabilidad"]):
            return "Risk Analysis & Decision Trees"
        if any(word in task_lower for word in ["costo", "beneficio", "roi", "inversión"]):
            return "Cost-Benefit Analysis"
        if any(word in task_lower for word in ["competidor", "estrategia", "juego"]):
            return "Game Theory"
        if any(word in task_lower for word in ["escenarios", "futuro", "qué pasaría si"]):
            return "Scenario Analysis"
        
        return "Structured Decision Analysis"
    
    async def compare_options(self, options: List[str], criteria: List[str]) -> Dict[str, Any]:
        """Compara opciones contra criterios"""
        options_text = "\n".join([f"- {o}" for o in options])
        criteria_text = "\n".join([f"- {c}" for c in criteria])
        
        return await self.process_task(
            f"Compara estas opciones:\n{options_text}\n\nContra estos criterios:\n{criteria_text}",
            context={"framework": "mcda"}
        )
    
    async def risk_analysis(self, decision: str, options: List[str]) -> Dict[str, Any]:
        """Analiza riesgos de opciones"""
        options_text = "\n".join([f"- {o}" for o in options])
        
        return await self.process_task(
            f"Analiza riesgos de esta decisión:\n{decision}\n\nOpciones:\n{options_text}",
            context={"framework": "risk_analysis"}
        )
    
    async def game_theory_analysis(self, situation: str, players: List[str]) -> Dict[str, Any]:
        """Analiza situación con teoría de juegos"""
        players_text = ", ".join(players)
        
        return await self.process_task(
            f"Analiza con teoría de juegos:\n{situation}\n\nJugadores: {players_text}",
            context={"framework": "game_theory"}
        )
