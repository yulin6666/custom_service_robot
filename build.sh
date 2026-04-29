#!/bin/bash

# Docker build script (using BuildKit cache acceleration)

echo "======================================"
echo "  Building Docker Image with BuildKit"
echo "======================================"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed, please install Docker first"
    exit 1
fi

echo "✅ Docker environment check passed"
echo ""

# Enable BuildKit
export DOCKER_BUILDKIT=1

echo "📦 Starting image build..."
echo "Using BuildKit cache to accelerate dependency downloads"
echo ""

# Build image
docker build -t customer-service-bot . \
    --progress=plain \
    --build-arg BUILDKIT_INLINE_CACHE=1

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Image built successfully!"
    echo ""
    echo "📝 Run container: docker run -d -p 8080:8080 --name customer-service-bot customer-service-bot"
    echo "📝 View logs: docker logs -f customer-service-bot"
    echo "📝 Stop container: docker stop customer-service-bot"
else
    echo ""
    echo "❌ Build failed, please check error messages"
    exit 1
fi
