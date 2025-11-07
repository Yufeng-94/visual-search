from shared_contracts.protos.search_service.search_service_pb2_grpc import SearchServiceStub
from shared_contracts.protos.search_service.search_service_pb2 import SearchRequest, SearchResponse
import grpc
import time
import uuid

from openapi_server.models.search_images200_response import SearchImages200Response

class SearchService:
    '''
    NOTE: This is a simplified example. In production, consider adding error handling,
    retries, timeouts, and circuit breakers for robustness.
    '''
    def __init__(self):
        # Init search service client
        self.channel = grpc.insecure_channel('localhost:50071')
        self.stub = SearchServiceStub(self.channel)

    def search(self, file):
        search_id = str(uuid.uuid4())
        st = time.time()
        # Convert request protocol
        image_bytes = file.read()
        grpc_request = SearchRequest(
            jpg_image=image_bytes,
            max_results=4
        )

        # Call search service
        grpc_response: SearchResponse = self.stub.search(grpc_request)
        et = time.time()

        # Convert response protocol
        return SearchImages200Response(
            search_id=search_id,
            processing_ms=int((et - st) * 1000),
            similar_images=[
                {
                    'image_url': img_result.image_url,
                    'similarity_score': img_result.similarity_score
                } for img_result in grpc_response.results
            ]
        )
