#!/bin/bash

echo "🚀 开始部署工业检验平台..."

# 检查Docker是否运行
if ! docker info >/dev/null 2>&1; then
    echo "❌ Docker未运行，请先启动Docker"
    exit 1
fi

echo "🧪 运行后端测试..."
cd backend
python -m pytest tests/ -v
BACKEND_TEST_RESULT=$?

if [ $BACKEND_TEST_RESULT -eq 0 ]; then
    echo "✅ 后端测试通过"
else
    echo "❌ 后端测试失败"
    exit 1
fi

echo "🧪 运行前端测试..."
cd ../frontend
CI=true npm test -- --watchAll=false
FRONTEND_TEST_RESULT=$?

if [ $FRONTEND_TEST_RESULT -eq 0 ]; then
    echo "✅ 前端测试通过"
else
    echo "❌ 前端测试失败"
    exit 1
fi

echo "🐳 构建并启动Docker容器..."
cd ..
docker-compose up --build -d

echo "⏳ 等待服务启动 (30秒)..."
sleep 30

echo "✅ 服务已启动!"
echo "🌐 前端访问: http://localhost:3000"
echo "📚 API文档: http://localhost:8000/docs"

# 创建GitHub仓库并推送
read -p "是否创建GitHub仓库并推送代码? (y/n): " choice
if [ "$choice" == "y" ]; then
    echo "🐙 创建GitHub仓库并推送代码..."
    git init
    git add .
    git commit -m "feat: 完整工业检验平台实现"
    git branch -M main
    
    echo "请在GitHub上创建新仓库，然后输入仓库URL:"
    read repo_url
    git remote add origin $repo_url
    git push -u origin main
    echo "🚀 代码已推送到GitHub!"
fi

echo "🎉 部署完成！"