"""
ChromaDB Vector Store
 
Responsibilities:
1. Create/Open Collection
2. Store Embeddings
3. Retrieve Similar Chunks
"""
 
import chromadb
 
CHROMA_DB_PATH = "chroma_db"
 
client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
 
 
def get_collection_name(file_name: str) -> str:
    """
    Convert filename to collection name.
    Example:
        Employee Handbook.pdf
            ↓
        employee_handbook
    """
 
    collection_name = (
        file_name
        .replace(".pdf", "")
        .replace(".docx", "")
        .replace(" ", "_")
        .lower()
    )
 
    return collection_name
 
 
def get_collection(collection_name: str):
    """
    Create or retrieve an existing collection.
    """
 
    return client.get_or_create_collection(
        name=collection_name
    )
 
 
def store_embeddings(collection_name: str,
                     chunks: list[str],
                     embeddings):
    """
    Store chunks and embeddings into ChromaDB.
    """
 
    collection = get_collection(collection_name)
 
    ids = [
        f"{collection_name}_{index}"
        for index in range(len(chunks))
    ]
 
    metadatas = [
        {
            "chunk_id": index
        }
        for index in range(len(chunks))
    ]
 
    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=chunks,
        metadatas=metadatas,
    )
 
 
def retrieve_chunks(collection_name: str,
                    query_embedding,
                    n_results: int = 3):
    """
    Retrieve most similar chunks.
    """
 
    collection = get_collection(collection_name)
 
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
    )
 
    return results
 
 
def retrieve_documents(collection_name: str,
                       query_embedding,
                       n_results: int = 3):
    """
    Return only document chunks.
    """
 
    results = retrieve_chunks(
        collection_name=collection_name,
        query_embedding=query_embedding,
        n_results=n_results,
    )
 
    documents = results.get("documents", [])
 
    if documents:
        return documents[0]
 
    return []
 
 
def get_collection_count(collection_name: str):
    """
    Return total chunks stored.
    """
 
    collection = get_collection(collection_name)
 
    return collection.count()
 