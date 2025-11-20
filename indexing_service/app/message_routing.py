from typing import Dict
from queue import Queue
import redis as redis
import time
import asyncio
import threading
from shared_contracts.message_queue.message_data_models import EncodingResults
import logging

logger = logging.getLogger("indexing_service.message_routing")

result_queue: Dict[str, Queue] = {}

def route_message_to_result_queue(
        channel: str, redis_client: redis.Redis
        ):
    last_id = '$' # Only new messages
    
    while True:
        try:
            streams = redis_client.xread(
                {channel: last_id},
                count=5,
                block=0, 
            )

            if streams:
                for stream_name, message_list in streams:
                    for message_id, message_data in message_list:
                        message = message_data.get(b'data').decode()
                        encoding_results = EncodingResults.model_validate_json(message)

                        if encoding_results.job_id in result_queue:
                            result_queue[encoding_results.job_id].put(encoding_results)
                            logger.info(f"Routed encoding results to queue {encoding_results.job_id}.")
                        else:
                            logger.warning(f"No queue found for job_id: {encoding_results.job_id}")

                        last_id = message_id

        except Exception as e:
            logger.error(f"Error routing message: {str(e)}")
            time.sleep(0.5)  # Prevent tight loop on error

def add_to_result_queue(job_id: str) -> None:
    q = Queue()
    result_queue[job_id] = q
    logger.info(f"Created result queue for job_id: {job_id}")

def start_redis_router(channel: str, redis_client: redis.Redis) -> threading.Thread:
    """Start the async router in background thread"""

    thread = threading.Thread(
        target=route_message_to_result_queue, 
        args=(channel, redis_client), 
        daemon=True
        )
    thread.start()
    return thread