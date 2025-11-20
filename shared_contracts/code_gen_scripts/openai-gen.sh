#!/bin/bash
# run it in project root folder!!
docker run --rm \
    -v ${PWD}:/local \
    openapitools/openapi-generator-cli generate \
    -i /local/shared_contracts/shared_contracts/open_api/entry_point.yaml \
    -g python-flask \
    -o /local/entry_point/generated_code