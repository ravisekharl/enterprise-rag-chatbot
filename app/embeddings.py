"""
Embedding Utility

Responsible for converting text chunks
into vector embeddings.
"""


from google import genai
from app.config import (
    GEMINI_API_KEY,
    EMBEDDING_MODEL
)

client = genai.Client(api_key=GEMINI_API_KEY)


def generate_embeddings(texts: list[str]):
    """
    Convert chunks into vector embeddings.

    Parameters:
        texts : List of text chunks

    Returns:
        List of embeddings
    """
    
    embeddings = []
    for text in texts:
        response = client.models.embed_content(model=EMBEDDING_MODEL,
                                               contents=text)
        embeddings.append(response.embeddings[0].values)

    return embeddings

