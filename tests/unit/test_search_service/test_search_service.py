
import torchvision
from app.services.search import SearchService
from unittest.mock import patch, Mock
import torch


def test_search_service_happy_path(
        mock_image_storage,
        mock_vector_db,
        mock_image_encoder,
        mock_image_process,
        mock_device,
):
    service = SearchService(
        vector_db=mock_vector_db,
        image_storage=mock_image_storage,
        image_encoder=mock_image_encoder,
        image_process=mock_image_process,
        device=mock_device,
    )

    # Data flow path test
    with patch.object(service, '_extract_urls_from_results', side_effect=lambda x: x) as mock_extract_urls, \
         patch('app.services.search.decode_image') as mock_decode_image:

        mock_image_encoder.return_value = torch.tensor([[0.1]*2048]).unsqueeze(0)
        mock_vector_db.query_image.return_value = ['url1']
        mock_processed_image = Mock()
        mock_image_process.return_value = mock_processed_image
        mock_processed_image.unsqueeze.to.return_value = torch.ones(1, 3, 224, 224)
        
        retrieved_image = service.search(
            input_image_path='path1',
            top_k=3,
        )

        mock_extract_urls.assert_called_once()
        mock_image_encoder.assert_called_once()
        mock_vector_db.query_image.assert_called_once()
        mock_image_storage.query_images.assert_called_once()



