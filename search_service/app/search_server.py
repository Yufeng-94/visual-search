import grpc
from concurrent import futures
from app.search_servicer import SearchServicer
from proto.search_service_pb2_grpc import add_SearchServiceServicer_to_server

def serve():
    # Create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # Add Servicer to the server
    add_SearchServiceServicer_to_server(SearchServicer(), server)
    # Listen on port 50051
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

