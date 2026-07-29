"""
    RAG Service
    
    This module orchestrates the complete RAG workflow.
    
    Workflow:
    
    Upload Document
            ↓
    Extract Text
            ↓
    Chunk Text
            ↓
    Generate Embeddings
            ↓
    Store in ChromaDB
    
    User Question
            ↓
    Generate Question Embedding
            ↓
    Retrieve Similar Chunks
            ↓
    Build Prompt
            ↓
    Gemini
            ↓
    Answer
"""
 
from pathlib import Path
 
from app.document_processor import extract_text
from app.chunker import chunk_text
from app.embeddings import generate_embeddings
 
from app.vector_store import (
    get_collection_name,
    store_embeddings,
    retrieve_documents,
)
 
from app.llm import ask_gemini
 
 
def build_prompt(context: str, question: str) -> str:
    """
    Builds the prompt sent to Gemini.
    """
 
    return f"""
            You are an intelligent Enterprise RAG Assistant.
            
            Answer the user's question ONLY from the provided context.
            
            If the answer cannot be found in the context,
            reply exactly with:
            
            "I could not find the answer in the uploaded document."
            
            --------------------
            Context
            --------------------
            
            {context}
            
            --------------------
            Question
            --------------------
            
            {question}
            
            --------------------
            Answer
            --------------------
            """
 
 
def ingest_document(
    file_path: Path,
    file_name: str,
) -> str:
    """
    Complete document ingestion pipeline.
 
    Returns:
        Collection Name
    """
 
    print("=" * 60)
    print("Extracting Text...")
 
    text = extract_text(file_path)
 
    print("Done")
 
    print("=" * 60)
    print("Creating Chunks...")
 
    chunks = chunk_text(text)
 
    print(f"Total Chunks : {len(chunks)}")
 
    print("=" * 60)
    print("Generating Embeddings...")
 
    embeddings = generate_embeddings(chunks)
 
    print("Embeddings Created")
 
    collection_name = get_collection_name(file_name)
 
    print("=" * 60)
    print("Saving into ChromaDB...")
 
    store_embeddings(
        collection_name=collection_name,
        chunks=chunks,
        embeddings=embeddings,
    )
 
    print("Completed Successfully")
 
    return collection_name
 
 
def ask_question(
    question: str,
    collection_name: str,
) -> str:
    """
    Complete RAG Question Answering Pipeline.
    """
 
    print("=" * 60)
    print("Generating Question Embedding...")
 
    question_embedding = generate_embeddings([question])[0]
 
    print("Searching Similar Chunks...")
 
    documents = retrieve_documents(
        collection_name=collection_name,
        query_embedding=question_embedding,
    )
 
    if not documents:
        return "No relevant information found."
 
    context = "\n\n".join(documents)
 
    prompt = build_prompt(
        context=context,
        question=question,
    )
 
    print("Sending Prompt to Gemini...")
 
    answer = ask_gemini(prompt)
 
    return answer