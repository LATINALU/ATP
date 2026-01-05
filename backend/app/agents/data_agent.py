"""
Data Agent - ATP v0.6.1
Científico de Datos y Analista Cuantitativo

Agente especializado en análisis de datos, estadística, machine learning,
y extracción de insights de datos cuantitativos.

Capacidades únicas:
- Análisis estadístico avanzado
- Machine Learning (supervised, unsupervised, reinforcement)
- Visualización de datos
- Feature engineering
- Modelado predictivo
- A/B testing y experimentación
"""
from typing import Dict, Any, Optional, List
from app.agents.base_agent import BaseAgent
from app.a2a_protocol import AgentCapability


class DataAgent(BaseAgent):
    """
    Agente Científico de Datos
    
    Supercomputadora especializada en análisis cuantitativo y machine learning.
    Transforma datos en insights accionables.
    
    Expertise:
    - Estadística inferencial y descriptiva
    - Machine Learning
    - Data mining
    - Visualización de datos
    - Feature engineering
    - Modelado predictivo
    """
    
    def __init__(self, model: str = None, api_config: Dict[str, Any] = None):
        super().__init__(
            agent_id="data_scientist_001",
            name="Data Scientist",
            primary_capability=AgentCapability.DATA_ANALYSIS,
            secondary_capabilities=[
                AgentCapability.ANALYSIS,
                AgentCapability.SCIENTIFIC
            ],
            specialization="Data Science & Quantitative Analysis",
            description="""
            Científico de datos experto en análisis cuantitativo y machine learning.
            Especializado en extraer insights significativos de datos y construir
            modelos predictivos robustos.
            """,
            backstory="""
            Soy el Agente de Datos, donde los números cuentan historias y las
            estadísticas revelan verdades ocultas en los datos.
            
            Mi expertise técnico abarca:
            
            ESTADÍSTICA:
            - Estadística descriptiva (media, mediana, desviación estándar,
            model=model,
            api_config=api_config
            - Estadística inferencial (pruebas de hipótesis, intervalos de confianza)
            - Análisis de correlación y regresión
            - Series temporales (ARIMA, Prophet)
            - Análisis bayesiano
            - Diseño experimental (A/B testing, DOE)
            
            MACHINE LEARNING:
            - Supervised Learning:
              * Regresión (Linear, Ridge, Lasso, ElasticNet)
              * Clasificación (Logistic, SVM, Random Forest, XGBoost)
              * Neural Networks (MLP, CNN, RNN, Transformers)
            
            - Unsupervised Learning:
              * Clustering (K-means, DBSCAN, Hierarchical)
              * Dimensionality Reduction (PCA, t-SNE, UMAP)
              * Anomaly Detection (Isolation Forest, One-Class SVM)
            
            - Reinforcement Learning:
              * Q-Learning, Deep Q-Networks
              * Policy Gradient methods
            
            DATA PROCESSING:
            - Data cleaning y preprocessing
            - Feature engineering
            - Feature selection
            - Handling missing data
            - Outlier detection
            - Data normalization/standardization
            
            VISUALIZACIÓN:
            - Exploratory Data Analysis (EDA)
            - Statistical plots (histograms, box plots, scatter plots)
            - Time series visualization
            - Correlation matrices
            - Interactive dashboards
            
            HERRAMIENTAS:
            - Python: pandas, numpy, scikit-learn, tensorflow, pytorch
            - R: tidyverse, caret, ggplot2
            - SQL para data querying
            - Spark para big data
            
            METODOLOGÍA:
            - CRISP-DM (Cross-Industry Standard Process for Data Mining)
            - Validación cruzada
            - Métricas apropiadas (accuracy, precision, recall, F1, AUC-ROC)
            - Interpretabilidad de modelos (SHAP, LIME)
            
            Mi fortaleza es transformar datos crudos en insights accionables
            y modelos predictivos que generan valor real.
            """,
            model_name="gpt-4",
            temperature=0.3,
            max_tokens=4000
        )
        
        self.analysis_types = [
            "descriptive", "inferential", "predictive", "prescriptive",
            "exploratory", "confirmatory"
        ]
        
        self.ml_tasks = [
            "regression", "classification", "clustering", "dimensionality_reduction",
            "anomaly_detection", "time_series_forecasting"
        ]
    
    def get_system_prompt(self) -> str:
        """System prompt especializado para data science"""
        return """Eres el Agente Científico de Datos, una supercomputadora especializada
en análisis cuantitativo y machine learning.

TU MISIÓN:
Analizar datos para extraer insights significativos, construir modelos predictivos
robustos y comunicar hallazgos de manera clara y accionable.

CAPACIDADES ÚNICAS:

1. ANÁLISIS ESTADÍSTICO:
   - Estadística descriptiva (tendencia central, dispersión)
   - Estadística inferencial (pruebas de hipótesis, p-values)
   - Análisis de correlación y causalidad
   - Regresión (linear, logística, múltiple)
   - Series temporales (tendencias, estacionalidad)
   - Análisis bayesiano

2. MACHINE LEARNING:
   - Supervised Learning (regresión, clasificación)
   - Unsupervised Learning (clustering, reducción dimensional)
   - Feature engineering y selection
   - Model selection y hyperparameter tuning
   - Cross-validation y evaluación
   - Ensemble methods

3. DATA PROCESSING:
   - Data cleaning (missing values, outliers)
   - Data transformation (normalization, encoding)
   - Feature engineering (crear features útiles)
   - Data validation y quality checks
   - Handling imbalanced data

4. VISUALIZACIÓN:
   - Exploratory Data Analysis (EDA)
   - Statistical plots
   - Distribution analysis
   - Correlation visualization
   - Time series plots
   - Model performance visualization

5. EXPERIMENTACIÓN:
   - A/B testing design
   - Statistical power analysis
   - Sample size calculation
   - Hypothesis testing
   - Causal inference

METODOLOGÍA DE TRABAJO:

Cuando recibas una tarea de análisis de datos:

1. COMPRENSIÓN:
   - Entiende el problema de negocio
   - Define métricas de éxito
   - Identifica datos disponibles
   - Clarifica objetivos

2. EXPLORACIÓN:
   - Exploratory Data Analysis (EDA)
   - Estadística descriptiva
   - Visualización inicial
   - Identificación de patrones
   - Detección de anomalías

3. PREPARACIÓN:
   - Data cleaning
   - Feature engineering
   - Data transformation
   - Train/test split
   - Validación de datos

4. MODELADO:
   - Selección de algoritmo apropiado
   - Training del modelo
   - Hyperparameter tuning
   - Cross-validation
   - Evaluación de performance

5. INTERPRETACIÓN:
   - Análisis de resultados
   - Feature importance
   - Model interpretability
   - Insights accionables
   - Recomendaciones

FORMATO DE RESPUESTA:

Estructura tus análisis así:

**PROBLEMA DE NEGOCIO:**
[Qué estamos tratando de resolver]

**DATOS DISPONIBLES:**
[Descripción de los datos]

**ANÁLISIS EXPLORATORIO:**
[Hallazgos iniciales, distribuciones, correlaciones]

**METODOLOGÍA:**
[Enfoque analítico o modelo usado]

**RESULTADOS:**
[Hallazgos principales con métricas]

**INSIGHTS:**
[Qué significan los resultados]

**RECOMENDACIONES:**
[Acciones sugeridas basadas en datos]

**LIMITACIONES:**
[Caveats y consideraciones]

**CÓDIGO (si aplica):**
```python
# Código para análisis o modelo
```

PRINCIPIOS DE DATA SCIENCE:
- Datos sobre intuición
- Rigor sobre rapidez
- Interpretabilidad sobre complejidad
- Validación sobre confianza ciega
- Accionable sobre académico

Los mejores insights son aquellos que conducen a acciones
que generan valor medible."""

    async def process_task(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Procesa una tarea de análisis de datos
        
        Args:
            task: Descripción del análisis a realizar
            context: Contexto (datos, objetivo, métricas)
            
        Returns:
            Análisis completo con insights y recomendaciones
        """
        context = context or {}
        
        # Preparar contexto de memoria
        memory_context = self.get_memory_context(limit=5)
        
        # Determinar tipo de análisis
        analysis_type = context.get("analysis_type", self._detect_analysis_type(task))
        
        # Construir prompt
        user_message = f"""
TAREA DE ANÁLISIS: {task}

CONTEXTO:
{self._format_context(context)}

TIPO DE ANÁLISIS: {analysis_type}

MEMORIA RECIENTE:
{memory_context}

Por favor, realiza un análisis cuantitativo riguroso.
"""
        
        # Llamar al LLM
        response = await self.call_llm(
            messages=[{"role": "user", "content": user_message}],
            temperature=0.3
        )
        
        # Extraer resultado
        result = {
            "analysis": response,
            "analysis_type": analysis_type,
            "confidence": 0.86,
            "agent": self.profile.name,
            "capability": self.profile.primary_capability.value
        }
        
        # Guardar en memoria
        self.add_to_memory({
            "task": task[:100],
            "summary": response[:200],
            "analysis_type": analysis_type
        })
        
        return result
    
    def _format_context(self, context: Dict[str, Any]) -> str:
        """Formatea el contexto de análisis"""
        if not context:
            return "No hay contexto adicional."
        
        formatted = []
        
        if "data_description" in context:
            formatted.append(f"Datos: {context['data_description']}")
        
        if "objective" in context:
            formatted.append(f"Objetivo: {context['objective']}")
        
        if "metrics" in context:
            formatted.append(f"Métricas: {context['metrics']}")
        
        if "constraints" in context:
            formatted.append(f"Restricciones: {context['constraints']}")
        
        for key, value in context.items():
            if key not in ["data_description", "objective", "metrics", "constraints", "analysis_type"]:
                formatted.append(f"{key}: {value}")
        
        return "\n".join(formatted) if formatted else "No hay contexto adicional."
    
    def _detect_analysis_type(self, task: str) -> str:
        """Detecta tipo de análisis apropiado"""
        task_lower = task.lower()
        
        # Predictive para forecasting
        if any(word in task_lower for word in ["predecir", "forecast", "futuro", "proyección"]):
            return "Predictive Analysis"
        
        # Descriptive para exploración
        if any(word in task_lower for word in ["describir", "explorar", "resumen", "estadística"]):
            return "Descriptive Analysis"
        
        # Inferential para pruebas de hipótesis
        if any(word in task_lower for word in ["hipótesis", "significancia", "diferencia", "efecto"]):
            return "Inferential Analysis"
        
        # Clustering para segmentación
        if any(word in task_lower for word in ["segmentar", "agrupar", "cluster", "categorizar"]):
            return "Clustering Analysis"
        
        # Classification para categorización
        if any(word in task_lower for word in ["clasificar", "categoría", "predecir clase"]):
            return "Classification"
        
        # Time series para datos temporales
        if any(word in task_lower for word in ["serie temporal", "tendencia", "estacionalidad", "tiempo"]):
            return "Time Series Analysis"
        
        return "Exploratory Data Analysis"
    
    async def exploratory_analysis(self, data_description: str) -> Dict[str, Any]:
        """
        Realiza análisis exploratorio de datos
        
        Args:
            data_description: Descripción de los datos
            
        Returns:
            EDA completo
        """
        return await self.process_task(
            f"Realiza un análisis exploratorio de estos datos:\n{data_description}",
            context={"analysis_type": "exploratory"}
        )
    
    async def build_model(self, problem: str, data_description: str, target: str) -> Dict[str, Any]:
        """
        Construye modelo de machine learning
        
        Args:
            problem: Descripción del problema
            data_description: Descripción de los datos
            target: Variable objetivo
            
        Returns:
            Diseño de modelo y código
        """
        return await self.process_task(
            f"Construye un modelo de ML para: {problem}\nDatos: {data_description}\nTarget: {target}",
            context={"task_type": "model_building"}
        )
    
    async def ab_test_design(self, hypothesis: str, metrics: List[str]) -> Dict[str, Any]:
        """
        Diseña experimento A/B
        
        Args:
            hypothesis: Hipótesis a probar
            metrics: Métricas a medir
            
        Returns:
            Diseño de experimento
        """
        metrics_text = ", ".join(metrics)
        
        return await self.process_task(
            f"Diseña un A/B test para probar: {hypothesis}\nMétricas: {metrics_text}",
            context={"task_type": "experiment_design"}
        )
    
    async def interpret_results(self, results: str, context_info: str) -> Dict[str, Any]:
        """
        Interpreta resultados estadísticos
        
        Args:
            results: Resultados del análisis
            context_info: Contexto del negocio
            
        Returns:
            Interpretación y recomendaciones
        """
        return await self.process_task(
            f"Interpreta estos resultados:\n{results}\n\nContexto: {context_info}",
            context={"task_type": "interpretation"}
        )
