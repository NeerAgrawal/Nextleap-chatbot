"""
Context retriever for Phase 3: Retrieve relevant context from Phase 2 vector DB.
"""
import sys
from pathlib import Path
from typing import List, Dict, Optional

# Add Phase 2 to path to import vector store
phase2_path = Path(__file__).parent.parent.parent.parent / 'phase_2' / 'src'
sys.path.insert(0, str(phase2_path))

from vector_db.chroma_client import FAISSVectorStore
from metadata_store.sqlite_store import MetadataStore


class ContextRetriever:
    """Retrieve relevant context from vector database for RAG."""
    
    def __init__(self, 
                 vector_db_path: str,
                 metadata_db_path: str,
                 collection_name: str = "nextleap_course_v1",
                 top_k: int = 5):
        """
        Initialize context retriever.
        
        Args:
            vector_db_path: Path to FAISS vector database
            metadata_db_path: Path to SQLite metadata database
            collection_name: Collection name
            top_k: Number of results to retrieve
        """
        print(f"[INFO] Initializing context retriever...")
        
        # Load vector store
        self.vector_store = FAISSVectorStore(
            persist_directory=vector_db_path,
            collection_name=collection_name
        )
        
        # Load metadata store
        self.metadata_store = MetadataStore(db_path=metadata_db_path)
        
        self.top_k = top_k
        
        print(f"[OK] Context retriever initialized (top_k={top_k})")
    
    def retrieve(self, query_embedding: List[float], 
                 category_filter: Optional[str] = None) -> List[Dict]:
        """
        Retrieve relevant chunks for query.
        
        Args:
            query_embedding: Query embedding vector
            category_filter: Optional category filter (e.g., "curriculum")
        
        Returns:
            List of relevant chunks with content and metadata
        """
        # Search vector database
        filter_metadata = {"category": category_filter} if category_filter else None
        
        results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=self.top_k,
            filter_metadata=filter_metadata
        )
        
        # Format results
        retrieved_chunks = []
        for i, (chunk_id, distance, doc, metadata) in enumerate(zip(
            results['ids'],
            results['distances'],
            results['documents'],
            results['metadatas']
        )):
            similarity = 1 - distance  # Convert L2 distance to similarity
            
            retrieved_chunks.append({
                "chunk_id": chunk_id,
                "content": doc,
                "metadata": metadata,
                "similarity": float(similarity),
                "rank": i + 1
            })
        
        return retrieved_chunks
    
    def build_context(self, retrieved_chunks: List[Dict], max_chunks: int = 5) -> str:
        """
        Build formatted context from retrieved chunks.
        
        Args:
            retrieved_chunks: List of retrieved chunks
            max_chunks: Maximum number of chunks to include
        
        Returns:
            Formatted context string for LLM
        """
        context_parts = ["Context Information:", "---"]
        
        for chunk in retrieved_chunks[:max_chunks]:
            metadata = chunk['metadata']
            
            # Format source info
            if metadata['category'] == 'curriculum':
                source = f"Week {metadata.get('week', '?')}: {metadata.get('title', 'Course Content')}"
            elif metadata['category'] == 'instructors':
                source = f"Instructor: {metadata.get('instructor_name', 'Faculty')}"
            elif metadata['category'] == 'tools':
                source = f"Tools: {metadata.get('tool_category', 'Technology')}"
            else:
                source = f"{metadata['category'].title()}"
            
            context_parts.append(f"\n[{source}]")
            context_parts.append(chunk['content'])
            context_parts.append(f"(Source: {metadata['source']}, Relevance: {chunk['similarity']:.2f})")
        
        context_parts.append("\n---")
        
        return "\n".join(context_parts)
    
    def close(self):
        """Close database connections."""
        self.metadata_store.close()


if __name__ == "__main__":
    # Test retriever
    import numpy as np
    
    retriever = ContextRetriever(
        vector_db_path="../../phase_2/database/vector_db",
        metadata_db_path="../../phase_2/database/metadata.db"
    )
    
    # Test with random embedding
    test_embedding = np.random.randn(384).tolist()
    chunks = retriever.retrieve(test_embedding)
    
    print(f"\nRetrieved {len(chunks)} chunks")
    for chunk in chunks[:2]:
        print(f"- {chunk['chunk_id']}: {chunk['similarity']:.3f}")
    
    retriever.close()
