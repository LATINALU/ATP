"""
ATP Backend - FastAPI Server
Servidor principal para el sistema de agentes ATP
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import CORS_ORIGINS, MODELS, HOST, PORT
from app.models import ChatRequest, ChatResponse, HealthResponse, AgentInfo
from app.agent_service import AgentService, AGENT_DEFINITIONS
from app.api_models import fetch_available_models, get_model_description
from pydantic import BaseModel
from typing import List, Optional


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager for the app"""
    print("🚀 ATP Backend iniciando...")
    print(f"📡 Modelos disponibles: {list(MODELS.keys())}")
    print(f"🤖 Agentes disponibles: {len(AGENT_DEFINITIONS)}")
    yield
    print("👋 ATP Backend cerrando...")


app = FastAPI(
    title="ATP - Agentes de Tareas Polivalentes",
    description="Sistema de 30 Agentes de IA con capacidad extrema de razonamiento",
    version="1.0.0",
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
        version="1.0.0",
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)
