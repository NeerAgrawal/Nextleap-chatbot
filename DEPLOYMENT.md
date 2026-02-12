# Nextleap RAG Chatbot - Production Deployment Guide

## 🚀 Quick Start

### Prerequisites
- Python 3.14+
- Groq API key ([Get one here](https://console.groq.com))
- ~2GB disk space for models and databases

### Installation

1. **Clone/Navigate to project**
   ```bash
   cd Nextleap
   ```

2. **Install dependencies for each phase**
   ```bash
   # Phase 1
   cd phase_1
   pip install -r requirements.txt
   
   # Phase 2  
   cd ../phase_2
   pip install -r requirements.txt
   
   # Phase 3
   cd ../phase_3
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   # Copy example and add your Groq API key
   cp .env.example .env
   # Edit .env and add: GROQ_API_KEY=your_actual_key_here
   ```

### Running the Chatbot

#### Development/Testing
```bash
cd phase_3
python scripts/app.py
```

Then open browser to: **http://localhost:5000**

#### Production
```bash
# Install Gunicorn
pip install gunicorn

# Run with production server
cd phase_3
gunicorn -w 4 -b 0.0.0.0:5000 --timeout 120 scripts.app:app
```

---

## 📁 Project Structure

```
Nextleap/
├── .env                      # Your API keys (DO NOT COMMIT)
├── .env.example              # Template for environment variables
├── ARCHITECTURE.md           # Full system architecture
│
├── phase_1/                  # Data collection & preprocessing
│   ├── data/
│   │   ├── raw/             # Scraped HTML
│   │   └── processed/       # Structured JSON (curriculum, instructors, etc.)
│   ├── src/
│   │   └── scrapers/        # Web scraping logic
│   └── requirements.txt
│
├── phase_2/                  # Embedding generation & storage
│   ├── database/
│   │   ├── vector_db/       # FAISS vector index
│   │   └── metadata.db      # SQLite metadata
│   ├── data/
│   │   └── chunks/          # Text chunks with metadata
│   ├── src/
│   │   ├── chunking/        # Text chunking
│   │   ├── embeddings/      # Embedding generation
│   │   ├── vector_db/       # FAISS client
│   │   └── metadata_store/  # SQLite client
│   └── requirements.txt
│
└── phase_3/                  # Query processing & LLM
    ├── frontend/
    │   ├── index.html       # Chatbot UI
    │   ├── styles.css       # Premium styling
    │   └── script.js        # Frontend logic
    ├── src/
    │   ├── query/           # Query processing
    │   ├── retrieval/       # Context retrieval
    │   ├── llm/             # Groq LLM client
    │   └── api/             # Chatbot orchestrator
    ├── scripts/
    │   └── app.py           # Flask API server
    ├── tests/
    │   └── test_groq_llm.py # Unit tests
    └── requirements.txt
```

---

## 🔧 Configuration

### Environment Variables (`.env`)
```bash
# Groq API
GROQ_API_KEY=your_key_here
GROQ_MODEL=llama-3.3-70b-versatile
GROQ_TEMPERATURE=0.3
GROQ_MAX_TOKENS=1024

# Retrieval
TOP_K_RESULTS=5
SIMILARITY_THRESHOLD=0.3
```

### Key Components
- **Vector DB**: FAISS (31 chunks, 384-dim embeddings)
- **Embedding Model**: all-MiniLM-L6-v2
- **LLM**: Groq llama-3.3-70b-versatile
- **Metadata DB**: SQLite

---

## 🧪 Testing

### Run Unit Tests
```bash
cd phase_3
python tests/test_groq_llm.py
```

### Test Queries
Try these in the chatbot:
- "What topics are covered in the curriculum?"
- "Who are the instructors?"
- "What is the class schedule?"
- "What tools will I learn?"
- "How much does the course cost?"

---

## 🌐 API Endpoints

### `POST /api/chat`
Send a query and get a response.

**Request:**
```json
{
  "query": "What topics are covered in week 1?"
}
```

**Response:**
```json
{
  "answer": "Week 1 covers Mapping Business Outcomes...",
  "sources": [...],
  "metadata": {
    "model": "llama-3.3-70b-versatile",
    "tokens_used": 245,
    "chunks_retrieved": 5
  }
}
```

### `GET /api/health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "chatbot": "initialized"
}
```

---

## 🚢 Deployment Options

### Option 1: Local/VM
```bash
gunicorn -w 4 -b 0.0.0.0:5000 --timeout 120 scripts.app:app
```

### Option 2: Docker
```dockerfile
FROM python:3.14-slim
WORKDIR /app

# Copy all phases
COPY phase_1/ ./phase_1/
COPY phase_2/ ./phase_2/
COPY phase_3/ ./phase_3/
COPY .env ./

# Install dependencies
RUN pip install -r phase_3/requirements.txt gunicorn

# Expose port
EXPOSE 5000

# Run with Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "--timeout", "120", "--chdir", "phase_3", "scripts.app:app"]
```

```bash
docker build -t nextleap-chatbot .
docker run -p 5000:5000 --env-file .env nextleap-chatbot
```

### Option 3: Cloud Platforms
- **Render**: Push to GitHub, connect repo, deploy
- **Railway**: Similar to Render, auto-deploys
- **Heroku**: May need custom buildpack for Python 3.14
- **AWS/GCP/Azure**: Deploy on EC2/Compute Engine

---

## 🔒 Security Notes

### Development
- ✅ CORS enabled for all origins
- ✅ API key in `.env` file

### Production
- ⚠️ **Restrict CORS** to your domain only
- ⚠️ **Never commit** `.env` to git
- ⚠️ **Add rate limiting** to prevent abuse
- ⚠️ **Use HTTPS** in production
- ⚠️ **Sanitize user inputs** before processing

### Urgent Production Updates Needed
```python
# In phase_3/scripts/app.py, update CORS:
from flask_cors import CORS
CORS(app, origins=["https://yourdomain.com"])  # Restrict origins

# Add input validation:
from markupsafe import escape
query = escape(data.get('query', '').strip())
```

---

## 📊 Monitoring & Maintenance

### Logs
- Check Flask/Gunicorn logs for errors
- Monitor Groq API usage on console.groq.com

### Updating Course Content
When Nextleap updates their course:
```bash
# Re-scrape (Phase 1)
cd phase_1
python scripts/web_scraper.py

# Re-generate embeddings (Phase 2)
cd ../phase_2
python scripts/run_phase2.py

# Restart chatbot (Phase 3)
# Database will automatically use new data
```

### Performance
- **Response Time**: ~2-5 seconds per query
- **API Costs**: ~$0.001-0.003 per query (Groq pricing)
- **Concurrent Users**: Supports 4 with Gunicorn workers

---

## ❓ Troubleshooting

### Chatbot not responding
1. Check Flask server is running: `curl http://localhost:5000/api/health`
2. Check browser console (F12) for JavaScript errors
3. Verify GROQ_API_KEY in `.env`

### "API Offline" status
- Server not running or wrong port
- Check terminal for error messages

### Poor search quality
- Semantic search works best with natural questions
- Try specific questions: "What is the class schedule?" vs "schedule?"
- Week-specific queries may need improvement (known issue)

### Database errors
- Ensure phase_2/database/ exists with vector_db/ and metadata.db
- Re-run Phase 2 if databases are corrupted

---

## 📞 Support

- **Architecture**: See [ARCHITECTURE.md](./ARCHITECTURE.md)
- **Groq API**: https://console.groq.com/docs
- **FAISS**: https://github.com/facebookresearch/faiss

---

## ✅ Deployment Checklist

- [ ] Install all dependencies (phase 1, 2, 3)
- [ ] Copy `.env.example` to `.env`
- [ ] Add valid GROQ_API_KEY to `.env`
- [ ] Test locally: `python phase_3/scripts/app.py`
- [ ] Verify chatbot responds to test queries
- [ ] Install Gunicorn: `pip install gunicorn`
- [ ] Test production server locally
- [ ] Add CORS restrictions for production
- [ ] Add input sanitization
- [ ] Deploy to hosting platform
- [ ] Test deployed URL
- [ ] Monitor API usage and costs

**Status**: ✅ Ready for deployment!
