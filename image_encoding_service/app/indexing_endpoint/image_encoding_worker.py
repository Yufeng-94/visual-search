import redis
import boto3
from shared_contracts.message_queue.message_contract import MessageContract
from shared_contracts.message_queue.message_data_models import ImageEncodingCommand, EncodingResults

from app.image_encoder.image_encoder_loader import load_image_encoder
import torch
from torchvision.io import decode_image
import numpy as np

class ImageEncodingWorker:
    """
    Worker class that:
    1. Collecting encoding commands from message queue
    2. Performing batch image encoding
    3. Sending back encoded results to message queue
    4. Handling failures and retries
    """
    def __init__(self, device: torch.device, batch_size: int = 16):
        self.device = device
        self.batch_size = batch_size
        self.sub_channel = MessageContract.get_channel_for_message(ImageEncodingCommand)
        self.pub_channel = MessageContract.get_channel_for_message(EncodingResults)
        self.redis_client = redis.Redis(host='redis', port=6379)
        self.image_encoder, self.image_process = load_image_encoder(
            device=device
        )
        self.s3_client = boto3.client(
                's3', 
                endpoint_url='http://localstack:4566',
                aws_access_key_id="test",  # Placeholder credentials
                aws_secret_access_key="test",  # Placeholder credentials
                )

    def collect_encoding_commands(self, last_id: str, batch_size: int) -> list[ImageEncodingCommand]:

        messages = self.redis_client.xread(
            {self.sub_channel: last_id},
            count = batch_size,
            block = 0, # milliseconds
        )

        if messages:
            collected_commands = []
            for _, message_list in messages:
                for message_id, raw_message in message_list:
                    # Process each message
                    message = raw_message.get(b'data').decode()
                    print(f"Received encoding command message: {message}")
                    command = ImageEncodingCommand.model_validate_json(message)
                    collected_commands.append(command)

            last_id = message_id

            return collected_commands, last_id
        else:
            # print("No new encoding commands found.")
            return [], last_id

    def perform_batch_encoding(self, commands: list[ImageEncodingCommand]) -> list[EncodingResults]:
        image_tensors = [self.read_image_as_tensor(cmd) for cmd in commands]
        batch_tensor = torch.stack(image_tensors) # (B, C, H, W)
        print(f"Performing image preprocessing for tensor size: {batch_tensor.size()}")
        batch_tensor = self.image_process(batch_tensor).to(self.device) # (B, C, H, W)
        print(f"Performing batch encoding for tensor size: {batch_tensor.size()}")

        with torch.no_grad():
            batch_embeddings = self.image_encoder(batch_tensor) # (B, D)
            batch_embeddings = batch_embeddings.cpu().numpy()
            print(f"Completed batch encoding, obtained embeddings of shape: {batch_embeddings.shape}")
        
        encoded_results = [self.parse_encoded_result(cmd, emb) for cmd, emb in zip(commands, batch_embeddings)]

        return encoded_results

    def send_encoded_results(self, results: list[EncodingResults]):
        try:
            for result in results:
                message = EncodingResults.model_dump_json(result)
                self.redis_client.xadd(
                    self.pub_channel,
                    {'data': message}
                )
        except Exception as e:
            print(f"Failed to send encoded results: {e}")
        

    def handle_failures(self):
        pass # Placeholder for failure handling logic

    def read_image_as_tensor(self, command: ImageEncodingCommand) -> torch.Tensor:
        # Load image from S3
        response = self.s3_client.get_object(
            Bucket=command.image_bucket,
            Key=command.image_key
        )
        image_bytes = response['Body'].read()
        buf = np.frombuffer(image_bytes, dtype=np.uint8).copy()
        image_tensor = torch.from_numpy(buf)
        image_tensor = decode_image(image_tensor) # (C, H, W)

        return image_tensor

    def parse_encoded_result(self, command: ImageEncodingCommand, embedding: np.ndarray) -> EncodingResults:
        
        return EncodingResults(
            job_id=command.job_id,
            encoded_image=embedding.tolist()
        )


    def run(self):

        last_id = '$'

        while True:
            
            encoding_commands, last_id = self.collect_encoding_commands(last_id=last_id, batch_size=self.batch_size)
            if encoding_commands:
                print(f"Collected {len(encoding_commands)} encoding commands.")

                # Perform batch encoding
                print("Starting batch encoding...")
                encoded_results = self.perform_batch_encoding(encoding_commands)
                print(f"Completed batch encoding for {len(encoded_results)} images.")

                # Send back encoded results
                self.send_encoded_results(encoded_results)
                print("Sent encoded results back to message queue.")
            else:
                # print("No encoding commands to process. Waiting for new commands...")
                continue