#!/usr/bin/env python3
"""
测试您的CSV数据
使用方法: python3 test_your_data.py your_file.csv
"""

import pandas as pd
import sys
import os

def test_csv_file(file_path):
    """测试CSV文件"""
    print(f"🔍 测试文件: {file_path}")
    print("=" * 50)
    
    try:
        # 读取CSV文件
        df = pd.read_csv(file_path)
        
        print(f"✅ 文件读取成功")
        print(f"📊 数据形状: {df.shape}")
        print(f"📋 列名: {list(df.columns)}")
        
        # 检查必要的列
        required_columns = ['date', 'contract', 'open', 'high', 'low', 'close', 'volume', 'open_interest']
        
        print(f"\n🔍 检查必要列...")
        missing_columns = []
        found_columns = []
        
        for col in required_columns:
            if col in df.columns:
                found_columns.append(col)
                print(f"  ✅ {col}")
            else:
                missing_columns.append(col)
                print(f"  ❌ {col}")
        
        # 检查可能的替代列名
        print(f"\n🔍 检查可能的替代列名...")
        symbol_found = 'symbol' in df.columns
        contract_found = 'contract' in df.columns
        
        if symbol_found:
            print(f"  ✅ 找到 'symbol' 列 (可以映射为 'contract')")
        if contract_found:
            print(f"  ✅ 找到 'contract' 列")
        
        if not symbol_found and not contract_found:
            print(f"  ❌ 未找到 'symbol' 或 'contract' 列")
        
        # 显示前几行数据
        print(f"\n📄 前3行数据:")
        print(df.head(3))
        
        # 检查数据类型
        print(f"\n📊 数据类型:")
        print(df.dtypes)
        
        # 检查缺失值
        print(f"\n🔍 缺失值检查:")
        missing_counts = df.isnull().sum()
        if missing_counts.sum() > 0:
            print(missing_counts[missing_counts > 0])
        else:
            print("  ✅ 无缺失值")
        
        # 总结
        print(f"\n📋 总结:")
        if len(missing_columns) == 0:
            print("  ✅ 所有必要列都存在")
            print("  ✅ 可以直接使用")
        else:
            print(f"  ❌ 缺少列: {missing_columns}")
            
            if symbol_found:
                print("  💡 建议: 将 'symbol' 列映射为 'contract'")
            elif contract_found:
                print("  ✅ 'contract' 列已存在")
            else:
                print("  ❌ 需要添加合约列")
        
        return len(missing_columns) == 0
        
    except FileNotFoundError:
        print(f"❌ 文件未找到: {file_path}")
        return False
    except Exception as e:
        print(f"❌ 读取文件失败: {e}")
        return False

def main():
    """主函数"""
    if len(sys.argv) != 2:
        print("使用方法: python3 test_your_data.py your_file.csv")
        print("示例: python3 test_your_data.py data.csv")
        return
    
    file_path = sys.argv[1]
    
    if not os.path.exists(file_path):
        print(f"❌ 文件不存在: {file_path}")
        return
    
    success = test_csv_file(file_path)
    
    if success:
        print(f"\n🎉 测试通过！您的数据文件可以正常使用。")
    else:
        print(f"\n⚠️  测试失败！请检查您的数据文件。")
        print(f"💡 参考 TROUBLESHOOTING.md 获取帮助。")

if __name__ == "__main__":
    main()