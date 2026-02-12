"""
Phase 2 Main Execution Script: Embedding Generation & Vector Storage

This script:
1. Loads Phase 1 processed data
2. Chunks data into semantic units
3. Generates embeddings using sentence-transformers
4. Stores in ChromaDB vector database
5. Stores metadata in SQLite
6. Runs test queries to verify retrieval
"""
import sys
from pathlib import Path
import yaml

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from chunking.chunker import TextChunker
from embeddings.embedding_generator import EmbeddingGenerator
from vector_db.chroma_client import FAISSVectorStore
from metadata_store.sqlite_store import MetadataStore


def load_config():
    """Load configuration."""
    config_path = Path(__file__).parent.parent / 'config' / 'config.yaml'
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def print_header(title: str):
    """Print formatted header."""
    print("\n" + "=" * 70)
    print(f" {title}")
    print("=" * 70 + "\n")


def main():
    print_header("PHASE 2: EMBEDDING GENERATION & VECTOR STORAGE")
    
    # Load config
    config = load_config()
    
    # Step 1: Load and Chunk Data
    print("Step 1: Loading Phase 1 data and creating chunks...")
    print("-" * 70)
    
    chunker = TextChunker()
    phase1_data_path = Path(__file__).parent.parent / '..' / 'phase_1' / 'data' / 'processed'
    phase1_data = chunker.load_phase1_data(str(phase1_data_path))
    
    chunks = chunker.create_all_chunks(phase1_data)
    
    # Save chunks
    chunks_output_path = Path(__file__).parent.parent / 'data' / 'chunks' / 'all_chunks.json'
    chunker.save_chunks(chunks, str(chunks_output_path))
    print()
    
    # Step 2: Generate Embeddings
    print("Step 2: Generating embeddings...")
    print("-" * 70)
    
    embedding_gen = EmbeddingGenerator(
        model_name=config['embedding']['model_name']
    )
    
    chunks_with_embeddings = embedding_gen.generate_chunk_embeddings(chunks)
    print(f"[INFO] Embedding dimension: {embedding_gen.embedding_dimension}")
    print()
    
    # Step 3: Store in FAISS
    print("Step 3: Storing embeddings in FAISS...")
    print("-" * 70)
    
    faiss_path = Path(__file__).parent.parent / 'database' / 'vector_db'
    vector_store = FAISSVectorStore(
        persist_directory=str(faiss_path),
        collection_name=config['vector_db']['collection_name']
    )
    
    # Clear existing data if any (for fresh run)
    current_stats = vector_store.get_collection_stats()
    if current_stats['total_chunks'] > 0:
        print(f"[INFO] Collection already has {current_stats['total_chunks']} items. Clearing...")
        vector_store.clear_collection()
    
    vector_store.add_chunks(chunks_with_embeddings)
    
    faiss_stats = vector_store.get_collection_stats()
    print(f"[INFO] FAISS stats: {faiss_stats}")
    print()
    
    # Step 4: Store Metadata in SQLite
    print("Step 4: Storing metadata in SQLite...")
    print("-" * 70)
    
    sqlite_path = Path(__file__).parent.parent / config['metadata_db']['path']
    metadata_store = MetadataStore(db_path=str(sqlite_path))
    
    metadata_store.add_chunks(chunks_with_embeddings)
    metadata_store.add_instructors(phase1_data['instructors'])
    
    sqlite_stats = metadata_store.get_stats()
    print(f"[INFO] SQLite stats:")
    for key, value in sqlite_stats.items():
        print(f"  - {key}: {value}")
    print()
    
    # Step 5: Test Retrieval
    print("Step 5: Testing semantic search...")
    print("-" * 70)
    
    test_queries = [
        "What topics are covered in week 1?",
        "Who teaches the AI modules?",
        "What is the class schedule on Saturday?",
        "How much does the course cost?"
    ]
    
    for query in test_queries:
        print(f"\nQuery: '{query}'")
        
        # Generate query embedding
        query_embedding = embedding_gen.model.encode([query], normalize_embeddings=True)[0]
        
        # Search
        results = vector_store.search(query_embedding.tolist(), top_k=3)
        
        print(f"Top 3 results:")
        for i, (chunk_id, distance, doc) in enumerate(zip(results['ids'], results['distances'], results['documents'])):
            similarity = 1 - distance  # Convert distance to similarity (for L2)
            print(f"  {i+1}. [{chunk_id}] (similarity: {similarity:.3f})")
            # Handle Unicode characters in console output
            doc_preview = doc[:100].encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')
            print(f"     {doc_preview}...")
    
    print()
    
    # Summary
    print_header("PHASE 2 COMPLETED SUCCESSFULLY!")
    
    print("[SUMMARY]:")
    print(f"  * Total chunks created: {len(chunks)}")
    print(f"  * Curriculum weeks: {len([c for c in chunks if c['metadata']['category'] == 'curriculum'])}")
    print(f"  * Instructors: {len([c for c in chunks if c['metadata']['category'] == 'instructors'])}")
    print(f"  * Tool categories: {len([c for c in chunks if c['metadata']['category'] == 'tools'])}")
    print(f"  * General info chunks: {len([c for c in chunks if c['metadata']['category'] == 'general'])}")
    print(f"  * Embedding dimension: {embedding_gen.embedding_dimension}")
    
    print("\n[OUTPUT]:")
    print(f"  * Chunks: {chunks_output_path}")
    print(f"  * ChromaDB: {chroma_path}")
    print(f"  * SQLite: {sqlite_path}")
    
    print("\n" + "=" * 70)
    
    # Cleanup
    metadata_store.close()


if __name__ == "__main__":
    main()
