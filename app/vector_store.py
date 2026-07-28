"""
Vector Store Module

Stores document chunks and thier
embeddings in ChromaDB.
"""

import chromadb

# Create a local ChromaDB client
client = chromadb.PersistentClient(path="chroma_db")



def get_collection_name(file_name:str) ->str:
    """
    Convert uploaded filename into a valid
    Chromadb collection name.
    """

    collection_name = file_name.split(".")[0].lower().replace(" ", "_")
    return collection_name


def get_collection(file_name:str):
    """
    Create or return an existing 
    ChromaDB collection.
    """

    collection_name = get_collection_name(file_name)
    collection = client.get_or_create_collection(name=collection_name)

    return collection


def store_embeddings(file_name: str,
                     chunks: list[str],
                     embeddings: list[list[float]]):


    collection = get_collection(file_name)

    ids = []
    metadatas = []

    for index in range(len(chunks)):
        ids.append(f"chunk_{index}")
        metadatas.append(
            {
                "chunk_number":index + 1,
                "source_document": file_name
            }
        )
    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print(
        f"Sucessfully stored "
        f"{len(chunks)} chunks"
        f"in collection"
        f"'{collection.name}'"
    )


def get_collection_count(file_name: str) ->int:

    collection = get_collection(file_name)
    return collection.count()



    
    
    
