"""
ATP Agentic RAG System v1.0.1
Sistema de Generación Aumentada por Recuperación con Agentes

Arquitectura:
- CAPA 1: Interacción Inicial (Query del usuario)
- CAPA 2: Cerebro del Coordinador (Memory + Planning)
- CAPA 3: Delegación de Tareas (Sub-agentes especializados)
- CAPA 4: Conexión con el Mundo Real (MCP Servers)
- CAPA 5: Procesamiento y Salida (Síntesis final)
"""

from .central_agent import CentralAgent, get_central_agent
from .memory import MemorySystem, ShortTermMemory, LongTermMemory
from .planning import PlanningEngine, ReACTPlanner, ChainOfThoughtPlanner
from .mcp_servers import MCPServerManager, LocalDataServer, SearchEngineServer, CloudEngineServer
from .sub_agents import SubAgentManager

__version__ = "1.0.1"
__all__ = [
    "CentralAgent",
    "get_central_agent",
    "MemorySystem",
    "ShortTermMemory", 
    "LongTermMemory",
    "PlanningEngine",
    "ReACTPlanner",
    "ChainOfThoughtPlanner",
    "MCPServerManager",
    "LocalDataServer",
    "SearchEngineServer",
    "CloudEngineServer",
    "SubAgentManager"
]
