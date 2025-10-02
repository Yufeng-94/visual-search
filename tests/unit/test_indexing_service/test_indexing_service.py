from unittest.mock import patch, Mock
import torch
from app.services.indexing import IndexService


def test_indexing_happy_path(
        mock_image_storage,
        mock_vector_db,
        mock_image_encoder,
        mock_image_process,
        mock_device,
):
    service = IndexService(
        vector_db=mock_vector_db,
        image_storage=mock_image_storage,
        image_encoder=mock_image_encoder,
        image_process=mock_image_process,
        device=mock_device,
    )

    # Data flow path test
    with patch.object(service, '_load_metadata', return_value=[{'id': '1'}, {'id': '2'}, {'id': '3'}]) as mock_load_metadata, \
         patch.object(service, '_load_process_images', return_value=Mock(to=lambda device: torch.tensor([[0.1]*2048]*3))) as mock_load_process_images:

        service.index_images(
            image_paths=['path1', 'path2', 'path3'],
            metadata_paths=['meta1', 'meta2', 'meta3'],
            batch_size=3,
            parallel=1,
        )

        mock_load_metadata.assert_called_once()
        mock_load_process_images.assert_called_once()
        mock_image_storage.upload_images.assert_called_once()
        mock_image_encoder.assert_called_once()
        mock_vector_db.add_batch_images.assert_called_once()


        mock_vector_db.add_batch_images.call_args.kwargs['metadata_list'] == [{'id': '1', 'image_url': 'http://image1.jpg'}, {'id': '2', 'image_url': 'http://image2.jpg'}, {'id': '3', 'image_url': 'http://image3.jpg'}]
        