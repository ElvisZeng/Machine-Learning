#!/usr/bin/env python3
"""
测试新的CSV数据结构
"""

import pandas as pd
import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_new_data_structure():
    """测试新的数据结构"""
    print("🧪 测试新的CSV数据结构...")
    
    try:
        # 读取新生成的示例数据
        df = pd.read_csv('sample_futures_data_new.csv')
        
        print("✅ 数据加载成功")
        print(f"数据形状: {df.shape}")
        print(f"列名: {list(df.columns)}")
        
        # 检查必要的列
        required_columns = ['合约', '交易日', '开盘价', '最高价', '最低价', '收盘价', '成交量', '持仓量']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            print(f"❌ 缺少必要的列: {missing_columns}")
            return False
        
        print("✅ 所有必要列都存在")
        
        # 检查可选列
        optional_columns = ['成交金额', '结算价', '前结算价', '品种']
        existing_optional = [col for col in optional_columns if col in df.columns]
        print(f"✅ 可选列: {existing_optional}")
        
        # 测试数据加载功能
        from app import FuturesStrategyAnalyzer
        
        analyzer = FuturesStrategyAnalyzer()
        
        # 创建列映射
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
        
        # 测试数据加载
        success, message = analyzer.load_data('sample_futures_data_new.csv', column_mapping)
        
        if not success:
            print(f"❌ 数据加载失败: {message}")
            return False
        
        print("✅ 数据加载成功")
        print(f"加载后的数据形状: {analyzer.data.shape}")
        print(f"加载后的列名: {list(analyzer.data.columns)}")
        
        # 测试特征创建
        success, message = analyzer.create_features()
        
        if not success:
            print(f"❌ 特征创建失败: {message}")
            return False
        
        print("✅ 特征创建成功")
        print(f"特征数据形状: {analyzer.features.shape}")
        
        # 检查新增的特征
        new_features = ['turnover_ratio', 'avg_price', 'settle_change', 'close_vs_settle', 'settle_vs_pre_settle']
        existing_new_features = [f for f in new_features if f in analyzer.features.columns]
        print(f"✅ 新增特征: {existing_new_features}")
        
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
        print(f"操作建议: {result['action']}")
        print(f"成功率: {result['success_rate']:.1f}%")
        print(f"盈亏比: {result['profit_loss_ratio']:.2f}")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("📈 新CSV数据结构测试")
    print("=" * 60)
    
    if test_new_data_structure():
        print("\n🎉 新数据结构测试通过！")
        print("系统已成功适配新的CSV格式")
    else:
        print("\n❌ 新数据结构测试失败")
    
    print("=" * 60)

if __name__ == "__main__":
    main()