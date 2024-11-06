# RAG Document Ingestion and Querying with FastAPI and ChromaDB

This project implements a lightweight FastAPI server for document ingestion and querying using Retrieval-Augmented Generation (RAG). It leverages ChromaDB for storing and querying document embeddings, and the sentence-transformers library for generating embeddings. The server supports PDF, DOCX, and TXT file types for document ingestion and enables text-based search across documents.

## Features:
- Upload documents (PDF, DOCX, TXT) and generate embeddings.
- Store and query document embeddings using ChromaDB.
- Search documents using a text query and retrieve the most relevant results.

## Setup

### Prerequisites:
- Python 3.8+
- Install dependencies using `requirements.txt`.

### Installation:
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/rag-fastapi-chromadb.git
   cd rag-fastapi-chromadb
2. Install dependencies:

   pip install -r requirements.txt

## Running the Application:

    Start the FastAPI server using Uvicorn:

    uvicorn main:app --reload

    The server will run locally at http://127.0.0.1:8000.

## API Endpoints:

    POST /ingest/: Upload a document (PDF, DOCX, TXT) to generate and store embeddings.
        Example usage with curl:

    curl -X 'POST' \
    'http://127.0.0.1:8000/ingest/' \
    -F 'file=@path_to_file.pdf'

GET /search/: Search documents using a query. Returns the top 5 most relevant documents.

    Example usage with curl:

        curl 'http://127.0.0.1:8000/search/?query=machine%20learning'

## Files:

    main.py: Contains the FastAPI server, document ingestion, and query logic.
    requirements.txt: Lists the dependencies for the project.
    README.md: Documentation for the project.
