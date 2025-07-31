#!/bin/bash

echo "============================================================"
echo "📊 期货交易策略分析系统 - 用户格式版本"
echo "============================================================"
echo ""

# 检查Python版本
echo "🐍 检查Python版本..."
python3 --version
if [ $? -ne 0 ]; then
    echo "❌ Python3未安装，请先安装Python3"
    exit 1
fi

# 检查依赖包
echo ""
echo "🔍 检查依赖包..."
python3 check_dependencies.py

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ 依赖检查失败，请先安装缺失的包"
    echo "运行: pip3 install --break-system-packages --user -r requirements.txt"
    exit 1
fi

# 显示用户格式信息
echo ""
echo "📋 支持的数据格式:"
echo "symbol,date,open,high,low,close,volume,open_interest,turnover,settle,pre_settle,variety"
echo "IF1005,2010-4-16,3450,3488,3413.2,3415.6,48988,2702,5053880,3431.2,3399,IF"
echo ""

# 测试用户格式
echo "🧪 测试用户数据格式..."
python3 test_user_format.py

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 用户格式测试通过"
else
    echo ""
    echo "⚠️  用户格式测试失败，但系统仍可正常使用"
fi

echo ""
echo "🚀 启动应用程序..."
echo "📖 使用说明:"
echo "1. 上传您的CSV文件（格式: symbol,date,open,high,low,close,volume,open_interest,...）"
echo "2. 系统会自动识别列映射"
echo "3. 确认映射后点击'导入数据'"
echo "4. 开始分析您的期货数据"
echo ""
echo "🌐 浏览器将自动打开: http://localhost:8501"
echo ""

# 启动Streamlit应用
python3 -m streamlit run app.py