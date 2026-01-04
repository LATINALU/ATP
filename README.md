<<<<<<< HEAD
# ATP - Agentes de Tareas Polivalentes

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-green.svg" alt="Version">
  <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License">
  <img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PRs Welcome">
  <img src="https://img.shields.io/badge/python-3.11+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/next.js-14-black.svg" alt="Next.js">
</p>

Sistema de **30 Agentes de IA** con CrewAI, organizados en 5 niveles de importancia, diseñados para resolver cualquier tipo de tarea con capacidad extrema de razonamiento.

## 🚀 Características

- **30 Agentes especializados** organizados por niveles de importancia
- **Interfaz Web moderna** con diseño cyberpunk/hacker (React + Next.js + TailwindCSS)
- **Múltiples proveedores de IA**: OpenAI, DeepSeek, Groq, OpenRouter y más
- **Configuración dinámica de APIs** desde la interfaz
- **Selección de modelo por agente** - cada agente puede usar un modelo diferente
- **Razonamiento profundo** con Chain-of-Thought integrado
- **Selección automática** de agentes según la tarea
- **Ejecución en Docker** para portabilidad
- **API REST** con FastAPI
- **Temas personalizables** (Cyberpunk, Matrix, Neon, etc.)

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
| `legal_agent` | Aspectos legales y cumplimiento |
| `financial_agent` | Análisis financiero y económico |
| `creative_agent` | Creatividad e innovación |
| `technical_agent` | Arquitectura técnica y sistemas |
| `educational_agent` | Enseñanza y diseño instruccional |
| `marketing_agent` | Marketing y estrategia comercial |

### Nivel 4 - SOPORTE (Calidad y Mantenimiento)
| Agente | Función |
|--------|---------|
| `qa_agent` | Quality Assurance y testing |
| `documentation_agent` | Documentación técnica |
| `optimization_agent` | Optimización y rendimiento |
| `security_agent` | Seguridad de la información |
| `integration_agent` | Integración de sistemas y APIs |
| `review_agent` | Revisión y feedback constructivo |

### Nivel 5 - AUXILIARES (Funciones Complementarias)
| Agente | Función |
|--------|---------|
| `translation_agent` | Traducción y localización |
| `summary_agent` | Resumen y condensación |
| `formatting_agent` | Formato y presentación |
| `validation_agent` | Validación y verificación |
| `coordination_agent` | Coordinación de equipos |
| `explanation_agent` | Explicación de conceptos |

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

**Desarrollado con ❤️ usando CrewAI, FastAPI y Next.js**
=======

>>>>>>> c87baecc3169cff7d8a25b166435b778b08b7ed2
