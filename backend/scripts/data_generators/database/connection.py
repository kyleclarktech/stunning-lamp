"""Database connection management for FalkorDB."""

import os
import falkordb
from typing import Optional


class DatabaseConnection:
    """Manages FalkorDB connection."""
    
    def __init__(self, host: str = None, port: int = None, graph_name: str = "agent_poc"):
        """Initialize database connection parameters."""
        self.host = host or os.getenv("FALKOR_HOST", "localhost")
        self.port = port or int(os.getenv("FALKOR_PORT", 6379))
        self.graph_name = graph_name
        self._client = None
        self._db = None
    
    def connect(self) -> falkordb.Graph:
        """Connect to FalkorDB and return graph instance."""
        if not self._client:
            print(f"🔌 Connecting to FalkorDB at {self.host}:{self.port}...")
            self._client = falkordb.FalkorDB(host=self.host, port=self.port)
            self._db = self._client.select_graph(self.graph_name)
        return self._db
    
    def clear_graph(self) -> None:
        """Clear all data from the graph."""
        if not self._db:
            self.connect()
        
        print("🧹 Clearing existing data...")
        try:
            self._db.query("MATCH (n) DETACH DELETE n")
        except:
            pass  # Graph might not exist yet
    
    @property
    def db(self) -> falkordb.Graph:
        """Get the database instance."""
        if not self._db:
            self.connect()
        return self._db