#!/usr/bin/env bash

if [ -z "$1" ]; then
  echo "No dockerfile path"
  exit 1
fi

DOCKERFILE_PATH=$1

docker login

IMAGE_NAME="gintowt/zadanie3:latest"

echo "Building img..."
docker build -f "$DOCKERFILE_PATH" -t "$IMAGE_NAME" .

echo "Pushing image to Docker Hub..."
docker push "$IMAGE_NAME"

