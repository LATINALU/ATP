"""
Agent Factory - Fábrica central para crear y gestionar todos los agentes ATP
"""
from typing import Dict, List, Optional
from crewai import Agent

from agents.level1_critical import get_level1_agents
from agents.level2_essential import get_level2_agents
from agents.level3_specialized import get_level3_agents
from agents.level4_support import get_level4_agents
from agents.level5_auxiliary import get_level5_agents
from agents.base_agent import BaseAgent


class AgentFactory:
    """
    Fábrica central que gestiona la creación y selección de agentes.
    Implementa selección inteligente basada en el tipo de tarea.
    """
    
    # Mapeo de palabras clave a agentes recomendados
    TASK_KEYWORDS = {
        # Nivel 1 - Críticos
        "razonar": ["reasoning_agent", "critical_thinking_agent"],
        "pensar": ["reasoning_agent", "critical_thinking_agent"],
        "lógica": ["reasoning_agent", "critical_thinking_agent"],
        "analizar": ["analysis_agent", "reasoning_agent"],
        "análisis": ["analysis_agent", "data_agent"],
        "planificar": ["planning_agent", "coordination_agent"],
        "plan": ["planning_agent", "coordination_agent"],
        "estrategia": ["planning_agent", "decision_agent"],
        "investigar": ["research_agent", "analysis_agent"],
        "buscar": ["research_agent"],
        "sintetizar": ["synthesis_agent", "summary_agent"],
        "integrar": ["synthesis_agent", "integration_agent"],
        "evaluar": ["critical_thinking_agent", "review_agent"],
        "criticar": ["critical_thinking_agent", "review_agent"],
        
        # Nivel 2 - Esenciales
        "código": ["coding_agent", "technical_agent"],
        "programar": ["coding_agent", "technical_agent"],
        "desarrollar": ["coding_agent", "technical_agent"],
        "python": ["coding_agent"],
        "javascript": ["coding_agent"],
        "escribir": ["writing_agent", "creative_agent"],
        "redactar": ["writing_agent"],
        "texto": ["writing_agent", "formatting_agent"],
        "datos": ["data_agent", "analysis_agent"],
        "estadística": ["data_agent"],
        "métricas": ["data_agent", "financial_agent"],
        "comunicar": ["communication_agent", "writing_agent"],
        "presentar": ["communication_agent", "formatting_agent"],
        "decidir": ["decision_agent", "reasoning_agent"],
        "decisión": ["decision_agent", "planning_agent"],
        "problema": ["problem_solving_agent", "reasoning_agent"],
        "solución": ["problem_solving_agent", "creative_agent"],
        
        # Nivel 3 - Especializados
        "legal": ["legal_agent", "validation_agent"],
        "contrato": ["legal_agent"],
        "ley": ["legal_agent"],
        "finanzas": ["financial_agent", "data_agent"],
        "dinero": ["financial_agent"],
        "inversión": ["financial_agent"],
        "presupuesto": ["financial_agent", "planning_agent"],
        "creativo": ["creative_agent", "writing_agent"],
        "idea": ["creative_agent", "problem_solving_agent"],
        "innovar": ["creative_agent", "problem_solving_agent"],
        "técnico": ["technical_agent", "coding_agent"],
        "arquitectura": ["technical_agent"],
        "sistema": ["technical_agent", "integration_agent"],
        "enseñar": ["educational_agent", "explanation_agent"],
        "explicar": ["educational_agent", "explanation_agent"],
        "aprender": ["educational_agent", "research_agent"],
        "marketing": ["marketing_agent", "creative_agent"],
        "vender": ["marketing_agent", "communication_agent"],
        "marca": ["marketing_agent", "creative_agent"],
        
        # Nivel 4 - Soporte
        "calidad": ["qa_agent", "review_agent"],
        "testing": ["qa_agent", "validation_agent"],
        "probar": ["qa_agent", "validation_agent"],
        "documentar": ["documentation_agent", "writing_agent"],
        "documentación": ["documentation_agent"],
        "optimizar": ["optimization_agent", "technical_agent"],
        "mejorar": ["optimization_agent", "review_agent"],
        "rendimiento": ["optimization_agent", "technical_agent"],
        "seguridad": ["security_agent", "validation_agent"],
        "proteger": ["security_agent"],
        "vulnerabilidad": ["security_agent", "qa_agent"],
        "integrar": ["integration_agent", "technical_agent"],
        "conectar": ["integration_agent"],
        "api": ["integration_agent", "technical_agent"],
        "revisar": ["review_agent", "qa_agent"],
        "feedback": ["review_agent", "communication_agent"],
        
        # Nivel 5 - Auxiliares
        "traducir": ["translation_agent"],
        "idioma": ["translation_agent"],
        "inglés": ["translation_agent"],
        "español": ["translation_agent"],
        "resumir": ["summary_agent", "synthesis_agent"],
        "resumen": ["summary_agent"],
        "formato": ["formatting_agent"],
        "presentación": ["formatting_agent", "communication_agent"],
        "validar": ["validation_agent", "qa_agent"],
        "verificar": ["validation_agent", "qa_agent"],
        "coordinar": ["coordination_agent", "planning_agent"],
        "organizar": ["coordination_agent", "planning_agent"],
    }
    
    def __init__(self, tools: list = None):
        """Inicializa la fábrica con herramientas opcionales para los agentes"""
        self.tools = tools or []
        self._agents_cache = {}
        self._initialize_all_agents()
    
    def _initialize_all_agents(self):
        """Inicializa todos los agentes disponibles"""
        all_agents = {}
        all_agents.update(get_level1_agents(self.tools))
        all_agents.update(get_level2_agents(self.tools))
        all_agents.update(get_level3_agents(self.tools))
        all_agents.update(get_level4_agents(self.tools))
        all_agents.update(get_level5_agents(self.tools))
        self._agents_cache = all_agents
    
    def get_agent(self, agent_name: str) -> Optional[Agent]:
        """Obtiene un agente específico por nombre"""
        if agent_name in self._agents_cache:
            return self._agents_cache[agent_name].create_agent()
        return None
    
    def get_agents_by_level(self, level: int) -> Dict[str, Agent]:
        """Obtiene todos los agentes de un nivel específico"""
        return {
            name: agent.create_agent() 
            for name, agent in self._agents_cache.items() 
            if agent.level == level
        }
    
    def get_all_agents(self) -> Dict[str, Agent]:
        """Obtiene todos los agentes disponibles"""
        return {
            name: agent.create_agent() 
            for name, agent in self._agents_cache.items()
        }
    
    def select_agents_for_task(self, task_description: str, max_agents: int = 5) -> List[Agent]:
        """
        Selecciona automáticamente los agentes más apropiados para una tarea.
        Utiliza análisis de palabras clave y priorización por nivel.
        """
        task_lower = task_description.lower()
        agent_scores = {}
        
        # Calcular puntuación para cada agente basado en palabras clave
        for keyword, agents in self.TASK_KEYWORDS.items():
            if keyword in task_lower:
                for agent_name in agents:
                    if agent_name not in agent_scores:
                        agent_scores[agent_name] = 0
                    # Dar más peso a agentes de niveles más altos (críticos)
                    agent_level = self._agents_cache[agent_name].level
                    weight = 6 - agent_level  # Nivel 1 = peso 5, Nivel 5 = peso 1
                    agent_scores[agent_name] += weight
        
        # Si no hay coincidencias, usar agentes por defecto (nivel 1)
        if not agent_scores:
            agent_scores = {
                "reasoning_agent": 5,
                "analysis_agent": 4,
                "synthesis_agent": 3,
            }
        
        # Ordenar por puntuación y seleccionar los mejores
        sorted_agents = sorted(agent_scores.items(), key=lambda x: x[1], reverse=True)
        selected_names = [name for name, _ in sorted_agents[:max_agents]]
        
        return [self.get_agent(name) for name in selected_names]
    
    def get_agent_info(self, agent_name: str) -> Optional[dict]:
        """Obtiene información sobre un agente específico"""
        if agent_name in self._agents_cache:
            return self._agents_cache[agent_name].get_info()
        return None
    
    def list_all_agents(self) -> List[dict]:
        """Lista información de todos los agentes disponibles"""
        agents_info = []
        for name, agent in self._agents_cache.items():
            info = agent.get_info()
            agents_info.append(info)
        
        # Ordenar por nivel
        return sorted(agents_info, key=lambda x: (x['level'], x['name']))
    
    def get_agents_summary(self) -> str:
        """Genera un resumen legible de todos los agentes disponibles"""
        summary = []
        summary.append("=" * 60)
        summary.append("SISTEMA ATP - 30 AGENTES DE IA")
        summary.append("=" * 60)
        
        level_names = {
            1: "NIVEL 1 - CRÍTICOS (Núcleo de Razonamiento)",
            2: "NIVEL 2 - ESENCIALES (Capacidades Fundamentales)",
            3: "NIVEL 3 - ESPECIALIZADOS (Dominios Específicos)",
            4: "NIVEL 4 - SOPORTE (Calidad y Mantenimiento)",
            5: "NIVEL 5 - AUXILIARES (Funciones Complementarias)",
        }
        
        for level in range(1, 6):
            summary.append(f"\n{level_names[level]}")
            summary.append("-" * 50)
            
            level_agents = [
                agent for agent in self._agents_cache.values() 
                if agent.level == level
            ]
            
            for agent in level_agents:
                info = agent.get_info()
                summary.append(f"  • {info['name']}: {info['role']}")
        
        summary.append("\n" + "=" * 60)
        return "\n".join(summary)
