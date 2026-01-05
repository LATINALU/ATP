export type Language = 'es' | 'en';

export const translations = {
  es: {
    // Node Workflow Editor
    nodeWorkflowEditor: 'Editor de Flujo de Nodos',
    chatInterface: 'Interfaz de Chat',
    save: 'Guardar',
    load: 'Cargar',
    clear: 'Limpiar',
    import: 'Importar',
    export: 'Exportar',
    runWorkflow: 'Ejecutar Flujo',
    running: 'Ejecutando...',
    
    // Nodes
    addNodes: 'Agregar Nodos',
    inputNode: 'Entrada',
    agentNode: 'Agente',
    promptNode: 'Prompt',
    aiProviderNode: 'Proveedor IA',
    outputNode: 'Salida',
    
    // Descriptions
    userInput: 'Entrada del usuario',
    aiAgent: 'Agente IA',
    promptsPositiveNegative: 'Prompts +/-',
    modelConfig: 'Configuración de modelo',
    finalResult: 'Resultado final',
    
    // How to use
    howToUse: '💡 Cómo usar',
    clickNodesToAdd: 'Click en nodos para agregarlos',
    dragToConnect: 'Arrastra para conectar nodos',
    clickToConfig: 'Click en nodos para configurar',
    runToExecute: 'Ejecuta para procesar workflow',
    
    // Connection colors
    connectionColors: '🎨 Colores de Conexiones',
    inputConnection: 'Input → Prompt (Cyan)',
    promptConnection: 'Prompt → Agent (Púrpura)',
    agentConnection: 'Agent → AI Provider/Agent/Output (Verde)',
    providerConnection: 'AI Provider → Agent (Naranja)',
    
    // Validation
    invalidConnection: 'Conexión no válida',
    validConnections: 'Conexiones válidas',
    
    // Agent
    selectAgent: 'Seleccionar Agente',
    additionalInstructions: 'Instrucciones Adicionales',
    addSpecificInstructions: 'Agregar instrucciones específicas para este agente...',
    
    // Prompt
    positivePrompt: '✓ Prompt Positivo',
    negativePrompt: '✗ Prompt Negativo',
    whatYouWant: 'Lo que quieres...',
    whatYouDontWant: 'Lo que no quieres...',
    clickToEdit: 'Click + para editar prompts',
    
    // AI Provider
    provider: 'Proveedor',
    model: 'Modelo',
    temperature: 'Temperatura',
    maxTokens: 'Tokens Máximos',
    selectModel: '-- Seleccionar Modelo --',
    enterModelName: 'Ingresa nombre del modelo',
    
    // Output
    noOutputYet: 'Sin salida aún. Ejecuta el workflow para ver resultados.',
    copyResult: 'Copiar resultado',
    
    // Messages
    workflowSaved: '✅ Workflow guardado en el navegador!',
    workflowLoaded: '✅ Workflow cargado desde el navegador!',
    noSavedWorkflow: '⚠️ No se encontró workflow guardado en el navegador.',
    workflowImported: '✅ Workflow importado exitosamente!',
    invalidWorkflowFormat: '⚠️ Formato de workflow inválido.',
    errorParsingWorkflow: '❌ Error al analizar archivo de workflow.',
    workflowExecutedSuccess: '✅ Workflow ejecutado exitosamente!',
    workflowExecutionFailed: '❌ Ejecución de workflow falló',
    
    // Themes
    selectTheme: 'Seleccionar Tema',
    themesAvailable: '10 temas disponibles',
    
    // Settings
    newChat: 'Nuevo Chat',
    switchToNodeEditor: 'Cambiar a Editor de Nodos',
    configureAPIs: 'Configurar APIs',
  },
  en: {
    // Node Workflow Editor
    nodeWorkflowEditor: 'Node Workflow Editor',
    chatInterface: 'Chat Interface',
    save: 'Save',
    load: 'Load',
    clear: 'Clear',
    import: 'Import',
    export: 'Export',
    runWorkflow: 'Run Workflow',
    running: 'Running...',
    
    // Nodes
    addNodes: 'Add Nodes',
    inputNode: 'Input',
    agentNode: 'Agent',
    promptNode: 'Prompt',
    aiProviderNode: 'AI Provider',
    outputNode: 'Output',
    
    // Descriptions
    userInput: 'User input',
    aiAgent: 'AI Agent',
    promptsPositiveNegative: 'Prompts +/-',
    modelConfig: 'Model config',
    finalResult: 'Final result',
    
    // How to use
    howToUse: '💡 How to use',
    clickNodesToAdd: 'Click nodes to add them',
    dragToConnect: 'Drag to connect nodes',
    clickToConfig: 'Click nodes to configure',
    runToExecute: 'Run to execute workflow',
    
    // Connection colors
    connectionColors: '🎨 Connection Colors',
    inputConnection: 'Input → Prompt (Cyan)',
    promptConnection: 'Prompt → Agent (Purple)',
    agentConnection: 'Agent → AI Provider/Agent/Output (Green)',
    providerConnection: 'AI Provider → Agent (Orange)',
    
    // Validation
    invalidConnection: 'Invalid connection',
    validConnections: 'Valid connections',
    
    // Agent
    selectAgent: 'Select Agent',
    additionalInstructions: 'Additional Instructions',
    addSpecificInstructions: 'Add specific instructions for this agent...',
    
    // Prompt
    positivePrompt: '✓ Positive Prompt',
    negativePrompt: '✗ Negative Prompt',
    whatYouWant: 'What you want...',
    whatYouDontWant: "What you don't want...",
    clickToEdit: 'Click + to edit prompts',
    
    // AI Provider
    provider: 'Provider',
    model: 'Model',
    temperature: 'Temperature',
    maxTokens: 'Max Tokens',
    selectModel: '-- Select Model --',
    enterModelName: 'Enter model name',
    
    // Output
    noOutputYet: 'No output yet. Run the workflow to see results.',
    copyResult: 'Copy result',
    
    // Messages
    workflowSaved: '✅ Workflow saved to browser storage!',
    workflowLoaded: '✅ Workflow loaded from browser storage!',
    noSavedWorkflow: '⚠️ No saved workflow found in browser storage.',
    workflowImported: '✅ Workflow imported successfully!',
    invalidWorkflowFormat: '⚠️ Invalid workflow file format.',
    errorParsingWorkflow: '❌ Error parsing workflow file.',
    workflowExecutedSuccess: '✅ Workflow executed successfully!',
    workflowExecutionFailed: '❌ Workflow execution failed',
    
    // Themes
    selectTheme: 'Select Theme',
    themesAvailable: '10 themes available',
    
    // Settings
    newChat: 'New Chat',
    switchToNodeEditor: 'Switch to Node Editor',
    configureAPIs: 'Configure APIs',
  },
};

export function getTranslation(lang: Language, key: keyof typeof translations.es): string {
  return translations[lang][key] || translations.es[key];
}

export function getCurrentLanguage(): Language {
  if (typeof window !== 'undefined') {
    const saved = localStorage.getItem('atp-language') as Language;
    return saved || 'es';
  }
  return 'es';
}

export function setCurrentLanguage(lang: Language): void {
  if (typeof window !== 'undefined') {
    localStorage.setItem('atp-language', lang);
  }
}
