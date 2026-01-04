"use client";

import { useState, useEffect } from "react";
import { createPortal } from "react-dom";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import { 
  Brain, 
  Target, 
  Search, 
  BarChart3, 
  Layers, 
  AlertTriangle,
  Code2,
  PenTool,
  Database,
  MessageSquare,
  Scale,
  Lightbulb,
  Gavel,
  DollarSign,
  Palette,
  Cpu,
  GraduationCap,
  Megaphone,
  CheckCircle2,
  FileText,
  Zap,
  Shield,
  Link2,
  Eye,
  Languages,
  FileSearch,
  Layout,
  CheckSquare,
  Users,
  HelpCircle
} from "lucide-react";

interface AgentCardProps {
  name: string;
  role: string;
  level: number;
  goal?: string;
  backstory?: string;
  isSelected?: boolean;
  isActive?: boolean;
  onClick?: () => void;
}

// Información detallada de cada agente
const AGENT_DETAILS: Record<string, { goal: string; backstory: string; skills: string[] }> = {
  reasoning_agent: {
    goal: "Aplicar razonamiento riguroso y sistemático para resolver problemas complejos",
    backstory: "Maestro en pensamiento lógico, utiliza razonamiento deductivo, inductivo, abductivo y analógico para llegar a conclusiones bien fundamentadas.",
    skills: ["Lógica formal", "Análisis causal", "Inferencia", "Argumentación"]
  },
  planning_agent: {
    goal: "Crear planes de acción detallados, realistas y ejecutables",
    backstory: "Estratega formado en las mejores prácticas de gestión de proyectos. Descompone objetivos grandes en metas alcanzables.",
    skills: ["Planificación estratégica", "Gestión de recursos", "Cronogramas", "Priorización"]
  },
  research_agent: {
    goal: "Investigar exhaustivamente cualquier tema con rigor académico",
    backstory: "Investigador con la curiosidad de un científico y la meticulosidad de un detective.",
    skills: ["Búsqueda de información", "Análisis de fuentes", "Síntesis de datos", "Verificación"]
  },
  analysis_agent: {
    goal: "Analizar situaciones complejas identificando todos los factores relevantes",
    backstory: "Especializado en diseccionar la complejidad para revelar estructura y significado.",
    skills: ["Análisis de datos", "Identificación de patrones", "Evaluación de riesgos", "Métricas"]
  },
  synthesis_agent: {
    goal: "Integrar información de múltiples fuentes y perspectivas",
    backstory: "El tejedor de conocimiento que transforma fragmentos de información en tapices de comprensión.",
    skills: ["Integración de ideas", "Conexión de conceptos", "Resumen ejecutivo", "Visión holística"]
  },
  critical_thinking_agent: {
    goal: "Evaluar rigurosamente argumentos, evidencias y conclusiones",
    backstory: "Guardián de la calidad intelectual del sistema, detecta falacias y sesgos.",
    skills: ["Detección de falacias", "Evaluación de evidencia", "Pensamiento escéptico", "Validación"]
  },
  coding_agent: {
    goal: "Escribir código limpio, eficiente y mantenible en cualquier lenguaje",
    backstory: "Ingeniero de software con dominio de múltiples paradigmas y lenguajes de programación.",
    skills: ["Python", "JavaScript", "SQL", "Arquitectura de software", "Debug"]
  },
  writing_agent: {
    goal: "Crear contenido escrito claro, persuasivo y adaptado a la audiencia",
    backstory: "Wordsmith que transforma ideas en palabras que informan, persuaden e inspiran.",
    skills: ["Redacción", "Copywriting", "Storytelling", "Edición", "SEO"]
  },
  data_agent: {
    goal: "Analizar datos para extraer insights significativos y accionables",
    backstory: "Científico de datos que convierte números en narrativas y patrones en predicciones.",
    skills: ["Estadística", "Visualización", "Machine Learning", "ETL", "BI"]
  },
  communication_agent: {
    goal: "Facilitar comunicación efectiva entre diferentes partes",
    backstory: "Experto en comunicación que adapta mensajes para diferentes audiencias.",
    skills: ["Comunicación clara", "Presentaciones", "Negociación", "Empatía"]
  },
  decision_agent: {
    goal: "Facilitar la toma de decisiones informadas y estratégicas",
    backstory: "Analista de decisiones que evalúa opciones con criterios objetivos.",
    skills: ["Análisis de decisiones", "Evaluación de riesgos", "Trade-offs", "Priorización"]
  },
  problem_solving_agent: {
    goal: "Resolver problemas complejos con enfoques creativos y sistemáticos",
    backstory: "Solucionador de problemas que combina creatividad con metodología.",
    skills: ["Pensamiento lateral", "Root cause analysis", "Brainstorming", "Innovación"]
  },
  legal_agent: {
    goal: "Proporcionar orientación sobre aspectos legales y regulatorios",
    backstory: "Experto en marcos legales y cumplimiento normativo.",
    skills: ["Derecho contractual", "Compliance", "Propiedad intelectual", "Regulaciones"]
  },
  financial_agent: {
    goal: "Analizar aspectos financieros y económicos",
    backstory: "Analista financiero que evalúa viabilidad económica y optimiza recursos.",
    skills: ["Análisis financiero", "Presupuestos", "ROI", "Proyecciones", "Costos"]
  },
  creative_agent: {
    goal: "Generar ideas innovadoras y soluciones creativas",
    backstory: "Creativo que piensa fuera de la caja y encuentra conexiones inesperadas.",
    skills: ["Ideación", "Diseño thinking", "Innovación", "Creatividad", "Brainstorming"]
  },
  technical_agent: {
    goal: "Proporcionar expertise técnico especializado",
    backstory: "Experto técnico con conocimiento profundo de sistemas y tecnologías.",
    skills: ["Arquitectura", "DevOps", "Cloud", "Seguridad", "Performance"]
  },
  educational_agent: {
    goal: "Facilitar el aprendizaje y la comprensión de conceptos",
    backstory: "Educador que hace accesible el conocimiento complejo.",
    skills: ["Pedagogía", "Explicaciones claras", "Ejemplos", "Tutoriales"]
  },
  marketing_agent: {
    goal: "Desarrollar estrategias de marketing efectivas",
    backstory: "Estratega de marketing que conecta productos con audiencias.",
    skills: ["Estrategia de marca", "Digital marketing", "Contenido", "Analytics"]
  },
  qa_agent: {
    goal: "Asegurar la calidad de entregables y procesos",
    backstory: "Inspector de calidad meticuloso que no deja pasar errores.",
    skills: ["Testing", "QA", "Revisión", "Estándares", "Mejora continua"]
  },
  documentation_agent: {
    goal: "Crear documentación clara y completa",
    backstory: "Documentalista que captura conocimiento de forma estructurada.",
    skills: ["Documentación técnica", "Manuales", "APIs", "Wikis"]
  },
  optimization_agent: {
    goal: "Optimizar procesos y sistemas para máxima eficiencia",
    backstory: "Optimizador que encuentra formas de hacer más con menos.",
    skills: ["Optimización", "Eficiencia", "Automatización", "Performance"]
  },
  security_agent: {
    goal: "Identificar y mitigar riesgos de seguridad",
    backstory: "Experto en seguridad que protege sistemas e información.",
    skills: ["Ciberseguridad", "Análisis de riesgos", "Compliance", "Auditoría"]
  },
  integration_agent: {
    goal: "Integrar sistemas y procesos de forma efectiva",
    backstory: "Integrador que conecta sistemas dispares en soluciones cohesivas.",
    skills: ["APIs", "Integraciones", "Middleware", "ETL", "Workflows"]
  },
  review_agent: {
    goal: "Revisar y mejorar trabajo existente",
    backstory: "Revisor crítico que eleva la calidad del trabajo.",
    skills: ["Code review", "Edición", "Feedback", "Mejoras"]
  },
  translation_agent: {
    goal: "Traducir contenido manteniendo significado y contexto",
    backstory: "Traductor que preserva la esencia del mensaje en diferentes idiomas.",
    skills: ["Traducción", "Localización", "Contexto cultural", "Terminología"]
  },
  summary_agent: {
    goal: "Condensar información en resúmenes claros y útiles",
    backstory: "Sintetizador que extrae lo esencial de grandes volúmenes de información.",
    skills: ["Resumen ejecutivo", "Puntos clave", "Condensación", "Claridad"]
  },
  formatting_agent: {
    goal: "Dar formato profesional y atractivo a cualquier contenido",
    backstory: "Diseñador de información que hace el contenido visualmente efectivo.",
    skills: ["Formato", "Presentación", "Estructura", "Diseño visual"]
  },
  validation_agent: {
    goal: "Verificar la exactitud de información y datos",
    backstory: "Verificador meticuloso que asegura la precisión de los datos.",
    skills: ["Validación", "Fact-checking", "Verificación", "Consistencia"]
  },
  coordination_agent: {
    goal: "Coordinar el trabajo entre múltiples agentes y tareas",
    backstory: "Director de orquesta que sincroniza el trabajo de múltiples partes.",
    skills: ["Coordinación", "Gestión de equipos", "Workflows", "Comunicación"]
  },
  explanation_agent: {
    goal: "Explicar conceptos complejos de manera simple y clara",
    backstory: "Traductor de complejidad a claridad, hace accesible lo difícil.",
    skills: ["Explicaciones", "Analogías", "Simplificación", "Claridad"]
  },
};

const levelVariants: Record<number, string> = {
  1: "level1",
  2: "level2",
  3: "level3",
  4: "level4",
  5: "level5",
};

const levelColors: Record<number, string> = {
  1: "border-red-500/50 hover:border-red-500 hover:shadow-[0_0_20px_rgba(255,0,64,0.3)]",
  2: "border-orange-500/50 hover:border-orange-500 hover:shadow-[0_0_20px_rgba(255,102,0,0.3)]",
  3: "border-yellow-500/50 hover:border-yellow-500 hover:shadow-[0_0_20px_rgba(255,255,0,0.3)]",
  4: "border-cyan-500/50 hover:border-cyan-500 hover:shadow-[0_0_20px_rgba(0,212,255,0.3)]",
  5: "border-purple-500/50 hover:border-purple-500 hover:shadow-[0_0_20px_rgba(189,0,255,0.3)]",
};

const agentIcons: Record<string, React.ComponentType<{ className?: string }>> = {
  reasoning_agent: Brain,
  planning_agent: Target,
  research_agent: Search,
  analysis_agent: BarChart3,
  synthesis_agent: Layers,
  critical_thinking_agent: AlertTriangle,
  coding_agent: Code2,
  writing_agent: PenTool,
  data_agent: Database,
  communication_agent: MessageSquare,
  decision_agent: Scale,
  problem_solving_agent: Lightbulb,
  legal_agent: Gavel,
  financial_agent: DollarSign,
  creative_agent: Palette,
  technical_agent: Cpu,
  educational_agent: GraduationCap,
  marketing_agent: Megaphone,
  qa_agent: CheckCircle2,
  documentation_agent: FileText,
  optimization_agent: Zap,
  security_agent: Shield,
  integration_agent: Link2,
  review_agent: Eye,
  translation_agent: Languages,
  summary_agent: FileSearch,
  formatting_agent: Layout,
  validation_agent: CheckSquare,
  coordination_agent: Users,
  explanation_agent: HelpCircle,
};

interface AgentModel {
  id: string;
  name: string;
}

interface AgentCardPropsExtended extends AgentCardProps {
  availableModels?: AgentModel[];
  selectedModel?: string;
  onModelChange?: (agentName: string, modelId: string) => void;
  customInstructions?: string;
  onInstructionsChange?: (agentName: string, instructions: string) => void;
}

export function AgentCard({ 
  name, 
  role, 
  level, 
  isSelected, 
  isActive, 
  onClick,
  availableModels = [],
  selectedModel,
  onModelChange,
  customInstructions = "",
  onInstructionsChange,
}: AgentCardPropsExtended) {
  const [localInstructions, setLocalInstructions] = useState(customInstructions);
  const [showDetails, setShowDetails] = useState(false);
  const Icon = agentIcons[name] || Brain;
  const levelColor = levelColors[level] || levelColors[1];
  const badgeVariant = levelVariants[level] as "level1" | "level2" | "level3" | "level4" | "level5";
  const details = AGENT_DETAILS[name];

  return (
    <div className="relative">
      <Card
        className={cn(
          "cursor-pointer transition-all duration-300 relative overflow-hidden group",
          levelColor,
          isSelected && "ring-2 ring-primary shadow-[0_0_30px_rgba(0,255,65,0.4)]",
          isActive && "animate-pulse"
        )}
        onClick={onClick}
      >
        {/* Scan line effect on hover */}
        <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none">
          <div className="absolute inset-0 bg-gradient-to-b from-transparent via-primary/5 to-transparent animate-scan-line" />
        </div>

        <CardHeader className="pb-2">
          <div className="flex items-center justify-between">
            <div className="p-2 rounded-lg bg-primary/10 border border-primary/30">
              <Icon className="h-5 w-5 text-primary" />
            </div>
            <Badge variant={badgeVariant}>Nivel {level}</Badge>
          </div>
          <CardTitle className="text-sm mt-2 line-clamp-1">
            {name.replace(/_/g, " ").replace(/agent/i, "").trim()}
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-xs text-muted-foreground line-clamp-2">{role}</p>
          
          {/* Selected Model indicator */}
          {selectedModel && (
            <div className="mt-2 px-2 py-1 bg-accent/10 rounded text-xs text-accent truncate">
              🤖 {selectedModel.split("/").pop()}
            </div>
          )}
          
          {isActive && (
            <div className="mt-2 flex items-center gap-2">
              <div className="h-2 w-2 rounded-full bg-green-500 animate-pulse" />
              <span className="text-xs text-green-400">Procesando...</span>
            </div>
          )}
          
          {/* Ver más button */}
          <button
            onClick={(e) => {
              e.stopPropagation();
              setShowDetails(true);
            }}
            className="mt-2 w-full px-2 py-1.5 text-xs bg-primary/10 hover:bg-primary/20 text-primary border border-primary/30 rounded-lg transition-colors"
          >
            👁️ Ver más / Configurar IA
          </button>
        </CardContent>
      </Card>

      {/* Modal con información detallada - posicionado a la derecha sobre la terminal */}
      {showDetails && details && (
        <>
          {/* Overlay - también con Portal */}
          {createPortal(
            <div 
              className="fixed inset-0 bg-black/40 z-[999998]" 
              onClick={(e) => {
                e.stopPropagation();
                // Guardar instrucciones al cerrar
                if (localInstructions !== customInstructions) {
                  onInstructionsChange?.(name, localInstructions);
                }
                setShowDetails(false);
              }}
            />,
            document.body
          )}
          
          {/* Modal - posicionado más a la izquierda */}
          {createPortal(
            <div 
              className="fixed z-[999999] w-[500px] max-h-[80vh] overflow-y-auto p-4 bg-card border-2 border-primary rounded-lg shadow-2xl transition-all duration-500 ease-out"
              style={{
                left: showDetails ? '25%' : '-100%',
                top: '50%',
                transform: showDetails ? 'translate(-50%, -50%)' : 'translate(-50%, -50%)',
                opacity: showDetails ? 1 : 0,
                visibility: showDetails ? 'visible' : 'hidden',
              }}
              onClick={(e) => e.stopPropagation()}
            >
            <div className="space-y-3">
              {/* Header */}
              <div className="flex items-center justify-between pb-2 border-b border-primary/50">
                <div className="flex items-center gap-2">
                  <div className="p-2 rounded-lg bg-primary/20">
                    <Icon className="h-6 w-6 text-primary" />
                  </div>
                  <div>
                    <span className="font-bold text-lg text-primary block">
                      {name.replace(/_/g, " ").replace(/agent/i, "").trim()}
                    </span>
                    <span className="text-xs text-muted-foreground">Nivel {level}</span>
                  </div>
                </div>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    if (localInstructions !== customInstructions) {
                      onInstructionsChange?.(name, localInstructions);
                    }
                    setShowDetails(false);
                  }}
                  className="p-2 hover:bg-muted rounded-lg text-muted-foreground hover:text-foreground"
                >
                  ✕
                </button>
              </div>
              
              {/* Model Selector */}
              {availableModels.length > 0 && (
                <div className="bg-accent/10 p-3 rounded-lg border border-accent/30">
                  <span className="text-xs font-bold text-accent block mb-2">🤖 MODELO DE IA</span>
                  <select
                    value={selectedModel || ""}
                    onChange={(e) => onModelChange?.(name, e.target.value)}
                    className="w-full px-3 py-2 rounded-lg border border-border bg-background text-foreground text-sm focus:outline-none focus:ring-2 focus:ring-primary/50"
                    onClick={(e) => e.stopPropagation()}
                  >
                    <option value="">Usar modelo por defecto</option>
                    {availableModels.map((model) => (
                      <option key={model.id} value={model.id}>
                        {model.name.split("/").pop()}
                      </option>
                    ))}
                  </select>
                </div>
              )}

              {/* Custom Instructions */}
              <div className="bg-yellow-500/10 p-3 rounded-lg border border-yellow-500/30">
                <span className="text-xs font-bold text-yellow-600 dark:text-yellow-400 block mb-2">
                  📝 INSTRUCCIONES EXTRAS
                </span>
                <textarea
                  value={localInstructions}
                  onChange={(e) => setLocalInstructions(e.target.value)}
                  placeholder="Añade instrucciones específicas para este agente... Ej: 'Responde siempre en español', 'Sé más detallado', 'Usa formato de lista'"
                  className="w-full px-3 py-2 rounded-lg border border-border bg-background text-foreground text-sm focus:outline-none focus:ring-2 focus:ring-yellow-500/50 min-h-[80px] resize-y"
                  onClick={(e) => e.stopPropagation()}
                />
                <button
                  onClick={() => {
                    onInstructionsChange?.(name, localInstructions);
                  }}
                  className="mt-2 w-full px-3 py-1.5 text-xs bg-yellow-500/20 hover:bg-yellow-500/30 text-yellow-600 dark:text-yellow-400 border border-yellow-500/30 rounded-lg transition-colors"
                >
                  💾 Guardar instrucciones
                </button>
              </div>
              
              {/* Goal */}
              <div className="bg-primary/5 p-3 rounded-lg">
                <span className="text-xs font-bold text-primary">🎯 OBJETIVO</span>
                <p className="text-sm text-foreground mt-1">{details.goal}</p>
              </div>
              
              {/* Backstory */}
              <div className="bg-muted/50 p-3 rounded-lg">
                <span className="text-xs font-bold text-primary">📖 DESCRIPCIÓN</span>
                <p className="text-sm text-muted-foreground mt-1">{details.backstory}</p>
              </div>
              
              {/* Skills */}
              <div>
                <span className="text-xs font-bold text-primary">⚡ HABILIDADES</span>
                <div className="flex flex-wrap gap-1.5 mt-2">
                  {details.skills.map((skill) => (
                    <span
                      key={skill}
                      className="px-2.5 py-1 text-xs font-medium bg-primary/20 text-primary rounded-full border border-primary/40"
                    >
                      {skill}
                    </span>
                  ))}
                </div>
              </div>
            </div>
            </div>,
            document.body
          )}
        </>
      )}
    </div>
  );
}
