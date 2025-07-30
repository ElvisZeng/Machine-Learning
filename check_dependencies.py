#!/usr/bin/env python3
"""
依赖包检查脚本
"""

def check_dependencies():
    """检查所有必要的依赖包"""
    
    # 包名映射：显示名称 -> 导入名称
    package_mapping = {
        'streamlit': 'streamlit',
        'pandas': 'pandas', 
        'numpy': 'numpy',
        'scikit-learn': 'sklearn',  # 包名是scikit-learn，导入时用sklearn
        'plotly': 'plotly',
        'matplotlib': 'matplotlib',
        'seaborn': 'seaborn',
        'ta': 'ta',
        'joblib': 'joblib',
        'xgboost': 'xgboost',
        'lightgbm': 'lightgbm',
        'catboost': 'catboost'
    }
    
    print("🔍 检查依赖包...")
    print("=" * 50)
    
    failed_packages = []
    successful_packages = []
    
    for display_name, import_name in package_mapping.items():
        try:
            __import__(import_name)
            print(f"✅ {display_name}")
            successful_packages.append(display_name)
        except ImportError as e:
            print(f"❌ {display_name}: {e}")
            failed_packages.append(display_name)
    
    print("=" * 50)
    
    if failed_packages:
        print(f"\n❌ 缺少以下依赖包: {failed_packages}")
        print("\n请运行以下命令安装:")
        print("pip3 install --break-system-packages --user -r requirements.txt")
        return False
    else:
        print(f"\n✅ 所有依赖包已安装 ({len(successful_packages)}/{len(package_mapping)})")
        return True

def check_python_version():
    """检查Python版本"""
    import sys
    
    print(f"🐍 Python版本: {sys.version}")
    
    if sys.version_info >= (3, 8):
        print("✅ Python版本符合要求 (>= 3.8)")
        return True
    else:
        print("❌ Python版本过低，需要3.8或更高版本")
        return False

def main():
    """主函数"""
    print("📈 期货交易策略分析系统 - 依赖检查")
    print("=" * 60)
    
    # 检查Python版本
    python_ok = check_python_version()
    
    print()
    
    # 检查依赖包
    deps_ok = check_dependencies()
    
    print("\n" + "=" * 60)
    
    if python_ok and deps_ok:
        print("🎉 环境检查通过！可以启动应用程序")
        print("\n启动命令:")
        print("python3 -m streamlit run app.py")
        print("或者:")
        print("./start.sh")
    else:
        print("⚠️  环境检查失败，请先解决上述问题")
    
    print("=" * 60)

if __name__ == "__main__":
    main()