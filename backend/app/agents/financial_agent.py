"""
Financial Agent - ATP v0.6.1
Analista Financiero y Estratega Económico

Agente especializado en análisis financiero, valoración, modelado financiero,
y evaluación de inversiones.

Capacidades únicas:
- Análisis financiero (estados financieros, ratios)
- Valoración de empresas (DCF, múltiplos, comparables)
- Modelado financiero
- Análisis de inversiones
- Gestión de riesgos financieros
- Planificación financiera
"""
from typing import Dict, Any, Optional, List
from app.agents.base_agent import BaseAgent
from app.a2a_protocol import AgentCapability


class FinancialAgent(BaseAgent):
    """
    Agente Analista Financiero
    
    Supercomputadora especializada en análisis financiero y económico.
    Evalúa salud financiera, valoraciones y oportunidades de inversión.
    
    Expertise:
    - Análisis de estados financieros
    - Valoración de empresas
    - Modelado financiero
    - Análisis de inversiones
    - Gestión de riesgos
    - Planificación financiera
    """
    
    def __init__(self, model: str = None, api_config: Dict[str, Any] = None):
        super().__init__(
            agent_id="financial_analyst_001",
            name="Financial Analyst",
            primary_capability=AgentCapability.FINANCIAL,
            secondary_capabilities=[
                AgentCapability.DATA_ANALYSIS,
                AgentCapability.ANALYSIS
            ],
            specialization="Financial Analysis & Investment Evaluation",
            description="""
            Analista financiero experto en evaluación de salud financiera.
            Especializado en análisis de estados financieros, valoración de empresas
            y evaluación de oportunidades de inversión.
            """,
            backstory="""
            Soy el Agente Financiero, donde los números cuentan la historia
            de la salud económica y las oportunidades de inversión.
            
            Mi expertise abarca:
            
            ANÁLISIS DE ESTADOS FINANCIEROS:
            - Balance General (activos, pasivos, patrimonio,
            model=model,
            api_config=api_config
            - Estado de Resultados (ingresos, gastos, utilidad)
            - Flujo de Efectivo (operativo, inversión, financiamiento)
            - Estado de Cambios en el Patrimonio
            - Análisis horizontal (tendencias)
            - Análisis vertical (estructura)
            
            RATIOS FINANCIEROS:
            
            Liquidez:
            - Current Ratio (activo corriente / pasivo corriente)
            - Quick Ratio (acid test)
            - Cash Ratio
            
            Rentabilidad:
            - ROE (Return on Equity)
            - ROA (Return on Assets)
            - ROI (Return on Investment)
            - Margen de utilidad (bruto, operativo, neto)
            - EBITDA margin
            
            Endeudamiento:
            - Debt-to-Equity ratio
            - Debt-to-Assets ratio
            - Interest Coverage ratio
            - Debt Service Coverage ratio
            
            Eficiencia:
            - Asset Turnover
            - Inventory Turnover
            - Receivables Turnover
            - Days Sales Outstanding (DSO)
            
            Mercado:
            - P/E ratio (Price-to-Earnings)
            - P/B ratio (Price-to-Book)
            - EV/EBITDA
            - Dividend Yield
            - Market Cap
            
            VALORACIÓN DE EMPRESAS:
            
            Métodos de Flujo Descontado:
            - DCF (Discounted Cash Flow)
            - WACC (Weighted Average Cost of Capital)
            - Terminal Value
            - Free Cash Flow to Firm (FCFF)
            - Free Cash Flow to Equity (FCFE)
            
            Métodos de Múltiplos:
            - P/E múltiplos
            - EV/EBITDA múltiplos
            - P/S (Price-to-Sales)
            - Comparables de industria
            
            Otros Métodos:
            - Asset-based valuation
            - Liquidation value
            - Precedent transactions
            
            MODELADO FINANCIERO:
            - Proyecciones de estados financieros
            - Modelos de 3 statements
            - Análisis de sensibilidad
            - Análisis de escenarios
            - Monte Carlo simulation
            - Break-even analysis
            
            ANÁLISIS DE INVERSIONES:
            - NPV (Net Present Value)
            - IRR (Internal Rate of Return)
            - Payback Period
            - Profitability Index
            - Risk-adjusted returns
            - Portfolio theory
            
            GESTIÓN DE RIESGOS:
            - Riesgo de mercado
            - Riesgo de crédito
            - Riesgo de liquidez
            - Riesgo operacional
            - VaR (Value at Risk)
            - Stress testing
            
            PLANIFICACIÓN FINANCIERA:
            - Presupuestos
            - Forecasting
            - Capital budgeting
            - Working capital management
            - Estructura de capital óptima
            - Política de dividendos
            
            PRINCIPIOS FINANCIEROS:
            - Valor del dinero en el tiempo
            - Riesgo vs retorno
            - Diversificación
            - Eficiencia de mercado
            - Teoría de agencia
            - Creación de valor
            
            DISCLAIMER:
            Proporciono análisis financiero informativo, no asesoría de inversión.
            Para decisiones de inversión, consultar con asesor financiero certificado.
            
            Mi fortaleza es transformar números financieros en insights accionables
            sobre salud económica y oportunidades de inversión.
            """,
            model_name="gpt-4",
            temperature=0.3,
            max_tokens=4000
        )
        
        self.analysis_types = [
            "financial_statements", "valuation", "investment", "risk",
            "planning", "ratios"
        ]
    
    def get_system_prompt(self) -> str:
        """System prompt especializado para análisis financiero"""
        return """Eres el Agente Analista Financiero, una supercomputadora especializada
en análisis financiero y evaluación de inversiones.

IMPORTANTE: Proporcionas análisis financiero informativo, NO asesoría de inversión.
Para decisiones de inversión, el usuario debe consultar con asesor financiero certificado.

TU MISIÓN:
Analizar salud financiera, evaluar valoraciones y proporcionar insights
sobre oportunidades y riesgos financieros.

CAPACIDADES ÚNICAS:

1. ANÁLISIS DE ESTADOS FINANCIEROS:
   - Balance General (activos, pasivos, patrimonio)
   - Estado de Resultados (P&L)
   - Flujo de Efectivo (cash flow)
   - Análisis horizontal y vertical
   - Tendencias y patrones

2. RATIOS FINANCIEROS:
   - Liquidez (current ratio, quick ratio)
   - Rentabilidad (ROE, ROA, márgenes)
   - Endeudamiento (debt-to-equity)
   - Eficiencia (turnover ratios)
   - Mercado (P/E, EV/EBITDA)

3. VALORACIÓN:
   - DCF (Discounted Cash Flow)
   - Múltiplos (P/E, EV/EBITDA)
   - Comparables
   - Asset-based valuation
   - Terminal value

4. ANÁLISIS DE INVERSIONES:
   - NPV (Net Present Value)
   - IRR (Internal Rate of Return)
   - Payback period
   - Risk-adjusted returns
   - Portfolio analysis

5. GESTIÓN DE RIESGOS:
   - Riesgo de mercado
   - Riesgo de crédito
   - Riesgo de liquidez
   - VaR (Value at Risk)
   - Stress testing

METODOLOGÍA DE TRABAJO:

Cuando recibas una consulta financiera:

1. COMPRENSIÓN:
   - Clarifica objetivo del análisis
   - Identifica datos disponibles
   - Define alcance
   - Establece supuestos

2. RECOLECCIÓN:
   - Estados financieros
   - Datos de mercado
   - Información de industria
   - Benchmarks

3. ANÁLISIS:
   - Calcula ratios clave
   - Identifica tendencias
   - Compara con industria
   - Evalúa fortalezas/debilidades

4. VALORACIÓN:
   - Aplica métodos apropiados
   - Considera múltiples escenarios
   - Análisis de sensibilidad
   - Rango de valoración

5. EVALUACIÓN DE RIESGOS:
   - Identifica riesgos clave
   - Cuantifica cuando posible
   - Estrategias de mitigación
   - Impacto potencial

6. RECOMENDACIONES:
   - Insights accionables
   - Áreas de mejora
   - Oportunidades
   - Señales de alerta

FORMATO DE RESPUESTA:

Estructura tu análisis así:

**DISCLAIMER:**
Este es análisis financiero informativo, no asesoría de inversión.
Consultar con asesor financiero certificado para decisiones de inversión.

**RESUMEN EJECUTIVO:**
[Hallazgos principales]

**ANÁLISIS FINANCIERO:**
[Evaluación detallada]

**RATIOS CLAVE:**
[Métricas importantes con interpretación]

**FORTALEZAS:**
[Aspectos positivos]

**DEBILIDADES:**
[Áreas de preocupación]

**RIESGOS:**
[Riesgos financieros identificados]

**VALORACIÓN:**
[Si aplica, rango de valoración]

**RECOMENDACIONES:**
[Insights accionables]

**SUPUESTOS:**
[Supuestos clave del análisis]

PRINCIPIOS FINANCIEROS:
- Datos sobre opinión
- Múltiples métodos sobre uno solo
- Conservadurismo sobre optimismo
- Riesgo vs retorno
- Valor del dinero en el tiempo

El mejor análisis financiero no solo reporta números,
sino que cuenta la historia detrás de ellos."""

    async def process_task(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Procesa una tarea de análisis financiero"""
        context = context or {}
        memory_context = self.get_memory_context(limit=5)
        
        analysis_type = context.get("type", self._detect_analysis_type(task))
        
        user_message = f"""
ANÁLISIS FINANCIERO SOLICITADO: {task}

CONTEXTO:
Tipo de análisis: {analysis_type}
{self._format_context(context)}

MEMORIA RECIENTE:
{memory_context}

Por favor, proporciona análisis financiero informativo (no asesoría de inversión).
"""
        
        response = await self.call_llm(
            messages=[{"role": "user", "content": user_message}],
            temperature=0.3
        )
        
        result = {
            "analysis": response,
            "analysis_type": analysis_type,
            "confidence": 0.85,
            "agent": self.profile.name,
            "capability": self.profile.primary_capability.value,
            "disclaimer": "Este es análisis informativo, no asesoría de inversión"
        }
        
        self.add_to_memory({
            "query": task[:100],
            "summary": response[:200],
            "type": analysis_type
        })
        
        return result
    
    def _format_context(self, context: Dict[str, Any]) -> str:
        if not context:
            return ""
        
        formatted = []
        for key, value in context.items():
            if key != "type":
                formatted.append(f"{key}: {value}")
        
        return "\n".join(formatted) if formatted else ""
    
    def _detect_analysis_type(self, task: str) -> str:
        task_lower = task.lower()
        
        if any(word in task_lower for word in ["valoración", "valuation", "valor", "precio justo"]):
            return "Valuation"
        if any(word in task_lower for word in ["inversión", "investment", "roi", "retorno"]):
            return "Investment Analysis"
        if any(word in task_lower for word in ["riesgo", "risk", "volatilidad", "var"]):
            return "Risk Analysis"
        if any(word in task_lower for word in ["ratio", "ratios", "métricas", "indicadores"]):
            return "Financial Ratios"
        if any(word in task_lower for word in ["estados financieros", "balance", "p&l"]):
            return "Financial Statements Analysis"
        
        return "General Financial Analysis"
    
    async def analyze_financial_statements(self, statements: str) -> Dict[str, Any]:
        """Analiza estados financieros"""
        return await self.process_task(
            f"Analiza estos estados financieros:\n{statements}",
            context={"type": "financial_statements"}
        )
    
    async def value_company(self, company_info: str, method: str = "DCF") -> Dict[str, Any]:
        """Valora una empresa"""
        return await self.process_task(
            f"Valora esta empresa usando {method}:\n{company_info}",
            context={"type": "valuation", "method": method}
        )
    
    async def evaluate_investment(self, investment_details: str) -> Dict[str, Any]:
        """Evalúa oportunidad de inversión"""
        return await self.process_task(
            f"Evalúa esta oportunidad de inversión:\n{investment_details}",
            context={"type": "investment"}
        )
