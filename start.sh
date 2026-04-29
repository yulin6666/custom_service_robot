#!/bin/bash

# Smart Customer Service Bot Quick Start Script

echo "======================================"
echo "  Smart Customer Service Bot REST API"
echo "======================================"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed, please install Docker first"
    echo "   Download: https://www.docker.com/get-started"
    exit 1
fi

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose is not installed, please install docker-compose first"
    exit 1
fi

echo "✅ Docker environment check passed"
echo ""

# Choose startup method
echo "Please select startup method:"
echo "1) Start with Docker Compose (Recommended)"
echo "2) Start with Docker"
echo "3) Start with local Python environment"
echo ""
read -p "Enter option (1-3): " choice

case $choice in
    1)
        echo ""
        echo "Starting service with Docker Compose..."
        docker-compose up -d
        echo ""
        echo "✅ Service started!"
        echo ""
        echo "📝 View logs: docker-compose logs -f"
        echo "🛑 Stop service: docker-compose down"
        ;;
    2)
        echo ""
        echo "Building Docker image..."
        docker build -t customer-service-bot .
        echo ""
        echo "Starting container..."
        docker run -d -p 8000:8000 --name customer-service-bot customer-service-bot
        echo ""
        echo "✅ Service started!"
        echo ""
        echo "📝 View logs: docker logs -f customer-service-bot"
        echo "🛑 Stop service: docker stop customer-service-bot"
        ;;
    3)
        echo ""
        echo "Checking Python environment..."
        if ! command -v python3 &> /dev/null; then
            echo "❌ Python3 is not installed"
            exit 1
        fi

        echo "Installing dependencies..."
        pip install -r requirements.txt

        echo ""
        echo "Starting service..."
        python3 api.py
        ;;
    *)
        echo "❌ Invalid option"
        exit 1
        ;;
esac

echo ""
echo "======================================"
echo "  Service Information"
echo "======================================"
echo "📍 API Address: http://localhost:8000"
echo "📖 API Docs: http://localhost:8000/docs"
echo "🏥 Health Check: http://localhost:8000/health"
echo "🖼️  State Graph: http://localhost:8000/api/v1/graph"
echo ""
echo "💡 Quick Test: python3 test_api.py"
echo ""
