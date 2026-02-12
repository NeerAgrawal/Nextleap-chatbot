"""
Embedding generator using sentence-transformers for Phase 2.
"""
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict


class EmbeddingGenerator:
    """Generate semantic embeddings for text chunks."""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize embedding model.
        
        Args:
            model_name: Sentence transformer model name
        """
        print(f"[INFO] Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.model_name = model_name
        print(f"[OK] Model loaded successfully")
    
    def generate_embeddings(self, texts: List[str], batch_size: int = 32, 
                           normalize: bool = True) -> np.ndarray:
        """
        Generate embeddings for a list of texts.
        
        Args:
            texts: List of text strings to embed
            batch_size: Batch size for encoding
            normalize: Whether to normalize embeddings for cosine similarity
        
        Returns:
            numpy array of embeddings (shape: [num_texts, embedding_dim])
        """
        print(f"[INFO] Generating embeddings for {len(texts)} texts...")
        
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            normalize_embeddings=normalize,
            show_progress_bar=True
        )
        
        print(f"[OK] Generated embeddings with shape: {embeddings.shape}")
        return embeddings
    
    def generate_chunk_embeddings(self, chunks: List[Dict]) -> List[Dict]:
        """
        Generate embeddings for chunks and attach to chunk data.
        
        Args:
            chunks: List of chunk dictionaries with 'content' field
        
        Returns:
            Chunks with embeddings added
        """
        # Extract text content
        texts = [chunk['content'] for chunk in chunks]
        
        # Generate embeddings
        embeddings = self.generate_embeddings(texts)
        
        # Attach embeddings to chunks
        for idx, chunk in enumerate(chunks):
            chunk['embedding'] = embeddings[idx].tolist()
        
        return chunks
    
    @property
    def embedding_dimension(self) -> int:
        """Get the embedding dimension of the model."""
        return self.model.get_sentence_embedding_dimension()


if __name__ == "__main__":
    # Test embedding generator
    generator = EmbeddingGenerator()
    
    # Test with sample texts
    test_texts = [
        "Week 1: Mapping Business Outcomes to Product Outcomes",
        "Instructor: Arindam Mukherjee teaches the first 3 weeks"
    ]
    
    embeddings = generator.generate_embeddings(test_texts)
    print(f"\nTest embedding shape: {embeddings.shape}")
    print(f"Embedding dimension: {generator.embedding_dimension}")
