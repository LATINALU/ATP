"""
Configuración del backend ATP con Groq como proveedor predeterminado.
Siempre se solicitará al menos una API key de Groq.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Model configurations (todos requieren Groq)
DEFAULT_GROQ_MODEL = "openai/gpt-oss-120b"

MODELS = {
    "groq-default": {
        "provider": "groq",
        "model": DEFAULT_GROQ_MODEL,
        "api_key": GROQ_API_KEY,
        "base_url": "https://api.groq.com/openai/v1",
    },
    "groq-llama": {
        "provider": "groq",
        "model": "llama-3.3-70b-versatile",
        "api_key": GROQ_API_KEY,
        "base_url": "https://api.groq.com/openai/v1",
    },
    "groq-mixtral": {
        "provider": "groq",
        "model": "mixtral-8x7b-32768",
        "api_key": GROQ_API_KEY,
        "base_url": "https://api.groq.com/openai/v1",
    },
}

# Default model
DEFAULT_MODEL = "groq-default"

# Server config
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# CORS origins
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
]
