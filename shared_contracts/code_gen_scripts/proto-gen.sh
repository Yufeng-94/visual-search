#!/bin/bash

python -m grpc_tools.protoc \
    --proto_path=. \
    --python_out=. \
    --grpc_python_out=. \
    --pyi_out=. \
    shared_contracts/protos/search_service/search_service.proto

# shared_contracts/protos/search_service/search_service.proto

# shared_contracts/protos/indexing_service/indexing_service.proto

# shared_contracts/protos/image_encoding_service/image_encoding_service.proto