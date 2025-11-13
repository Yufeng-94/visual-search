import grpc
import uuid
from qdrant_client import QdrantClient
import boto3
from shared_contracts.protos.image_encoding_service.image_encoding_service_pb2_grpc import ImageEncodingServiceStub
from shared_contracts.protos.image_encoding_service.image_encoding_service_pb2 import ImageRequest, ImageResponse
from shared_contracts.vector_db.vector_db_contracts import VectorDBContracts
from shared_contracts.protos.search_service.search_service_pb2 import SearchResponse, ImageResult

from typing import List

class SearchEngine:
    def __init__(self):
        # Create a channel to the image encoder service
        self.image_encoder_grpc_channel = grpc.insecure_channel('image-encoding-service:50071')
        # Create a stub for the image encoder service
        self.image_encoder_stub = ImageEncodingServiceStub(self.image_encoder_grpc_channel)

        self.vector_db_client = QdrantClient(
            host="qdrant", 
            grpc_port=6334, 
            prefer_grpc=True,
            timeout=30,
        )

        self.s3_client = boto3.client(
            's3', 
            endpoint_url='http://localstack:4566',
            aws_access_key_id="test",  # Placeholder credentials
            aws_secret_access_key="test",  # Placeholder credentials
            )

    def search(
            self, 
            image: bytes, 
            max_results: int
            ):
        
        job_id = str(uuid.uuid4())

        # Get the image embedding from the image encoder service
        embedding = self._send_to_image_encoder(image, job_id)
        print("Embedding received from image encoder.")
        
        # Query image from vector database using the embedding
        search_results = self._search_vector_db(embedding, max_results)
        print("Search results received from vector database.")

        # Fetch search results
        results = [self._parse_search_results(point) for point in search_results.points]
        print("Search results parsed.")
        return SearchResponse(results=results)

    def _send_to_image_encoder(self, image: bytes, job_id: str) -> List[float]:

        request = ImageRequest(query_image=image, job_id=job_id)
        response = self.image_encoder_stub.encode_image(request)
        return list(response.encoded_image)
    
    def _search_vector_db(self, query_vector: List[float], max_results: int):

        search_result = self.vector_db_client.query_points(
            collection_name=VectorDBContracts.collection_name,
            query=query_vector,
            limit=max_results,
        )
        return search_result
    
    def _parse_search_results(self, point) -> ImageResult:
        
        # Get image url
        image_bucket = point.payload['image_bucket']
        image_key = point.payload['image_key']
        image_url = self.s3_client.generate_presigned_url(
            'get_object',
            Params = {
                'Bucket': image_bucket,
                'Key': image_key,
            }
        )

        return ImageResult(
            image_url=image_url,
            similarity_score=point.score,
        )
