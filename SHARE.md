# 🤖 ATP - Agentes de Tareas Polivalentes v2.0.0

## 🌐 Acceso a la Aplicación

**URL:** http://147.93.191.92

## 🎯 ¿Qué es ATP?

ATP es un sistema de **30 Agentes de IA especializados** organizados en 5 niveles, con un **Editor de Nodos Visual** para crear flujos de trabajo complejos.

## ✨ Características Principales

### 🔷 Editor de Nodos Visual
- Crea workflows arrastrando y conectando nodos
- 9 tipos de nodos diferentes
- Validación de conexiones por colores
- Import/Export de workflows

### 🤖 30 Agentes Especializados
- **Nivel 1**: Razonamiento, Planificación, Investigación
- **Nivel 2**: Programación, Escritura, Análisis de Datos
- **Nivel 3**: Creatividad, Optimización, Seguridad
- **Nivel 4**: Documentación, Traducción, Testing
- **Nivel 5**: Resumen, Validación, Clasificación

### 🎨 Personalización
- 10 temas profesionales
- Soporte Español/Inglés
- Configuración de múltiples proveedores de IA

## 🔐 Seguridad y Privacidad

### ✅ Tus API Keys son 100% Privadas

**IMPORTANTE:** Esta aplicación NO almacena tus credenciales en el servidor.

- ✅ Tus API keys se guardan **SOLO en tu navegador** (localStorage)
- ✅ **NUNCA** se envían al servidor
- ✅ Solo **TÚ** tienes acceso a tus credenciales
- ✅ Cada usuario usa sus propias API keys
- ✅ No hay base de datos de usuarios

**¿Cómo funciona?**
1. Configuras tus API keys en tu navegador
2. Se guardan localmente en tu dispositivo
3. Las peticiones a APIs se hacen directamente desde tu navegador
4. El servidor solo sirve la interfaz web

## 🚀 Cómo Empezar

### Paso 1: Configurar tus API Keys

1. Haz clic en el icono ⚙️ (Settings) en la esquina superior derecha
2. Agrega tus API keys de los proveedores que uses:
   - OpenAI: https://platform.openai.com/api-keys
   - Anthropic: https://console.anthropic.com/
   - Groq: https://console.groq.com/
   - DeepSeek: https://platform.deepseek.com/
   - Otros proveedores disponibles

3. Haz clic en "Detectar Modelos Disponibles"
4. Selecciona los modelos que quieres usar
5. Guarda la configuración

### Paso 2: Usar el Chat

1. Ve a la página principal
2. Selecciona un modelo orquestador en el header
3. Escribe tu consulta
4. Selecciona los agentes que quieres usar
5. ¡Envía y recibe respuestas!

### Paso 3: Crear Workflows Visuales

1. Ve a "Node Workflow Editor"
2. Arrastra nodos desde el sidebar
3. Conecta nodos según los colores:
   - 🟣 Morado: Prompts
   - 🟠 Naranja: AI Provider
   - 🔵 Azul: Datos entre agentes
4. Configura cada nodo
5. Ejecuta el workflow

## 🎨 Tipos de Nodos

| Nodo | Descripción | Handles |
|------|-------------|---------|
| **Prompt Principal** | Inicio del flujo | 1 salida morada 🟣 |
| **Agent L1-L5** | 30 agentes (6 por nivel) | 3 entradas (🟣🟠🔵) + 1 salida azul 🔵 |
| **AI Provider** | Configuración de modelo | 1 salida naranja 🟠 |
| **Output Base** | Resultado intermedio | 1 entrada azul 🔵 + 1 salida morada 🟣 |
| **Output Final** | Resultado final | 1 entrada azul 🔵 + botones Copy/Save/View |

## 🔗 Reglas de Conexión

```
🟣 Prompt → Agent (entrada morada)
🟠 AI Provider → Agent (entrada naranja)
🔵 Agent → Output Base (entrada azul)
🟣 Output Base → Agent (entrada morada)
🟣 Output Base → Output Final
```

## 💡 Ejemplos de Uso

### Ejemplo 1: Análisis Simple
```
[Prompt] → [Agent L1: Reasoning] → [Output Final]
           ↑
    [AI Provider: GPT-4]
```

### Ejemplo 2: Workflow Complejo
```
[Prompt] → [Agent L1: Research] → [Output Base] → [Agent L2: Writing] → [Output Final]
           ↑                       ↑
    [AI Provider: GPT-4]    [AI Provider: Claude]
```

### Ejemplo 3: Cadena de Agentes
```
[Prompt] → [Agent L1] → [Output Base] → [Agent L2] → [Output Base] → [Agent L3] → [Output Final]
```

## 🎓 Proveedores de IA Soportados

| Proveedor | Modelos Destacados | Obtener API Key |
|-----------|-------------------|-----------------|
| **OpenAI** | GPT-4o, GPT-4-turbo | https://platform.openai.com/ |
| **Anthropic** | Claude 3.5 Sonnet | https://console.anthropic.com/ |
| **Groq** | Llama 3, Mixtral | https://console.groq.com/ |
| **DeepSeek** | DeepSeek V2 | https://platform.deepseek.com/ |
| **Together AI** | Múltiples modelos | https://api.together.xyz/ |
| **OpenRouter** | 100+ modelos | https://openrouter.ai/ |
| **Ollama** | Modelos locales | https://ollama.ai/ |

## 📱 Funciones Adicionales

### Import/Export de Workflows
- Guarda tus workflows como archivos JSON
- Comparte workflows con otros usuarios
- Importa workflows de ejemplo

### Temas Personalizables
- Corporate (profesional)
- Gamer (vibrante)
- Minimalist (limpio)
- Cyborg (futurista)
- Y 6 temas más

### Multiidioma
- Español
- English
- Toggle rápido en el header

## ❓ Preguntas Frecuentes

### ¿Es gratis?
Sí, la aplicación es gratuita. Solo necesitas tus propias API keys de los proveedores de IA que quieras usar.

### ¿Mis API keys están seguras?
Sí, 100%. Se almacenan SOLO en tu navegador (localStorage) y nunca se envían al servidor.

### ¿Puedo usar la aplicación sin API keys?
No, necesitas configurar al menos un proveedor de IA para usar los agentes.

### ¿Qué pasa si borro mi navegador?
Perderás tu configuración local. Usa la función Export para hacer backup de tus workflows.

### ¿Puedo usar múltiples proveedores?
Sí, puedes configurar múltiples proveedores y elegir cuál usar en cada nodo.

### ¿Los workflows se guardan en el servidor?
No, se guardan en tu navegador (localStorage). Usa Export para guardarlos como archivos.

## 🆘 Soporte

Si tienes problemas:
1. Verifica que tus API keys sean válidas
2. Revisa la consola del navegador (F12)
3. Intenta refrescar la página
4. Borra localStorage y reconfigura

## 📚 Recursos

- **Documentación completa**: Ver README.md en el repositorio
- **Guía de seguridad**: Ver SECURITY.md
- **Deployment**: Ver DEPLOYMENT.md

## 🎉 ¡Disfruta ATP!

Crea workflows complejos, combina agentes especializados y aprovecha el poder de múltiples modelos de IA en un solo lugar.

**Recuerda:** Tus datos y credenciales están 100% seguros en tu navegador. ¡Explora sin preocupaciones!

---

**Desarrollado con ❤️ usando Next.js, FastAPI, ReactFlow y OpenAI SDK**
