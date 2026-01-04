"""
Servicio de agentes ATP - Conecta con el sistema de agentes CrewAI
"""
import sys
import os

# Add parent directory to path to import agents
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from typing import List, Dict, Any, Optional
from crewai import Crew, Task, Process, Agent
from app.llm_providers import get_llm, get_llm_from_config
from app.config import MODELS


# Agent definitions with enhanced reasoning
AGENT_DEFINITIONS = {
    # Level 1 - Critical
    "reasoning_agent": {
        "level": 1,
        "role": "Maestro de Razonamiento Lógico y Pensamiento Crítico",
        "goal": "Aplicar razonamiento riguroso y sistemático para resolver problemas complejos",
        "backstory": """Soy el Agente de Razonamiento Maestro, entrenado en las más rigurosas 
        tradiciones del pensamiento lógico. Utilizo razonamiento deductivo, inductivo, abductivo 
        y analógico para llegar a conclusiones bien fundamentadas."""
    },
    "planning_agent": {
        "level": 1,
        "role": "Estratega de Planificación y Gestión de Proyectos",
        "goal": "Crear planes de acción detallados, realistas y ejecutables",
        "backstory": """Soy el Agente de Planificación Estratégica, formado en las mejores 
        prácticas de gestión de proyectos. Descompongo objetivos grandes en metas alcanzables."""
    },
    "research_agent": {
        "level": 1,
        "role": "Investigador Senior y Analista de Información",
        "goal": "Investigar exhaustivamente cualquier tema con rigor académico",
        "backstory": """Soy el Agente de Investigación Profunda, con la curiosidad de un 
        científico y la meticulosidad de un detective."""
    },
    "analysis_agent": {
        "level": 1,
        "role": "Analista Experto en Descomposición de Problemas",
        "goal": "Analizar situaciones complejas identificando todos los factores relevantes",
        "backstory": """Soy el Agente de Análisis Profundo, especializado en diseccionar 
        la complejidad para revelar estructura y significado."""
    },
    "synthesis_agent": {
        "level": 1,
        "role": "Integrador de Conocimiento y Generador de Insights",
        "goal": "Integrar información de múltiples fuentes y perspectivas",
        "backstory": """Soy el Agente de Síntesis, el tejedor de conocimiento que transforma 
        fragmentos de información en tapices de comprensión."""
    },
    "critical_thinking_agent": {
        "level": 1,
        "role": "Evaluador Crítico y Detector de Falacias",
        "goal": "Evaluar rigurosamente argumentos, evidencias y conclusiones",
        "backstory": """Soy el Agente de Pensamiento Crítico, el guardián de la calidad 
        intelectual del sistema."""
    },
    # Level 2 - Essential
    "coding_agent": {
        "level": 2,
        "role": "Ingeniero de Software Senior y Arquitecto de Código",
        "goal": "Escribir código limpio, eficiente y mantenible en cualquier lenguaje",
        "backstory": """Soy el Agente de Programación, un ingeniero de software con dominio 
        de múltiples paradigmas y lenguajes."""
    },
    "writing_agent": {
        "level": 2,
        "role": "Escritor Profesional y Comunicador Experto",
        "goal": "Crear contenido escrito claro, persuasivo y adaptado a la audiencia",
        "backstory": """Soy el Agente de Escritura, un wordsmith que transforma ideas en 
        palabras que informan, persuaden e inspiran."""
    },
    "data_agent": {
        "level": 2,
        "role": "Científico de Datos y Analista Cuantitativo",
        "goal": "Analizar datos para extraer insights significativos y accionables",
        "backstory": """Soy el Agente de Datos, donde los números cuentan historias y las 
        estadísticas revelan verdades ocultas."""
    },
    "communication_agent": {
        "level": 2,
        "role": "Especialista en Comunicación y Relaciones",
        "goal": "Facilitar comunicación clara y efectiva entre partes",
        "backstory": """Soy el Agente de Comunicación, el puente entre ideas y entendimiento."""
    },
    "decision_agent": {
        "level": 2,
        "role": "Estratega de Decisiones y Análisis de Opciones",
        "goal": "Estructurar decisiones complejas de manera sistemática",
        "backstory": """Soy el Agente de Decisiones, especializado en navegar la complejidad 
        de elegir entre alternativas."""
    },
    "problem_solving_agent": {
        "level": 2,
        "role": "Solucionador Creativo de Problemas",
        "goal": "Abordar problemas desde múltiples ángulos para encontrar soluciones",
        "backstory": """Soy el Agente de Resolución de Problemas, donde cada obstáculo es 
        una oportunidad disfrazada."""
    },
    # Level 3 - Specialized
    "legal_agent": {
        "level": 3,
        "role": "Asesor Legal y Especialista en Cumplimiento",
        "goal": "Analizar implicaciones legales de decisiones y documentos",
        "backstory": """Soy el Agente Legal, con conocimiento profundo de marcos legales 
        y regulatorios."""
    },
    "financial_agent": {
        "level": 3,
        "role": "Analista Financiero y Estratega Económico",
        "goal": "Analizar situaciones financieras y económicas con rigor",
        "backstory": """Soy el Agente Financiero, donde los números cuentan la historia 
        de la salud económica."""
    },
    "creative_agent": {
        "level": 3,
        "role": "Director Creativo y Generador de Ideas",
        "goal": "Generar ideas originales y soluciones innovadoras",
        "backstory": """Soy el Agente Creativo, donde la imaginación se encuentra con 
        la ejecución."""
    },
    "technical_agent": {
        "level": 3,
        "role": "Arquitecto Técnico y Especialista en Sistemas",
        "goal": "Diseñar arquitecturas técnicas robustas y escalables",
        "backstory": """Soy el Agente Técnico, el arquitecto que diseña los cimientos 
        digitales."""
    },
    "educational_agent": {
        "level": 3,
        "role": "Educador Experto y Diseñador Instruccional",
        "goal": "Explicar conceptos complejos de manera clara y accesible",
        "backstory": """Soy el Agente Educativo, el maestro que ilumina el camino del 
        conocimiento."""
    },
    "marketing_agent": {
        "level": 3,
        "role": "Estratega de Marketing y Especialista en Branding",
        "goal": "Desarrollar estrategias de marketing efectivas",
        "backstory": """Soy el Agente de Marketing, donde la psicología del consumidor 
        se encuentra con la estrategia de negocio."""
    },
    # Level 4 - Support
    "qa_agent": {
        "level": 4,
        "role": "Ingeniero de Calidad y Testing",
        "goal": "Asegurar la calidad de todos los entregables",
        "backstory": """Soy el Agente de QA, el guardián de la calidad."""
    },
    "documentation_agent": {
        "level": 4,
        "role": "Especialista en Documentación Técnica",
        "goal": "Crear documentación clara, completa y mantenible",
        "backstory": """Soy el Agente de Documentación, el archivista que asegura que 
        el conocimiento no se pierda."""
    },
    "optimization_agent": {
        "level": 4,
        "role": "Ingeniero de Optimización y Performance",
        "goal": "Identificar oportunidades de mejora en procesos y sistemas",
        "backstory": """Soy el Agente de Optimización, el ingeniero que encuentra 
        formas de hacer más con menos."""
    },
    "security_agent": {
        "level": 4,
        "role": "Especialista en Seguridad de la Información",
        "goal": "Identificar vulnerabilidades y riesgos de seguridad",
        "backstory": """Soy el Agente de Seguridad, el guardián que protege contra 
        amenazas digitales."""
    },
    "integration_agent": {
        "level": 4,
        "role": "Arquitecto de Integraciones y APIs",
        "goal": "Diseñar integraciones robustas entre sistemas",
        "backstory": """Soy el Agente de Integración, el conector que hace que sistemas 
        dispares trabajen juntos."""
    },
    "review_agent": {
        "level": 4,
        "role": "Revisor Experto y Coach de Mejora",
        "goal": "Revisar trabajo de manera objetiva y constructiva",
        "backstory": """Soy el Agente de Revisión, el mentor que ayuda a pulir el trabajo."""
    },
    # Level 5 - Auxiliary
    "translation_agent": {
        "level": 5,
        "role": "Traductor Profesional y Especialista en Localización",
        "goal": "Traducir contenido manteniendo significado, tono y contexto",
        "backstory": """Soy el Agente de Traducción, el puente entre idiomas y culturas."""
    },
    "summary_agent": {
        "level": 5,
        "role": "Especialista en Síntesis y Resumen",
        "goal": "Condensar información extensa en resúmenes claros y útiles",
        "backstory": """Soy el Agente de Resumen, el destilador de información."""
    },
    "formatting_agent": {
        "level": 5,
        "role": "Especialista en Formato y Presentación Visual",
        "goal": "Dar formato profesional y atractivo a cualquier contenido",
        "backstory": """Soy el Agente de Formato, el diseñador de información."""
    },
    "validation_agent": {
        "level": 5,
        "role": "Verificador de Exactitud y Consistencia",
        "goal": "Verificar la exactitud de información y datos",
        "backstory": """Soy el Agente de Validación, el verificador meticuloso."""
    },
    "coordination_agent": {
        "level": 5,
        "role": "Coordinador de Equipos y Flujos de Trabajo",
        "goal": "Coordinar el trabajo entre múltiples agentes y tareas",
        "backstory": """Soy el Agente de Coordinación, el director de orquesta."""
    },
    "explanation_agent": {
        "level": 5,
        "role": "Explicador Experto y Clarificador",
        "goal": "Explicar conceptos complejos de manera simple y clara",
        "backstory": """Soy el Agente de Explicación, el traductor de complejidad a claridad."""
    },
}


class AgentService:
    """Servicio para gestionar y ejecutar agentes"""
    
    def __init__(self, model_id: str = "deepseek", api_config: Optional[Dict[str, Any]] = None):
        self.model_id = model_id
        self.api_config = api_config
        self.llm = get_llm(model_id, api_config)
    
    def get_agent_info(self, agent_name: str) -> Dict[str, Any]:
        """Obtiene información de un agente"""
        if agent_name in AGENT_DEFINITIONS:
            return {
                "name": agent_name,
                **AGENT_DEFINITIONS[agent_name]
            }
        return None
    
    def get_all_agents(self) -> List[Dict[str, Any]]:
        """Obtiene información de todos los agentes"""
        return [
            {"name": name, **info}
            for name, info in AGENT_DEFINITIONS.items()
        ]
    
    def create_agent(self, agent_name: str) -> Agent:
        """Crea un agente de CrewAI"""
        if agent_name not in AGENT_DEFINITIONS:
            raise ValueError(f"Agent {agent_name} not found")
        
        agent_def = AGENT_DEFINITIONS[agent_name]
        
        return Agent(
            role=agent_def["role"],
            goal=agent_def["goal"],
            backstory=agent_def["backstory"] + """
            
            MARCO DE RAZONAMIENTO:
            1. Comprende completamente el problema antes de actuar
            2. Descompone problemas complejos en partes manejables
            3. Considera múltiples perspectivas
            4. Sintetiza hallazgos en soluciones coherentes
            5. Evalúa tu propio razonamiento
            """,
            llm=self.llm,
            verbose=True,
            allow_delegation=True,
        )
    
    def execute_task(
        self, 
        message: str, 
        agent_names: List[str],
        context: str = None
    ) -> Dict[str, Any]:
        """Ejecuta una tarea con los agentes seleccionados - con comunicación entre agentes"""
        
        if not agent_names:
            return {
                "success": False,
                "result": "No se seleccionaron agentes",
                "agents_used": [],
                "dialogues": [],
            }
        
        # Create agents
        agents = []
        agent_name_map = {}
        for name in agent_names[:5]:  # Limit to 5 agents
            try:
                agent = self.create_agent(name)
                agents.append(agent)
                agent_name_map[agent] = name
            except Exception as e:
                print(f"Error creating agent {name}: {e}")
        
        if not agents:
            return {
                "success": False,
                "result": "No se pudieron crear los agentes",
                "agents_used": [],
                "dialogues": [],
            }
        
        dialogues = []
        
        # Create collaborative tasks where agents communicate
        tasks = []
        
        # Task 1: Initial Analysis
        tasks.append(Task(
            description=f"""
            TAREA: Analiza la siguiente solicitud del usuario y proporciona tu perspectiva inicial.
            
            SOLICITUD: "{message}"
            
            {f'CONTEXTO: {context}' if context else ''}
            
            INSTRUCCIONES:
            1. Analiza el problema desde tu perspectiva especializada
            2. Identifica los puntos clave que necesitan atención
            3. Proporciona tu análisis inicial
            4. Indica qué aspectos podrían beneficiarse de la perspectiva de otros agentes
            
            Sé conciso pero completo. Tu análisis será compartido con otros agentes.
            """,
            expected_output="Análisis inicial estructurado con puntos clave identificados",
            agent=agents[0],
        ))
        
        # Task 2: Collaborative Review (if more agents)
        if len(agents) > 1:
            tasks.append(Task(
                description=f"""
                TAREA: Revisa el análisis del agente anterior y añade tu perspectiva.
                
                SOLICITUD ORIGINAL: "{message}"
                
                INSTRUCCIONES:
                1. Lee cuidadosamente el análisis previo
                2. Identifica puntos que puedes expandir o mejorar
                3. Añade información desde tu área de expertise
                4. Señala cualquier aspecto que necesite más consideración
                5. Comunica tus hallazgos de forma clara
                
                Colabora constructivamente con el análisis previo.
                """,
                expected_output="Análisis expandido con perspectiva adicional",
                agent=agents[1],
                context=[tasks[0]],
            ))
        
        # Task 3: Deep Analysis (if more agents)
        if len(agents) > 2:
            tasks.append(Task(
                description=f"""
                TAREA: Profundiza en los aspectos más complejos identificados.
                
                SOLICITUD ORIGINAL: "{message}"
                
                INSTRUCCIONES:
                1. Revisa los análisis de los agentes anteriores
                2. Identifica los aspectos que requieren análisis más profundo
                3. Aplica razonamiento crítico a las conclusiones previas
                4. Proporciona insights adicionales desde tu expertise
                5. Prepara puntos para la síntesis final
                """,
                expected_output="Análisis profundo con insights críticos",
                agent=agents[2],
                context=tasks[:2],
            ))
        
        # Task 4: Validation (if more agents)
        if len(agents) > 3:
            tasks.append(Task(
                description=f"""
                TAREA: Valida y verifica las conclusiones de los agentes anteriores.
                
                SOLICITUD ORIGINAL: "{message}"
                
                INSTRUCCIONES:
                1. Revisa todos los análisis previos
                2. Verifica la consistencia de las conclusiones
                3. Identifica posibles errores o inconsistencias
                4. Confirma los puntos bien fundamentados
                5. Sugiere correcciones si es necesario
                """,
                expected_output="Validación de conclusiones con correcciones si aplica",
                agent=agents[3],
                context=tasks[:3],
            ))
        
        # Task 5: Final Synthesis (if more agents)
        if len(agents) > 4:
            tasks.append(Task(
                description=f"""
                TAREA: Sintetiza todo el trabajo de los agentes en una respuesta final.
                
                SOLICITUD ORIGINAL: "{message}"
                
                INSTRUCCIONES:
                1. Integra todos los análisis y perspectivas
                2. Crea una respuesta coherente y completa
                3. Asegura que responde completamente a la solicitud
                4. Formatea la respuesta de manera clara y profesional
                5. Incluye conclusiones y recomendaciones si aplica
                
                Esta es la respuesta final que verá el usuario.
                """,
                expected_output="Respuesta final integrada, clara y completa",
                agent=agents[4],
                context=tasks[:4],
            ))
        
        # Create and run crew with hierarchical process for better collaboration
        try:
            crew = Crew(
                agents=agents,
                tasks=tasks,
                process=Process.sequential,
                verbose=True,
                memory=True,  # Enable memory for better context sharing
            )
            
            result = crew.kickoff()
            
            # Build dialogue from task outputs
            for i, task in enumerate(tasks):
                if hasattr(task, 'output') and task.output:
                    agent_name = agent_names[i] if i < len(agent_names) else f"agent_{i}"
                    dialogues.append({
                        "agent": agent_name,
                        "message": str(task.output),
                        "step": i + 1,
                    })
            
            return {
                "success": True,
                "result": str(result),
                "agents_used": agent_names[:5],
                "dialogues": dialogues,
            }
        except Exception as e:
            return {
                "success": False,
                "result": f"Error ejecutando los agentes: {str(e)}",
                "agents_used": agent_names[:5],
                "dialogues": dialogues,
            }
