# I Built Every Block of A RAG System to Learn It All
![RAG Architecture Diagram](docs/rag_architecture.png)
## What is it

Building Every block of RAG system for learning  



<b>Work in Progress</b>
## My Key Learning Points

### Architectural Insights

- **Python**: 
  - Modular Design, Isolated components
  - Easy extending/swapping to vector databases, LLM provider
  - Gradual adoption of new techniques

- **FastAPI Backend**:
  - Load model/service on startup (if using Local LLM)
  - Clean separation of endpoints with router
  - Rate limit using `slowapi`

### RAG-Specific Learnings
- **Document Processing and Chunking Matter**:
  - PyMuPDF4LLM is faster than docling. More to try: Markitdown, MinerU... 
  - Header Markdown preserves and gives more context to each chunk and between chunks

- **Vector DB**:
    - Qdrant has more advanced search and filter
    - Chroma for simplicity and fast for prototype projects
    - Should try Milvus (pretty much the same as Qdrant for a small-scale project) w
    - Postgre + PGVector also make a great combo

- **Retrieval Optimization**:
  - Find the embedding model at https://huggingface.co/spaces/mteb/leaderboard
  - Hybrid search (Dense + BM25) (is already in Qdrant). But sometimes metadata filtering then vector search work well
  - Reranking using Cohere API (can switch to local reranker like bge-reranker)
  - Not always, but Query expansion (rewrite the question into 1 or more) HyDE can work
  - Caching the most frequent Q&A pair for fast retrieval. Fuzzy matching is enough for my case

- **Memory**:
  - Some last messages should be enough for short-term memory. SQLite should be fine
  - [mem0.ai](https://mem0.ai/) for more sophisticated memory management

- **Evaluation**:
  - Ragas metrics, use LLM as a Judge. Can also simply use cosine similarity. The final evaluator should be human 
  - Langfuse Tracing. New version of Mlflow can do it too


## Tech Stack

### Core Components
| Component | Technology | Purpose |
|-----------|------------|---------|
| **LLM** | OpenAI GPT-4o-mini | Text Generate |
| **Embeddings** | OpenAI text-embedding-3-large | Semantic representations |
| **Vector DB** | Qdrant | High-performance vector search |
| **API Framework** | FastAPI | REST API endpoints |
| **Document Processing** | PyMuPDF4LLM | PDF-to-Markdown conversion |

### Supporting 
| Component | Technology | Purpose |
|-----------|------------|---------|
| **Tracing** | Langfuse | LLM monitoring/tracing |
| **Evaluation** | Ragas | Retrieval quality metrics |
| **Chunking** | Custom LangChain Header Markdown Text Splitters | Document segmentation |
| **Environment** | Docker | Containerization |

## Project Structure

```bash
.
├── app/                       # API Layer
│   ├── api/                   # Versioned endpoints
│   │   └── v1/                # API v1
│   │       ├── chat.py        # Chat interactions
│   │       └── documents.py   # Document management
│   └── models/                # Pydantic schemas
│       ├── chat.py
│       └── documents.py       # PDF processing models
│       
├── core/                      # Business Logic
│   ├── embedding/             # Embedding strategies
│   │   ├── base.py            # Abstract class
│   │   └── openai.py          # OpenAI embeddings
│   ├── llm/                   # LLM interfaces
│   │   ├── base.py            # Abstract class
│   │   └── openai.py          # GPT-4 implementation
│   ├── processing/            # Document processors
│   │   ├── document_processor.py   # PDF→Markdown pipeline
│   │   └── document_splitter.py    # Smart text splitting
│   ├── retrieval/             # Retrieval modules
│   │   ├── base.py            # Abstract class
│   │   ├── qdrant.py          # Vector DB operations
│   │   └── reranker.py        # Cross-encoder
│   ├── tracing/               # Retrieval modules
│   │   └── tracer.py          # Langfuse tracer
│   └── evaluation/            # Quality metrics
│       └── ragas_eval.py      # Ragas integration
│
├── data/                      # Data Storage
│
├── scripts/                   # Operational scripts
│   ├── ingest.py              # Bulk ingestion
│   └── evaluate.py            # Batch evaluation
│
├── tests/                     # Test suites
└── infra/                     # Deployment
    ├── docker-compose.yml     # Qdrant/Langfuse
    └── Dockerfile             # App container
```
