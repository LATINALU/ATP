"""
Configuración del backend ATP con soporte para DeepSeek y Groq
"""
import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Model configurations
MODELS = {
    "deepseek": {
        "provider": "deepseek",
        "model": "deepseek-chat",
        "api_key": DEEPSEEK_API_KEY,
        "base_url": "https://api.deepseek.com/v1",
    },
    "groq-llama": {
        "provider": "groq",
        "model": "llama-3.3-70b-versatile",
        "api_key": GROQ_API_KEY,
    },
    "groq-mixtral": {
        "provider": "groq",
        "model": "mixtral-8x7b-32768",
        "api_key": GROQ_API_KEY,
    },
}

# Default model
DEFAULT_MODEL = "deepseek"

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
