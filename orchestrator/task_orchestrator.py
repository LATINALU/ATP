"""
Task Orchestrator - Orquestador principal que coordina los agentes para completar tareas
"""
from typing import List, Optional, Dict, Any
from crewai import Crew, Task, Process
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from agents.agent_factory import AgentFactory


console = Console()


class TaskOrchestrator:
    """
    Orquestador principal del sistema ATP.
    Analiza tareas del usuario en lenguaje natural y coordina los agentes apropiados.
    """
    
    def __init__(self, tools: list = None):
        """Inicializa el orquestador con la fábrica de agentes"""
        self.factory = AgentFactory(tools)
        self.execution_history = []
    
    def analyze_task(self, user_input: str) -> Dict[str, Any]:
        """
        Analiza la tarea del usuario y determina:
        - Tipo de tarea
        - Agentes necesarios
        - Estrategia de ejecución
        """
        analysis = {
            "original_input": user_input,
            "detected_keywords": [],
            "recommended_agents": [],
            "complexity": "medium",
            "process_type": Process.sequential,
        }
        
        # Detectar palabras clave
        task_lower = user_input.lower()
        for keyword in self.factory.TASK_KEYWORDS.keys():
            if keyword in task_lower:
                analysis["detected_keywords"].append(keyword)
        
        # Determinar complejidad
        word_count = len(user_input.split())
        if word_count < 20:
            analysis["complexity"] = "simple"
        elif word_count > 100:
            analysis["complexity"] = "complex"
        
        # Seleccionar agentes
        num_agents = {"simple": 2, "medium": 3, "complex": 5}[analysis["complexity"]]
        analysis["recommended_agents"] = self.factory.select_agents_for_task(
            user_input, 
            max_agents=num_agents
        )
        
        # Determinar proceso
        if analysis["complexity"] == "complex":
            analysis["process_type"] = Process.hierarchical
        
        return analysis
    
    def create_tasks_from_input(
        self, 
        user_input: str, 
        agents: List,
        context: Optional[str] = None
    ) -> List[Task]:
        """
        Crea tareas de CrewAI basadas en el input del usuario.
        Distribuye el trabajo entre los agentes seleccionados.
        """
        tasks = []
        
        # Tarea principal de análisis y comprensión
        if len(agents) >= 1:
            tasks.append(Task(
                description=f"""
                FASE 1: COMPRENSIÓN Y ANÁLISIS
                
                Analiza profundamente la siguiente solicitud del usuario:
                
                "{user_input}"
                
                {f'Contexto adicional: {context}' if context else ''}
                
                Tu análisis debe incluir:
                1. ¿Qué está pidiendo exactamente el usuario?
                2. ¿Cuáles son los requisitos explícitos e implícitos?
                3. ¿Qué información adicional sería útil?
                4. ¿Cuáles son los posibles desafíos o consideraciones?
                5. ¿Cuál es el mejor enfoque para abordar esta tarea?
                
                Proporciona un análisis estructurado y detallado.
                """,
                expected_output="Análisis completo de la tarea con requisitos, consideraciones y enfoque recomendado",
                agent=agents[0],
            ))
        
        # Tarea de desarrollo/ejecución principal
        if len(agents) >= 2:
            tasks.append(Task(
                description=f"""
                FASE 2: DESARROLLO Y EJECUCIÓN
                
                Basándote en el análisis previo, ejecuta la tarea principal:
                
                "{user_input}"
                
                Aplica tu expertise específico para:
                1. Desarrollar la solución o respuesta principal
                2. Asegurar calidad y completitud
                3. Considerar casos edge y excepciones
                4. Documentar tu proceso de razonamiento
                
                Entrega un resultado de alta calidad y profesional.
                """,
                expected_output="Solución completa y detallada a la solicitud del usuario",
                agent=agents[1],
                context=[tasks[0]] if tasks else None,
            ))
        
        # Tarea de revisión y mejora
        if len(agents) >= 3:
            tasks.append(Task(
                description=f"""
                FASE 3: REVISIÓN Y REFINAMIENTO
                
                Revisa el trabajo realizado en las fases anteriores:
                
                1. Verifica que la solución responde completamente a: "{user_input}"
                2. Identifica áreas de mejora o gaps
                3. Sugiere refinamientos específicos
                4. Asegura coherencia y calidad
                5. Valida la precisión de la información
                
                Proporciona feedback constructivo y mejoras concretas.
                """,
                expected_output="Revisión detallada con mejoras y validación de calidad",
                agent=agents[2],
                context=tasks[:2] if len(tasks) >= 2 else tasks,
            ))
        
        # Tarea de síntesis final
        if len(agents) >= 4:
            tasks.append(Task(
                description=f"""
                FASE 4: SÍNTESIS E INTEGRACIÓN
                
                Integra todo el trabajo realizado en una respuesta final cohesiva:
                
                1. Combina los mejores elementos de cada fase
                2. Asegura una narrativa clara y fluida
                3. Elimina redundancias
                4. Añade cualquier elemento faltante
                5. Formatea para máxima claridad
                
                El resultado debe ser la mejor respuesta posible a: "{user_input}"
                """,
                expected_output="Respuesta final integrada, pulida y lista para entregar",
                agent=agents[3],
                context=tasks[:3] if len(tasks) >= 3 else tasks,
            ))
        
        # Tarea de validación final (si hay 5 agentes)
        if len(agents) >= 5:
            tasks.append(Task(
                description=f"""
                FASE 5: VALIDACIÓN FINAL
                
                Realiza una validación final exhaustiva:
                
                1. ¿La respuesta cumple todos los requisitos del usuario?
                2. ¿Es precisa, completa y útil?
                3. ¿El tono y formato son apropiados?
                4. ¿Hay errores o inconsistencias?
                5. Califica la respuesta del 1-10 y justifica
                
                Si encuentras problemas críticos, señálalos claramente.
                Si todo está bien, confirma la calidad del entregable.
                """,
                expected_output="Validación final con calificación y confirmación de calidad",
                agent=agents[4],
                context=tasks[:4] if len(tasks) >= 4 else tasks,
            ))
        
        return tasks
    
    def execute_task(
        self, 
        user_input: str, 
        context: Optional[str] = None,
        verbose: bool = True
    ) -> Dict[str, Any]:
        """
        Ejecuta una tarea completa coordinando los agentes necesarios.
        """
        # Mostrar inicio
        if verbose:
            console.print(Panel(
                f"[bold blue]Procesando solicitud:[/bold blue]\n{user_input}",
                title="🚀 ATP - Sistema de Agentes",
                border_style="blue"
            ))
        
        # Analizar la tarea
        analysis = self.analyze_task(user_input)
        
        if verbose:
            self._display_analysis(analysis)
        
        # Crear tareas
        tasks = self.create_tasks_from_input(
            user_input, 
            analysis["recommended_agents"],
            context
        )
        
        # Crear y ejecutar el crew
        crew = Crew(
            agents=analysis["recommended_agents"],
            tasks=tasks,
            process=analysis["process_type"],
            verbose=verbose,
        )
        
        # Ejecutar
        if verbose:
            console.print("\n[bold green]Iniciando ejecución...[/bold green]\n")
        
        result = crew.kickoff()
        
        # Guardar en historial
        execution_record = {
            "input": user_input,
            "analysis": analysis,
            "result": str(result),
        }
        self.execution_history.append(execution_record)
        
        # Mostrar resultado
        if verbose:
            console.print(Panel(
                str(result),
                title="✅ Resultado Final",
                border_style="green"
            ))
        
        return {
            "success": True,
            "result": str(result),
            "analysis": analysis,
        }
    
    def _display_analysis(self, analysis: Dict[str, Any]):
        """Muestra el análisis de la tarea de forma visual"""
        table = Table(title="Análisis de Tarea", show_header=True)
        table.add_column("Aspecto", style="cyan")
        table.add_column("Valor", style="green")
        
        table.add_row("Complejidad", analysis["complexity"])
        table.add_row("Palabras clave", ", ".join(analysis["detected_keywords"][:5]) or "Ninguna específica")
        table.add_row("Agentes seleccionados", str(len(analysis["recommended_agents"])))
        table.add_row("Proceso", "Jerárquico" if analysis["process_type"] == Process.hierarchical else "Secuencial")
        
        console.print(table)
        
        # Mostrar agentes seleccionados
        console.print("\n[bold]Agentes asignados:[/bold]")
        for i, agent in enumerate(analysis["recommended_agents"], 1):
            console.print(f"  {i}. {agent.role}")
    
    def execute_with_specific_agents(
        self, 
        user_input: str, 
        agent_names: List[str],
        verbose: bool = True
    ) -> Dict[str, Any]:
        """
        Ejecuta una tarea con agentes específicos seleccionados manualmente.
        """
        agents = [self.factory.get_agent(name) for name in agent_names if self.factory.get_agent(name)]
        
        if not agents:
            return {
                "success": False,
                "error": "No se encontraron agentes válidos con los nombres proporcionados"
            }
        
        tasks = self.create_tasks_from_input(user_input, agents)
        
        crew = Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential,
            verbose=verbose,
        )
        
        result = crew.kickoff()
        
        return {
            "success": True,
            "result": str(result),
            "agents_used": agent_names,
        }
    
    def get_available_agents(self) -> str:
        """Retorna un resumen de los agentes disponibles"""
        return self.factory.get_agents_summary()
    
    def quick_task(self, user_input: str, agent_name: str) -> str:
        """
        Ejecuta una tarea rápida con un solo agente.
        Útil para tareas simples y directas.
        """
        agent = self.factory.get_agent(agent_name)
        if not agent:
            return f"Error: Agente '{agent_name}' no encontrado"
        
        task = Task(
            description=user_input,
            expected_output="Respuesta completa y útil a la solicitud",
            agent=agent,
        )
        
        crew = Crew(
            agents=[agent],
            tasks=[task],
            verbose=False,
        )
        
        result = crew.kickoff()
        return str(result)
