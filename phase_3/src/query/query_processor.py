"""
Query processor for Phase 3: Process user queries and generate embeddings.
"""
from sentence_transformers import SentenceTransformer
import re


class QueryProcessor:
    """Process and prepare user queries for retrieval."""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize query processor.
        
        Args:
            model_name: Embedding model name (same as Phase 2)
        """
        print(f"[INFO] Loading query embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        print(f"[OK] Query processor initialized")
    
    def normalize_query(self, query: str) -> str:
        """
        Normalize query text.
        
        Args:
            query: Raw user query
        
        Returns:
            Normalized query string
        """
        # Remove extra whitespace
        query = re.sub(r'\s+', ' ', query).strip()
        
        return query
    
    def generate_query_embedding(self, query: str) -> list:
        """
        Generate embedding for query.
        
        Args:
            query: Query text
        
        Returns:
            Query embedding as list
        """
        embedding = self.model.encode([query], normalize_embeddings=True)[0]
        return embedding.tolist()
    
    def process_query(self, query: str) -> dict:
        """
        Process query end-to-end.
        
        Args:
            query: Raw user query
        
        Returns:
            Processed query dict with normalized text and embedding
        """
        normalized = self.normalize_query(query)
        embedding = self.generate_query_embedding(normalized)
        
        return {
            "original_query": query,
            "normalized_query": normalized,
            "embedding": embedding
        }


if __name__ == "__main__":
    # Test query processor
    processor = QueryProcessor()
    
    test_query = "What topics are covered in week 1?"
    result = processor.process_query(test_query)
    
    print(f"\nOriginal: {result['original_query']}")
    print(f"Normalized: {result['normalized_query']}")
    print(f"Embedding shape: {len(result['embedding'])}")
