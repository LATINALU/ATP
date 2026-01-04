"""
ATP Backend - FastAPI Server v1.0.1 - Modo Agentic RAG
Servidor principal para el sistema ATP con Agentic RAG
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import sys
import os

# Añadir path del proyecto para imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from pydantic import BaseModel
from typing import List, Optional, Dict, Any

# Importar sistema Agentic RAG
try:
    from agentic_rag import CentralAgent, get_central_agent
    AGENTIC_RAG_AVAILABLE = True
    print("✅ Sistema Agentic RAG disponible")
except ImportError as e:
    AGENTIC_RAG_AVAILABLE = False
    print(f"⚠️ Agentic RAG no disponible: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager for the app"""
    print("🚀 ATP Backend v1.0.1 iniciando (Modo Agentic RAG)...")
    
    # Inicializar Agentic RAG si está disponible
    if AGENTIC_RAG_AVAILABLE:
        print("🧠 Inicializando sistema Agentic RAG...")
        central_agent = get_central_agent("./data")
        await central_agent.initialize()
        print("✅ Agentic RAG inicializado correctamente")
    
    yield
    print("👋 ATP Backend cerrando...")


app = FastAPI(
    title="ATP - Agentes de Tareas Polivalentes",
    description="Sistema de 30 Agentes de IA con Agentic RAG y capacidad extrema de razonamiento",
    version="1.0.1",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Modelos Pydantic
class HealthResponse(BaseModel):
    status: str
    version: str
    agentic_rag: bool
    message: str


class AgenticRAGRequest(BaseModel):
    """Request para el sistema Agentic RAG"""
    query: str
    agents: Optional[List[str]] = None
    use_memory: bool = True
    use_planning: bool = True
    model_id: Optional[str] = None
    api_config: Optional[Dict[str, Any]] = None


class AgenticRAGResponse(BaseModel):
    """Response del sistema Agentic RAG"""
    success: bool
    query: str
    response: str
    agents_used: List[str]
    sources_consulted: List[str]
    reasoning_trace: List[str]
    plan_id: Optional[str] = None
    error: Optional[str] = None


# Variables de configuración
HOST = "0.0.0.0"
PORT = 8000


@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        version="1.0.1",
        agentic_rag=AGENTIC_RAG_AVAILABLE,
        message="ATP Backend con Agentic RAG funcionando"
    )


@app.get("/api/agents")
async def get_agents():
    """Get all available agents"""
    if not AGENTIC_RAG_AVAILABLE:
        return {"agents": [], "total": 0, "error": "Agentic RAG no disponible"}
    
    central_agent = get_central_agent()
    agents = central_agent.get_available_agents()
    return {"agents": agents, "total": len(agents)}


@app.get("/api/models")
async def get_models():
    """Get available models"""
    return {
        "models": [
            {"id": "deepseek", "provider": "deepseek", "model": "deepseek-chat"},
            {"id": "groq-llama", "provider": "groq", "model": "llama-3.3-70b"},
        ]
    }


@app.post("/api/agentic-rag", response_model=AgenticRAGResponse)
async def agentic_rag_chat(request: AgenticRAGRequest):
    """
    Endpoint principal del sistema Agentic RAG
    Procesa consultas usando el flujo completo:
    1. Memoria (corto y largo plazo)
    2. Planificación (ReACT + CoT)
    3. Delegación a sub-agentes
    4. MCP Servers (datos locales, búsqueda, cloud)
    5. Síntesis final
    """
    if not AGENTIC_RAG_AVAILABLE:
        return AgenticRAGResponse(
            success=False,
            query=request.query,
            response="",
            agents_used=[],
            sources_consulted=[],
            reasoning_trace=["Agentic RAG no disponible"],
            error="Sistema Agentic RAG no inicializado"
        )
    
    try:
        central_agent = get_central_agent()
        
        # Configurar modelo si se especifica
        if request.model_id:
            central_agent.set_model(request.model_id)
        
        # Procesar consulta
        result = await central_agent.process_query(
            query=request.query,
            selected_agents=request.agents
        )
        
        return AgenticRAGResponse(
            success=True,
            query=result.query,
            response=result.response,
            agents_used=result.agents_used,
            sources_consulted=result.sources_consulted,
            reasoning_trace=result.reasoning_trace,
            plan_id=result.plan_id
        )
        
    except Exception as e:
        return AgenticRAGResponse(
            success=False,
            query=request.query,
            response="",
            agents_used=[],
            sources_consulted=[],
            reasoning_trace=[f"Error: {str(e)}"],
            error=str(e)
        )


@app.get("/api/agentic-rag/status")
async def agentic_rag_status():
    """Obtener estado del sistema Agentic RAG"""
    if not AGENTIC_RAG_AVAILABLE:
        return {"available": False, "error": "Agentic RAG no disponible"}
    
    central_agent = get_central_agent()
    return {
        "available": True,
        "status": central_agent.get_system_status()
    }


@app.get("/api/agentic-rag/agents")
async def agentic_rag_agents():
    """Obtener agentes disponibles en Agentic RAG"""
    if not AGENTIC_RAG_AVAILABLE:
        return {"available": False, "agents": []}
    
    central_agent = get_central_agent()
    return {
        "available": True,
        "agents": central_agent.get_available_agents()
    }


@app.post("/api/agentic-rag/memory/store")
async def store_memory(fact: str, category: str = "general"):
    """Almacenar conocimiento en memoria a largo plazo"""
    if not AGENTIC_RAG_AVAILABLE:
        return {"success": False, "error": "Agentic RAG no disponible"}
    
    central_agent = get_central_agent()
    entry = central_agent.store_knowledge(fact, category)
    return {
        "success": True,
        "entry_id": entry.id,
        "message": "Conocimiento almacenado correctamente"
    }


@app.post("/api/agentic-rag/session/clear")
async def clear_session():
    """Limpiar sesión actual (memoria a corto plazo)"""
    if not AGENTIC_RAG_AVAILABLE:
        return {"success": False, "error": "Agentic RAG no disponible"}
    
    central_agent = get_central_agent()
    central_agent.clear_session()
    return {"success": True, "message": "Sesión limpiada correctamente"}


@app.get("/api/agentic-rag/history")
async def get_history(limit: int = 20):
    """Obtener historial de consultas"""
    if not AGENTIC_RAG_AVAILABLE:
        return {"available": False, "history": []}
    
    central_agent = get_central_agent()
    return {
        "available": True,
        "history": central_agent.get_query_history(limit)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)
