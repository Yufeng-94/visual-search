from qdrant_client.models import VectorParams
from qdrant_client import QdrantClient
from app.db.vector_db import VectorDB
from app.db.vector_db_loader import load_vector_db
import numpy as np

def test_vector_db_create(qdrant_client, vector_db_config):
    database_name = vector_db_config['database_name']
    dimension = vector_db_config['dimension']
    distance = vector_db_config['distance']

    try:
        qdrant_client.delete_collection(collection_name=database_name)
    except:
        pass
    
    created_db = VectorDB.create_db(
        database_name=database_name,
        dimension=dimension,
        distance=distance,
        client=qdrant_client,
    )

    db_info = qdrant_client.get_collection(collection_name=database_name)

    assert db_info.config.params.vectors.size == dimension
    assert db_info.config.params.vectors.distance == distance
    assert created_db.name == database_name

    # Cleanup
    qdrant_client.delete_collection(collection_name=database_name)

def test_vector_db_load(qdrant_client, vector_db_config):
    database_name = vector_db_config['database_name']
    dimension = vector_db_config['dimension']
    distance = vector_db_config['distance']  

    # First, create the collection
    try:
        qdrant_client.delete_collection(collection_name=database_name)
    except:
        pass

    qdrant_client.create_collection(
        collection_name=database_name,
        vectors_config=VectorParams(
            size=dimension, distance=distance
        )
    )

    loaded_db = VectorDB.load_db(
        database_name=database_name,
        client=qdrant_client
    )

    assert loaded_db.database_name == database_name
    assert loaded_db.dimension == dimension
    assert loaded_db.distance == distance

    # Cleanup
    qdrant_client.delete_collection(collection_name=database_name)

def test_vector_db_add_and_query_images(qdrant_client, vector_db_config):
    database_name = vector_db_config['database_name']
    dimension = vector_db_config['dimension']
    distance = vector_db_config['distance']  

    # First, create the collection
    try:
        qdrant_client.delete_collection(collection_name=database_name)
    except:
        pass

    db = VectorDB.create_db(
        database_name=database_name,
        dimension=dimension,
        distance=distance,
        client=qdrant_client,
    )

    # Add a batch of dummy image vectors
    num_vectors = 5
    vectors = np.random.rand(num_vectors, dimension).astype(np.float32).tolist()
    metadata = [{"image_name":f"000{i}"} for i in range(num_vectors)]

    db.add_batch_images(
        image_embeddings=vectors,
        metadata_list=metadata
    )

     # Query with one of the added vectors
    query_vector = vectors[2]
    results = db.query_image(
        query_vector=query_vector,
        k=3
    )

    assert len(results) == 3
    assert results[0].payload['image_name'] == metadata[2]['image_name']

    # Cleanup
    qdrant_client.delete_collection(collection_name=database_name)

def test_vector_db_loader(vector_db_config):
    database_name = vector_db_config['database_name']
    dimension = vector_db_config['dimension']
    distance = vector_db_config['distance']
    location = vector_db_config['location']

    try:
        client = QdrantClient(path=location)
        client.delete_collection(collection_name=database_name)

        # Cleanup client
        client.close()
        del client
    except:
        pass

    # Load (create) the vector DB
    db = load_vector_db(
        database_name=database_name,
        dimension=dimension,
        distance=distance,
        location=location,
    )

    assert db.database_name == database_name
    assert db.dimension == dimension
    assert db.distance == distance

    # Cleanup
    db.client.delete_collection(collection_name=database_name)