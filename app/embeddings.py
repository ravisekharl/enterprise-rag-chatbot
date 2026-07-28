"""
Embedding Utility

Responsible for converting text chunks
into vector embeddings.
"""

from sentence_transformers import SentenceTransformer

# Load embedding model only once
model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embeddings(chunks: list[str]) -> list[list[float]]:
    """
    Convert chunks into vector embeddings.

    Parameters:
        chunks : List of text chunks

    Returns:
        List of embeddings
    """
    
    embeddings = model.encode(chunks)
    return embeddings.tolist()

