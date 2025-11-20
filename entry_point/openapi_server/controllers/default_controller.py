import connexion
from flask import render_template

from openapi_server.models.get_health200_response import GetHealth200Response  # noqa: E501
from openapi_server.models.get_health500_response import GetHealth500Response  # noqa: E501
from openapi_server.models.index_images200_response import IndexImages200Response  # noqa: E501
from openapi_server.models.index_images400_response import IndexImages400Response  # noqa: E501
from openapi_server.models.index_images_request import IndexImagesRequest  # noqa: E501
from openapi_server.models.search_images200_response import SearchImages200Response  # noqa: E501
from openapi_server import util

from app.api.indexing_service import IndexingService
from app.api.search_service import SearchService

indexing_service = IndexingService()
search_service = SearchService()

def get_health():  # noqa: E501
    """Health check endpoint

     # noqa: E501


    :rtype: Union[GetHealth200Response, Tuple[GetHealth200Response, int], Tuple[GetHealth200Response, int, Dict[str, str]]
    """
    return GetHealth200Response(status="Server is running").to_dict()


def get_root():  # noqa: E501
    """Root page

     # noqa: E501


    :rtype: Union[str, Tuple[str, int], Tuple[str, int, Dict[str, str]]
    """
    return render_template('index.html')



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