#!/usr/bin/env python3
"""
期货交易策略分析系统测试脚本
"""

import pandas as pd
import numpy as np
from datetime import datetime
import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_data_generation():
    """测试数据生成功能"""
    print("🧪 测试数据生成功能...")
    
    try:
        from sample_data import generate_sample_futures_data
        
        # 生成示例数据
        data = generate_sample_futures_data()
        
        # 验证数据格式
        required_columns = ['date', 'contract', 'open', 'high', 'low', 'close', 'volume', 'open_interest']
        missing_columns = [col for col in required_columns if col not in data.columns]
        
        if missing_columns:
            print(f"❌ 缺少必要的列: {missing_columns}")
            return False
        
        print(f"✅ 数据生成成功")
        print(f"   数据形状: {data.shape}")
        print(f"   合约数量: {data['contract'].nunique()}")
        print(f"   日期范围: {data['date'].min()} 至 {data['date'].max()}")
        
        return True
        
    except Exception as e:
        print(f"❌ 数据生成失败: {e}")
        return False

def test_analyzer_class():
    """测试分析器类"""
    print("\n🧪 测试分析器类...")
    
    try:
        from app import FuturesStrategyAnalyzer
        
        # 创建分析器实例
        analyzer = FuturesStrategyAnalyzer()
        
        # 生成测试数据
        from sample_data import generate_sample_futures_data
        test_data = generate_sample_futures_data()
        
        # 保存测试数据
        test_data.to_csv('test_data.csv', index=False)
        
        # 测试数据加载
        column_mapping = {
            '交易日': 'date',
            '合约': 'contract',
            '开盘价': 'open',
            '最高价': 'high',
            '最低价': 'low',
            '收盘价': 'close',
            '成交量': 'volume',
            '持仓量': 'open_interest'
        }
        
        success, message = analyzer.load_data('test_data.csv', column_mapping)
        if not success:
            print(f"❌ 数据加载失败: {message}")
            return False
        
        print("✅ 数据加载成功")
        
        # 测试特征创建
        success, message = analyzer.create_features()
        if not success:
            print(f"❌ 特征创建失败: {message}")
            return False
        
        print("✅ 特征创建成功")
        
        # 测试目标变量创建
        success, message = analyzer.create_target()
        if not success:
            print(f"❌ 目标变量创建失败: {message}")
            return False
        
        print("✅ 目标变量创建成功")
        
        # 测试模型训练
        success, message = analyzer.train_model('random_forest')
        if not success:
            print(f"❌ 模型训练失败: {message}")
            return False
        
        print("✅ 模型训练成功")
        
        # 测试策略预测
        success, result = analyzer.predict_strategy(analyzer.target)
        if not success:
            print(f"❌ 策略预测失败: {result}")
            return False
        
        print("✅ 策略预测成功")
        print(f"   操作建议: {result['action']}")
        print(f"   成功率: {result['success_rate']:.1f}%")
        print(f"   盈亏比: {result['profit_loss_ratio']:.2f}")
        
        # 清理测试文件
        if os.path.exists('test_data.csv'):
            os.remove('test_data.csv')
        
        return True
        
    except Exception as e:
        print(f"❌ 分析器测试失败: {e}")
        return False

def test_imports():
    """测试所有必要的导入"""
    print("🧪 测试包导入...")
    
    required_packages = [
        'streamlit', 'pandas', 'numpy', 'sklearn', 
        'plotly', 'matplotlib', 'seaborn', 'ta', 'joblib',
        'xgboost', 'lightgbm', 'catboost'
    ]
    
    failed_imports = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError as e:
            print(f"❌ {package}: {e}")
            failed_imports.append(package)
    
    if failed_imports:
        print(f"\n❌ 以下包导入失败: {failed_imports}")
        return False
    
    print("✅ 所有包导入成功")
    return True

def test_config():
    """测试配置文件"""
    print("\n🧪 测试配置文件...")
    
    try:
        from config import (
            DATA_CONFIG, FEATURE_CONFIG, TARGET_CONFIG, 
            MODEL_CONFIG, STRATEGY_CONFIG, UI_CONFIG
        )
        
        # 验证配置完整性
        configs = [
            ('DATA_CONFIG', DATA_CONFIG),
            ('FEATURE_CONFIG', FEATURE_CONFIG),
            ('TARGET_CONFIG', TARGET_CONFIG),
            ('MODEL_CONFIG', MODEL_CONFIG),
            ('STRATEGY_CONFIG', STRATEGY_CONFIG),
            ('UI_CONFIG', UI_CONFIG)
        ]
        
        for name, config in configs:
            if not isinstance(config, dict):
                print(f"❌ {name} 不是字典类型")
                return False
            print(f"✅ {name}")
        
        return True
        
    except Exception as e:
        print(f"❌ 配置文件测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=" * 60)
    print("📈 期货交易策略分析系统 - 功能测试")
    print("=" * 60)
    
    tests = [
        ("包导入测试", test_imports),
        ("配置文件测试", test_config),
        ("数据生成测试", test_data_generation),
        ("分析器功能测试", test_analyzer_class)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}")
        print("-" * 40)
        
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} 通过")
            else:
                print(f"❌ {test_name} 失败")
        except Exception as e:
            print(f"❌ {test_name} 异常: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！系统功能正常")
        print("\n🚀 启动应用程序:")
        print("python3 -m streamlit run app.py")
    else:
        print("⚠️  部分测试失败，请检查错误信息")
    
    print("=" * 60)

if __name__ == "__main__":
    main()