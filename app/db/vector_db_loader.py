from app.db.vector_db import VectorDB
from qdrant_client import QdrantClient
from qdrant_client.models import Distance

def load_vector_db(
        database_name: str,
        dimension: int,
        distance: Distance,
        location: str,
) -> VectorDB:
    
    client = QdrantClient(path=location)
    
    try:
        vector_db = VectorDB.load_db(
            database_name=database_name,
            client=client
        )

    except:
        vector_db = VectorDB.create_db(
            database_name=database_name,
            dimension=dimension,
            distance=distance,
            client=client,
        )

    return vector_db