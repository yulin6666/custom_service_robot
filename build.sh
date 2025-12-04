#!/bin/bash

# Docker 构建脚本（使用 BuildKit 缓存加速）

echo "======================================"
echo "  使用 BuildKit 构建 Docker 镜像"
echo "======================================"
echo ""

# 检查 Docker 是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker 未安装，请先安装 Docker"
    exit 1
fi

echo "✅ Docker 环境检查通过"
echo ""

# 启用 BuildKit
export DOCKER_BUILDKIT=1

echo "📦 开始构建镜像..."
echo "使用 BuildKit 缓存加速依赖下载"
echo ""

# 构建镜像
docker build -t customer-service-bot . \
    --progress=plain \
    --build-arg BUILDKIT_INLINE_CACHE=1

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 镜像构建成功！"
    echo ""
    echo "📝 运行容器: docker run -d -p 8080:8080 --name customer-service-bot customer-service-bot"
    echo "📝 查看日志: docker logs -f customer-service-bot"
    echo "📝 停止容器: docker stop customer-service-bot"
else
    echo ""
    echo "❌ 构建失败，请检查错误信息"
    exit 1
fi
