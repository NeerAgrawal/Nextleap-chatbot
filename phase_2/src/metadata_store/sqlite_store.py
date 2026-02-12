"""
SQLite metadata store for Phase 2.
"""
import sqlite3
import json
from pathlib import Path
from typing import List, Dict, Optional


class MetadataStore:
    """SQLite database for storing chunk metadata and content."""
    
    def __init__(self, db_path: str = "database/metadata.db"):
        """
        Initialize SQLite database.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        
        print(f"[INFO] Initializing SQLite metadata store: {db_path}")
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        
        self._create_tables()
        print(f"[OK] Metadata store initialized")
    
    def _create_tables(self):
        """Create database tables."""
        # Chunks table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS chunks (
                chunk_id TEXT PRIMARY KEY,
                content TEXT NOT NULL,
                source TEXT,
                category TEXT,
                week INTEGER,
                metadata JSON,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Instructors table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS instructors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                title TEXT,
                background TEXT,
                teaches TEXT
            )
        ''')
        
        # Tools table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tools (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT,
                description TEXT
            )
        ''')
        
        # Create indexes
        self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_category ON chunks(category)')
        self.cursor.execute('CREATE INDEX IF NOT EXISTS idx_week ON chunks(week)')
        
        self.conn.commit()
    
    def add_chunks(self, chunks: List[Dict]):
        """
        Add chunks to database.
        
        Args:
            chunks: List of chunk dictionaries
        """
        print(f"\n[INFO] Adding {len(chunks)} chunks to SQLite...")
        
        for chunk in chunks:
            metadata_json = json.dumps(chunk.get('metadata', {}))
            week = chunk.get('metadata', {}).get('week')
            
            self.cursor.execute('''
                INSERT OR REPLACE INTO chunks 
                (chunk_id, content, source, category, week, metadata)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                chunk['chunk_id'],
                chunk['content'],
                chunk.get('metadata', {}).get('source'),
                chunk.get('metadata', {}).get('category'),
                week,
                metadata_json
            ))
        
        self.conn.commit()
        print(f"[OK] Successfully added {len(chunks)} chunks to SQLite")
    
    def add_instructors(self, instructors: List[Dict]):
        """Add instructors to database."""
        for inst in instructors:
            self.cursor.execute('''
                INSERT OR REPLACE INTO instructors (name, title, background, teaches)
                VALUES (?, ?, ?, ?)
            ''', (
                inst['name'],
                inst.get('title', ''),
                inst.get('background', ''),
                inst.get('teaches', '')
            ))
        
        self.conn.commit()
        print(f"[OK] Added {len(instructors)} instructors to SQLite")
    
    def get_chunk_by_id(self, chunk_id: str) -> Optional[Dict]:
        """Get chunk by ID."""
        self.cursor.execute('SELECT * FROM chunks WHERE chunk_id = ?', (chunk_id,))
        row = self.cursor.fetchone()
        
        if row:
            return dict(row)
        return None
    
    def get_chunks_by_category(self, category: str) -> List[Dict]:
        """Get all chunks in a category."""
        self.cursor.execute('SELECT * FROM chunks WHERE category = ?', (category,))
        return [dict(row) for row in self.cursor.fetchall()]
    
    def get_chunks_by_week(self, week: int) -> List[Dict]:
        """Get all chunks for a specific week."""
        self.cursor.execute('SELECT * FROM chunks WHERE week = ?', (week,))
        return [dict(row) for row in self.cursor.fetchall()]
    
    def get_stats(self) -> Dict:
        """Get database statistics."""
        stats = {}
        
        # Total chunks
        self.cursor.execute('SELECT COUNT(*) FROM chunks')
        stats['total_chunks'] = self.cursor.fetchone()[0]
        
        # Chunks by category
        self.cursor.execute('SELECT category, COUNT(*) FROM chunks GROUP BY category')
        stats['chunks_by_category'] = {row[0]: row[1] for row in self.cursor.fetchall()}
        
        # Total instructors
        self.cursor.execute('SELECT COUNT(*) FROM instructors')
        stats['total_instructors'] = self.cursor.fetchone()[0]
        
        return stats
    
    def close(self):
        """Close database connection."""
        self.conn.close()


if __name__ == "__main__":
    # Test metadata store
    store = MetadataStore(db_path="../database/metadata.db")
    stats = store.get_stats()
    print(f"\nDatabase stats: {stats}")
    store.close()
