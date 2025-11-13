from shared_contracts.protos.search_service.search_service_pb2_grpc import SearchServiceServicer
from shared_contracts.protos.search_service.search_service_pb2 import SearchRequest, SearchResponse, ImageResult
from grpc import ServicerContext
from app.search_engine import SearchEngine

class SearchServicer(SearchServiceServicer):
    '''A servicer to implement the service methods.'''

    def __init__(self):
        super().__init__()
        self.search_engine = SearchEngine()

    def search(
            self, 
            request: SearchRequest, 
            context: ServicerContext
            ) -> SearchResponse:
        # Implement the search logic here
        image = request.jpg_image
        max_results = request.max_results

        response = self.search_engine.search(
            image=image,
            max_results=max_results,
        )

        return response