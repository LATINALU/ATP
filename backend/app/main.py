"""
ATP Backend - FastAPI Server v1.0.1
Servidor principal para el sistema de agentes ATP con Agentic RAG
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import sys
import os

# Añadir path del proyecto para imports
sys.path.insert(0, '/app')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import CORS_ORIGINS, MODELS, HOST, PORT
from app.models import ChatRequest, ChatResponse, HealthResponse, AgentInfo
from app.agent_service import AgentService, AGENT_DEFINITIONS
from app.api_models import fetch_available_models, get_model_description
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

# Importar sistema Agentic RAG
try:
    from agentic_rag import CentralAgent, get_central_agent
    AGENTIC_RAG_AVAILABLE = True
except ImportError:
    AGENTIC_RAG_AVAILABLE = False
    print("⚠️ Agentic RAG no disponible - usando modo legacy")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager for the app"""
    print("🚀 Agentic Task Platform v2.0.1 iniciando...")
    print(f"📡 Modelos disponibles: {list(MODELS.keys())}")
    print(f"🤖 Agentes disponibles: {len(AGENT_DEFINITIONS)}")
    
    # Inicializar Agentic RAG si está disponible
    if AGENTIC_RAG_AVAILABLE:
        print("🧠 Inicializando sistema Agentic RAG...")
        central_agent = get_central_agent("./data")
        await central_agent.initialize()
        print("✅ Agentic RAG inicializado correctamente")
    
    yield
    print("👋 Agentic Task Platform cerrando...")


app = FastAPI(
    title="Agentic Task Platform",
    description="Sistema de 30 Agentes de IA con Agentic RAG y capacidad extrema de razonamiento",
    version="2.0.1",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        version="2.0.1",
        models_available=list(MODELS.keys()),
        agents_count=len(AGENT_DEFINITIONS),
    )


@app.get("/api/agents")
async def get_agents():
    """Get all available agents"""
    agents = []
    for name, info in AGENT_DEFINITIONS.items():
        agents.append({
            "name": name,
            "role": info["role"],
            "level": info["level"],
            "goal": info["goal"],
        })
    return {"agents": agents, "total": len(agents)}


@app.get("/api/agents/{agent_name}")
async def get_agent(agent_name: str):
    """Get a specific agent's information"""
    if agent_name not in AGENT_DEFINITIONS:
        raise HTTPException(status_code=404, detail=f"Agent {agent_name} not found")
    
    info = AGENT_DEFINITIONS[agent_name]
    return {
        "name": agent_name,
        "role": info["role"],
        "level": info["level"],
        "goal": info["goal"],
        "backstory": info["backstory"],
    }


@app.get("/api/models")
async def get_models():
    """Get available models"""
    return {
        "models": [
            {"id": model_id, "provider": config["provider"], "model": config["model"]}
            for model_id, config in MODELS.items()
        ]
    }


class FetchModelsRequest(BaseModel):
    """Request para obtener modelos de una API"""
    api_type: str
    api_key: str
    base_url: Optional[str] = None


@app.post("/api/fetch-models")
async def fetch_models(request: FetchModelsRequest):
    """
    Consulta una API para obtener los modelos disponibles.
    Útil para configurar qué modelo usar con cada agente.
    """
    try:
        models = await fetch_available_models(
            api_type=request.api_type,
            api_key=request.api_key,
            base_url=request.base_url
        )
        
        if not models:
            return {
                "success": False,
                "models": [],
                "error": "No se pudieron obtener los modelos. Verifica tu API key."
            }
        
        return {
            "success": True,
            "models": models,
            "count": len(models)
        }
    except Exception as e:
        return {
            "success": False,
            "models": [],
            "error": str(e)
        }


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint - processes user messages with selected agents
    """
    try:
        # Validate request
        if not request.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        if not request.agents:
            raise HTTPException(status_code=400, detail="At least one agent must be selected")
        
        # Validate agents
        invalid_agents = [a for a in request.agents if a not in AGENT_DEFINITIONS]
        if invalid_agents:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid agents: {invalid_agents}"
            )
        
        # Create agent service with selected model and API config
        api_config = None
        if request.apiConfig:
            api_config = {
                "type": request.apiConfig.type,
                "api_key": request.apiConfig.apiKey,
                "base_url": request.apiConfig.baseUrl,
            }
        
        service = AgentService(model_id=request.model, api_config=api_config)
        
        # Execute task
        result = service.execute_task(
            message=request.message,
            agent_names=request.agents,
            context=request.context,
        )
        
        return ChatResponse(
            success=result["success"],
            result=result["result"],
            agents_used=result["agents_used"],
            model_used=request.model,
            error=None if result["success"] else result.get("error"),
        )
        
    except HTTPException:
        raise
    except Exception as e:
        return ChatResponse(
            success=False,
            result="",
            agents_used=request.agents,
            model_used=request.model,
            error=str(e),
        )


@app.post("/api/quick-chat")
async def quick_chat(message: str, model: str = "deepseek"):
    """
    Quick chat endpoint - uses default agents for simple queries
    """
    default_agents = ["reasoning_agent", "synthesis_agent"]
    
    service = AgentService(model_id=model)
    result = service.execute_task(
        message=message,
        agent_names=default_agents,
    )
    
    return {
        "success": result["success"],
        "result": result["result"],
        "model": model,
    }


# ============== ENDPOINTS AGENTIC RAG ==============

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
