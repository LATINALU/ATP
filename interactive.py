"""
ATP - Modo Interactivo
Interfaz conversacional para interactuar con los 30 agentes de IA

Ejecutar con: python interactive.py
Docker: docker-compose run atp-interactive
"""
import os
import sys
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt, Confirm
from rich.table import Table

# Cargar variables de entorno
load_dotenv()

# Verificar API key
if not os.getenv("OPENAI_API_KEY"):
    print("❌ Error: OPENAI_API_KEY no está configurada")
    print("Por favor, crea un archivo .env con tu API key de OpenAI")
    sys.exit(1)

from orchestrator import TaskOrchestrator
from agents import AgentFactory

console = Console()


class InteractiveSession:
    """Sesión interactiva con el sistema ATP"""
    
    def __init__(self):
        self.orchestrator = TaskOrchestrator()
        self.factory = AgentFactory()
        self.context = []
        self.session_history = []
    
    def display_header(self):
        """Muestra el encabezado de la sesión"""
        header = """
[bold cyan]╭─────────────────────────────────────────────────────────────╮
│           ATP - MODO INTERACTIVO                            │
│           Sistema de 30 Agentes de IA                       │
╰─────────────────────────────────────────────────────────────╯[/bold cyan]

[dim]Comandos disponibles:[/dim]
  [green]/agentes[/green]     - Ver todos los agentes disponibles
  [green]/nivel N[/green]     - Ver agentes del nivel N (1-5)
  [green]/usar AGENTE[/green] - Usar un agente específico
  [green]/historial[/green]   - Ver historial de la sesión
  [green]/limpiar[/green]     - Limpiar contexto de conversación
  [green]/ayuda[/green]       - Mostrar esta ayuda
  [green]/salir[/green]       - Terminar sesión

[dim]Escribe cualquier tarea en lenguaje natural para que los agentes la procesen.[/dim]
"""
        console.print(header)
    
    def show_agents(self, level: int = None):
        """Muestra los agentes disponibles"""
        if level:
            agents = self.factory.get_agents_by_level(level)
            title = f"Agentes Nivel {level}"
        else:
            console.print(self.factory.get_agents_summary())
            return
        
        table = Table(title=title, show_header=True)
        table.add_column("Nombre", style="cyan")
        table.add_column("Rol", style="green")
        
        for name, agent in agents.items():
            table.add_row(name, agent.role[:50] + "...")
        
        console.print(table)
    
    def use_specific_agent(self, agent_name: str, task: str):
        """Usa un agente específico para una tarea"""
        result = self.orchestrator.quick_task(task, agent_name)
        return result
    
    def process_command(self, user_input: str) -> bool:
        """Procesa comandos especiales. Retorna True si debe continuar."""
        input_lower = user_input.lower().strip()
        
        if input_lower == "/salir":
            console.print("\n[bold green]¡Hasta pronto! 👋[/bold green]")
            return False
        
        elif input_lower == "/agentes":
            self.show_agents()
        
        elif input_lower.startswith("/nivel"):
            try:
                level = int(input_lower.split()[1])
                if 1 <= level <= 5:
                    self.show_agents(level)
                else:
                    console.print("[red]Nivel debe ser entre 1 y 5[/red]")
            except (IndexError, ValueError):
                console.print("[red]Uso: /nivel N (donde N es 1-5)[/red]")
        
        elif input_lower.startswith("/usar"):
            parts = input_lower.split(maxsplit=1)
            if len(parts) < 2:
                console.print("[red]Uso: /usar nombre_agente[/red]")
                console.print("[dim]Ejemplo: /usar reasoning_agent[/dim]")
            else:
                agent_name = parts[1]
                if self.factory.get_agent(agent_name):
                    console.print(f"[green]Agente '{agent_name}' seleccionado.[/green]")
                    console.print("[dim]Escribe tu tarea para este agente:[/dim]")
                    task = Prompt.ask("Tarea")
                    if task:
                        with console.status("[bold green]Procesando..."):
                            result = self.use_specific_agent(agent_name, task)
                        console.print(Panel(result, title="Resultado", border_style="green"))
                else:
                    console.print(f"[red]Agente '{agent_name}' no encontrado[/red]")
                    console.print("[dim]Usa /agentes para ver la lista completa[/dim]")
        
        elif input_lower == "/historial":
            if not self.session_history:
                console.print("[dim]No hay historial en esta sesión[/dim]")
            else:
                for i, entry in enumerate(self.session_history, 1):
                    console.print(f"\n[bold]#{i}[/bold] {entry['input'][:50]}...")
                    console.print(f"[dim]Agentes: {len(entry.get('agents', []))}[/dim]")
        
        elif input_lower == "/limpiar":
            self.context = []
            console.print("[green]Contexto limpiado[/green]")
        
        elif input_lower == "/ayuda":
            self.display_header()
        
        else:
            return None  # No es un comando, procesar como tarea
        
        return True
    
    def process_task(self, user_input: str):
        """Procesa una tarea del usuario"""
        # Añadir contexto previo si existe
        context = "\n".join(self.context[-3:]) if self.context else None
        
        console.print("\n[bold blue]Analizando tarea...[/bold blue]")
        
        try:
            result = self.orchestrator.execute_task(
                user_input,
                context=context,
                verbose=True
            )
            
            # Guardar en historial
            self.session_history.append({
                "input": user_input,
                "result": result.get("result", ""),
                "agents": [a.role for a in result.get("analysis", {}).get("recommended_agents", [])]
            })
            
            # Actualizar contexto
            self.context.append(f"Tarea anterior: {user_input[:100]}")
            
        except Exception as e:
            console.print(f"[red]Error al procesar la tarea: {str(e)}[/red]")
            console.print("[dim]Verifica tu API key y conexión a internet[/dim]")
    
    def run(self):
        """Ejecuta la sesión interactiva"""
        self.display_header()
        
        while True:
            try:
                console.print()
                user_input = Prompt.ask("[bold cyan]Tu tarea[/bold cyan]")
                
                if not user_input.strip():
                    continue
                
                # Verificar si es un comando
                if user_input.startswith("/"):
                    result = self.process_command(user_input)
                    if result is False:
                        break
                    elif result is None:
                        # No era un comando válido
                        console.print("[red]Comando no reconocido. Usa /ayuda[/red]")
                else:
                    # Procesar como tarea
                    self.process_task(user_input)
                    
            except KeyboardInterrupt:
                console.print("\n\n[yellow]Sesión interrumpida[/yellow]")
                if Confirm.ask("¿Deseas salir?"):
                    break
            except Exception as e:
                console.print(f"[red]Error: {str(e)}[/red]")


def main():
    """Función principal"""
    session = InteractiveSession()
    session.run()


if __name__ == "__main__":
    main()
