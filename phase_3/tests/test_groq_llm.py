"""
Unit tests for Groq LLM client.
"""
import pytest
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from project root
project_root = Path(__file__).parent.parent.parent
env_path = project_root / '.env'
load_dotenv(dotenv_path=env_path)

# Import after loading env
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from llm.groq_client import GroqLLMClient


class TestGroqLLMClient:
    """Test suite for Groq LLM client."""
    
    @pytest.fixture
    def llm_client(self):
        """Create LLM client for testing."""
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            pytest.skip("GROQ_API_KEY not set in .env")
        
        return GroqLLMClient(api_key=api_key)
    
    def test_initialization(self, llm_client):
        """Test LLM client initialization."""
        assert llm_client is not None
        assert llm_client.model == "llama-3.3-70b-versatile"
        assert llm_client.temperature == 0.3
    
    def test_generate_response_with_context(self, llm_client):
        """Test response generation with valid context."""
        context = """Context Information:
---
[Week 1: Mapping Business Outcomes to Product Outcomes]
Systems Thinking: understanding actors, flows, bottlenecks
Building KPI Trees for structured problem solving
First principles thinking
(Source: curriculum, Relevance: 0.92)
---"""
        
        query = "What is covered in week 1?"
        
        response = llm_client.generate_response(query, context)
        
        # Verify response structure
        assert "answer" in response
        assert "model" in response
        assert "tokens_used" in response
        assert "finish_reason" in response
        
        # Verify answer contains relevant information
        answer = response['answer'].lower()
        assert len(response['answer']) > 20  # Non-trivial answer
        assert response['finish_reason'] == "stop"  # Completed normally
        
        # Check if answer mentions relevant concepts
        relevant_terms = ["week 1", "systems thinking", "kpi", "business", "product"]
        found_terms = sum(1 for term in relevant_terms if term in answer)
        assert found_terms >= 2, f"Answer should mention at least 2 relevant terms. Answer: {response['answer']}"
        
        print(f"\nTest passed!")
        print(f"Query: {query}")
        print(f"Answer: {response['answer']}")
        print(f"Tokens: {response['tokens_used']}")
    
    def test_generate_response_no_context(self, llm_client):
        """Test response when context doesn't contain answer."""
        context = """Context Information:
---
[Week 8: RAGs and AI Automations]
Embeddings and vector databases
Chunking and retrieval techniques
(Source: curriculum, Relevance: 0.45)
---"""
        
        query = "What is the course fee?"
        
        response = llm_client.generate_response(query, context)
        
        # Should indicate lack of information
        answer = response['answer'].lower()
        assert any(phrase in answer for phrase in [
            "don't have", "not have", "doesn't contain", 
            "not enough information", "cannot", "can't"
        ]), f"Should indicate missing information. Answer: {response['answer']}"
        
        print(f"\nTest passed!")
        print(f"Query: {query}")
        print(f"Answer: {response['answer']}")
    
    def test_generate_response_instructor_query(self, llm_client):
        """Test response for instructor-related query."""
        context = """Context Information:
---
[Instructor: Eshan Tiwari]
Title: Lead Data Scientist at Meta
Background: worked at Google in data science roles
Teaches: modules on AI
(Source: instructors, Relevance: 0.88)
---"""
        
        query = "Who teaches the AI modules?"
        
        response = llm_client.generate_response(query, context)
        
        answer = response['answer'].lower()
        assert "eshan" in answer or "tiwari" in answer, f"Should mention instructor name. Answer: {response['answer']}"
        assert "ai" in answer, "Should mention AI"
        
        print(f"\nTest passed!")
        print(f"Query: {query}")
        print(f"Answer: {response['answer']}")


def run_tests():
    """Run all tests."""
    print("\n" + "=" * 70)
    print(" RUNNING GROQ LLM UNIT TESTS")
    print("=" * 70 + "\n")
    
    pytest.main([__file__, "-v", "-s"])


if __name__ == "__main__":
    run_tests()
