"""
Servicio de agentes ATP v1.0.1
Usa OpenAI SDK directamente - Sistema simplificado y robusto
"""
from typing import List, Dict, Any, Optional
from app.llm_providers import chat_completion, get_openai_client

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
    """Servicio para gestionar y ejecutar agentes usando OpenAI SDK directamente"""
    
    def __init__(self, model_id: str = "deepseek", api_config: Optional[Dict[str, Any]] = None):
        self.model_id = model_id
        self.api_config = api_config
    
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
    
    def _build_system_prompt(self, agent_name: str) -> str:
        """Construye el system prompt para un agente"""
        agent_def = AGENT_DEFINITIONS.get(agent_name, {})
        return f"""Eres {agent_def.get('role', 'un asistente experto')}.

TU OBJETIVO: {agent_def.get('goal', 'Ayudar al usuario de la mejor manera posible')}

CONTEXTO: {agent_def.get('backstory', '')}

MARCO DE RAZONAMIENTO:
1. Comprende completamente el problema antes de actuar
2. Descompone problemas complejos en partes manejables
3. Considera múltiples perspectivas
4. Sintetiza hallazgos en soluciones coherentes
5. Evalúa tu propio razonamiento

Proporciona respuestas completas, profesionales y bien estructuradas."""
    
    def execute_task(
        self, 
        message: str, 
        agent_names: List[str],
        context: str = None
    ) -> Dict[str, Any]:
        """Ejecuta una tarea con los agentes seleccionados usando OpenAI SDK directamente"""
        
        if not agent_names:
            return {
                "success": False,
                "result": "No se seleccionaron agentes",
                "agents_used": [],
                "dialogues": [],
            }
        
        dialogues = []
        previous_responses = []
        final_result = ""
        
        # Limitar a 5 agentes máximo
        selected_agents = agent_names[:5]
        
        try:
            for i, agent_name in enumerate(selected_agents):
                if agent_name not in AGENT_DEFINITIONS:
                    continue
                
                # Construir mensajes para este agente
                messages = [
                    {"role": "system", "content": self._build_system_prompt(agent_name)}
                ]
                
                # Añadir contexto de agentes anteriores si existe
                if previous_responses:
                    context_msg = "ANÁLISIS PREVIOS DE OTROS AGENTES:\n"
                    for resp in previous_responses:
                        context_msg += f"\n--- {resp['agent']} ---\n{resp['response']}\n"
                    messages.append({"role": "assistant", "content": context_msg})
                
                # Añadir contexto adicional si existe
                user_msg = message
                if context:
                    user_msg = f"CONTEXTO: {context}\n\nSOLICITUD: {message}"
                
                messages.append({"role": "user", "content": user_msg})
                
                # Llamar al LLM usando chat_completion
                agent_response = chat_completion(
                    messages=messages,
                    api_config=self.api_config
                )
                
                # Guardar respuesta
                dialogues.append({
                    "agent": agent_name,
                    "message": agent_response,
                    "step": i + 1,
                })
                
                previous_responses.append({
                    "agent": AGENT_DEFINITIONS[agent_name]["role"],
                    "response": agent_response
                })
                
                final_result = agent_response
            
            # Si hay múltiples agentes, crear una síntesis final
            if len(selected_agents) > 1 and len(previous_responses) > 1:
                synthesis_messages = [
                    {"role": "system", "content": "Eres el Agente de Síntesis Final. Tu trabajo es integrar las respuestas de múltiples agentes en una respuesta coherente y completa."}
                ]
                
                synthesis_content = f"SOLICITUD ORIGINAL: {message}\n\nRESPUESTAS DE LOS AGENTES:\n"
                for resp in previous_responses:
                    synthesis_content += f"\n--- {resp['agent']} ---\n{resp['response']}\n"
                
                synthesis_content += "\nINSTRUCCIONES: Integra los mejores puntos de cada agente, elimina redundancias, y crea una respuesta final coherente y profesional."
                
                synthesis_messages.append({"role": "user", "content": synthesis_content})
                
                final_result = chat_completion(
                    messages=synthesis_messages,
                    api_config=self.api_config
                )
                
                dialogues.append({
                    "agent": "synthesis",
                    "message": final_result,
                    "step": len(selected_agents) + 1,
                })
            
            return {
                "success": True,
                "result": final_result,
                "agents_used": selected_agents,
                "dialogues": dialogues,
            }
            
        except Exception as e:
            error_msg = str(e)
            return {
                "success": False,
                "result": "",
                "error": error_msg,
                "agents_used": selected_agents,
                "dialogues": dialogues,
            }
