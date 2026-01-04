"""
MCP Servers (Model Context Protocol) para Agentic RAG
Conexión con el mundo real:
- Local Data Server: Archivos locales del usuario
- Search Engine Server: Búsquedas en internet
- Cloud Engine Server: Servicios en la nube
"""

import os
import json
import asyncio
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from datetime import datetime
import hashlib


@dataclass
class MCPResponse:
    """Respuesta de un servidor MCP"""
    server_id: str
    success: bool
    data: Any
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    error: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return {
            "server_id": self.server_id,
            "success": self.success,
            "data": self.data,
            "metadata": self.metadata,
            "timestamp": self.timestamp.isoformat(),
            "error": self.error
        }


class BaseMCPServer(ABC):
    """Clase base para servidores MCP"""
    
    def __init__(self, server_id: str, name: str):
        self.server_id = server_id
        self.name = name
        self.is_connected = False
        self.last_activity = None
        
    @abstractmethod
    async def connect(self) -> bool:
        """Conectar al servidor"""
        pass
    
    @abstractmethod
    async def disconnect(self) -> bool:
        """Desconectar del servidor"""
        pass
    
    @abstractmethod
    async def query(self, request: Dict) -> MCPResponse:
        """Ejecutar consulta en el servidor"""
        pass
    
    def get_status(self) -> Dict:
        return {
            "server_id": self.server_id,
            "name": self.name,
            "is_connected": self.is_connected,
            "last_activity": self.last_activity.isoformat() if self.last_activity else None
        }


class LocalDataServer(BaseMCPServer):
    """
    Servidor de Datos Locales
    Permite a la IA leer archivos locales (documentos, código, etc.)
    """
    
    def __init__(self, base_path: str = "./data"):
        super().__init__("local_data", "Local Data Server")
        self.base_path = base_path
        self.allowed_extensions = [
            '.txt', '.md', '.json', '.yaml', '.yml',
            '.py', '.js', '.ts', '.tsx', '.jsx',
            '.html', '.css', '.sql', '.csv'
        ]
        self.file_cache: Dict[str, Dict] = {}
        
    async def connect(self) -> bool:
        """Verificar acceso al sistema de archivos"""
        try:
            os.makedirs(self.base_path, exist_ok=True)
            self.is_connected = True
            self.last_activity = datetime.now()
            return True
        except Exception as e:
            self.is_connected = False
            return False
    
    async def disconnect(self) -> bool:
        self.is_connected = False
        self.file_cache.clear()
        return True
    
    async def query(self, request: Dict) -> MCPResponse:
        """
        Ejecutar consulta de archivos locales
        
        Tipos de request:
        - {"action": "list", "path": "..."}
        - {"action": "read", "path": "..."}
        - {"action": "search", "query": "...", "path": "..."}
        """
        self.last_activity = datetime.now()
        action = request.get("action", "list")
        
        try:
            if action == "list":
                result = await self._list_files(request.get("path", self.base_path))
            elif action == "read":
                result = await self._read_file(request.get("path"))
            elif action == "search":
                result = await self._search_files(
                    request.get("query", ""),
                    request.get("path", self.base_path)
                )
            else:
                return MCPResponse(
                    server_id=self.server_id,
                    success=False,
                    data=None,
                    error=f"Unknown action: {action}"
                )
            
            return MCPResponse(
                server_id=self.server_id,
                success=True,
                data=result,
                metadata={"action": action}
            )
            
        except Exception as e:
            return MCPResponse(
                server_id=self.server_id,
                success=False,
                data=None,
                error=str(e)
            )
    
    async def _list_files(self, path: str) -> List[Dict]:
        """Listar archivos en un directorio"""
        files = []
        if os.path.exists(path):
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                files.append({
                    "name": item,
                    "path": item_path,
                    "is_dir": os.path.isdir(item_path),
                    "size": os.path.getsize(item_path) if os.path.isfile(item_path) else 0
                })
        return files
    
    async def _read_file(self, path: str) -> Dict:
        """Leer contenido de un archivo"""
        if not path:
            raise ValueError("Path is required")
        
        ext = os.path.splitext(path)[1].lower()
        if ext not in self.allowed_extensions:
            raise ValueError(f"File type {ext} not allowed")
        
        # Verificar cache
        cache_key = hashlib.md5(path.encode()).hexdigest()
        if cache_key in self.file_cache:
            cached = self.file_cache[cache_key]
            if os.path.getmtime(path) == cached.get("mtime"):
                return cached["data"]
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        result = {
            "path": path,
            "content": content,
            "size": len(content),
            "lines": content.count('\n') + 1
        }
        
        # Cachear resultado
        self.file_cache[cache_key] = {
            "data": result,
            "mtime": os.path.getmtime(path)
        }
        
        return result
    
    async def _search_files(self, query: str, path: str) -> List[Dict]:
        """Buscar en archivos por contenido"""
        results = []
        query_lower = query.lower()
        
        for root, dirs, files in os.walk(path):
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in self.allowed_extensions:
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            if query_lower in content.lower():
                                # Encontrar líneas con coincidencias
                                matches = []
                                for i, line in enumerate(content.split('\n'), 1):
                                    if query_lower in line.lower():
                                        matches.append({
                                            "line_number": i,
                                            "content": line.strip()[:200]
                                        })
                                
                                results.append({
                                    "path": file_path,
                                    "matches": matches[:10],  # Limitar a 10 coincidencias
                                    "total_matches": len(matches)
                                })
                    except Exception:
                        continue
        
        return results


class SearchEngineServer(BaseMCPServer):
    """
    Servidor de Motor de Búsqueda
    Permite búsquedas en internet usando APIs configuradas
    """
    
    def __init__(self, api_providers: Dict[str, Dict] = None):
        super().__init__("search_engine", "Search Engine Server")
        self.api_providers = api_providers or {}
        self.search_history: List[Dict] = []
        
    async def connect(self) -> bool:
        """Verificar conexión con proveedores de búsqueda"""
        self.is_connected = len(self.api_providers) > 0
        self.last_activity = datetime.now()
        return self.is_connected
    
    async def disconnect(self) -> bool:
        self.is_connected = False
        return True
    
    def configure_provider(self, provider_name: str, config: Dict):
        """Configurar un proveedor de búsqueda"""
        self.api_providers[provider_name] = config
        self.is_connected = True
    
    async def query(self, request: Dict) -> MCPResponse:
        """
        Ejecutar búsqueda
        
        Request format:
        {
            "action": "search",
            "query": "...",
            "provider": "brave|serper|google",  # opcional
            "max_results": 10
        }
        """
        self.last_activity = datetime.now()
        action = request.get("action", "search")
        
        if action != "search":
            return MCPResponse(
                server_id=self.server_id,
                success=False,
                data=None,
                error=f"Unknown action: {action}"
            )
        
        query = request.get("query", "")
        if not query:
            return MCPResponse(
                server_id=self.server_id,
                success=False,
                data=None,
                error="Query is required"
            )
        
        try:
            # Intentar búsqueda con proveedores disponibles
            results = await self._perform_search(
                query,
                request.get("provider"),
                request.get("max_results", 10)
            )
            
            # Guardar en historial
            self.search_history.append({
                "query": query,
                "timestamp": datetime.now().isoformat(),
                "results_count": len(results)
            })
            
            return MCPResponse(
                server_id=self.server_id,
                success=True,
                data=results,
                metadata={"query": query, "provider": request.get("provider", "default")}
            )
            
        except Exception as e:
            return MCPResponse(
                server_id=self.server_id,
                success=False,
                data=None,
                error=str(e)
            )
    
    async def _perform_search(self, query: str, provider: str = None, 
                              max_results: int = 10) -> List[Dict]:
        """Realizar búsqueda usando el proveedor especificado o disponible"""
        
        # Si no hay proveedores configurados, retornar resultados simulados
        if not self.api_providers:
            return self._get_mock_results(query, max_results)
        
        # Seleccionar proveedor
        if provider and provider in self.api_providers:
            selected_provider = provider
        else:
            selected_provider = list(self.api_providers.keys())[0]
        
        config = self.api_providers[selected_provider]
        
        # Implementar llamadas reales a APIs según el proveedor
        # Por ahora retornamos mock results
        return self._get_mock_results(query, max_results)
    
    def _get_mock_results(self, query: str, max_results: int) -> List[Dict]:
        """Resultados simulados para desarrollo"""
        return [
            {
                "title": f"Resultado {i+1} para: {query}",
                "url": f"https://example.com/result{i+1}",
                "snippet": f"Este es un resultado de búsqueda simulado para la consulta '{query}'...",
                "source": "mock"
            }
            for i in range(min(max_results, 5))
        ]


class CloudEngineServer(BaseMCPServer):
    """
    Servidor de Motor en la Nube
    Conexión con servicios cloud (AWS, Azure, GCP)
    """
    
    def __init__(self):
        super().__init__("cloud_engine", "Cloud Engine Server")
        self.cloud_providers: Dict[str, Dict] = {}
        self.active_connections: Dict[str, bool] = {}
        
    async def connect(self) -> bool:
        """Conectar a servicios cloud configurados"""
        self.is_connected = True
        self.last_activity = datetime.now()
        return True
    
    async def disconnect(self) -> bool:
        self.is_connected = False
        self.active_connections.clear()
        return True
    
    def configure_cloud_provider(self, provider: str, credentials: Dict):
        """Configurar proveedor cloud"""
        self.cloud_providers[provider] = credentials
        self.active_connections[provider] = False
    
    async def query(self, request: Dict) -> MCPResponse:
        """
        Ejecutar operación en la nube
        
        Request format:
        {
            "action": "storage|compute|database",
            "provider": "aws|azure|gcp",
            "operation": "...",
            "params": {...}
        }
        """
        self.last_activity = datetime.now()
        action = request.get("action", "status")
        
        try:
            if action == "status":
                result = self._get_cloud_status()
            elif action == "storage":
                result = await self._storage_operation(request)
            elif action == "compute":
                result = await self._compute_operation(request)
            else:
                result = {"message": f"Action {action} not implemented yet"}
            
            return MCPResponse(
                server_id=self.server_id,
                success=True,
                data=result,
                metadata={"action": action}
            )
            
        except Exception as e:
            return MCPResponse(
                server_id=self.server_id,
                success=False,
                data=None,
                error=str(e)
            )
    
    def _get_cloud_status(self) -> Dict:
        """Obtener estado de conexiones cloud"""
        return {
            "configured_providers": list(self.cloud_providers.keys()),
            "active_connections": self.active_connections,
            "available_services": ["storage", "compute", "database"]
        }
    
    async def _storage_operation(self, request: Dict) -> Dict:
        """Operaciones de almacenamiento cloud"""
        operation = request.get("operation", "list")
        return {
            "operation": operation,
            "status": "simulated",
            "message": "Cloud storage operations will be implemented with actual credentials"
        }
    
    async def _compute_operation(self, request: Dict) -> Dict:
        """Operaciones de cómputo cloud"""
        operation = request.get("operation", "status")
        return {
            "operation": operation,
            "status": "simulated",
            "message": "Cloud compute operations will be implemented with actual credentials"
        }


class MCPServerManager:
    """
    Gestor de Servidores MCP
    Coordina todos los servidores MCP disponibles
    """
    
    def __init__(self, data_path: str = "./data"):
        self.servers: Dict[str, BaseMCPServer] = {}
        self.data_path = data_path
        
        # Inicializar servidores por defecto
        self._init_default_servers()
    
    def _init_default_servers(self):
        """Inicializar servidores por defecto"""
        self.servers["local_data"] = LocalDataServer(self.data_path)
        self.servers["search_engine"] = SearchEngineServer()
        self.servers["cloud_engine"] = CloudEngineServer()
    
    async def connect_all(self) -> Dict[str, bool]:
        """Conectar todos los servidores"""
        results = {}
        for server_id, server in self.servers.items():
            results[server_id] = await server.connect()
        return results
    
    async def disconnect_all(self) -> Dict[str, bool]:
        """Desconectar todos los servidores"""
        results = {}
        for server_id, server in self.servers.items():
            results[server_id] = await server.disconnect()
        return results
    
    def get_server(self, server_id: str) -> Optional[BaseMCPServer]:
        """Obtener servidor por ID"""
        return self.servers.get(server_id)
    
    async def query_server(self, server_id: str, request: Dict) -> MCPResponse:
        """Ejecutar consulta en un servidor específico"""
        server = self.servers.get(server_id)
        if not server:
            return MCPResponse(
                server_id=server_id,
                success=False,
                data=None,
                error=f"Server {server_id} not found"
            )
        
        if not server.is_connected:
            await server.connect()
        
        return await server.query(request)
    
    async def query_all(self, request: Dict) -> Dict[str, MCPResponse]:
        """Ejecutar consulta en todos los servidores"""
        results = {}
        for server_id in self.servers:
            results[server_id] = await self.query_server(server_id, request)
        return results
    
    def get_all_status(self) -> Dict[str, Dict]:
        """Obtener estado de todos los servidores"""
        return {
            server_id: server.get_status()
            for server_id, server in self.servers.items()
        }
    
    def configure_search_provider(self, provider_name: str, config: Dict):
        """Configurar proveedor de búsqueda"""
        search_server = self.servers.get("search_engine")
        if isinstance(search_server, SearchEngineServer):
            search_server.configure_provider(provider_name, config)
    
    def configure_cloud_provider(self, provider: str, credentials: Dict):
        """Configurar proveedor cloud"""
        cloud_server = self.servers.get("cloud_engine")
        if isinstance(cloud_server, CloudEngineServer):
            cloud_server.configure_cloud_provider(provider, credentials)
