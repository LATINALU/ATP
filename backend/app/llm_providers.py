"""
Proveedores de LLM para múltiples APIs
Usa OpenAI SDK compatible con todos los proveedores principales
"""
from langchain_openai import ChatOpenAI
from typing import Optional, Dict, Any
from app.config import MODELS, DEEPSEEK_API_KEY, GROQ_API_KEY

# Configuración de proveedores con sus endpoints y modelos por defecto
PROVIDERS = {
    "openai": {
        "base_url": "https://api.openai.com/v1",
        "model": "gpt-4o-mini",
    },
    "groq": {
        "base_url": "https://api.groq.com/openai/v1",
        "model": "llama-3.3-70b-versatile",
    },
    "deepseek": {
        "base_url": "https://api.deepseek.com/v1",
        "model": "deepseek-chat",
    },
    "together": {
        "base_url": "https://api.together.xyz/v1",
        "model": "meta-llama/Llama-3.3-70B-Instruct-Turbo",
    },
    "openrouter": {
        "base_url": "https://openrouter.ai/api/v1",
        "model": "openai/gpt-4o-mini",
    },
    "mistral": {
        "base_url": "https://api.mistral.ai/v1",
        "model": "mistral-large-latest",
    },
    "ollama": {
        "base_url": "http://localhost:11434/v1",
        "model": "llama3.2",
    },
    "anthropic": {
        "base_url": "https://api.anthropic.com/v1",
        "model": "claude-3-5-sonnet-20241022",
    },
    "cohere": {
        "base_url": "https://api.cohere.ai/v1",
        "model": "command-r-plus",
    },
}


def get_llm_from_config(api_config: Dict[str, Any]):
    """
    Crea un LLM usando OpenAI SDK (compatible con todos los proveedores).
    """
    api_type = api_config.get("type", "openai")
    api_key = api_config.get("api_key", "")
    custom_base_url = api_config.get("base_url")
    
    if not api_key:
        raise ValueError("API key es requerida. Configúrala en ⚙️ Configuración.")
    
    # Obtener configuración del proveedor
    provider_config = PROVIDERS.get(api_type, PROVIDERS["openai"])
    base_url = custom_base_url or provider_config["base_url"]
    model = provider_config["model"]
    
    return ChatOpenAI(
        model=model,
        api_key=api_key,
        base_url=base_url,
        temperature=0.7,
        max_tokens=4096,
    )


def get_llm(model_id: str = "deepseek", api_config: Optional[Dict[str, Any]] = None):
    """
    Obtiene el LLM configurado según el modelo seleccionado.
    Si se proporciona api_config, usa la configuración del usuario.
    """
    # Si hay configuración del usuario, usarla
    if api_config and api_config.get("api_key"):
        return get_llm_from_config(api_config)
    
    # Fallback a configuración por defecto (variables de entorno)
    if model_id not in MODELS:
        model_id = "deepseek"
    
    model_config = MODELS[model_id]
    provider = model_config["provider"]
    
    if provider == "deepseek":
        if not DEEPSEEK_API_KEY:
            raise ValueError("DeepSeek API key not configured. Please add your API key in Settings.")
        return ChatOpenAI(
            model=model_config["model"],
            api_key=DEEPSEEK_API_KEY,
            base_url=model_config["base_url"],
            temperature=0.7,
            max_tokens=4096,
        )
    elif provider == "groq":
        if not GROQ_API_KEY:
            raise ValueError("Groq API key not configured. Please add your API key in Settings.")
        return ChatGroq(
            model=model_config["model"],
            api_key=GROQ_API_KEY,
            temperature=0.7,
            max_tokens=4096,
        )
    else:
        raise ValueError(f"No API key configured for {provider}. Please add your API key in Settings.")


def test_connection(model_id: str = "deepseek", api_config: Optional[Dict[str, Any]] = None) -> bool:
    """Prueba la conexión con el modelo"""
    try:
        llm = get_llm(model_id, api_config)
        response = llm.invoke("Responde solo 'OK'")
        return "OK" in response.content or len(response.content) > 0
    except Exception as e:
        print(f"Error testing {model_id}: {e}")
        return False
