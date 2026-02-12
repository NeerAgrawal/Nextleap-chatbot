"""
Nextleap RAG Chatbot - Main orchestrator for Phase 3.
"""
import os
import sys
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Add Phase 3 src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from query.query_processor import QueryProcessor
from retrieval.retriever import ContextRetriever
from llm.groq_client import GroqLLMClient


class NextleapChatbot:
    """Main chatbot orchestrator integrating all Phase 3 components."""
    
    def __init__(self, 
                 vector_db_path: str,
                 metadata_db_path: str,
                 groq_api_key: Optional[str] = None):
        """
        Initialize Nextleap RAG chatbot.
        
        Args:
            vector_db_path: Path to FAISS vector database
            metadata_db_path: Path to SQLite metadata database
            groq_api_key: Groq API key (from .env if not provided)
        """
        print("\n" + "=" * 70)
        print(" NEXTLEAP RAG CHATBOT - INITIALIZING")
        print("=" * 70 + "\n")
        
        # Load environment variables
        load_dotenv()
        
        # Initialize components
        self.query_processor = QueryProcessor()
        
        self.retriever = ContextRetriever(
            vector_db_path=vector_db_path,
            metadata_db_path=metadata_db_path,
            top_k=int(os.getenv("TOP_K_RESULTS", 5))
        )
        
        self.llm_client = GroqLLMClient(
            api_key=groq_api_key or os.getenv("GROQ_API_KEY"),
            model=os.getenv("GROQ_MODEL", "mixtral-8x7b-32768"),
            temperature=float(os.getenv("GROQ_TEMPERATURE", 0.3)),
            max_tokens=int(os.getenv("GROQ_MAX_TOKENS", 1024))
        )
        
        print("\n[SUCCESS] Chatbot initialized and ready!")
        print("=" * 70 + "\n")
    
    def answer_query(self, user_query: str) -> dict:
        """
        Answer user query using RAG pipeline.
        
        Args:
            user_query: User's question
        
        Returns:
            Response dict with answer, context, and metadata
        """
        print(f"\n[QUERY] {user_query}")
        
        # Step 1: Process query
        processed = self.query_processor.process_query(user_query)
        
        # Step 2: Retrieve context
        retrieved_chunks = self.retriever.retrieve(processed['embedding'])
        context = self.retriever.build_context(retrieved_chunks)
        
        print(f"[INFO] Retrieved {len(retrieved_chunks)} relevant chunks")
        
        # Step 3: Generate response
        llm_response = self.llm_client.generate_response(
            query=user_query,
            context=context
        )
        
        # Build final response
        response = {
            "query": user_query,
            "answer": llm_response['answer'],
            "sources": [
                {
                    "chunk_id": chunk['chunk_id'],
                    "category": chunk['metadata']['category'],
                    "similarity": chunk['similarity']
                }
                for chunk in retrieved_chunks
            ],
            "metadata": {
                "model": llm_response['model'],
                "tokens_used": llm_response['tokens_used'],
                "chunks_retrieved": len(retrieved_chunks)
            }
        }
        
        return response
    
    def close(self):
        """Close database connections."""
        self.retriever.close()


def main():
    """Demo chatbot with sample queries."""
    # Paths to Phase 2 databases
    vector_db_path = Path(__file__).parent.parent.parent / 'phase_2' / 'database' / 'vector_db'
    metadata_db_path = Path(__file__).parent.parent.parent / 'phase_2' / 'database' / 'metadata.db'
    
    # Initialize chatbot
    chatbot = NextleapChatbot(
        vector_db_path=str(vector_db_path),
        metadata_db_path=str(metadata_db_path)
    )
    
    # Sample queries
    test_queries = [
        "What topics are covered in week 1?",
        "Who teaches the  AI modules?",
        "What is the class schedule on Saturday?",
        "How much does the course cost?"
    ]
    
    print("\n" + "=" * 70)
    print(" TESTING CHATBOT WITH SAMPLE QUERIES")
    print("=" * 70 + "\n")
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{'='*70}")
        print(f"Query {i}/{len(test_queries)}")
        print('='*70)
        
        response = chatbot.answer_query(query)
        
        print(f"\n[ANSWER]")
        print(response['answer'])
        
        print(f"\n[SOURCES] ({len(response['sources'])} chunks)")
        for source in response['sources'][:3]:
            print(f"  - {source['chunk_id']} ({source['category']}, similarity: {source['similarity']:.3f})")
        
        print(f"\n[METADATA] Tokens: {response['metadata']['tokens_used']}, Model: {response['metadata']['model']}")
    
    print("\n" + "=" * 70)
    print(" CHATBOT TESTING COMPLETE")
    print("=" * 70 + "\n")
    
    chatbot.close()


if __name__ == "__main__":
    main()
