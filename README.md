# Nextleap RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot for the [Nextleap Product Management Fellowship](https://nextleap.app/course/product-management-course) to help students get accurate answers about the curriculum, tools, instructors, and program structure.

## Project Overview

This chatbot uses RAG architecture with **GroqLLM** to provide contextual, accurate responses about the Nextleap Product Management Course.

## Project Structure

```
Nextleap/
├── ARCHITECTURE.md          # Complete system architecture
├── README.md               # This file
├── phase_1/                # Phase 1: Data Collection & Preprocessing
│   ├── src/               # Source code
│   │   ├── scrapers/      # Web scraping
│   │   ├── parsers/       # Content parsing (modular)
│   │   ├── utils/         # Helper utilities
│   │   └── preprocessing/ # Text cleaning
│   ├── data/              # Raw and processed data
│   ├── config/            # Configuration files
│   ├── scripts/           # Execution scripts
│   ├── requirements.txt   # Dependencies
│   └── README.md          # Phase 1 documentation
└── tests/                 # Test suite (future)
```

## Phase-Based Development

Each phase is organized in its own folder with dedicated:
- Source code (`src/`)
- Data files (`data/`)
- Configuration (`config/`)
- Scripts (`scripts/`)
- Documentation (`README.md`)

### ✅ Phase 1: Data Collection & Preprocessing (COMPLETE)

**What it does:**
- Scrapes course content from Nextleap website
- Parses curriculum (13 weeks), instructors (8), tools (18), and program details
- Stores structured JSON data

**Key Features:**
- Modular architecture with base classes and utilities
- HTML-based parsing for accuracy
- Extracts all 8 instructors with roles and teaching assignments
- Comprehensive program info: cost (Rs 39,999), duration (4 months), support

**Quick Start:**
```bash
cd phase_1
python scripts/run_phase1.py
```

**Output:**
- `data/processed/curriculum.json` - 13 weeks of course content
- `data/processed/instructors.json` - All 8 instructor profiles
- `data/processed/tools.json` - 18 tools across 5 categories
- `data/processed/general_info.json` - Program details, cost, support

See [phase_1/README.md](phase_1/README.md) for detailed documentation.

### 🚧 Phase 2: Embedding Generation & Vector Storage (Upcoming)

- Text chunking with semantic boundaries
- Generate embeddings using sentence-transformers
- Store in ChromaDB vector database
- SQLite metadata store

### 🚧 Phase 3: Query Processing & LLM Response (Upcoming)

- Query understanding and reformulation
- Context retrieval from vector DB
- Response generation with Groq LLM
- Citation and source tracking

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for the complete multi-phase system design.

## Technology Stack

**Current (Phase 1):**
- BeautifulSoup4, lxml - HTML parsing
- Requests - HTTP requests
- PyYAML - Configuration

**Planned:**
- sentence-transformers - Embeddings
- ChromaDB - Vector database
- Groq - LLM API
- Streamlit/Gradio - Web interface

## Development Workflow

1. **Phase 1** (Current): Collect and structure data
2. **Phase 2**: Generate embeddings and setup vector DB
3. **Phase 3**: Build query interface and LLM integration
4. **Deployment**: Web interface for end users

## Contributing

This project follows a phase-based structure. To add new functionality:
1. Review [ARCHITECTURE.md](ARCHITECTURE.md)
2. Create or extend parser modules in the relevant phase folder
3. Update phase-specific README

## License

Educational project for the Nextleap Product Management Fellowship.

---

**Status**: Phase 1 Complete ✅ | Phase 2 Upcoming  
**Last Updated**: February 2026
