"""
Coding Agent - ATP v0.6.1
Ingeniero de Software Senior y Arquitecto de Código

Agente especializado en desarrollo de software, arquitectura de código,
y mejores prácticas de ingeniería.

Capacidades únicas:
- Desarrollo multi-lenguaje (Python, JavaScript, TypeScript, Go, Rust, etc.)
- Arquitectura de software (Clean Architecture, DDD, Microservices)
- Patrones de diseño (GoF, Enterprise Patterns)
- Refactoring y optimización
- Code review y mejores prácticas
- Testing (TDD, BDD, Integration, E2E)
"""
from typing import Dict, Any, Optional, List
from app.agents.base_agent import BaseAgent
from app.a2a_protocol import AgentCapability


class CodingAgent(BaseAgent):
    """
    Agente Ingeniero de Software Senior
    
    Supercomputadora especializada en desarrollo de software de clase mundial.
    Domina múltiples lenguajes, paradigmas y arquitecturas.
    
    Expertise:
    - Desarrollo full-stack
    - Arquitectura de software
    - Patrones de diseño
    - Clean Code principles
    - SOLID principles
    - Testing strategies
    """
    
    def __init__(self, model: str = None, api_config: Dict[str, Any] = None):
        super().__init__(
            agent_id="coding_senior_001",
            name="Coding Senior Engineer",
            primary_capability=AgentCapability.CODING,
            secondary_capabilities=[
                AgentCapability.SYSTEM_ARCHITECTURE,
                AgentCapability.OPTIMIZATION
            ],
            specialization="Software Engineering & Code Architecture",
            description="""
            Ingeniero de software senior con expertise en múltiples lenguajes y paradigmas.
            Especializado en escribir código limpio, mantenible y escalable siguiendo
            mejores prácticas de la industria.
            """,
            backstory="""
            Soy el Agente de Programación, un ingeniero de software senior con dominio
            profundo de múltiples paradigmas y lenguajes de programación.
            
            Mi expertise técnico abarca:
            
            LENGUAJES:
            - Python (FastAPI, Django, Flask, asyncio,
            model=model,
            api_config=api_config
            - JavaScript/TypeScript (React, Node.js, Next.js)
            - Go (concurrency, microservices)
            - Rust (systems programming, performance)
            - Java (Spring, enterprise)
            - C# (.NET, Azure)
            
            PARADIGMAS:
            - Programación Orientada a Objetos (OOP)
            - Programación Funcional (FP)
            - Programación Reactiva
            - Programación Concurrente/Paralela
            - Event-Driven Architecture
            
            ARQUITECTURAS:
            - Clean Architecture (Uncle Bob)
            - Domain-Driven Design (DDD)
            - Hexagonal Architecture (Ports & Adapters)
            - Microservices Architecture
            - Event Sourcing & CQRS
            - Serverless Architecture
            
            PATRONES DE DISEÑO:
            - Creacionales: Factory, Builder, Singleton, Prototype
            - Estructurales: Adapter, Decorator, Facade, Proxy
            - Comportamiento: Strategy, Observer, Command, State
            - Enterprise: Repository, Unit of Work, Specification
            
            PRINCIPIOS:
            - SOLID (Single Responsibility, Open/Closed, Liskov, Interface Segregation, Dependency Inversion)
            - DRY (Don't Repeat Yourself)
            - KISS (Keep It Simple, Stupid)
            - YAGNI (You Aren't Gonna Need It)
            - Clean Code (Robert C. Martin)
            
            TESTING:
            - TDD (Test-Driven Development)
            - BDD (Behavior-Driven Development)
            - Unit Testing (pytest, jest, JUnit)
            - Integration Testing
            - E2E Testing (Playwright, Cypress)
            - Property-Based Testing
            
            Mi fortaleza es escribir código que no solo funciona, sino que es
            elegante, mantenible, testeable y escalable.
            """,
            model_name="gpt-4",
            temperature=0.2,  # Baja temperatura para código preciso
            max_tokens=4000
        )
        
        self.languages = [
            "python", "javascript", "typescript", "go", "rust",
            "java", "csharp", "cpp", "ruby", "php"
        ]
        
        self.frameworks = [
            "fastapi", "django", "flask", "react", "nextjs",
            "express", "spring", "dotnet", "rails"
        ]
    
    def get_system_prompt(self) -> str:
        """System prompt especializado para coding"""
        return """Eres el Agente Ingeniero de Software Senior, una supercomputadora especializada
en desarrollo de software de clase mundial.

TU MISIÓN:
Escribir código limpio, eficiente, mantenible y escalable en cualquier lenguaje,
siguiendo mejores prácticas de la industria y principios de ingeniería sólidos.

CAPACIDADES ÚNICAS:

1. DESARROLLO MULTI-LENGUAJE:
   - Python (backend, data science, automation)
   - JavaScript/TypeScript (frontend, backend, full-stack)
   - Go (microservices, sistemas distribuidos)
   - Rust (performance crítico, systems programming)
   - Java/C# (enterprise applications)
   
2. ARQUITECTURA DE SOFTWARE:
   - Clean Architecture (separación de concerns)
   - Domain-Driven Design (modelado de dominio)
   - Microservices (servicios desacoplados)
   - Event-Driven (arquitectura reactiva)
   - Hexagonal Architecture (ports & adapters)

3. PATRONES DE DISEÑO:
   - Creacionales: Factory, Builder, Singleton
   - Estructurales: Adapter, Decorator, Facade
   - Comportamiento: Strategy, Observer, Command
   - Enterprise: Repository, Unit of Work

4. PRINCIPIOS SOLID:
   - Single Responsibility Principle
   - Open/Closed Principle
   - Liskov Substitution Principle
   - Interface Segregation Principle
   - Dependency Inversion Principle

5. CLEAN CODE:
   - Nombres significativos
   - Funciones pequeñas y enfocadas
   - Comentarios solo cuando necesario
   - Manejo de errores robusto
   - Testing comprehensivo

6. TESTING:
   - TDD (escribir tests primero)
   - Unit tests (funciones individuales)
   - Integration tests (componentes juntos)
   - E2E tests (flujos completos)
   - Property-based testing

METODOLOGÍA DE TRABAJO:

Cuando recibas una tarea de programación:

1. COMPRENSIÓN:
   - Entiende requisitos completamente
   - Clarifica ambigüedades
   - Identifica edge cases
   - Define criterios de éxito

2. DISEÑO:
   - Diseña arquitectura apropiada
   - Selecciona patrones de diseño
   - Planifica estructura de módulos
   - Considera escalabilidad

3. IMPLEMENTACIÓN:
   - Escribe código limpio y legible
   - Aplica principios SOLID
   - Usa nombres significativos
   - Maneja errores apropiadamente

4. TESTING:
   - Escribe tests comprehensivos
   - Cubre casos edge
   - Verifica comportamiento esperado
   - Asegura cobertura adecuada

5. REFACTORING:
   - Elimina duplicación
   - Mejora claridad
   - Optimiza performance si necesario
   - Mantén simplicidad

FORMATO DE RESPUESTA:

Estructura tu código así:

**ANÁLISIS DE REQUISITOS:**
[Comprensión del problema]

**DISEÑO:**
[Arquitectura y patrones a usar]

**IMPLEMENTACIÓN:**
```language
# Código limpio y bien documentado
# Con type hints, docstrings, etc.
```

**TESTS:**
```language
# Tests comprehensivos
```

**EXPLICACIÓN:**
[Decisiones de diseño y trade-offs]

**MEJORAS FUTURAS:**
[Optimizaciones o extensiones posibles]

PRINCIPIOS DE CÓDIGO:
- Claridad sobre cleverness
- Simplicidad sobre complejidad
- Mantenibilidad sobre optimización prematura
- Testeable sobre no-testeable
- Explícito sobre implícito

El mejor código es el que otro desarrollador puede entender
y mantener sin necesidad de preguntarte."""

    async def process_task(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Procesa una tarea de programación
        
        Args:
            task: Descripción de lo que hay que programar
            context: Contexto (lenguaje, framework, requisitos)
            
        Returns:
            Código implementado con tests y explicación
        """
        context = context or {}
        
        # Preparar contexto de memoria
        memory_context = self.get_memory_context(limit=5)
        
        # Determinar lenguaje y framework
        language = context.get("language", self._detect_language(task))
        framework = context.get("framework", "")
        
        # Construir prompt
        user_message = f"""
TAREA DE PROGRAMACIÓN: {task}

CONTEXTO:
{self._format_context(context)}

LENGUAJE: {language}
FRAMEWORK: {framework if framework else "Ninguno específico"}

MEMORIA RECIENTE:
{memory_context}

Por favor, implementa esta funcionalidad siguiendo mejores prácticas.
"""
        
        # Llamar al LLM
        response = await self.call_llm(
            messages=[{"role": "user", "content": user_message}],
            temperature=0.2  # Baja temperatura para precisión
        )
        
        # Extraer resultado
        result = {
            "code": response,
            "language": language,
            "framework": framework,
            "confidence": 0.90,
            "agent": self.profile.name,
            "capability": self.profile.primary_capability.value
        }
        
        # Guardar en memoria
        self.add_to_memory({
            "task": task[:100],
            "summary": response[:200],
            "language": language
        })
        
        return result
    
    def _format_context(self, context: Dict[str, Any]) -> str:
        """Formatea el contexto de programación"""
        if not context:
            return "No hay contexto adicional."
        
        formatted = []
        
        if "requirements" in context:
            formatted.append(f"Requisitos: {context['requirements']}")
        
        if "constraints" in context:
            formatted.append(f"Restricciones: {context['constraints']}")
        
        if "architecture" in context:
            formatted.append(f"Arquitectura: {context['architecture']}")
        
        if "patterns" in context:
            formatted.append(f"Patrones sugeridos: {context['patterns']}")
        
        for key, value in context.items():
            if key not in ["requirements", "constraints", "architecture", "patterns", "language", "framework"]:
                formatted.append(f"{key}: {value}")
        
        return "\n".join(formatted) if formatted else "No hay contexto adicional."
    
    def _detect_language(self, task: str) -> str:
        """Detecta lenguaje apropiado basado en la tarea"""
        task_lower = task.lower()
        
        # Python para backend, data science, automation
        if any(word in task_lower for word in ["fastapi", "django", "flask", "pandas", "numpy", "backend api"]):
            return "Python"
        
        # TypeScript para frontend moderno
        if any(word in task_lower for word in ["react", "nextjs", "frontend", "ui", "component"]):
            return "TypeScript"
        
        # Go para microservices
        if any(word in task_lower for word in ["microservice", "grpc", "concurrent", "go"]):
            return "Go"
        
        # Rust para performance
        if any(word in task_lower for word in ["performance", "systems", "low-level", "rust"]):
            return "Rust"
        
        # Default a Python
        return "Python"
    
    async def code_review(self, code: str, language: str) -> Dict[str, Any]:
        """
        Realiza code review
        
        Args:
            code: Código a revisar
            language: Lenguaje del código
            
        Returns:
            Review con sugerencias de mejora
        """
        return await self.process_task(
            f"Realiza un code review exhaustivo de este código {language}:\n\n{code}",
            context={"task_type": "code_review", "language": language}
        )
    
    async def refactor_code(self, code: str, language: str, goal: str) -> Dict[str, Any]:
        """
        Refactoriza código
        
        Args:
            code: Código a refactorizar
            language: Lenguaje del código
            goal: Objetivo del refactoring
            
        Returns:
            Código refactorizado
        """
        return await self.process_task(
            f"Refactoriza este código {language} para: {goal}\n\nCódigo:\n{code}",
            context={"task_type": "refactoring", "language": language}
        )
    
    async def write_tests(self, code: str, language: str) -> Dict[str, Any]:
        """
        Escribe tests para código
        
        Args:
            code: Código a testear
            language: Lenguaje del código
            
        Returns:
            Tests comprehensivos
        """
        return await self.process_task(
            f"Escribe tests comprehensivos para este código {language}:\n\n{code}",
            context={"task_type": "testing", "language": language}
        )
    
    async def design_architecture(self, requirements: str) -> Dict[str, Any]:
        """
        Diseña arquitectura de software
        
        Args:
            requirements: Requisitos del sistema
            
        Returns:
            Diseño de arquitectura
        """
        return await self.process_task(
            f"Diseña la arquitectura de software para estos requisitos:\n{requirements}",
            context={"task_type": "architecture_design"}
        )
