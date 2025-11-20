from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, PointIdsList, Distance
from typing import List
import logging


logging.basicConfig(level=logging.INFO)

class VectorDB:
    """
    <Description>
    """
    def __init__(self):
        raise NotImplementedError("Use 'create_db' class method to create a new Qdrant collection.")

    @classmethod
    def create_db(
        cls, 
        database_name: str, 
        dimension: int, 
        distance: Distance, 
        client: QdrantClient,
        ):

        try:
            client.create_collection(
                collection_name=database_name,
                vectors_config=VectorParams(
                    size=dimension, distance=distance
                    )
            )
            logging.info(f"Created Qdrant collection '{database_name}' with dimension {dimension} and distance '{distance}'.")

            instance = cls.__new__(cls)
            instance._initialize(client, database_name, dimension, distance)

            return instance

        except Exception as e:
            logging.error(f"Failed to create Qdrant collection '{database_name}': {e}")
            raise e
    
    @classmethod
    def load_db(
        cls, 
        database_name: str, 
        client: QdrantClient
        ):

        try:
            collection_info = client.get_collection(collection_name=database_name)
            dimension = collection_info.config.params.vectors.size
            distance = collection_info.config.params.vectors.distance
            logging.info(f"Loaded Qdrant collection '{database_name}' with dimension {dimension} and distance '{distance}'.")

            instance = cls.__new__(cls)
            instance._initialize(client, database_name, dimension, distance)

            return instance
        
        except Exception as e:
            logging.error(f"Failed to load Qdrant collection '{database_name}': {e}")
            raise e
        
    def _initialize(self, client: QdrantClient, database_name: str, dimension: int, distance: str):
        self.client = client
        self.database_name = database_name
        self.dimension = dimension
        self.distance = distance


    def add_batch_images(
            self,
            image_embeddings: List[List], 
            metadata_list: List[dict],
            parallel: int=1,
            ):
        # Create IDs for each image
        ids = [int(m['image_name']) for m in metadata_list]

        # add to Qdrant
        self.client.upload_collection(
            collection_name=self.database_name,
            vectors=image_embeddings,
            payload=metadata_list,
            ids=ids,
            parallel=parallel,
        )


    def remove_images_batch(self, image_names: List[str]):
        image_ids = [int(name) for name in image_names]
        image_ids = PointIdsList(points=image_ids)
        try:
            response = self.client.delete(
                collection_name=self.database_name,
                points_selector=image_ids
            )
            if response.status == 'completed':
                logging.info(f"Removed images from Qdrant collection '{self.database_name}'.")
            else:
                logging.error(f"Failed to remove images from Qdrant collection '{self.database_name}': {response.status}")

        except Exception as e:
            logging.error(f"Failed to remove images from Qdrant collection '{self.database_name}': {e}")
    
    def query_image(self, query_vector: list, k: int=5) -> list:
        response = self.client.query_points(
            collection_name=self.database_name,
            query=query_vector,
            limit=k,
        )
        
        return response.points

    def get_number_of_vectors(self) -> int:
        try:
            collection_info = self.client.get_collection(collection_name=self.database_name)
            num_vectors = collection_info.points_count
            return num_vectors
        except Exception as e:
            logging.error(f"Failed to get number of vectors in Qdrant collection '{self.database_name}': {e}")
            return -1

    @classmethod
    def remove_db(cls, database_name: str, database_path: str, client: QdrantClient=None):
        if client is None:
            client = QdrantClient(path=database_path)
        try:
            client.delete_collection(collection_name=database_name)
            logging.info(f"Deleted Qdrant collect '{database_name}'.")
        except Exception as e:
            logging.error(f"Failed to delete Qdrant collection '{database_name}': {e}")

        