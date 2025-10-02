from app.models.image_encoder import PreTrainedImageEncoder
from torchvision.models import resnet50, ResNet50_Weights
from torchvision.transforms import Compose
import torch
from typing import Tuple

def load_image_encoder(device: torch.device) -> Tuple[PreTrainedImageEncoder, Compose]:
 
    # Init model with pre-trained weights
    pre_trained_weights = ResNet50_Weights.IMAGENET1K_V2
    model = resnet50(weights=pre_trained_weights)

    # Create image encoder from pre-trained model
    image_encoder = PreTrainedImageEncoder(model)
    image_encoder.to(device)

    # Set encoder to eval mode
    image_encoder.eval()

    # Init transforms
    image_process = pre_trained_weights.transforms()

    return image_encoder, image_process