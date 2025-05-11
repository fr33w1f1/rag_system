# I Built Every Block of A RAG System to Learn It All
![RAG Architecture Diagram](docs/rag_architecture.png)
## What is it

Building Every block of RAG system for learning  



<b>Work in Progress</b>
## My Key Learning Points

### Architectural Insights

- **Python**: 
  - Modular Design, Isolated components
  - Easy extending/swapping to vector databases, LLM provider, features

- **FastAPI Backend**:
  - Load model/service on startup (if using Local LLM)
  - Clean separation of endpoints with router
  - Rate limit using `slowapi`

### RAG-Specific Learnings
- **Document Processing and Chunking Matter**:
  - PyMuPDF4LLM is faster than docling. More to try: Markitdown, MinerU... 
  - Using LangChain for chunking speeds up the process, as it automatically handles chunking and metadata storage.
  - Header Markdown preserves and gives more context to each chunk and between chunks
  - Documents like scanned PDFs or image-based files are still a challenge—I haven’t found an efficient solution for handling them yet.

- **Vector DB**:
    - Qdrant has more advanced search and filter
    - Chroma for simplicity and fast for prototype projects
    - Should try Milvus (pretty much the same as Qdrant for a small-scale project)
    - PostgreSQL + PGVector also make a great combo

- **Retrieval Optimization**:
  - Find the embedding model at https://huggingface.co/spaces/mteb/leaderboard
  - Hybrid search (Dense + BM25) (is already in Qdrant). But sometimes metadata filtering then vector search work well
  - Reranking using Cohere API (can switch to local reranker like bge-reranker)
  - Not always, but Query expansion (rewrite the question into 1 or more) HyDE can work. These techniques with Reranking also slows down the pipeline and increases costs. Weigh pros and cons. 
  - Caching the most frequent Q&A pairs (correct pairs) for fast retrieval. Fuzzy matching is enough for my case

- **Memory**:
    - Some last messages should be enough for short-term memory. SQLite should be fine
    - [mem0.ai](https://mem0.ai/) for more sophisticated memory management

- **Evaluation**:
    - Create a ground truth dataset to benchmark
  - Use LLM as a Judge or simply use cosine similarity. The final evaluator should be human 
  - Langfuse Tracing. New version of Mlflow can do it too

### My Takeaways

  - You truly learn it when you build it step by step.
  - Start simple (sometimes it works right away) and establish a baseline. Add one feature at a time and measure its impact.
  - Ensure the code is flexible enough for future extensions.
  - Communities like r/rag and r/langchain are incredibly helpful—search around and explore. I've learned a lot from them.

  - For every RAG project, I need to focus on three key areas: preprocessing, retrieval, and evaluation.
  - As the number of users and documents grows, it's crucial to ensure the application can handle increased traffic and maintain performance.

## Tech Stack

### Core Components
| Component | Technology | Purpose |
|-----------|------------|---------|
| **LLM** | OpenAI GPT-4o-mini | Text Generate |
| **Embeddings** | OpenAI embedding + Qdrant/BM25  | Embedding representations |
| **Vector DB** | Qdrant | High-performance vector search |
| **API Framework** | FastAPI | REST API endpoints |
| **Document Processing** | PyMuPDF4LLM | PDF-to-Markdown conversion |

### Supporting 
| Component | Technology | Purpose |
|-----------|------------|---------|
| **Tracing** | Langfuse | LLM monitoring/tracing |
| **Evaluation** | LLM as a Judge | Retrieval quality metrics |
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
