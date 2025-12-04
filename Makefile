.PHONY: help install test build run docker-build docker-run docker-stop deploy-railway clean

help:
	@echo "可用命令："
	@echo "  make install          - 安装依赖"
	@echo "  make test            - 运行测试"
	@echo "  make run             - 本地运行服务"
	@echo "  make docker-build    - 构建 Docker 镜像"
	@echo "  make docker-run      - 运行 Docker 容器"
	@echo "  make docker-stop     - 停止 Docker 容器"
	@echo "  make deploy-railway  - 部署到 Railway"
	@echo "  make clean           - 清理缓存和临时文件"

install:
	pip install -r requirements.txt

test:
	@echo "启动服务并运行测试..."
	python test_api.py

run:
	@echo "启动 API 服务..."
	python api.py

docker-build:
	@echo "构建 Docker 镜像..."
	docker build -t customer-service-bot .

docker-run:
	@echo "运行 Docker 容器..."
	docker run -d -p 8000:8000 --name customer-service-bot \
		-e OPENAI_API_KEY=${OPENAI_API_KEY} \
		-e OPENAI_BASE_URL=${OPENAI_BASE_URL} \
		customer-service-bot
	@echo "服务已启动: http://localhost:8000"

docker-stop:
	@echo "停止 Docker 容器..."
	docker stop customer-service-bot || true
	docker rm customer-service-bot || true

docker-logs:
	docker logs -f customer-service-bot

docker-compose-up:
	docker-compose up -d

docker-compose-down:
	docker-compose down

deploy-railway:
	@echo "部署到 Railway..."
	@echo "请确保已安装 Railway CLI: npm install -g @railway/cli"
	railway up

clean:
	@echo "清理缓存和临时文件..."
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.log" -delete
	rm -f customer_service_graph.png test_graph.png
	@echo "清理完成"
