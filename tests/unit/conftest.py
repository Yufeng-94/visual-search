import os
import pytest
import torch
from unittest.mock import Mock
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

@pytest.fixture
def mock_device():
    return Mock()

@pytest.fixture
def mock_image_encoder():
    mock = Mock()
    mock.return_value=torch.tensor([[0.1]*2048]*3)
    
    return mock

@pytest.fixture
def mock_image_process():
    mock = Mock(return_value=torch.ones(3, 224, 224))
    return mock

@pytest.fixture
def mock_image_storage():
    mock = Mock()
    mock.upload_images = Mock(return_value=["http://image1.jpg", "http://image2.jpg", "http://image3.jpg"])
    
    return mock

@pytest.fixture
def mock_vector_db():
    return Mock()


    
  