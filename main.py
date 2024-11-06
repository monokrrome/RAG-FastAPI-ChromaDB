from fastapi import FastAPI, UploadFile, File
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from io import BytesIO
import fitz  # PyMuPDF for PDF processing
from docx import Document
import numpy as np

# Initialize FastAPI app
app = FastAPI()

# Initialize Chroma client with persistent storage
client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory="./chroma_db"))

# Create a collection to store document embeddings
collection = client.create_collection(name="documents")

# Load the sentence-transformer model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Function to generate embeddings from text
def generate_embeddings(text: str):
    return model.encode([text])

# Function to extract text from PDF
def extract_text_from_pdf(file: BytesIO):
    doc = fitz.open(file)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Function to extract text from DOCX
def extract_text_from_docx(file: BytesIO):
    doc = Document(file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

# Route for document ingestion (upload and embed)
@app.post("/ingest/")
async def ingest_document(file: UploadFile = File(...)):
    # Read the file content
    content = await file.read()
    file_type = file.filename.split('.')[-1].lower()

    # Extract text based on file type
    if file_type == 'pdf':
        text_content = extract_text_from_pdf(BytesIO(content))
    elif file_type == 'docx':
        text_content = extract_text_from_docx(BytesIO(content))
    elif file_type == 'txt':
        text_content = content.decode("utf-8")
    else:
        return {"message": "Unsupported file type. Only PDF, DOCX, and TXT are supported."}

    # Generate embeddings for the document text
    embedding = generate_embeddings(text_content)

    # Store the embedding in ChromaDB
    collection.add(
        documents=[text_content],
        metadatas=[{"filename": file.filename}],
        embeddings=embedding
    )

    return {"message": f"Document {file.filename} ingested successfully."}

# Route for document search/query
@app.get("/search/")
async def search_documents(query: str):
    # Generate embeddings for the search query
    query_embedding = generate_embeddings(query)

    # Perform similarity search in ChromaDB
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=5  # Get top 5 most relevant results
    )

    # Return the top 5 most similar documents
    documents = results['documents']
    metadata = results['metadatas']

    # Format the response to show relevant information
    response = [{"filename": metadata[i]['filename'], "content": documents[i]} for i in range(len(documents))]

    return {"results": response}
