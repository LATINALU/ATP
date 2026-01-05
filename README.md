# ATP - Agentes de Tareas Polivalentes

<p align="center">
  <img src="https://img.shields.io/badge/version-2.0.0-green.svg" alt="Version">
  <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License">
  <img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PRs Welcome">
  <img src="https://img.shields.io/badge/python-3.11+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/next.js-14-black.svg" alt="Next.js">
  <img src="https://img.shields.io/badge/ReactFlow-11+-purple.svg" alt="ReactFlow">
</p>

Sistema de **30 Agentes de IA** con OpenAI SDK, organizados en 5 niveles de importancia, con **Node Workflow Editor** profesional para crear flujos de trabajo visuales complejos.

> **v2.0.0 - Node Workflow System**: Sistema completamente rediseñado con editor de nodos visual, 30 agentes organizados en 5 niveles, validación de conexiones por colores, 10 temas profesionales, y soporte multiidioma (ES/EN).

## 🚀 Características Principales

### 🎯 Sistema de Nodos Profesional
- **9 Tipos de Nodos**:
  - 🟣 **Prompt Principal** - Inicio del flujo con prompts +/-
  - 🔴 **Agent Level 1-5** - 30 agentes organizados en 5 niveles (6 por nivel)
  - 🟠 **AI Provider** - Configuración de modelos y parámetros
  - 🔵 **Output Base** - Resultados intermedios con cadenas de agentes
  - 🟢 **Output Final** - Resultado final con Copy/Save/View

### 🎨 Sistema de Handles por Color
- 🟣 **Morado** - Conexiones de Prompt
- 🟠 **Naranja** - Conexiones de AI Provider
- 🔵 **Azul** - Conexiones de datos entre agentes
- ✅ **Validación estricta** - Solo conexiones válidas permitidas

### 🌍 Características Avanzadas
- **30 Agentes especializados** filtrados por nivel
- **Doble interfaz**:
  - 💬 **Chat Interface** - Conversacional con memoria
  - 🔷 **Node Workflow Editor** - Visual con drag & drop
- **10 Temas profesionales** rediseñados (Corporate, Gamer, Cyborg, etc.)
- **Soporte multiidioma** (Español/Inglés) con toggle
- **Import/Export** de workflows en JSON
- **Múltiples proveedores**: OpenAI, DeepSeek, Groq, Anthropic, Ollama, Together AI, OpenRouter
- **Ejecución asíncrona** de workflows con validación
- **API REST** con FastAPI + Docker

---

## 📊 Arquitectura de Agentes

### Nivel 1 - CRÍTICOS (Núcleo de Razonamiento)
| Agente | Función |
|--------|---------|
| `reasoning_agent` | Razonamiento lógico, deducción, inducción |
| `planning_agent` | Planificación estratégica y gestión de proyectos |
| `research_agent` | Investigación profunda y síntesis de información |
| `analysis_agent` | Análisis y descomposición de problemas |
| `synthesis_agent` | Integración de conocimiento y generación de insights |
| `critical_thinking_agent` | Evaluación crítica y detección de falacias |

### Nivel 2 - ESENCIALES (Capacidades Fundamentales)
| Agente | Función |
|--------|---------|
| `coding_agent` | Programación y desarrollo de software |
| `writing_agent` | Escritura y comunicación profesional |
| `data_agent` | Análisis de datos y estadísticas |
| `communication_agent` | Comunicación interpersonal y stakeholders |
| `decision_agent` | Toma de decisiones estructurada |
| `problem_solving_agent` | Resolución creativa de problemas |

### Nivel 3 - ESPECIALIZADOS (Dominios Específicos)
| Agente | Función |
|--------|---------|
| `creative_agent` | Creatividad e innovación |
| `optimization_agent` | Optimización de procesos y eficiencia |
| `quality_agent` | Control de calidad y testing |
| `security_agent` | Seguridad y auditoría |
| `marketing_agent` | Marketing digital y SEO |
| `design_agent` | Diseño UX/UI y prototipado |

### Nivel 4 - SOPORTE (Calidad y Mantenimiento)
| Agente | Función |
|--------|---------|
| `documentation_agent` | Documentación técnica y tutoriales |
| `translation_agent` | Traducción y localización |
| `formatting_agent` | Formato y presentación |
| `review_agent` | Revisión y edición de contenido |
| `testing_agent` | Testing de software y QA |
| `support_agent` | Atención al cliente y soporte |

### Nivel 5 - AUXILIARES (Funciones Complementarias)
| Agente | Función |
|--------|---------|
| `summarization_agent` | Resumen y síntesis de información |
| `validation_agent` | Validación y verificación de datos |
| `extraction_agent` | Extracción y parsing de información |
| `classification_agent` | Clasificación y categorización |
| `conversion_agent` | Conversión de formatos |
| `monitoring_agent` | Monitoreo y seguimiento de procesos |

---

## 🐳 Instalación con Docker

### Prerrequisitos
- Docker Desktop instalado y ejecutándose
- API Key de OpenAI

### Pasos

1. **Configurar variables de entorno**
```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar .env y añadir tu API key
# OPENAI_API_KEY=sk-tu-api-key-aqui
```

2. **Construir y ejecutar**
```bash
# Construir la imagen
docker-compose build

# Ejecutar el sistema principal
docker-compose up atp-agents

# O ejecutar en modo interactivo
docker-compose run atp-interactive
```

---

## 💻 Instalación Local (sin Docker)

### Prerrequisitos
- Python 3.11+
- pip

### Pasos

1. **Crear entorno virtual**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Configurar variables de entorno**
```bash
cp .env.example .env
# Editar .env con tu OPENAI_API_KEY
```

4. **Ejecutar**
```bash
# Modo principal
python main.py

# Modo interactivo
python interactive.py
```

---

## 🎯 Uso

### Modo Principal
```bash
python main.py
```
Muestra un menú con opciones para ver agentes y ejecutar demos.

### Modo Interactivo
```bash
python interactive.py
```

**Comandos disponibles:**
- `/agentes` - Ver todos los agentes
- `/nivel N` - Ver agentes del nivel N (1-5)
- `/usar AGENTE` - Usar un agente específico
- `/historial` - Ver historial de la sesión
- `/limpiar` - Limpiar contexto
- `/ayuda` - Mostrar ayuda
- `/salir` - Terminar

**Ejemplo de uso:**
```
Tu tarea: Analiza las ventajas de usar microservicios vs monolito

Tu tarea: Escribe un email profesional para solicitar una reunión

Tu tarea: /usar coding_agent
Tarea: Crea una función en Python para ordenar una lista
```

---

## 🧠 Sistema Agentic RAG (v1.0.1)

El sistema ATP ahora incluye **Agentic RAG** (Generación Aumentada por Recuperación con Agentes), una arquitectura avanzada de 5 capas:

### Arquitectura de Capas

```
┌─────────────────────────────────────────────────────────────────┐
│  CAPA 1: INTERACCIÓN INICIAL                                    │
│  Usuario → Query → Agente Central                               │
├─────────────────────────────────────────────────────────────────┤
│  CAPA 2: CEREBRO DEL COORDINADOR                                │
│  ┌─────────────┐  ┌─────────────────────────────────┐          │
│  │   MEMORY    │  │         PLANNING                │          │
│  │ Short Term  │  │  ReACT + Chain of Thought       │          │
│  │ Long Term   │  │  Descomposición de tareas       │          │
│  └─────────────┘  └─────────────────────────────────┘          │
├─────────────────────────────────────────────────────────────────┤
│  CAPA 3: DELEGACIÓN DE TAREAS                                   │
│  Agente Central → Sub-Agentes Especializados (30 agentes)       │
├─────────────────────────────────────────────────────────────────┤
│  CAPA 4: MCP SERVERS (Model Context Protocol)                   │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐            │
│  │ Local Data   │ │Search Engine │ │ Cloud Engine │            │
│  │ (Archivos)   │ │ (Internet)   │ │ (AWS/Azure)  │            │
│  └──────────────┘ └──────────────┘ └──────────────┘            │
├─────────────────────────────────────────────────────────────────┤
│  CAPA 5: PROCESAMIENTO Y SALIDA                                 │
│  Síntesis → LLM → Respuesta Final → Usuario                     │
└─────────────────────────────────────────────────────────────────┘
```

### Componentes Principales

| Componente | Descripción |
|------------|-------------|
| **Central Agent** | Coordinador principal que orquesta todo el flujo |
| **Memory System** | Memoria a corto plazo (sesión) y largo plazo (persistente) |
| **Planning Engine** | ReACT + Chain of Thought para planificación inteligente |
| **MCP Servers** | Conexión con datos locales, búsqueda web y cloud |
| **Sub-Agent Manager** | Gestiona los 30 agentes especializados |

### Endpoints API Agentic RAG

```bash
# Consulta principal
POST /api/agentic-rag
{
  "query": "Tu consulta aquí",
  "agents": ["reasoning_agent", "coding_agent"],  # opcional
  "use_memory": true,
  "use_planning": true
}

# Estado del sistema
GET /api/agentic-rag/status

# Agentes disponibles
GET /api/agentic-rag/agents

# Almacenar conocimiento
POST /api/agentic-rag/memory/store?fact=...&category=...

# Limpiar sesión
POST /api/agentic-rag/session/clear

# Historial de consultas
GET /api/agentic-rag/history
```

---

## 🧠 Marco de Razonamiento

Cada agente implementa un marco de razonamiento profundo:

1. **COMPRENSIÓN** - Análisis completo del problema
2. **DESCOMPOSICIÓN** - División en partes manejables
3. **ANÁLISIS MULTI-PERSPECTIVA** - Múltiples ángulos
4. **SÍNTESIS** - Integración de hallazgos
5. **METACOGNICIÓN** - Evaluación del propio razonamiento

---

## 📁 Estructura del Proyecto

```
ATP/
├── agents/
│   ├── __init__.py
│   ├── base_agent.py          # Clase base con razonamiento
│   ├── agent_factory.py       # Fábrica de agentes
│   ├── level1_critical.py     # 6 agentes críticos
│   ├── level2_essential.py    # 6 agentes esenciales
│   ├── level3_specialized.py  # 6 agentes especializados
│   ├── level4_support.py      # 6 agentes de soporte
│   └── level5_auxiliary.py    # 6 agentes auxiliares
├── orchestrator/
│   ├── __init__.py
│   └── task_orchestrator.py   # Orquestador principal
├── config/
│   ├── __init__.py
│   └── settings.py            # Configuración central
├── tools/
│   ├── __init__.py
│   ├── search_tools.py        # Herramientas de búsqueda
│   └── web_tools.py           # Herramientas web
├── main.py                    # Punto de entrada principal
├── interactive.py             # Modo interactivo
├── requirements.txt           # Dependencias Python
├── Dockerfile                 # Imagen Docker
├── docker-compose.yml         # Orquestación Docker
├── .env.example              # Ejemplo de variables
└── README.md                 # Esta documentación
```

---

## ⚙️ Configuración Avanzada

### Variables de Entorno

| Variable | Descripción | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | API Key de OpenAI | Requerido |
| `OPENAI_MODEL` | Modelo a usar | `gpt-4o` |
| `SERPER_API_KEY` | API Key para búsquedas web | Opcional |

### Modelos Recomendados

- **gpt-4o** - Máximo razonamiento (recomendado)
- **gpt-4-turbo** - Balance rendimiento/costo
- **gpt-3.5-turbo** - Económico, menor capacidad

---

## 🔧 Personalización

### Añadir Nuevos Agentes

1. Crear clase heredando de `BaseAgent`
2. Definir `level`, `name`, `role`, `goal`, `backstory`
3. Registrar en el archivo de nivel correspondiente
4. Actualizar `TASK_KEYWORDS` en `agent_factory.py`

### Ejemplo:
```python
from agents.base_agent import BaseAgent

class MyCustomAgent(BaseAgent):
    def __init__(self, tools=None):
        super().__init__(
            level=3,
            name="my_custom_agent",
            role="Mi Rol Personalizado",
            goal="Objetivo del agente...",
            backstory="Historia y capacidades...",
            tools=tools
        )
```

---

## 📝 Licencia

MIT License - Uso libre para proyectos personales y comerciales.

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el repositorio
2. Crea una rama para tu feature
3. Envía un Pull Request

---

## 🖥️ Frontend (Interfaz Web)

El frontend es una aplicación moderna construida con:
- **Next.js 14** - Framework React
- **TailwindCSS** - Estilos
- **Radix UI** - Componentes accesibles
- **Lucide Icons** - Iconografía

### Instalación del Frontend

```bash
cd frontend
npm install
npm run dev
```

Abre [http://localhost:3000](http://localhost:3000) en tu navegador.

### Configuración de APIs

1. Haz clic en el icono ⚙️ (configuración)
2. Añade tus API keys (OpenAI, DeepSeek, Groq, etc.)
3. Haz clic en "Detectar Modelos" para ver los modelos disponibles
4. Selecciona el modelo orquestador en el header
5. Configura modelos específicos por agente en "Ver más"

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor lee [CONTRIBUTING.md](CONTRIBUTING.md) para más detalles.

### Formas de contribuir:
- 🐛 Reportar bugs
- 💡 Sugerir nuevas características
- 📝 Mejorar documentación
- 🔧 Enviar Pull Requests

### Áreas que necesitan ayuda:
- [ ] Mejorar la integración con más proveedores de IA
- [ ] Añadir más agentes especializados
- [ ] Mejorar el sistema de razonamiento
- [ ] Tests unitarios y de integración
- [ ] Documentación en inglés
- [ ] Optimización de rendimiento

---

**Desarrollado con ❤️ usando CrewAI, FastAPI, Next.js y Google ADK**
