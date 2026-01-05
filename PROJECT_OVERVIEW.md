# Agentic Task Platform (ATP) – Vision General v0.6.6

Este documento resume cómo funciona el proyecto completo para facilitar futuras depuraciones y limpieza de código.

---
## 1. Pila tecnológica
- **Frontend**: Next.js/React (app router), Tailwind + componentes UI personalizados.
- **Backend**: FastAPI en Python, 30 agentes especializados corriendo sobre LangGraph.
- **Modelo LLM**: Groq obligatorio (`openai/gpt-oss-120b` por defecto). Todo el flujo exige una API key válida de Groq.
- **Infraestructura local**: Docker Compose levanta `frontend`, `backend` y `agents`.

---
## 2. Flujo completo
1. **Usuario** abre `http://localhost:3000` y selecciona agentes en el sidebar.
2. **Modal de ⚙️ Configuración (ApiSettings)** registra proveedores y API keys. Ahora solo se considera Groq:
   - La UI guarda providers en `localStorage` (`atp-api-providers`).
   - Si no hay un provider Groq activo, el frontend bloquea cualquier envío.
3. **ChatInterface** arma el mensaje (texto + adjuntos) y lo envía a `/api/chat` con:
   ```json
   {
     "message": "...",
     "agents": ["reasoning", ...],
     "model": "openai/gpt-oss-120b",
     "apiConfig": { "type": "groq", "api_key": "...", ... }
   }
   ```
4. **Backend FastAPI** valida y construye instancias de agentes (`ReasoningAgent`, etc.) pasando el `model` y `api_config` recibidos.
5. **AgentOrchestrator** (LangGraph) coordina los agentes seleccionados y genera el `final_result`.
6. **Respuesta** vuelve al frontend y se muestra en el chat, guardándose también en el panel de memoria si el usuario lo decide.

---
## 3. Backend (carpeta `backend/app`)
### 3.1 `config.py`
- Define `GROQ_API_KEY` y modelos disponibles: `groq-default`, `groq-llama`, `groq-mixtral`.
- `DEFAULT_MODEL = "groq-default"` (alias de `openai/gpt-oss-120b`).
- Todo se conecta al endpoint de Groq `https://api.groq.com/openai/v1`.

### 3.2 `main.py`
- Endpoints principales:
  - `GET /api/health` – estado del servidor.
  - `GET /api/agents` – lista de los 30 agentes.
  - `GET /api/models` – modelos definidos en `config.py` (todos Groq).
  - `POST /api/fetch-models` – helper para detectar modelos disponibles de un provider.
  - `POST /api/chat` – punto central de procesamiento.
- Mapea IDs de agentes a clases concretas y ejecuta `orchestrator.execute(...)`.

### 3.3 `llm_providers.py`
- Wrapper sobre el SDK oficial de OpenAI apuntando a los endpoints Groq.
- `get_openai_client` valida `api_config` y, si no existe, usa la variable de entorno `GROQ_API_KEY`. Ahora el fallback se basa exclusivamente en Groq.

### 3.4 Agentes
- Residen en `backend/app/agents/` (30 archivos). Comparten `BaseAgent` y reciben dos parámetros críticos (`model` y `api_config`).

---
## 4. Frontend (carpeta `frontend/src`)
### 4.1 `app/page.tsx`
- Contenedor principal. Estados claves:
  - `model`: inicia en `openai/gpt-oss-120b`.
  - `apiProviders`: providers configurados desde `ApiSettings`.
  - `availableModels`: se llena con los modelos habilitados del provider Groq.
- `handleSendMessage` ahora exige:
  - Haber configurado al menos un provider Groq activo.
  - Mostrar alertas amigables cuando falta la API key.

### 4.2 Componentes relevantes
- **`Sidebar`**: selección de agentes por niveles, sin dependencias nuevas.
- **`ChatInterface`**: manejo de mensajes, adjuntos, atajos. Llama a `onSendMessage`.
- **`MemoryPanel`**: guarda conversaciones en `localStorage` (`atp-memories`).
- **`ApiSettings`**: único lugar donde se configuran API keys. Aunque soporta múltiples proveedores, el flujo actual solo considera Groq para enviar mensajes.

### 4.3 Almacenamiento local
- `atp-api-providers`: providers activos + API keys.
- `atp-agent-models`, `atp-agent-instructions`: personalizaciones por agente.
- `atp-memories`: historial guardado desde el panel de memoria.

---
## 5. Dependencias y configuración
- `.env` debe contener al menos: `GROQ_API_KEY=sk-...`
- Docker Compose levanta todo con `docker-compose up -d`.
- Health check: `curl http://localhost:3000/api/health` (o `/api/health` vía backend).

---
## 6. Código pendiente de depurar
1. **ApiSettings** aún muestra proveedores no Groq. Futuro cleanup:
   - Simplificar UI para enfocarla 100% en Groq.
   - Eliminar lógica y llamados a otros providers si ya no se usarán.
2. **MemoryPanel**: migrar a una solución persistente (opcional). Por ahora sigue con `localStorage`.
3. **Hooks y helpers**: revisar `useVersionSync`, `versionManager`, etc., si no se utilizan en la nueva UX.
4. **Backend**: confirmar si `/api/quick-chat` y endpoints de detección de modelos siguen siendo necesarios.

---
## 7. Próximos pasos sugeridos
1. **Depuración de frontend**: remover soporte visual a proveedores extras, dejar un flujo claro solo para Groq.
2. **Validar fallback**: si no hay modelos disponibles, el frontend ya muestra `GROQ_FALLBACK_MODELS`. Revisar copy y UI.
3. **Documentar APIs**: añadir en README instrucciones rápidas (Docker + GROQ_API_KEY).
4. **Pruebas end-to-end**: verificar que los 30 agentes reciben `api_config` correctamente usando `openai/gpt-oss-120b`.

---
### Resumen
- **Modelo por defecto**: `openai/gpt-oss-120b` (Groq).
- **Requisito obligatorio**: API key de Groq configurada en ⚙️.
- **Estructura**: se mantiene intacta, sin páginas de pruebas alternativas.
- **Este documento** servirá como referencia para continuar con la limpieza de código y garantizar que el sistema base funcione solo con la estructura oficial.
