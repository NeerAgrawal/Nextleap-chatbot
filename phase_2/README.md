# Phase 2: Embedding Generation & Vector Storage

Transform Phase 1 processed data into semantic embeddings stored in ChromaDB for efficient retrieval.

## Structure

```
phase_2/
├── src/
│   ├── chunking/           # Text chunking
│   ├── embeddings/         # Embedding generation
│   ├── vector_db/          # ChromaDB client
│   └── metadata_store/     # SQLite database
├── data/
│   └── chunks/            # Chunked text output
├── database/
│   ├── chroma_db/         # ChromaDB storage
│   └── metadata.db        # SQLite metadata
├── scripts/
│   └── run_phase2.py      # Main execution
├── config/
│   └── config.yaml        # Configuration
└── requirements.txt       # Dependencies
```

## Quick Start

```bash
cd phase_2

# Install dependencies
pip install -r requirements.txt

# Run Phase 2 pipeline
python scripts/run_phase2.py
```

## What It Does

1. **Loads Phase 1 Data** - Curriculum, instructors, tools, general info
2. **Chunks Text** - Semantic chunking (13 weeks + 8 instructors + tools + general info)
3. **Generates Embeddings** - Using sentence-transformers (all-MiniLM-L6-v2, 384 dims)
4. **Stores in ChromaDB** - Vector database for similarity search
5. **Stores in SQLite** - Metadata and full content for retrieval
6. **Tests Retrieval** - Sample queries to verify search quality

## Output

- `data/chunks/all_chunks.json` - All text chunks with metadata
- `database/chroma_db/` - ChromaDB vector storage
- `database/metadata.db` - SQLite metadata database

## Configuration

Edit `config/config.yaml` to customize:
- Embedding model
- Batch size
- Collection name
- Database paths

## Dependencies

- sentence-transformers - Embedding generation
- chromadb - Vector database
- numpy - Array operations
- pyyaml - Config loading
