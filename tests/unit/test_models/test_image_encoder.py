import torch
from app.models.image_encoder import PreTrainedImageEncoder

def test_model_initialization(pre_trained_model):

    model = PreTrainedImageEncoder(pre_trained_model)

    assert model is not None
    assert isinstance(model, torch.nn.Module)

def test_image_process_shape(image_process):

    model_input = torch.randn((10, 3, 500, 700))
    model_input_processed = image_process(model_input)

    assert model_input_processed.size(2) == 224
    assert model_input_processed.size(3) == 224

def test_model_forward_pass_shape(pre_trained_model):
    model = PreTrainedImageEncoder(pre_trained_model)

    model_input = torch.randn((10, 3, 224, 224))

    with torch.no_grad():
        output = model(model_input)

    assert output.size(0) == 10
    assert output.size(1) == 2048
