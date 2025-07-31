#!/usr/bin/env python3
"""
测试用户提供的数据格式
"""

import pandas as pd
import numpy as np
from datetime import datetime

def create_user_format_data():
    """创建符合用户格式的测试数据"""
    
    # 基于用户提供的数据格式
    data = [
        ['IF1005', '2010-4-16', 3450, 3488, 3413.2, 3415.6, 48988, 2702, 5053880, 3431.2, 3399, 'IF'],
        ['IF1006', '2010-4-16', 3460, 3490, 3420.0, 3425.0, 52000, 2800, 5200000, 3440.0, 3400, 'IF'],
        ['IC1005', '2010-4-16', 5000, 5050, 4980.0, 4990.0, 30000, 1500, 3000000, 5000.0, 4950, 'IC'],
        ['IH1005', '2010-4-16', 2800, 2830, 2780.0, 2790.0, 25000, 1200, 2500000, 2800.0, 2750, 'IH']
    ]
    
    columns = ['symbol', 'date', 'open', 'high', 'low', 'close', 'volume', 'open_interest', 'turnover', 'settle', 'pre_settle', 'variety']
    
    df = pd.DataFrame(data, columns=columns)
    
    # 保存为CSV文件
    df.to_csv('user_format_data.csv', index=False)
    
    print("✅ 用户格式测试数据已创建: user_format_data.csv")
    print(f"数据形状: {df.shape}")
    print(f"列名: {list(df.columns)}")
    print("\n数据内容:")
    print(df)
    
    return df

def test_user_format():
    """测试用户数据格式"""
    print("\n🧪 测试用户数据格式...")
    
    try:
        # 读取用户格式数据
        df = pd.read_csv('user_format_data.csv')
        
        print(f"✅ 数据读取成功")
        print(f"列名: {list(df.columns)}")
        
        # 检查必要的列
        required_columns = ['date', 'contract', 'open', 'high', 'low', 'close', 'volume', 'open_interest']
        
        # 模拟列映射
        column_mapping = {
            'symbol': 'contract',  # 关键映射
            'date': 'date',
            'open': 'open',
            'high': 'high',
            'low': 'low',
            'close': 'close',
            'volume': 'volume',
            'open_interest': 'open_interest'
        }
        
        # 应用映射
        df_mapped = df.rename(columns=column_mapping)
        print(f"映射后的列名: {list(df_mapped.columns)}")
        
        # 检查必要列
        missing_columns = [col for col in required_columns if col not in df_mapped.columns]
        
        if missing_columns:
            print(f"❌ 缺少列: {missing_columns}")
            return False
        
        print("✅ 所有必要列都存在")
        
        # 测试数据加载
        from app import FuturesStrategyAnalyzer
        
        analyzer = FuturesStrategyAnalyzer()
        success, message = analyzer.load_data('user_format_data.csv', column_mapping)
        
        if not success:
            print(f"❌ 数据加载失败: {message}")
            return False
        
        print("✅ 数据加载成功")
        print(f"加载后的数据形状: {analyzer.data.shape}")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("📊 用户数据格式测试")
    print("=" * 60)
    
    # 创建测试数据
    create_user_format_data()
    
    # 测试格式
    if test_user_format():
        print("\n🎉 用户数据格式测试通过！")
        print("系统完全支持您的数据格式")
    else:
        print("\n❌ 用户数据格式测试失败")
    
    print("=" * 60)

if __name__ == "__main__":
    main()