import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_sample_futures_data_new():
    """生成符合新CSV结构的示例期货数据"""
    
    # 设置参数
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2023, 12, 31)
    contracts = ['IF2401', 'IF2402', 'IF2403', 'IC2401', 'IC2402', 'IH2401']
    varieties = ['IF', 'IC', 'IH']  # 品种
    
    data_list = []
    
    for contract in contracts:
        # 为每个合约生成数据
        current_date = start_date
        base_price = np.random.uniform(3000, 5000)  # 基础价格
        
        # 确定品种
        variety = None
        for v in varieties:
            if v in contract:
                variety = v
                break
        
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
            
            # 生成成交金额
            turnover = volume * close_price * np.random.uniform(0.95, 1.05)
            
            # 生成结算价和前结算价
            settle_price = close_price * np.random.uniform(0.995, 1.005)
            pre_settle_price = settle_price * np.random.uniform(0.98, 1.02)
            
            data_list.append({
                '合约': contract,
                '交易日': current_date.strftime('%Y-%m-%d'),
                '开盘价': round(open_price, 2),
                '最高价': round(high_price, 2),
                '最低价': round(low_price, 2),
                '收盘价': round(close_price, 2),
                '成交量': volume,
                '持仓量': open_interest,
                '成交金额': round(turnover, 2),
                '结算价': round(settle_price, 2),
                '前结算价': round(pre_settle_price, 2),
                '品种': variety
            })
            
            current_date += timedelta(days=1)
    
    # 创建DataFrame
    df = pd.DataFrame(data_list)
    
    # 按日期和合约排序
    df = df.sort_values(['交易日', '合约'])
    
    return df

if __name__ == "__main__":
    # 生成示例数据
    sample_data = generate_sample_futures_data_new()
    
    # 保存为CSV文件
    sample_data.to_csv('sample_futures_data_new.csv', index=False, encoding='utf-8-sig')
    
    print("示例数据已生成并保存为 'sample_futures_data_new.csv'")
    print(f"数据形状: {sample_data.shape}")
    print(f"日期范围: {sample_data['交易日'].min()} 至 {sample_data['交易日'].max()}")
    print(f"合约数量: {sample_data['合约'].nunique()}")
    print(f"品种数量: {sample_data['品种'].nunique()}")
    print("\n列名:")
    print(list(sample_data.columns))
    print("\n前5行数据:")
    print(sample_data.head())