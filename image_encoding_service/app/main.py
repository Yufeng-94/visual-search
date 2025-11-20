from app.indexing_endpoint.image_encoding_worker import ImageEncodingWorker
from app.search_endpoint.image_encoding_servicer import ImageEncodingServicer
from shared_contracts.protos.image_encoding_service.image_encoding_service_pb2_grpc import add_ImageEncodingServiceServicer_to_server
import torch
import grpc
from concurrent import futures
import threading
import logging

foramtter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

handler = logging.StreamHandler()
handler.setFormatter(foramtter)

logger = logging.getLogger("image_encoding_service")
logger.setLevel(logging.INFO)
logger.addHandler(handler)

def main():
    # Init Async encoding worker for indexing endpoint
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    batch_size = 16
    logger.info(f"Using device: {device}")
    worker = ImageEncodingWorker(device=device, batch_size=batch_size)
    servicer = ImageEncodingServicer(device=device)


    worker_thread = threading.Thread(target=worker.run, daemon=True)
    worker_thread.start()
    logger.info("Message queue worker started in background thread")

    # Init gRPC server for search endpoint
    serve(servicer=servicer)

def serve(servicer: ImageEncodingServicer):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    

    add_ImageEncodingServiceServicer_to_server(
        servicer=servicer,
        server=server,
    )

    server.add_insecure_port('[::]:50071')
    server.start()
    logger.info("Server started on port 50071")
    server.wait_for_termination()

if __name__ == "__main__":
    main()