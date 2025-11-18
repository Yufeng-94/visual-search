from app.indexing_servicer import IndexingServicer
from shared_contracts.protos.indexing_service.indexing_service_pb2_grpc import add_IndexingServiceServicer_to_server
import grpc
from concurrent import futures

def serve():
    # Create gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # Init servicer
    indexing_servicer = IndexingServicer()

    # Add servicer to server
    add_IndexingServiceServicer_to_server(indexing_servicer, server)

    # Listen on port
    server.add_insecure_port('[::]:50072')
    server.start()
    print("Indexing Service gRPC server started on port 50072")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
