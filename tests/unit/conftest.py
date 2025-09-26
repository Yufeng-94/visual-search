import os
import pytest
from torchvision.models import resnet50, ResNet50_Weights

@pytest.fixture
def pre_trained_model():
    os.environ['TORCH_HOME'] = 'tests/unit/test_models/test_model_cache'
    # Init model with pre-trained weights
    pre_trained_weights = ResNet50_Weights.IMAGENET1K_V2
    model = resnet50(weights=pre_trained_weights)

    return model

@pytest.fixture
def image_process():
    # Init transforms
    image_process = ResNet50_Weights.IMAGENET1K_V2.transforms()

    return image_process
  