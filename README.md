# Agentic Task Platform (ATP)

<p align="center">
  <img src="https://img.shields.io/badge/version-0.9.0-orange.svg" alt="Version">
  <img src="https://img.shields.io/badge/status-alpha-yellow.svg" alt="Status">
  <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License">
  <img src="https://img.shields.io/badge/python-3.11+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/LangGraph-StateGraph-green.svg" alt="LangGraph">
  <img src="https://img.shields.io/badge/A2A_Protocol-Orchestrated-purple.svg" alt="A2A Protocol">
</p>

ATP es una plataforma agentic diseñada para equipos que necesitan coordinar **30 agentes especializados** mediante un pipeline visual y un backend unificado basado en **LangGraph + A2A Protocol**.  
La versión **0.9.0** alinea completamente **Node Workflow Editor**, **Chat Interface** y **Agent Orchestrator** bajo el flujo auditado:  
**User Query → LangGraph StateGraph → A2A Messages → Agents Cluster → A2A Responses → Synthesis → Final Result** (idéntico en backend y editor visual).

---

## 🚀 Highlights Clave

| Área | Novedades |
|------|-----------|
| **Orquestación** | Backend FastAPI con LangGraph StateGraph, agentes aislados y protocolo A2A para mensajes estructurados. El orquestador se registra como agente y cada ejecución queda trazada (`✅/❌`). |
| **Node Workflow Editor** | 7 nodos oficiales, handles color-coded y validaciones estrictas para recrear el pipeline real. El backend del editor usa exactamente el mismo estado LangGraph/A2A documentado. |
| **Chat Mode** | Conversación multiagente en tiempo real, uso opcional de API keys del usuario y fallback al modelo gratuito `llama-3.3-70b-versatile` de Groq configurado en backend. |
| **Memoria Conversacional** | Guardado con tags automáticos, filtros (favoritos / últimas 24h) y estadísticas rápidas. |
| **Docker Ready** | Un único `docker-compose.yml` levanta frontend (Next.js 14) y backend (FastAPI) con hot-reload. |
| **Documentación** | Nuevos manuales (`PROJECT_OVERVIEW.md`, `LANGGRAPH_A2A_ARCHITECTURE.md`, etc.) enfocados en operaciones y despliegue. |

---

## 🧬 Pipeline Oficial (LangGraph + A2A)

```
┌──────────────┐    ┌──────────────┐    ┌───────────────┐    ┌───────────────┐
│  User Query  │ -> │  LangGraph   │ -> │  A2A Messages │ -> │ Agents Cluster │
└──────────────┘    └──────────────┘    └───────────────┘    └───────────────┘
        │                    │                    │                    │
        ▼                    ▼                    ▼                    ▼
┌──────────────┐    ┌──────────────┐    ┌───────────────┐    ┌──────────────┐
│A2A Responses │ -> │  Synthesis   │ -> │  Final Result │ -> │ Frontend UI  │
└──────────────┘    └──────────────┘    └───────────────┘    └──────────────┘
```

Cada etapa está representada por un nodo React Flow con handles y reglas propias. Los `WorkflowExecutor` en frontend y `AgentOrchestrator` en backend comparten el mismo contrato `/api/chat`.

---

## 🧩 Node Workflow Editor (React Flow)

| Nodo | Descripción | Color de Handle |
|------|-------------|-----------------|
| **User Query Intake** | Prompt, contexto, persona y urgencia del usuario. | Cyan |
| **LangGraph StateGraph** | Estrategia, modelo, paralelismo y límites de agentes. | Fuchsia |
| **A2A Message Dispatch** | Configuración del canal A2A, prioridades y payloads. | Amber |
| **Agents Cluster** | Selección multi-nivel (hasta 30 agentes) + concurrencia. | Sky |
| **A2A Responses Collector** | Conteo de respuestas, timeout y auto-retry. | Indigo |
| **Synthesis Engine** | Estrategia de síntesis, tono, # secciones, trace. | Violet |
| **Final Result** | Presentación, exportación y acciones del output final. | Emerald |

🧠 *Solo se permiten conexiones que respeten los colores y el orden oficial del flujo.*

---

## 💬 Chat Interface

- Selección de agentes por nivel con contador visible (`✓ X / 30 activos`).
- Vista de razonamiento en vivo + progreso por agente.
- Configuración de modelos por agente y proveedor en el momento.
- Memoria conversacional moderna con favoritos, tags, filtros y snapshot de la conversación activa.
- El frontend envía siempre el pipeline completo al backend (`/api/chat`) para mantener la paridad con el editor visual.

---

## 👥 Catálogo de Agentes (30 perfiles)

### Nivel 1 – Núcleo de Razonamiento
`reasoning`, `planning`, `research`, `analysis`, `synthesis`, `critical_thinking`

### Nivel 2 – Producción Profesional
`coding`, `data`, `writing`, `communication`, `decision`, `problem_solving`

### Nivel 3 – Dominios Especializados
`legal`, `financial`, `creative`, `technical`, `educational`, `marketing`

### Nivel 4 – Soporte Operativo
`qa`, `documentation`, `optimization`, `security`, `integration`, `review`

### Nivel 5 – Auxiliares Estratégicos
`translation`, `summary`, `formatting`, `validation`, `coordination`, `explanation`

Cada agente cuenta con su propio módulo en `backend/app/agents/` y comparte una clase base `BaseAgent` con tracing, logging y configuración de modelo/API.

---

## 🐳 Getting Started con Docker

### Requisitos
- Docker Desktop / Podman
- Python 3.11+ (solo si quieres ejecutar localmente sin contenedores)
- Una API Key de **Groq** (el backend está configurado para usar `openai/gpt-oss-120b` vía Groq)

### Pasos
```bash
# 1. Clonar el proyecto
git clone https://github.com/LATINALU/ATP.git
cd ATP

# 2. Configurar variables (usa el template actualizado)
copy .env.example .env  # Windows
# edit .env y establece GROQ_API_KEY=tu_api_key_de_groq

# 3. Levantar todo el stack
docker-compose up -d --build

# Backend → http://localhost:8001/api/health
# Frontend → http://localhost:3000
```

> El backend monta el código como volumen (`./backend:/app`), por lo que cualquier cambio se refleja sin reconstruir la imagen. El frontend se sirve en modo producción (Next.js 14 build).

---

## 🧱 Estructura de Carpetas

```
ATP/
├── backend/
│   ├── app/
│   │   ├── agents/                 # 30 agentes especializados
│   │   ├── orchestrator.py         # LangGraph + A2A executor
│   │   ├── a2a_protocol.py         # Abstracción de mensajes A2A
│   │   ├── main.py                 # FastAPI endpoints (/api/chat, /api/health, etc.)
│   │   └── config.py               # Defaults (Groq models, CORS, etc.)
│   └── requirements.txt
├── frontend/
│   ├── src/app/page.tsx            # Chat mode
│   ├── src/app/nodes/page.tsx      # Node Workflow Editor
│   ├── src/components/             # UI system (AgentCard, MemoryPanel, ThemeSelector…)
│   └── src/lib/workflowExecutor.ts # Cliente que construye el payload del pipeline
├── docker-compose.yml
├── README.md
└── docs/
    ├── PROJECT_OVERVIEW.md
    ├── LANGGRAPH_A2A_ARCHITECTURE.md
    ├── IMPLEMENTATION_SUMMARY.md
    └── CLEANUP_REPORT.md
```

---

## 🔌 API Principal

### `POST /api/chat`
```json
{
  "message": "Describe la arquitectura del sistema.",
  "agents": ["reasoning", "synthesis", "documentation"],
  "model": "openai/gpt-oss-120b",
  "apiConfig": { "id": "groq", "...": "..." },
  "context": {
    "langgraph": {...},
    "a2a": {...},
    "synthesis": {...}
  }
}
```
Respuesta:
```json
{
  "success": true,
  "result": "Texto final.",
  "agents_used": ["reasoning", "synthesis", "documentation"],
  "model_used": "openai/gpt-oss-120b",
  "error": null
}
```

> **Nota:** Si el usuario no aporta `apiConfig`, el backend usa las credenciales Groq definidas en `backend/app/config.py`.

---

## 🧪 Desarrollo Local (sin Docker)

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001

# Frontend
cd frontend
npm install
npm run dev
```

Asegúrate de exponer `GROQ_API_KEY` en tu entorno antes de iniciar el backend.

---

## 🗺️ Roadmap
- [ ] Streaming de eventos A2A en tiempo real hacia el frontend.
- [ ] Persistencia de memorias en backend (actualmente solo LocalStorage).
- [ ] Integración con más proveedores vía `ApiSettings`.
- [ ] Testing e2e (Playwright) para garantir la paridad Chat ↔️ Nodes.

---

## 🤝 Contribuir
1. Haz fork del repo.
2. Crea una rama descriptiva (`feature/node-validation`).
3. Envía un PR siguiendo el flujo del pipeline (mantén sincronizados frontend y backend).

Sugerencias bienvenidas: bugs, mejoras de UI, nuevos agentes, optimización de LangGraph, etc.

---

## 📝 Licencia
MIT © LATINALU – uso libre para proyectos personales y comerciales.  
Por favor, enlaza este repositorio cuando reutilices componentes esenciales.
