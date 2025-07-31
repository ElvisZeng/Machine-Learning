#!/usr/bin/env python3
"""
测试UI中的列映射问题
"""

import pandas as pd
import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def simulate_ui_mapping():
    """模拟UI中的列映射过程"""
    print("🎯 模拟UI中的列映射过程...")
    
    try:
        # 读取CSV文件
        df = pd.read_csv('test_bug_fix.csv')
        print(f"原始列名: {list(df.columns)}")
        
        # 模拟UI中的智能列映射
        smart_mapping = {
            'date': ['date', '交易日', 'Date', 'DATE'],
            'contract': ['symbol', 'contract', '合约', 'Contract', 'CONTRACT'],
            'open': ['open', '开盘价', 'Open', 'OPEN'],
            'high': ['high', '最高价', 'High', 'HIGH'],
            'low': ['low', '最低价', 'Low', 'LOW'],
            'close': ['close', '收盘价', 'Close', 'CLOSE'],
            'volume': ['volume', '成交量', 'Volume', 'VOLUME'],
            'open_interest': ['open_interest', '持仓量', 'Open_Interest', 'OPEN_INTEREST']
        }
        
        # 自动检测列映射
        auto_mapping = {}
        for eng_col, possible_names in smart_mapping.items():
            for col_name in df.columns:
                if col_name in possible_names:
                    auto_mapping[col_name] = eng_col
                    break
        
        print(f"自动检测的映射: {auto_mapping}")
        
        # 模拟用户确认的列映射
        user_mapping = {
            'symbol': 'contract',  # 用户确认的映射
            'date': 'date',
            'open': 'open',
            'high': 'high',
            'low': 'low',
            'close': 'close',
            'volume': 'volume',
            'open_interest': 'open_interest'
        }
        
        print(f"用户确认的映射: {user_mapping}")
        
        # 应用用户映射
        df_mapped = df.rename(columns=user_mapping)
        print(f"映射后的列名: {list(df_mapped.columns)}")
        
        # 检查必要的列
        required_columns = ['date', 'contract', 'open', 'high', 'low', 'close', 'volume', 'open_interest']
        missing_columns = [col for col in required_columns if col not in df_mapped.columns]
        
        if missing_columns:
            print(f"❌ 缺少必要的列: {missing_columns}")
            return False
        
        print("✅ 所有必要列都存在")
        return True
        
    except Exception as e:
        print(f"❌ 模拟失败: {e}")
        return False

def test_direct_loading():
    """测试直接加载（不通过UI）"""
    print("\n🧪 测试直接加载...")
    
    try:
        from app import FuturesStrategyAnalyzer
        
        analyzer = FuturesStrategyAnalyzer()
        
        # 直接使用正确的列映射
        column_mapping = {
            'symbol': 'contract',
            'date': 'date',
            'open': 'open',
            'high': 'high',
            'low': 'low',
            'close': 'close',
            'volume': 'volume',
            'open_interest': 'open_interest'
        }
        
        success, message = analyzer.load_data('test_bug_fix.csv', column_mapping)
        
        if not success:
            print(f"❌ 直接加载失败: {message}")
            return False
        
        print("✅ 直接加载成功")
        return True
        
    except Exception as e:
        print(f"❌ 直接加载测试失败: {e}")
        return False

def check_common_issues():
    """检查常见问题"""
    print("\n🔍 检查常见问题...")
    
    # 检查CSV文件编码
    try:
        with open('test_bug_fix.csv', 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
        print(f"CSV第一行: {first_line}")
        
        # 检查是否有隐藏字符
        print(f"列名字节表示: {[ord(c) for c in first_line.split(',')]}")
        
    except Exception as e:
        print(f"❌ 文件读取问题: {e}")
    
    # 检查pandas读取
    try:
        df = pd.read_csv('test_bug_fix.csv')
        print(f"Pandas读取的列名: {list(df.columns)}")
        print(f"列名类型: {[type(col) for col in df.columns]}")
        
    except Exception as e:
        print(f"❌ Pandas读取问题: {e}")

def main():
    """主函数"""
    print("=" * 60)
    print("🎯 UI列映射问题诊断")
    print("=" * 60)
    
    # 检查常见问题
    check_common_issues()
    
    # 模拟UI映射
    if simulate_ui_mapping():
        print("\n✅ UI映射模拟成功")
    else:
        print("\n❌ UI映射模拟失败")
    
    # 测试直接加载
    if test_direct_loading():
        print("\n✅ 直接加载测试成功")
    else:
        print("\n❌ 直接加载测试失败")
    
    print("\n💡 建议:")
    print("1. 确保在UI中正确选择了列映射")
    print("2. 检查CSV文件是否有隐藏字符")
    print("3. 尝试使用不同的编码格式")
    print("4. 确保列名完全匹配（包括大小写）")
    
    print("=" * 60)

if __name__ == "__main__":
    main()