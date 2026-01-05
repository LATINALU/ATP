"""
ATP Backend - FastAPI Server v0.6.6
Servidor principal para el sistema de agentes ATP con LangGraph y Protocolo A2A
Sistema de 30 Agentes Especializados - Professional UI/UX
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
from app.api_models import fetch_available_models, get_model_description
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

# Importar nuevo sistema de agentes con LangGraph
from app.orchestrator import AgentOrchestrator
from app.agents import (
    ReasoningAgent, PlanningAgent, ResearchAgent, AnalysisAgent, SynthesisAgent,
    CriticalThinkingAgent, CodingAgent, DataAgent, WritingAgent, CommunicationAgent,
    DecisionAgent, ProblemSolvingAgent, LegalAgent, FinancialAgent, CreativeAgent,
    TechnicalAgent, EducationalAgent, MarketingAgent, QAAgent, DocumentationAgent,
    OptimizationAgent, SecurityAgent, IntegrationAgent, ReviewAgent, TranslationAgent,
    SummaryAgent, FormattingAgent, ValidationAgent, CoordinationAgent, ExplanationAgent
)

# Definiciones de los 30 agentes
AGENT_DEFINITIONS = {
    "reasoning": {"name": "Reasoning Agent", "level": 1, "description": "Razonamiento lógico multi-paradigma"},
    "planning": {"name": "Planning Agent", "level": 1, "description": "Planificación estratégica y gestión de proyectos"},
    "research": {"name": "Research Agent", "level": 1, "description": "Investigación académica rigurosa"},
    "analysis": {"name": "Analysis Agent", "level": 1, "description": "Descomposición de problemas complejos"},
    "synthesis": {"name": "Synthesis Agent", "level": 1, "description": "Integración de conocimiento e insights"},
    "critical_thinking": {"name": "Critical Thinking Agent", "level": 1, "description": "Evaluación crítica y detección de falacias"},
    "coding": {"name": "Coding Agent", "level": 2, "description": "Desarrollo de software y arquitectura"},
    "data": {"name": "Data Agent", "level": 2, "description": "Ciencia de datos y análisis cuantitativo"},
    "writing": {"name": "Writing Agent", "level": 2, "description": "Escritura profesional y contenido"},
    "communication": {"name": "Communication Agent", "level": 2, "description": "Comunicación efectiva y resolución de conflictos"},
    "decision": {"name": "Decision Agent", "level": 2, "description": "Análisis de decisiones y teoría de juegos"},
    "problem_solving": {"name": "Problem Solving Agent", "level": 2, "description": "Solución creativa con TRIZ y Design Thinking"},
    "legal": {"name": "Legal Agent", "level": 3, "description": "Análisis legal y cumplimiento normativo"},
    "financial": {"name": "Financial Agent", "level": 3, "description": "Análisis financiero y valoración"},
    "creative": {"name": "Creative Agent", "level": 3, "description": "Pensamiento creativo e innovación"},
    "technical": {"name": "Technical Agent", "level": 3, "description": "Arquitectura técnica y sistemas distribuidos"},
    "educational": {"name": "Educational Agent", "level": 3, "description": "Pedagogía y diseño instruccional"},
    "marketing": {"name": "Marketing Agent", "level": 3, "description": "Estrategia de marketing y branding"},
    "qa": {"name": "QA Agent", "level": 4, "description": "Testing y aseguramiento de calidad"},
    "documentation": {"name": "Documentation Agent", "level": 4, "description": "Documentación técnica y knowledge management"},
    "optimization": {"name": "Optimization Agent", "level": 4, "description": "Performance y optimización de procesos"},
    "security": {"name": "Security Agent", "level": 4, "description": "Seguridad de la información y threat analysis"},
    "integration": {"name": "Integration Agent", "level": 4, "description": "Integraciones y arquitectura de APIs"},
    "review": {"name": "Review Agent", "level": 4, "description": "Revisión experta y feedback constructivo"},
    "translation": {"name": "Translation Agent", "level": 5, "description": "Traducción profesional y localización"},
    "summary": {"name": "Summary Agent", "level": 5, "description": "Síntesis y resumen de información"},
    "formatting": {"name": "Formatting Agent", "level": 5, "description": "Formato profesional y presentación visual"},
    "validation": {"name": "Validation Agent", "level": 5, "description": "Validación de datos y verificación"},
    "coordination": {"name": "Coordination Agent", "level": 5, "description": "Coordinación de tareas y gestión de flujos"},
    "explanation": {"name": "Explanation Agent", "level": 5, "description": "Explicaciones claras y comprensibles"},
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager for the app"""
    print("🚀 Agentic Task Platform v0.6.6 iniciando...")
    print(f"📡 Modelos disponibles: {list(MODELS.keys())}")
    print(f"🤖 30 Agentes Especializados con LangGraph y Protocolo A2A")
    print(f"🧠 Sistema de Orquestación con StateGraph")
    print(f"🎨 UI/UX Profesional - Grid 2 columnas, Estados mejorados")
    
    yield
    print("👋 Agentic Task Platform cerrando...")


app = FastAPI(
    title="Agentic Task Platform",
    description="Sistema de Agentes Especializados con LangGraph y Protocolo A2A - Professional UI/UX",
    version="0.6.6",
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
        version="0.6.6",
        models_available=list(MODELS.keys()),
        agents_count=len(AGENT_DEFINITIONS),
    )


@app.get("/api/agents")
async def get_agents():
    """Get all 30 specialized agents"""
    agents = []
    for agent_id, info in AGENT_DEFINITIONS.items():
        agents.append({
            "id": agent_id,
            "name": info["name"],
            "level": info["level"],
            "description": info["description"],
        })
    return {"agents": agents, "total": len(agents)}


@app.get("/api/agents/{agent_id}")
async def get_agent(agent_id: str):
    """Get a specific agent's information"""
    if agent_id not in AGENT_DEFINITIONS:
        raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")
    
    info = AGENT_DEFINITIONS[agent_id]
    return {
        "id": agent_id,
        "name": info["name"],
        "level": info["level"],
        "description": info["description"],
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
    Main chat endpoint - processes user messages with selected agents using LangGraph Orchestrator
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
        
        # Create orchestrator with selected agents
        orchestrator = AgentOrchestrator()
        
        # Map agent IDs to agent instances with model configuration
        agent_map = {
            "reasoning": ReasoningAgent(model=request.model, api_config=request.apiConfig),
            "planning": PlanningAgent(model=request.model, api_config=request.apiConfig),
            "research": ResearchAgent(model=request.model, api_config=request.apiConfig),
            "analysis": AnalysisAgent(model=request.model, api_config=request.apiConfig),
            "synthesis": SynthesisAgent(model=request.model, api_config=request.apiConfig),
            "critical_thinking": CriticalThinkingAgent(model=request.model, api_config=request.apiConfig),
            "coding": CodingAgent(model=request.model, api_config=request.apiConfig),
            "data": DataAgent(model=request.model, api_config=request.apiConfig),
            "writing": WritingAgent(model=request.model, api_config=request.apiConfig),
            "communication": CommunicationAgent(model=request.model, api_config=request.apiConfig),
            "decision": DecisionAgent(model=request.model, api_config=request.apiConfig),
            "problem_solving": ProblemSolvingAgent(model=request.model, api_config=request.apiConfig),
            "legal": LegalAgent(model=request.model, api_config=request.apiConfig),
            "financial": FinancialAgent(model=request.model, api_config=request.apiConfig),
            "creative": CreativeAgent(model=request.model, api_config=request.apiConfig),
            "technical": TechnicalAgent(model=request.model, api_config=request.apiConfig),
            "educational": EducationalAgent(model=request.model, api_config=request.apiConfig),
            "marketing": MarketingAgent(model=request.model, api_config=request.apiConfig),
            "qa": QAAgent(model=request.model, api_config=request.apiConfig),
            "documentation": DocumentationAgent(model=request.model, api_config=request.apiConfig),
            "optimization": OptimizationAgent(model=request.model, api_config=request.apiConfig),
            "security": SecurityAgent(model=request.model, api_config=request.apiConfig),
            "integration": IntegrationAgent(model=request.model, api_config=request.apiConfig),
            "review": ReviewAgent(model=request.model, api_config=request.apiConfig),
            "translation": TranslationAgent(model=request.model, api_config=request.apiConfig),
            "summary": SummaryAgent(model=request.model, api_config=request.apiConfig),
            "formatting": FormattingAgent(model=request.model, api_config=request.apiConfig),
            "validation": ValidationAgent(model=request.model, api_config=request.apiConfig),
            "coordination": CoordinationAgent(model=request.model, api_config=request.apiConfig),
            "explanation": ExplanationAgent(model=request.model, api_config=request.apiConfig),
        }
        
        # Get selected agent instances
        selected_agents = [agent_map[agent_id] for agent_id in request.agents if agent_id in agent_map]
        
        # Execute task with orchestrator
        result = await orchestrator.execute(
            task=request.message,
            agents=selected_agents,
            context=request.context or {}
        )
        
        return ChatResponse(
            success=True,
            result=result.get("final_result", ""),
            agents_used=request.agents,
            model_used=request.model,
            error=None,
        )
        
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        error_traceback = traceback.format_exc()
        print(f"❌ ERROR EN /api/chat: {str(e)}")
        print(f"📋 TRACEBACK:\n{error_traceback}")
        return ChatResponse(
            success=False,
            result="",
            agents_used=request.agents,
            model_used=request.model,
            error=str(e),
        )


@app.post("/api/quick-chat")
async def quick_chat(message: str, model: str = "gpt-4"):
    """
    Quick chat endpoint - uses default agents for simple queries
    """
    default_agents = ["reasoning", "synthesis"]
    
    orchestrator = AgentOrchestrator()
    
    agent_map = {
        "reasoning": ReasoningAgent(),
        "synthesis": SynthesisAgent(),
    }
    
    selected_agents = [agent_map[agent_id] for agent_id in default_agents]
    
    result = await orchestrator.execute(
        task=message,
        agents=selected_agents,
        context={}
    )
    
    return {
        "success": True,
        "result": result.get("final_result", ""),
        "model": model,
    }


# ============== SISTEMA COMPLETO ==============
# El sistema ATP v0.6.1 usa 30 agentes especializados con LangGraph
# Los endpoints principales son:
# - /api/chat: Chat con agentes seleccionados
# - /api/quick-chat: Chat rápido con agentes por defecto
# - /api/agents: Listar todos los agentes
# - /api/models: Listar modelos disponibles


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)
