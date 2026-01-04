"""
Sistema de Memoria para Agentic RAG
- Short Term Memory: Contexto de la conversación actual
- Long Term Memory: Datos persistentes y conocimiento acumulado
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
import hashlib


@dataclass
class MemoryEntry:
    """Entrada individual de memoria"""
    id: str
    content: str
    timestamp: datetime
    type: str  # "query", "response", "context", "fact"
    metadata: Dict[str, Any] = field(default_factory=dict)
    relevance_score: float = 1.0
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "type": self.type,
            "metadata": self.metadata,
            "relevance_score": self.relevance_score
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> "MemoryEntry":
        return cls(
            id=data["id"],
            content=data["content"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            type=data["type"],
            metadata=data.get("metadata", {}),
            relevance_score=data.get("relevance_score", 1.0)
        )


class ShortTermMemory:
    """
    Memoria a corto plazo - Contexto de la sesión actual
    Mantiene las últimas N interacciones para contexto inmediato
    """
    
    def __init__(self, max_entries: int = 50, max_tokens: int = 8000):
        self.entries: List[MemoryEntry] = []
        self.max_entries = max_entries
        self.max_tokens = max_tokens
        self.session_id = self._generate_session_id()
        
    def _generate_session_id(self) -> str:
        return hashlib.md5(str(datetime.now()).encode()).hexdigest()[:12]
    
    def add(self, content: str, entry_type: str = "context", metadata: Dict = None) -> MemoryEntry:
        """Añadir nueva entrada a la memoria a corto plazo"""
        entry = MemoryEntry(
            id=f"stm_{len(self.entries)}_{self.session_id}",
            content=content,
            timestamp=datetime.now(),
            type=entry_type,
            metadata=metadata or {}
        )
        self.entries.append(entry)
        
        # Mantener límite de entradas
        if len(self.entries) > self.max_entries:
            self.entries = self.entries[-self.max_entries:]
            
        return entry
    
    def get_context(self, last_n: int = 10) -> List[MemoryEntry]:
        """Obtener las últimas N entradas para contexto"""
        return self.entries[-last_n:]
    
    def get_context_string(self, last_n: int = 10) -> str:
        """Obtener contexto como string formateado"""
        entries = self.get_context(last_n)
        context_parts = []
        for entry in entries:
            prefix = "Usuario" if entry.type == "query" else "Sistema"
            context_parts.append(f"[{prefix}]: {entry.content}")
        return "\n".join(context_parts)
    
    def search(self, query: str, top_k: int = 5) -> List[MemoryEntry]:
        """Búsqueda simple por coincidencia de palabras"""
        query_words = set(query.lower().split())
        scored_entries = []
        
        for entry in self.entries:
            entry_words = set(entry.content.lower().split())
            overlap = len(query_words & entry_words)
            if overlap > 0:
                score = overlap / len(query_words)
                scored_entries.append((entry, score))
        
        scored_entries.sort(key=lambda x: x[1], reverse=True)
        return [entry for entry, _ in scored_entries[:top_k]]
    
    def clear(self):
        """Limpiar memoria a corto plazo"""
        self.entries = []
        self.session_id = self._generate_session_id()


class LongTermMemory:
    """
    Memoria a largo plazo - Conocimiento persistente
    Almacena hechos, preferencias y conocimiento acumulado
    """
    
    def __init__(self, storage_path: str = "./data/long_term_memory.json"):
        self.storage_path = storage_path
        self.entries: Dict[str, MemoryEntry] = {}
        self.categories: Dict[str, List[str]] = {}  # category -> list of entry ids
        self._load()
    
    def _load(self):
        """Cargar memoria desde archivo"""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for entry_data in data.get("entries", []):
                        entry = MemoryEntry.from_dict(entry_data)
                        self.entries[entry.id] = entry
                    self.categories = data.get("categories", {})
            except Exception as e:
                print(f"Error loading long term memory: {e}")
    
    def _save(self):
        """Guardar memoria a archivo"""
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        data = {
            "entries": [entry.to_dict() for entry in self.entries.values()],
            "categories": self.categories
        }
        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def add(self, content: str, entry_type: str = "fact", 
            category: str = "general", metadata: Dict = None) -> MemoryEntry:
        """Añadir nueva entrada a la memoria a largo plazo"""
        entry_id = hashlib.md5(f"{content}{datetime.now()}".encode()).hexdigest()[:16]
        entry = MemoryEntry(
            id=f"ltm_{entry_id}",
            content=content,
            timestamp=datetime.now(),
            type=entry_type,
            metadata=metadata or {}
        )
        
        self.entries[entry.id] = entry
        
        # Categorizar
        if category not in self.categories:
            self.categories[category] = []
        self.categories[category].append(entry.id)
        
        self._save()
        return entry
    
    def get_by_category(self, category: str) -> List[MemoryEntry]:
        """Obtener entradas por categoría"""
        entry_ids = self.categories.get(category, [])
        return [self.entries[eid] for eid in entry_ids if eid in self.entries]
    
    def search(self, query: str, top_k: int = 10, category: str = None) -> List[MemoryEntry]:
        """Búsqueda en memoria a largo plazo"""
        query_words = set(query.lower().split())
        
        # Filtrar por categoría si se especifica
        if category:
            entries_to_search = self.get_by_category(category)
        else:
            entries_to_search = list(self.entries.values())
        
        scored_entries = []
        for entry in entries_to_search:
            entry_words = set(entry.content.lower().split())
            overlap = len(query_words & entry_words)
            if overlap > 0:
                score = (overlap / len(query_words)) * entry.relevance_score
                scored_entries.append((entry, score))
        
        scored_entries.sort(key=lambda x: x[1], reverse=True)
        return [entry for entry, _ in scored_entries[:top_k]]
    
    def update_relevance(self, entry_id: str, new_score: float):
        """Actualizar puntuación de relevancia de una entrada"""
        if entry_id in self.entries:
            self.entries[entry_id].relevance_score = new_score
            self._save()
    
    def delete(self, entry_id: str):
        """Eliminar entrada de memoria"""
        if entry_id in self.entries:
            del self.entries[entry_id]
            # Eliminar de categorías
            for category in self.categories:
                if entry_id in self.categories[category]:
                    self.categories[category].remove(entry_id)
            self._save()


class MemorySystem:
    """
    Sistema de Memoria Unificado
    Combina memoria a corto y largo plazo para el Agente Central
    """
    
    def __init__(self, storage_path: str = "./data"):
        self.short_term = ShortTermMemory()
        self.long_term = LongTermMemory(f"{storage_path}/long_term_memory.json")
        
    def remember_query(self, query: str, metadata: Dict = None):
        """Recordar una consulta del usuario"""
        self.short_term.add(query, "query", metadata)
        
    def remember_response(self, response: str, metadata: Dict = None):
        """Recordar una respuesta del sistema"""
        self.short_term.add(response, "response", metadata)
        
    def store_fact(self, fact: str, category: str = "general", metadata: Dict = None):
        """Almacenar un hecho en memoria a largo plazo"""
        return self.long_term.add(fact, "fact", category, metadata)
    
    def get_relevant_context(self, query: str, max_short: int = 5, max_long: int = 5) -> Dict:
        """Obtener contexto relevante de ambas memorias"""
        short_term_context = self.short_term.search(query, max_short)
        long_term_context = self.long_term.search(query, max_long)
        
        return {
            "short_term": [e.to_dict() for e in short_term_context],
            "long_term": [e.to_dict() for e in long_term_context],
            "session_context": self.short_term.get_context_string(10)
        }
    
    def get_full_context_for_llm(self, query: str) -> str:
        """Generar contexto completo formateado para el LLM"""
        context = self.get_relevant_context(query)
        
        parts = []
        
        # Contexto de sesión
        if context["session_context"]:
            parts.append("=== CONTEXTO DE SESIÓN ===")
            parts.append(context["session_context"])
        
        # Memoria a largo plazo relevante
        if context["long_term"]:
            parts.append("\n=== CONOCIMIENTO RELEVANTE ===")
            for entry in context["long_term"]:
                parts.append(f"- {entry['content']}")
        
        return "\n".join(parts)
    
    def clear_session(self):
        """Limpiar sesión actual (memoria a corto plazo)"""
        self.short_term.clear()
