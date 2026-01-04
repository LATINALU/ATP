"""
ATP - Agentes de Tareas Polivalentes
Sistema de 30 Agentes de IA con CrewAI

Ejecutar con: python main.py
Docker: docker-compose up atp-agents
"""
import os
import sys
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import print as rprint

# Cargar variables de entorno
load_dotenv()

# Verificar API key
if not os.getenv("OPENAI_API_KEY"):
    print("❌ Error: OPENAI_API_KEY no está configurada")
    print("Por favor, crea un archivo .env con tu API key de OpenAI")
    print("Ejemplo: OPENAI_API_KEY=sk-...")
    sys.exit(1)

from orchestrator import TaskOrchestrator
from agents import AgentFactory

console = Console()


def display_welcome():
    """Muestra el mensaje de bienvenida"""
    welcome_text = """
[bold cyan]╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     █████╗ ████████╗██████╗                                  ║
║    ██╔══██╗╚══██╔══╝██╔══██╗                                 ║
║    ███████║   ██║   ██████╔╝                                 ║
║    ██╔══██║   ██║   ██╔═══╝                                  ║
║    ██║  ██║   ██║   ██║                                      ║
║    ╚═╝  ╚═╝   ╚═╝   ╚═╝                                      ║
║                                                              ║
║         AGENTES DE TAREAS POLIVALENTES                       ║
║         Sistema de 30 Agentes de IA con CrewAI               ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝[/bold cyan]
"""
    console.print(welcome_text)


def display_agents_summary():
    """Muestra un resumen de los agentes disponibles"""
    factory = AgentFactory()
    
    levels = {
        1: ("CRÍTICOS", "red", ["reasoning", "planning", "research", "analysis", "synthesis", "critical_thinking"]),
        2: ("ESENCIALES", "yellow", ["coding", "writing", "data", "communication", "decision", "problem_solving"]),
        3: ("ESPECIALIZADOS", "green", ["legal", "financial", "creative", "technical", "educational", "marketing"]),
        4: ("SOPORTE", "blue", ["qa", "documentation", "optimization", "security", "integration", "review"]),
        5: ("AUXILIARES", "magenta", ["translation", "summary", "formatting", "validation", "coordination", "explanation"]),
    }
    
    for level, (name, color, agents) in levels.items():
        table = Table(title=f"Nivel {level} - {name}", show_header=True, header_style=f"bold {color}")
        table.add_column("Agente", style=color)
        table.add_column("Descripción")
        
        for agent_key in agents:
            agent_name = f"{agent_key}_agent"
            info = factory.get_agent_info(agent_name)
            if info:
                table.add_row(info['name'], info['role'][:60] + "...")
        
        console.print(table)
        console.print()


def run_demo():
    """Ejecuta una demostración del sistema"""
    console.print("\n[bold yellow]═══ DEMOSTRACIÓN DEL SISTEMA ATP ═══[/bold yellow]\n")
    
    orchestrator = TaskOrchestrator()
    
    # Ejemplo de tarea
    demo_task = """
    Necesito analizar las ventajas y desventajas de implementar microservicios 
    en una aplicación monolítica existente. Considera aspectos técnicos, 
    de equipo y de negocio.
    """
    
    console.print(Panel(
        f"[italic]{demo_task.strip()}[/italic]",
        title="Tarea de Demostración",
        border_style="yellow"
    ))
    
    console.print("\n[bold]Presiona Enter para ejecutar la demostración...[/bold]")
    input()
    
    result = orchestrator.execute_task(demo_task)
    
    return result


def main():
    """Función principal"""
    display_welcome()
    
    console.print("\n[bold]Opciones disponibles:[/bold]")
    console.print("  1. Ver todos los agentes disponibles")
    console.print("  2. Ejecutar demostración")
    console.print("  3. Modo interactivo (usar interactive.py)")
    console.print("  4. Salir")
    
    while True:
        console.print("\n")
        choice = console.input("[bold cyan]Selecciona una opción (1-4): [/bold cyan]")
        
        if choice == "1":
            display_agents_summary()
        elif choice == "2":
            run_demo()
        elif choice == "3":
            console.print("\n[yellow]Para modo interactivo, ejecuta:[/yellow]")
            console.print("  python interactive.py")
            console.print("  [dim]o con Docker: docker-compose run atp-interactive[/dim]")
        elif choice == "4":
            console.print("\n[bold green]¡Hasta pronto! 👋[/bold green]")
            break
        else:
            console.print("[red]Opción no válida. Intenta de nuevo.[/red]")


if __name__ == "__main__":
    main()
