"""
Herramientas de búsqueda para los agentes ATP
"""
from crewai_tools import (
    SerperDevTool,
    WebsiteSearchTool,
)


def get_search_tools():
    """
    Retorna herramientas de búsqueda disponibles.
    Nota: Algunas requieren API keys adicionales.
    """
    tools = []
    
    try:
        # Búsqueda web con Serper (requiere SERPER_API_KEY)
        import os
        if os.getenv("SERPER_API_KEY"):
            tools.append(SerperDevTool())
    except Exception:
        pass
    
    return tools


def get_basic_tools():
    """Retorna herramientas básicas que no requieren API keys adicionales"""
    return []
