#!/usr/bin/env python3
"""
调试列名映射问题
"""

import pandas as pd
import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def debug_column_mapping():
    """调试列名映射问题"""
    print("🔍 调试列名映射问题...")
    
    try:
        # 读取CSV文件
        df = pd.read_csv('test_bug_fix.csv')
        print(f"原始列名: {list(df.columns)}")
        
        # 模拟load_data方法中的列名映射逻辑
        required_column_mappings = {
            'date': ['date', '交易日', 'Date', 'DATE'],
            'contract': ['contract', 'symbol', '合约', 'Contract', 'CONTRACT'],
            'open': ['open', '开盘价', 'Open', 'OPEN'],
            'high': ['high', '最高价', 'High', 'HIGH'],
            'low': ['low', '最低价', 'Low', 'LOW'],
            'close': ['close', '收盘价', 'Close', 'CLOSE'],
            'volume': ['volume', '成交量', 'Volume', 'VOLUME'],
            'open_interest': ['open_interest', '持仓量', 'Open_Interest', 'OPEN_INTEREST']
        }
        
        # 检查并映射列名
        missing_columns = []
        column_rename_mapping = {}
        
        print("\n🔍 检查列名映射...")
        for required_col, possible_names in required_column_mappings.items():
            found = False
            print(f"检查 {required_col}: 可能的名称 {possible_names}")
            
            for possible_name in possible_names:
                if possible_name in df.columns:
                    print(f"  ✅ 找到 {possible_name}")
                    if possible_name != required_col:
                        column_rename_mapping[possible_name] = required_col
                        print(f"  🔄 将 {possible_name} 映射为 {required_col}")
                    found = True
                    break
            
            if not found:
                missing_columns.append(required_col)
                print(f"  ❌ 未找到 {required_col}")
        
        print(f"\n📊 映射结果:")
        print(f"缺失列: {missing_columns}")
        print(f"重命名映射: {column_rename_mapping}")
        
        if missing_columns:
            print(f"❌ 仍然缺少必要的列: {missing_columns}")
            return False
        
        # 重命名列
        if column_rename_mapping:
            df = df.rename(columns=column_rename_mapping)
            print(f"✅ 重命名后的列名: {list(df.columns)}")
        
        # 验证必要的列是否存在
        required_columns = ['date', 'contract', 'open', 'high', 'low', 'close', 'volume', 'open_interest']
        missing_after_rename = [col for col in required_columns if col not in df.columns]
        
        if missing_after_rename:
            print(f"❌ 重命名后仍然缺少列: {missing_after_rename}")
            return False
        
        print("✅ 所有必要列都存在！")
        return True
        
    except Exception as e:
        print(f"❌ 调试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_with_user_data():
    """测试用户数据"""
    print("\n🧪 测试用户数据...")
    
    try:
        from app import FuturesStrategyAnalyzer
        
        analyzer = FuturesStrategyAnalyzer()
        
        # 创建列映射
        column_mapping = {
            'symbol': 'contract',  # 这是关键映射
            'date': 'date',
            'open': 'open',
            'high': 'high',
            'low': 'low',
            'close': 'close',
            'volume': 'volume',
            'open_interest': 'open_interest'
        }
        
        print(f"使用的列映射: {column_mapping}")
        
        # 测试数据加载
        success, message = analyzer.load_data('test_bug_fix.csv', column_mapping)
        
        if not success:
            print(f"❌ 数据加载失败: {message}")
            return False
        
        print("✅ 数据加载成功")
        print(f"加载后的列名: {list(analyzer.data.columns)}")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("🐛 列名映射调试")
    print("=" * 60)
    
    # 调试列名映射
    if debug_column_mapping():
        print("\n✅ 列名映射逻辑正常")
    else:
        print("\n❌ 列名映射逻辑有问题")
    
    # 测试用户数据
    if test_with_user_data():
        print("\n✅ 用户数据测试通过")
    else:
        print("\n❌ 用户数据测试失败")
    
    print("=" * 60)

if __name__ == "__main__":
    main()