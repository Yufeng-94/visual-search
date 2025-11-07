import connexion

from openapi_server.models.index_images200_response import IndexImages200Response  # noqa: E501
from openapi_server.models.index_images_request import IndexImagesRequest  # noqa: E501
from openapi_server.models.inline_object import InlineObject  # noqa: E501
from openapi_server.models.inline_object1 import InlineObject1  # noqa: E501
from openapi_server.models.search_images200_response import SearchImages200Response  # noqa: E501
from openapi_server import util

from app.api.indexing_service import IndexingService
from app.api.search_service import SearchService

indexing_service = IndexingService()
search_service = SearchService()


def index_images(body=None):  # noqa: E501
    """Indexing images to database

    A request to index images to database by  specifying image storage and metadata buckets.  # noqa: E501

    :param index_images_request: 
    :type index_images_request: dict | bytes

    :rtype: Union[IndexImages200Response, Tuple[IndexImages200Response, int], Tuple[IndexImages200Response, int, Dict[str, str]]
    """
    index_images_request = body
    if connexion.request.is_json:
        index_images_request = IndexImagesRequest.from_dict(connexion.request.get_json())  # noqa: E501
        response = indexing_service.index(index_images_request)
    return response.to_dict()


def search_images(file):  # noqa: E501
    """Searching similar images

    A request to search similar images by uploading an image.  # noqa: E501

    :param file: The image file to be uploaded for searching similar images.
    :type file: str

    :rtype: Union[SearchImages200Response, Tuple[SearchImages200Response, int], Tuple[SearchImages200Response, int, Dict[str, str]]
    """
    response = search_service.search(file)
    return response.to_dict()