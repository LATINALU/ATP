"""
Configuración central del sistema ATP (Agentes de Tareas Polivalentes)
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Configuración de OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")

# Configuración de agentes
AGENT_CONFIG = {
    "verbose": True,
    "allow_delegation": True,
    "max_iter": 15,
    "max_rpm": 10,
}

# Niveles de importancia de agentes
AGENT_LEVELS = {
    1: "CRÍTICO - Núcleo de razonamiento",
    2: "ESENCIAL - Capacidades fundamentales", 
    3: "ESPECIALIZADO - Dominios específicos",
    4: "SOPORTE - Calidad y mantenimiento",
    5: "AUXILIAR - Funciones complementarias"
}

# Mapeo de tareas a agentes recomendados
TASK_AGENT_MAPPING = {
    "analisis": ["reasoning_agent", "analysis_agent", "synthesis_agent"],
    "codigo": ["coding_agent", "technical_agent", "qa_agent"],
    "escritura": ["writing_agent", "creative_agent", "formatting_agent"],
    "investigacion": ["research_agent", "data_agent", "summary_agent"],
    "planificacion": ["planning_agent", "decision_agent", "coordination_agent"],
    "legal": ["legal_agent", "validation_agent", "documentation_agent"],
    "financiero": ["financial_agent", "data_agent", "analysis_agent"],
    "educativo": ["educational_agent", "explanation_agent", "summary_agent"],
    "creativo": ["creative_agent", "writing_agent", "formatting_agent"],
    "tecnico": ["technical_agent", "coding_agent", "optimization_agent"],
}
