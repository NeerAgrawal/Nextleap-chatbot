# Phase 3: Query Processing & LLM Integration

Nextleap RAG chatbot with Groq LLM, vector search, and interactive frontend.

## Quick Start

```bash
cd phase_3

# 1. Install dependencies
pip install -r requirements.txt

# 2. Add your Groq API key to .env file in root directory
# Edit: Nextleap/.env
# Set: GROQ_API_KEY=your_api_key_here

# 3. Run unit tests (optional)
python tests/test_groq_llm.py

# 4. Start the chatbot server
python scripts/app.py

# 5. Open browser to http://localhost:5000
```

## Structure

```
phase_3/
├── src/
│   ├── query/              # Query processing
│   ├── retrieval/          # Context retrieval from Phase 2
│   ├── llm/                # Groq LLM client
│   └── api/                # Main chatbot orchestrator
├── frontend/               # Web UI (HTML/CSS/JS)
├── tests/                  # Unit tests
├── scripts/
│   └── app.py             # Flask API server
└── requirements.txt
```

## Components

- **Query Processor**: Normalize queries + generate embeddings
- **Context Retriever**: FAISS search + metadata filtering
- **Groq LLM**: Response generation with RAG
- **Flask API**: REST endpoint for chat
- **Frontend**: Modern, interactive chatbot UI

## API Endpoints

- `GET /` - Chatbot frontend
- `POST /api/chat` - Send query, get response
- `GET /api/health` - Health check

## Environment Variables

Create `.env` file in project root with:

```
GROQ_API_KEY=your_key_here
GROQ_MODEL=mixtral-8x7b-32768
GROQ_TEMPERATURE=0.3
TOP_K_RESULTS=5
```

## Testing

Run unit tests:
```bash
python tests/test_groq_llm.py
```

Tests cover:
- LLM initialization
- Response generation
- Context handling
- Error cases
