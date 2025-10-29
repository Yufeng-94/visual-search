from pydantic import BaseModel
from message_queue.message_channels import MessageChannels
from message_queue.message_data_models import (
    ImageEncodingCommand,
    EncodingStart,
    EncodingResults
)

class MessageContract:
    
    CHANNEL_TO_MESSAGE = {
        MessageChannels.IMAGE_ENCODING_COMMANDS: ImageEncodingCommand,
        MessageChannels.INDEXING_WORKFLOWS: EncodingStart,
        MessageChannels.INDEXING_EVENTS: EncodingResults
    }


    MESSAGE_TO_CHANNEL = {
        ImageEncodingCommand.__name__: MessageChannels.IMAGE_ENCODING_COMMANDS,
        EncodingStart.__name__: MessageChannels.INDEXING_WORKFLOWS,
        EncodingResults.__name__: MessageChannels.INDEXING_EVENTS
    }

    @classmethod
    def get_channel_for_message(cls, message_type: BaseModel) -> str:
        return cls.MESSAGE_TO_CHANNEL[message_type.__name__]

    @classmethod
    def get_message_for_channel(cls, channel: str) -> BaseModel:
        return cls.CHANNEL_TO_MESSAGE[channel]
    

    