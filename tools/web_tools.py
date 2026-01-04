"""
Herramientas web para los agentes ATP
"""
from crewai_tools import (
    ScrapeWebsiteTool,
    FileReadTool,
)


def get_web_tools():
    """
    Retorna herramientas web disponibles.
    """
    tools = []
    
    try:
        tools.append(ScrapeWebsiteTool())
    except Exception:
        pass
    
    try:
        tools.append(FileReadTool())
    except Exception:
        pass
    
    return tools
