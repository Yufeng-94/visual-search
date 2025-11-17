import grpc
from concurrent import futures
from shared_contracts.protos.image_encoding_service.image_encoding_service_pb2_grpc import add_ImageEncodingServiceServicer_to_server
from app.search_endpoint.image_encoding_servicer import ImageEncodingServicer

def serve():

    # create a gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # add servicer to the server
    # TODO: Add device argument
    add_ImageEncodingServiceServicer_to_server(
        servicer=ImageEncodingServicer(),
        server=server,
    )

    # listen on port 50061
    server.add_insecure_port('[::]:50061')

    # start the server
    server.start()
    print("Image Encoding Server started on port 50061")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()