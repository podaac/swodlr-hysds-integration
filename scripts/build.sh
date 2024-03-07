#!/bin/bash
ROOT_DIR=$(realpath $(dirname "$BASH_SOURCE")/../)
cd $ROOT_DIR
rm -r "$ROOT_DIR/dist"

poetry build -f wheel
WHL_FILE=(dist/*.whl)
VERSION=$(poetry version -s)

docker build \
    -f docker/Dockerfile \
    -t ghcr.io/podaac/swodlr-hysds-integration:$VERSION \
    --label "org.opencontainers.image.source=https://github.com/podaac/swodlr-hysds-integration" \
    --label "org.opencontainers.image.licenses=Apache-2.0" \
    --build-arg WHL_FILE=$WHL_FILE \
   $ROOT_DIR
