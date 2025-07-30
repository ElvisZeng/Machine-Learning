#!/bin/bash

echo "============================================================"
echo "📈 期货交易策略分析系统"
echo "============================================================"

# 检查Python版本
echo "🔍 检查Python环境..."
python3 --version

# 检查依赖包
echo "🔍 检查依赖包..."
python3 -c "
import sys
packages = ['streamlit', 'pandas', 'numpy', 'sklearn', 'plotly', 'matplotlib', 'seaborn', 'ta', 'joblib', 'xgboost', 'lightgbm', 'catboost']
failed = []
for pkg in packages:
    try:
        __import__(pkg)
        print(f'✅ {pkg}')
    except ImportError:
        print(f'❌ {pkg}')
        failed.append(pkg)
if failed:
    print(f'\\n❌ 缺少依赖包: {failed}')
    print('请运行: pip3 install --break-system-packages --user -r requirements.txt')
    sys.exit(1)
else:
    print('\\n✅ 所有依赖包已安装')
"

if [ $? -ne 0 ]; then
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