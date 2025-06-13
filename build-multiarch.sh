#!/bin/bash
# Build for multiple architectures including ARM
# Note: You must be logged in to Docker Hub first (docker login)

docker buildx build \
  --platform linux/amd64,linux/arm64,linux/arm/v7 \
  -t yourusername/photo-importer:latest \
  -t yourusername/photo-importer:$(date +%Y.%m.%d) \
  --push .
