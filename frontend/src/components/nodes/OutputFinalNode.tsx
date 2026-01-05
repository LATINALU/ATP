"use client";

import { memo, useState } from 'react';
import { Handle, Position, NodeProps } from 'reactflow';
import { CheckCircle, Copy, Save, Eye, Download } from 'lucide-react';

export default memo(({ data }: NodeProps) => {
  const [showFullView, setShowFullView] = useState(false);

  const handleSave = () => {
    if (data.result) {
      const blob = new Blob([data.result], { type: 'text/plain' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `output-final-${Date.now()}.txt`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
    }
  };

  const handleCopy = () => {
    if (data.result) {
      navigator.clipboard.writeText(data.result);
      alert('✅ Contenido copiado al portapapeles');
    }
  };

  return (
    <>
      <div className="px-4 py-3 shadow-lg rounded-lg border-2 border-green-500 bg-card/80 backdrop-blur-sm min-w-[320px]">
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center gap-2">
            <CheckCircle className="h-5 w-5 text-green-500" />
            <div className="font-bold text-sm">{data.label}</div>
          </div>
        </div>
        
        <div className="text-xs bg-background border border-border rounded p-2 min-h-[80px] max-h-[200px] overflow-y-auto">
          {data.result || (
            <span className="text-muted-foreground italic">
              Final workflow result will appear here. This is the terminal node.
            </span>
          )}
        </div>

        {/* Botones de acción */}
        {data.result && (
          <div className="flex gap-2 mt-2">
            <button
              onClick={handleCopy}
              className="flex-1 flex items-center justify-center gap-1 px-2 py-1.5 bg-blue-500 hover:bg-blue-600 text-white rounded text-xs transition-colors"
              title="Copiar contenido"
            >
              <Copy className="h-3 w-3" />
              Copy
            </button>
            <button
              onClick={handleSave}
              className="flex-1 flex items-center justify-center gap-1 px-2 py-1.5 bg-green-500 hover:bg-green-600 text-white rounded text-xs transition-colors"
              title="Guardar archivo"
            >
              <Save className="h-3 w-3" />
              Save
            </button>
            <button
              onClick={() => setShowFullView(true)}
              className="flex-1 flex items-center justify-center gap-1 px-2 py-1.5 bg-purple-500 hover:bg-purple-600 text-white rounded text-xs transition-colors"
              title="Ver completo"
            >
              <Eye className="h-3 w-3" />
              View
            </button>
          </div>
        )}

        {/* Handle: Solo 1 entrada azul */}
        <div className="mt-3 pt-2 border-t border-border">
          <div className="flex justify-center items-center">
            <div className="flex flex-col items-center gap-1">
              <Handle
                type="target"
                position={Position.Top}
                id="input"
                className="!w-4 !h-4 !bg-blue-500 !relative !transform-none !border-2 !border-white"
                style={{ position: 'relative' }}
              />
              <div className="text-[9px] text-blue-500 font-semibold">Data In</div>
            </div>
          </div>
        </div>
      </div>

      {/* Modal de vista completa */}
      {showFullView && data.result && (
        <div 
          className="fixed inset-0 bg-black/50 flex items-center justify-center z-[9999]"
          onClick={() => setShowFullView(false)}
        >
          <div 
            className="bg-card border-2 border-green-500 rounded-lg p-6 max-w-4xl max-h-[80vh] overflow-auto m-4"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-bold flex items-center gap-2">
                <CheckCircle className="h-5 w-5 text-green-500" />
                Final Output - Full View
              </h3>
              <button
                onClick={() => setShowFullView(false)}
                className="px-3 py-1 bg-muted hover:bg-muted/80 rounded text-sm"
              >
                Close
              </button>
            </div>
            <div className="bg-background border border-border rounded p-4 whitespace-pre-wrap text-sm">
              {data.result}
            </div>
            <div className="flex gap-2 mt-4">
              <button
                onClick={handleCopy}
                className="flex items-center gap-2 px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded transition-colors"
              >
                <Copy className="h-4 w-4" />
                Copy to Clipboard
              </button>
              <button
                onClick={handleSave}
                className="flex items-center gap-2 px-4 py-2 bg-green-500 hover:bg-green-600 text-white rounded transition-colors"
              >
                <Download className="h-4 w-4" />
                Download File
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
});
