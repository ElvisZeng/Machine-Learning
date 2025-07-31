#!/bin/bash

echo "============================================================"
echo "📈 期货交易策略分析系统"
echo "============================================================"

# 检查Python版本
echo "🔍 检查Python环境..."
python3 --version

# 检查依赖包
echo "🔍 检查依赖包..."
python3 check_dependencies.py

if [ $? -ne 0 ]; then
    echo "❌ 依赖检查失败，请先安装缺失的包"
    exit 1
fi

# 检查示例数据
if [ ! -f "sample_futures_data.csv" ]; then
    echo "📊 生成示例数据..."
    python3 sample_data.py
fi

# 启动应用程序
echo "🚀 启动应用程序..."
echo "📱 应用程序将在浏览器中打开"
echo "🌐 地址: http://localhost:8501"
echo ""
echo "按 Ctrl+C 停止应用程序"
echo "============================================================"

python3 -m streamlit run app.py --server.port 8501 --server.address 0.0.0.0