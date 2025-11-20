import grpc
from concurrent import futures
from app.search_servicer import SearchServicer
from shared_contracts.protos.search_service.search_service_pb2_grpc import add_SearchServiceServicer_to_server
import logging

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger = logging.getLogger("search_service")
logger.addHandler(handler)
logger.setLevel(logging.INFO)
logger.propagate = False

def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # Add Servicer to the server
    add_SearchServiceServicer_to_server(SearchServicer(), server)
    # Listen on port 50051
    server.add_insecure_port('[::]:50051')
    server.start()
    logger.info("Server started on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

