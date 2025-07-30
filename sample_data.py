import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_sample_futures_data():
    """生成示例期货数据"""
    
    # 设置参数
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2023, 12, 31)
    contracts = ['IF2401', 'IF2402', 'IF2403', 'IC2401', 'IC2402', 'IH2401']
    
    data_list = []
    
    for contract in contracts:
        # 为每个合约生成数据
        current_date = start_date
        base_price = np.random.uniform(3000, 5000)  # 基础价格
        
        while current_date <= end_date:
            # 跳过周末
            if current_date.weekday() >= 5:
                current_date += timedelta(days=1)
                continue
            
            # 生成价格数据
            price_change = np.random.normal(0, 0.02)  # 价格变动
            base_price *= (1 + price_change)
            
            # 生成OHLC数据
            open_price = base_price * (1 + np.random.normal(0, 0.005))
            high_price = max(open_price, base_price) * (1 + abs(np.random.normal(0, 0.01)))
            low_price = min(open_price, base_price) * (1 - abs(np.random.normal(0, 0.01)))
            close_price = base_price
            
            # 生成成交量和持仓量
            volume = int(np.random.uniform(1000, 10000))
            open_interest = int(np.random.uniform(50000, 200000))
            
            data_list.append({
                'date': current_date.strftime('%Y-%m-%d'),
                'contract': contract,
                'open': round(open_price, 2),
                'high': round(high_price, 2),
                'low': round(low_price, 2),
                'close': round(close_price, 2),
                'volume': volume,
                'open_interest': open_interest
            })
            
            current_date += timedelta(days=1)
    
    # 创建DataFrame
    df = pd.DataFrame(data_list)
    
    # 按日期和合约排序
    df = df.sort_values(['date', 'contract'])
    
    return df

if __name__ == "__main__":
    # 生成示例数据
    sample_data = generate_sample_futures_data()
    
    # 保存为CSV文件
    sample_data.to_csv('sample_futures_data.csv', index=False)
    
    print("示例数据已生成并保存为 'sample_futures_data.csv'")
    print(f"数据形状: {sample_data.shape}")
    print(f"日期范围: {sample_data['date'].min()} 至 {sample_data['date'].max()}")
    print(f"合约数量: {sample_data['contract'].nunique()}")
    print("\n前5行数据:")
    print(sample_data.head())