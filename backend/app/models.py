"""
Modelos Pydantic para el API
"""
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum


class ModelType(str, Enum):
    DEEPSEEK = "deepseek"
    GROQ_LLAMA = "groq-llama"
    GROQ_MIXTRAL = "groq-mixtral"


class ApiConfig(BaseModel):
    """Configuración de API proporcionada por el usuario"""
    id: str
    name: str
    type: str
    apiKey: str
    baseUrl: Optional[str] = None
    models: List[str] = []
    isActive: bool = True


class ChatRequest(BaseModel):
    message: str
    agents: List[str]
    model: str = "deepseek"
    context: Optional[str] = None
    apiConfig: Optional[ApiConfig] = None


class ChatResponse(BaseModel):
    success: bool
    result: str
    agents_used: List[str]
    model_used: str
    error: Optional[str] = None


class AgentInfo(BaseModel):
    name: str
    role: str
    level: int
    goal: str


class HealthResponse(BaseModel):
    status: str
    version: str
    models_available: List[str]
    agents_count: int
