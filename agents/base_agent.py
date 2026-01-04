"""
Clase base para todos los agentes ATP con capacidades avanzadas de razonamiento
"""
from crewai import Agent
from langchain_openai import ChatOpenAI
from config.settings import OPENAI_API_KEY, OPENAI_MODEL, AGENT_CONFIG


class BaseAgent:
    """
    Clase base que proporciona capacidades de razonamiento profundo a todos los agentes.
    Implementa Chain-of-Thought (CoT) y razonamiento estructurado.
    """
    
    REASONING_FRAMEWORK = """
    MARCO DE RAZONAMIENTO PROFUNDO:
    
    1. COMPRENSIÓN: Analiza completamente el problema antes de actuar
       - ¿Qué se está pidiendo exactamente?
       - ¿Cuáles son los requisitos implícitos y explícitos?
       - ¿Qué información falta o necesito clarificar?
    
    2. DESCOMPOSICIÓN: Divide problemas complejos en partes manejables
       - Identifica subproblemas independientes
       - Establece dependencias entre componentes
       - Prioriza por impacto y urgencia
    
    3. ANÁLISIS MULTI-PERSPECTIVA: Considera múltiples ángulos
       - ¿Qué diría un experto en este dominio?
       - ¿Cuáles son los casos edge o excepciones?
       - ¿Qué podría salir mal?
    
    4. SÍNTESIS: Integra hallazgos en una solución coherente
       - Combina insights de diferentes análisis
       - Verifica consistencia interna
       - Valida contra requisitos originales
    
    5. METACOGNICIÓN: Evalúa tu propio razonamiento
       - ¿Mi respuesta es completa y precisa?
       - ¿He considerado alternativas?
       - ¿Qué nivel de confianza tengo en esta respuesta?
    """
    
    def __init__(self, level: int, name: str, role: str, goal: str, backstory: str, tools: list = None):
        self.level = level
        self.name = name
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.tools = tools or []
        self._agent = None
    
    def _get_llm(self):
        """Obtiene el modelo de lenguaje configurado"""
        return ChatOpenAI(
            model=OPENAI_MODEL,
            api_key=OPENAI_API_KEY,
            temperature=0.7,
        )
    
    def _build_enhanced_backstory(self) -> str:
        """Construye un backstory enriquecido con capacidades de razonamiento"""
        return f"""
        {self.backstory}
        
        {self.REASONING_FRAMEWORK}
        
        PRINCIPIOS OPERATIVOS:
        - Siempre explica tu proceso de pensamiento paso a paso
        - Cuando enfrentes incertidumbre, expresa tu nivel de confianza
        - Busca clarificación antes de asumir
        - Prioriza precisión sobre velocidad
        - Colabora efectivamente con otros agentes cuando sea necesario
        - Documenta decisiones importantes y su justificación
        
        NIVEL DE IMPORTANCIA: {self.level} - {self._get_level_description()}
        """
    
    def _get_level_description(self) -> str:
        """Obtiene la descripción del nivel de importancia"""
        descriptions = {
            1: "CRÍTICO - Eres parte del núcleo de razonamiento del sistema",
            2: "ESENCIAL - Proporcionas capacidades fundamentales",
            3: "ESPECIALIZADO - Eres experto en un dominio específico",
            4: "SOPORTE - Garantizas calidad y mantenimiento",
            5: "AUXILIAR - Complementas las funciones principales"
        }
        return descriptions.get(self.level, "No definido")
    
    def create_agent(self) -> Agent:
        """Crea y retorna el agente de CrewAI"""
        if self._agent is None:
            self._agent = Agent(
                role=self.role,
                goal=self.goal,
                backstory=self._build_enhanced_backstory(),
                tools=self.tools,
                llm=self._get_llm(),
                verbose=AGENT_CONFIG["verbose"],
                allow_delegation=AGENT_CONFIG["allow_delegation"],
                max_iter=AGENT_CONFIG["max_iter"],
                max_rpm=AGENT_CONFIG["max_rpm"],
            )
        return self._agent
    
    def get_info(self) -> dict:
        """Retorna información del agente"""
        return {
            "name": self.name,
            "level": self.level,
            "role": self.role,
            "goal": self.goal,
        }
