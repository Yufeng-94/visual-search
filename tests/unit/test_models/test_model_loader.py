from app.models.model_loader import load_image_encoder
import pytest
import torch

@pytest.mark.parametrize("device_name", ["cpu", "cuda"])
def test_model_device(device_name):
    if device_name == "cuda" and not torch.cuda.is_available():
        pytest.skip("CUDA not available")

    device = torch.device(device_name)
    model, _ = load_image_encoder(device)

    assert next(model.named_parameters())[1].device.type == device.type