# RAG System for learning

A modular Retrieval-Augmented Generation (RAG) system designed for production deployment with optimized document processing and retrieval capabilities.

## Features

- **Multi-stage document processing** with PDF-to-Markdown conversion
- **Hybrid search** (vector + BM25) with Qdrant
- **Query expansion** and **cross-encoder reranking**
- **Observability** with Langfuse tracing
- **Evaluation** with Ragas metrics
- **Production-ready API** with FastAPI

## Tech Stack

### Core Components
| Component           | Technology                          | Purpose                          |
|---------------------|-------------------------------------|----------------------------------|
| Vector Database     | Qdrant                              | High-performance vector search   |
| Embeddings          | OpenAI `text-embedding-3-large`     | Text vectorization               |
| LLM                 | OpenAI GPT-4                        | Response generation              |
| API Framework       | FastAPI                             | REST API interface               |

### Document Processing
| Component           | Technology                          | Purpose                          |
|---------------------|-------------------------------------|----------------------------------|
| PDF Extraction      | PyMuPDF4LLM                         | Structure-aware PDF to Markdown  |
| Text Splitting      | LangChain MarkdownHeaderTextSplitter| Semantic chunking                |

### Operational Tools
| Component           | Technology                          | Purpose                          |
|---------------------|-------------------------------------|----------------------------------|
| Tracing             | Langfuse                            | LLM call tracing                 |
| Evaluation          | Ragas                               | Retrieval quality metrics        |
| Containerization    | Docker                              | Deployment packaging             |

## Getting Started

### Prerequisites

- Python 3.10+
- Qdrant server (or cloud instance)
- OpenAI API key
- Langfuse account (optional)

### Installation