"""
Groq LLM client for Phase 3: Generate responses using Groq API.
"""
import os
from groq import Groq
from typing import Optional


class GroqLLMClient:
    """Groq LLM client for generating RAG responses."""
    
    # System prompt template
    SYSTEM_PROMPT = """You are a helpful assistant for the NextLeap Product Management Fellowship.
Answer student questions using ONLY the provided context information.

Guidelines:
- Be accurate and cite specific weeks, instructors, or tools when relevant
- If the context doesn't contain the answer, say "I don't have enough information to answer that question based on the course materials."
- Be concise but comprehensive
- Use a friendly, supportive tone
- Format your response clearly with bullet points or paragraphs as appropriate"""
    
    def __init__(self, 
                 api_key: Optional[str] = None,
                 model: str = "llama-3.3-70b-versatile",
                 temperature: float = 0.3,
                 max_tokens: int = 1024):
        """
        Initialize Groq LLM client.
        
        Args:
            api_key: Groq API key (from env if not provided)
            model: Model name
            temperature: Temperature for generation
            max_tokens: Maximum tokens to generate
        """
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found. Please set it in .env file")
        
        self.client = Groq(api_key=self.api_key)
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        print(f"[OK] Groq LLM client initialized (model={model})")
    
    def generate_response(self, query: str, context: str) -> dict:
        """
        Generate response using Groq LLM.
        
        Args:
            query: User query
            context: Retrieved context
        
        Returns:
            Response dict with answer and metadata
        """
        # Build user prompt
        user_prompt = f"""Context:
{context}

Student Question: {query}

Answer:"""
        
        try:
            # Call Groq API
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": self.SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                model=self.model,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            # Extract response
            answer = chat_completion.choices[0].message.content
            
            return {
                "answer": answer,
                "model": self.model,
                "tokens_used": chat_completion.usage.total_tokens,
                "finish_reason": chat_completion.choices[0].finish_reason
            }
        
        except Exception as e:
            print(f"[ERROR] Groq API call failed: {e}")
            return {
                "answer": f"Error: Unable to generate response. {str(e)}",
                "model": self.model,
                "tokens_used": 0,
                "finish_reason": "error"
            }


if __name__ == "__main__":
    # Test LLM client (requires API key in .env)
    from dotenv import load_dotenv
    load_dotenv()
    
    try:
        client = GroqLLMClient()
        
        # Test query
        test_context = """
Context Information:
---
[Week 1: Mapping Business Outcomes to Product Outcomes]
Systems Thinking: understanding actors, flows, bottlenecks
Building KPI Trees for structured problem solving
(Source: curriculum, Relevance: 0.85)
---
"""
        
        test_query = "What is covered in week 1?"
        
        print(f"\n Testing Groq LLM...")
        response = client.generate_response(test_query, test_context)
        
        print(f"\nQuery: {test_query}")
        print(f"Answer: {response['answer']}")
        print(f"Tokens: {response['tokens_used']}")
        
    except Exception as e:
        print(f"[WARNING] Could not test LLM (API key needed): {e}")
