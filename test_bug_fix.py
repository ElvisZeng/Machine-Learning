#!/usr/bin/env python3
"""
测试列名映射bug修复
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def create_test_csv():
    """创建测试CSV文件，使用用户提供的列名格式"""
    
    # 生成测试数据
    dates = pd.date_range('2023-01-01', '2023-12-31', freq='D')
    contracts = ['IF2401', 'IF2402', 'IC2401', 'IH2401']
    
    data_list = []
    
    for contract in contracts:
        base_price = np.random.uniform(3000, 5000)
        
        for date in dates:
            if date.weekday() < 5:  # 跳过周末
                # 生成价格数据
                price_change = np.random.normal(0, 0.02)
                base_price *= (1 + price_change)
                
                open_price = base_price * (1 + np.random.normal(0, 0.005))
                high_price = max(open_price, base_price) * (1 + abs(np.random.normal(0, 0.01)))
                low_price = min(open_price, base_price) * (1 - abs(np.random.normal(0, 0.01)))
                close_price = base_price
                
                volume = int(np.random.uniform(1000, 10000))
                open_interest = int(np.random.uniform(50000, 200000))
                turnover = volume * close_price * np.random.uniform(0.95, 1.05)
                settle_price = close_price * np.random.uniform(0.995, 1.005)
                pre_settle_price = settle_price * np.random.uniform(0.98, 1.02)
                
                # 确定品种
                variety = contract[:2]
                
                data_list.append({
                    'symbol': contract,
                    'date': date.strftime('%Y-%m-%d'),
                    'open': round(open_price, 2),
                    'high': round(high_price, 2),
                    'low': round(low_price, 2),
                    'close': round(close_price, 2),
                    'volume': volume,
                    'open_interest': open_interest,
                    'turnover': round(turnover, 2),
                    'settle': round(settle_price, 2),
                    'pre_settle': round(pre_settle_price, 2),
                    'variety': variety
                })
    
    df = pd.DataFrame(data_list)
    df.to_csv('test_bug_fix.csv', index=False)
    
    print("✅ 测试CSV文件已创建: test_bug_fix.csv")
    print(f"数据形状: {df.shape}")
    print(f"列名: {list(df.columns)}")
    print(f"前3行数据:")
    print(df.head(3))
    
    return df

def test_column_mapping():
    """测试列名映射功能"""
    print("\n🧪 测试列名映射功能...")
    
    try:
        from app import FuturesStrategyAnalyzer
        
        # 创建分析器实例
        analyzer = FuturesStrategyAnalyzer()
        
        # 创建列映射（使用用户提供的列名）
        column_mapping = {
            'symbol': 'contract',  # symbol -> contract
            'date': 'date',        # date -> date
            'open': 'open',        # open -> open
            'high': 'high',        # high -> high
            'low': 'low',          # low -> low
            'close': 'close',      # close -> close
            'volume': 'volume',    # volume -> volume
            'open_interest': 'open_interest'  # open_interest -> open_interest
        }
        
        # 测试数据加载
        success, message = analyzer.load_data('test_bug_fix.csv', column_mapping)
        
        if not success:
            print(f"❌ 数据加载失败: {message}")
            return False
        
        print("✅ 数据加载成功")
        print(f"加载后的数据形状: {analyzer.data.shape}")
        print(f"加载后的列名: {list(analyzer.data.columns)}")
        
        # 验证必要的列是否存在
        required_columns = ['date', 'contract', 'open', 'high', 'low', 'close', 'volume', 'open_interest']
        missing_columns = [col for col in required_columns if col not in analyzer.data.columns]
        
        if missing_columns:
            print(f"❌ 仍然缺少必要的列: {missing_columns}")
            return False
        
        print("✅ 所有必要列都存在")
        
        # 测试特征创建
        success, message = analyzer.create_features()
        
        if not success:
            print(f"❌ 特征创建失败: {message}")
            return False
        
        print("✅ 特征创建成功")
        print(f"特征数据形状: {analyzer.features.shape}")
        
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
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("🐛 列名映射Bug修复测试")
    print("=" * 60)
    
    # 创建测试数据
    create_test_csv()
    
    # 测试列名映射
    if test_column_mapping():
        print("\n🎉 Bug修复测试通过！")
        print("列名映射问题已解决")
    else:
        print("\n❌ Bug修复测试失败")
        print("需要进一步调试")
    
    print("=" * 60)

if __name__ == "__main__":
    main()