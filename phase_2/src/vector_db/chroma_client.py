"""
FAISS vector database client for Phase 2 (ChromaDB alternative for Python 3.14 compatibility).
"""
import faiss
import numpy as np
import pickle
import json
from pathlib import Path
from typing import List, Dict, Optional


class FAISSVectorStore:
    """FAISS-based vector store for embedding storage and retrieval."""
    
    def __init__(self, persist_directory: str = "database/vector_db", 
                 collection_name: str = "nextleap_course_v1"):
        """
        Initialize FAISS vector store.
        
        Args:
            persist_directory: Path to persist FAISS data
            collection_name: Name of the collection
        """
        print(f"[INFO] Initializing FAISS vector store...")
        print(f"[INFO] Persist directory: {persist_directory}")
        
        self.persist_directory = Path(persist_directory)
        self.persist_directory.mkdir(parents=True, exist_ok=True)
        
        self.collection_name = collection_name
        self.index = None
        self.metadata_store = []  # Store metadata for each vector
        self.dimension = None
        
        # Try to load existing index
        self._load_index()
        
        print(f"[OK] FAISS vector store initialized")
    
    def _get_index_path(self) -> Path:
        """Get path to FAISS index file."""
        return self.persist_directory / f"{self.collection_name}.index"
    
    def _get_metadata_path(self) -> Path:
        """Get path to metadata file."""
        return self.persist_directory / f"{self.collection_name}_metadata.pkl"
    
    def _load_index(self):
        """Load existing FAISS index if it exists."""
        index_path = self._get_index_path()
        metadata_path = self._get_metadata_path()
        
        if index_path.exists() and metadata_path.exists():
            print(f"[INFO] Loading existing FAISS index from {index_path}")
            self.index = faiss.read_index(str(index_path))
            
            with open(metadata_path, 'rb') as f:
                self.metadata_store = pickle.load(f)
            
            self.dimension = self.index.d
            print(f"[OK] Loaded index with {self.index.ntotal} vectors")
    
    def _save_index(self):
        """Save FAISS index to disk."""
        index_path = self._get_index_path()
        metadata_path = self._get_metadata_path()
        
        faiss.write_index(self.index, str(index_path))
        
        with open(metadata_path, 'wb') as f:
            pickle.dump(self.metadata_store, f)
        
        print(f"[OK] Saved FAISS index to {index_path}")
    
    def add_chunks(self, chunks: List[Dict]):
        """
        Add chunks with embeddings to FAISS.
        
        Args:
            chunks: List of chunks with 'chunk_id', 'content', 'embedding', and 'metadata'
        """
        print(f"\n[INFO] Adding {len(chunks)} chunks to FAISS...")
        
        # Extract embeddings
        embeddings = np.array([chunk['embedding'] for chunk in chunks], dtype='float32')
        
        # Initialize index if not done yet
        if self.index is None:
            self.dimension = embeddings.shape[1]
            # Use L2 distance (can also use faiss.METRIC_INNER_PRODUCT for cosine similarity with normalized vectors)
            self.index = faiss.IndexFlatL2(self.dimension)
            print(f"[INFO] Created FAISS index with dimension {self.dimension}")
        
        # Add vectors to index
        self.index.add(embeddings)
        
        # Store metadata
        for chunk in chunks:
            self.metadata_store.append({
                'chunk_id': chunk['chunk_id'],
                'content': chunk['content'],
                'metadata': chunk['metadata']
            })
        
        # Save to disk
        self._save_index()
        
        print(f"[OK] Successfully added {len(chunks)} chunks to FAISS")
        print(f"[INFO] Total vectors in index: {self.index.ntotal}")
    
    def search(self, query_embedding: List[float], top_k: int = 5, 
               filter_metadata: Optional[Dict] = None) -> Dict:
        """
        Search for similar chunks.
        
        Args:
            query_embedding: Query embedding vector
            top_k: Number of results to return
            filter_metadata: Optional metadata filters (e.g., {"category": "curriculum"})
        
        Returns:
            Dictionary with ids, distances, documents, and metadatas
        """
        if self.index is None or self.index.ntotal == 0:
            print("[WARNING] Index is empty")
            return {"ids": [], "distances": [], "documents": [], "metadatas": []}
        
        # Convert query to numpy array
        query_vector = np.array([query_embedding], dtype='float32')
        
        # Search
        distances, indices = self.index.search(query_vector, min(top_k, self.index.ntotal))
        
        # Get results
        ids = []
        docs = []
        metadatas = []
        result_distances = []
        
        for i, idx in enumerate(indices[0]):
            if idx >= 0 and idx < len(self.metadata_store):
                metadata_entry = self.metadata_store[idx]
                
                # Apply metadata filter if provided
                if filter_metadata:
                    matches = all(
                        metadata_entry['metadata'].get(key) == value 
                        for key, value in filter_metadata.items()
                    )
                    if not matches:
                        continue
                
                ids.append(metadata_entry['chunk_id'])
                docs.append(metadata_entry['content'])
                metadatas.append(metadata_entry['metadata'])
                result_distances.append(float(distances[0][i]))
        
        return {
            "ids": ids,
            "distances": result_distances,
            "documents": docs,
"metadatas": metadatas
        }
    
    def get_collection_stats(self) -> Dict:
        """Get collection statistics."""
        return {
            "collection_name": self.collection_name,
            "total_chunks": self.index.ntotal if self.index else 0,
            "dimension": self.dimension
        }
    
    def clear_collection(self):
        """Clear all data from collection."""
        self.index = None
        self.metadata_store = []
        self.dimension = None
        
        # Remove files
        index_path = self._get_index_path()
        metadata_path = self._get_metadata_path()
        
        if index_path.exists():
            index_path.unlink()
        if metadata_path.exists():
            metadata_path.unlink()
        
        print(f"[INFO] Collection {self.collection_name} cleared")


if __name__ == "__main__":
    # Test FAISS vector store
    vector_store = FAISSVectorStore(persist_directory="../database/vector_db")
    stats = vector_store.get_collection_stats()
    print(f"\nCollection stats: {stats}")
