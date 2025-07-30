#!/usr/bin/env python3
"""
期货交易策略分析系统启动脚本
"""

import os
import sys
import subprocess
import importlib.util

def check_dependencies():
    """检查依赖包是否已安装"""
    required_packages = [
        'streamlit', 'pandas', 'numpy', 'scikit-learn', 
        'plotly', 'matplotlib', 'seaborn', 'ta', 'joblib',
        'xgboost', 'lightgbm', 'catboost'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        spec = importlib.util.find_spec(package)
        if spec is None:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ 缺少以下依赖包:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n请运行以下命令安装依赖:")
        print("pip install -r requirements.txt")
        return False
    
    print("✅ 所有依赖包已安装")
    return True

def generate_sample_data():
    """生成示例数据"""
    try:
        print("📊 正在生成示例数据...")
        from sample_data import generate_sample_futures_data
        
        sample_data = generate_sample_futures_data()
        sample_data.to_csv('sample_futures_data.csv', index=False)
        
        print("✅ 示例数据已生成: sample_futures_data.csv")
        print(f"   数据形状: {sample_data.shape}")
        print(f"   日期范围: {sample_data['date'].min()} 至 {sample_data['date'].max()}")
        print(f"   合约数量: {sample_data['contract'].nunique()}")
        
        return True
    except Exception as e:
        print(f"❌ 生成示例数据失败: {e}")
        return False

def start_application():
    """启动Streamlit应用程序"""
    try:
        print("🚀 正在启动期货交易策略分析系统...")
        print("📱 应用程序将在浏览器中打开")
        print("🌐 地址: http://localhost:8501")
        print("\n按 Ctrl+C 停止应用程序")
        print("-" * 50)
        
        # 启动Streamlit应用
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
        
    except KeyboardInterrupt:
        print("\n👋 应用程序已停止")
    except Exception as e:
        print(f"❌ 启动应用程序失败: {e}")

def main():
    """主函数"""
    print("=" * 60)
    print("📈 期货交易策略分析系统")
    print("=" * 60)
    
    # 检查依赖
    if not check_dependencies():
        return
    
    # 询问是否生成示例数据
    if not os.path.exists('sample_futures_data.csv'):
        print("\n📊 未找到示例数据文件")
        generate_sample = input("是否生成示例数据? (y/n): ").lower().strip()
        
        if generate_sample in ['y', 'yes', '是']:
            if not generate_sample_data():
                return
        else:
            print("ℹ️  您可以稍后手动运行 'python sample_data.py' 生成示例数据")
    else:
        print("✅ 示例数据文件已存在")
    
    print("\n" + "=" * 60)
    
    # 启动应用程序
    start_application()

if __name__ == "__main__":
    main()