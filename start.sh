#!/bin/bash

# 智能客服机器人快速启动脚本

echo "======================================"
echo "  智能客服机器人 REST API 服务"
echo "======================================"
echo ""

# 检查 Docker 是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker 未安装，请先安装 Docker"
    echo "   下载地址: https://www.docker.com/get-started"
    exit 1
fi

# 检查 docker-compose 是否安装
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose 未安装，请先安装 docker-compose"
    exit 1
fi

echo "✅ Docker 环境检查通过"
echo ""

# 选择启动方式
echo "请选择启动方式："
echo "1) 使用 Docker Compose 启动（推荐）"
echo "2) 使用 Docker 启动"
echo "3) 本地 Python 环境启动"
echo ""
read -p "请输入选项 (1-3): " choice

case $choice in
    1)
        echo ""
        echo "正在使用 Docker Compose 启动服务..."
        docker-compose up -d
        echo ""
        echo "✅ 服务已启动！"
        echo ""
        echo "📝 查看日志: docker-compose logs -f"
        echo "🛑 停止服务: docker-compose down"
        ;;
    2)
        echo ""
        echo "正在构建 Docker 镜像..."
        docker build -t customer-service-bot .
        echo ""
        echo "正在启动容器..."
        docker run -d -p 8000:8000 --name customer-service-bot customer-service-bot
        echo ""
        echo "✅ 服务已启动！"
        echo ""
        echo "📝 查看日志: docker logs -f customer-service-bot"
        echo "🛑 停止服务: docker stop customer-service-bot"
        ;;
    3)
        echo ""
        echo "正在检查 Python 环境..."
        if ! command -v python3 &> /dev/null; then
            echo "❌ Python3 未安装"
            exit 1
        fi

        echo "正在安装依赖..."
        pip install -r requirements.txt

        echo ""
        echo "正在启动服务..."
        python3 api.py
        ;;
    *)
        echo "❌ 无效选项"
        exit 1
        ;;
esac

echo ""
echo "======================================"
echo "  服务信息"
echo "======================================"
echo "📍 API 地址: http://localhost:8000"
echo "📖 API 文档: http://localhost:8000/docs"
echo "🏥 健康检查: http://localhost:8000/health"
echo "🖼️  状态图: http://localhost:8000/api/v1/graph"
echo ""
echo "💡 快速测试: python3 test_api.py"
echo ""
