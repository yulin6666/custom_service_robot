.PHONY: help install test build run docker-build docker-run docker-stop deploy-railway clean

help:
	@echo "Available commands:"
	@echo "  make install          - Install dependencies"
	@echo "  make test            - Run tests"
	@echo "  make run             - Run service locally"
	@echo "  make docker-build    - Build Docker image"
	@echo "  make docker-run      - Run Docker container"
	@echo "  make docker-stop     - Stop Docker container"
	@echo "  make deploy-railway  - Deploy to Railway"
	@echo "  make clean           - Clean cache and temporary files"

install:
	pip install -r requirements.txt

test:
	@echo "Starting service and running tests..."
	python test_api.py

run:
	@echo "Starting API service..."
	python api.py

docker-build:
	@echo "Building Docker image..."
	docker build -t customer-service-bot .

docker-run:
	@echo "Running Docker container..."
	docker run -d -p 8000:8000 --name customer-service-bot \
		-e OPENAI_API_KEY=${OPENAI_API_KEY} \
		-e OPENAI_BASE_URL=${OPENAI_BASE_URL} \
		customer-service-bot
	@echo "Service started: http://localhost:8000"

docker-stop:
	@echo "Stopping Docker container..."
	docker stop customer-service-bot || true
	docker rm customer-service-bot || true

docker-logs:
	docker logs -f customer-service-bot

docker-compose-up:
	docker-compose up -d

docker-compose-down:
	docker-compose down

deploy-railway:
	@echo "Deploying to Railway..."
	@echo "Please ensure Railway CLI is installed: npm install -g @railway/cli"
	railway up

clean:
	@echo "Cleaning cache and temporary files..."
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.log" -delete
	rm -f customer_service_graph.png test_graph.png
	@echo "Cleanup complete"
