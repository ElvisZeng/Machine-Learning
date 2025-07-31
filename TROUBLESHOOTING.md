# 🔧 故障排除指南

## 常见问题及解决方案

### 问题1: "缺少必要的列" 错误

**错误信息**: `数据加载失败: 缺少必要的列: ['date', 'contract', 'open', 'high', 'low', 'close', 'volume', 'open_interest']`

**可能原因**:
1. 列映射配置不正确
2. CSV文件列名与系统期望不匹配
3. 文件编码问题
4. 隐藏字符问题

**解决方案**:

#### 步骤1: 检查您的CSV文件列名
```bash
# 查看CSV文件的第一行（列名）
head -1 your_file.csv
```

您的文件应该包含以下列名之一：
- **格式1**: `symbol,date,open,high,low,close,volume,open_interest,...`
- **格式2**: `contract,date,open,high,low,close,volume,open_interest,...`
- **格式3**: `合约,交易日,开盘价,最高价,最低价,收盘价,成交量,持仓量,...`

#### 步骤2: 正确的列映射配置

在Streamlit界面中，确保列映射如下：

**如果您的列名是 `symbol`**:
```
日期列: date
合约列: symbol  ← 这是关键！
开盘价列: open
最高价列: high
最低价列: low
收盘价列: close
成交量列: volume
持仓量列: open_interest
```

**如果您的列名是 `contract`**:
```
日期列: date
合约列: contract
开盘价列: open
最高价列: high
最低价列: low
收盘价列: close
成交量列: volume
持仓量列: open_interest
```

#### 步骤3: 检查文件编码
如果仍有问题，尝试重新保存CSV文件为UTF-8编码：

```python
import pandas as pd

# 读取您的CSV文件
df = pd.read_csv('your_file.csv')

# 重新保存为UTF-8编码
df.to_csv('your_file_utf8.csv', index=False, encoding='utf-8')
```

### 问题2: 智能列映射不工作

**症状**: 系统没有自动检测到正确的列映射

**解决方案**:
1. 确保CSV文件的第一行是列名
2. 检查列名是否有空格或特殊字符
3. 手动配置列映射

### 问题3: 数据导入后为空

**症状**: 导入成功但数据为空

**可能原因**:
1. 数据格式问题
2. 日期格式不正确
3. 数值列包含非数字字符

**解决方案**:
1. 检查日期格式是否为 `YYYY-MM-DD`
2. 确保数值列不包含文本
3. 检查是否有空行或无效数据

## 详细操作步骤

### 正确的导入流程

1. **启动应用程序**
   ```bash
   python3 -m streamlit run app.py
   ```

2. **上传CSV文件**
   - 点击"选择文件"
   - 选择您的CSV文件

3. **配置列映射**
   - 系统会自动检测列映射
   - **重要**: 确保"合约列"选择正确
     - 如果您的列名是 `symbol`，选择 `symbol`
     - 如果您的列名是 `contract`，选择 `contract`

4. **确认映射**
   - 检查所有列映射是否正确
   - 点击"导入数据"

5. **验证导入**
   - 查看数据概览
   - 确认数据行数和列数正确

### 列映射参考表

| 系统期望列名 | 您的CSV列名 | 映射选择 |
|-------------|-------------|----------|
| date | date | date |
| contract | symbol | symbol |
| contract | contract | contract |
| open | open | open |
| high | high | high |
| low | low | low |
| close | close | close |
| volume | volume | volume |
| open_interest | open_interest | open_interest |

## 测试您的数据

### 快速测试脚本

创建一个测试文件 `test_my_data.py`:

```python
#!/usr/bin/env python3
import pandas as pd

# 读取您的CSV文件
df = pd.read_csv('your_file.csv')

print("列名:", list(df.columns))
print("数据形状:", df.shape)
print("前3行:")
print(df.head(3))

# 检查必要的列
required = ['date', 'contract', 'open', 'high', 'low', 'close', 'volume', 'open_interest']
missing = [col for col in required if col not in df.columns]

if missing:
    print("❌ 缺少列:", missing)
else:
    print("✅ 所有必要列都存在")
```

运行测试:
```bash
python3 test_my_data.py
```

## 常见错误及修复

### 错误1: "No module named 'pandas'"
**解决方案**: 安装依赖包
```bash
pip3 install --break-system-packages --user -r requirements.txt
```

### 错误2: "Permission denied"
**解决方案**: 使用用户权限安装
```bash
pip3 install --break-system-packages --user -r requirements.txt
```

### 错误3: "File not found"
**解决方案**: 检查文件路径和权限
```bash
ls -la your_file.csv
```

## 获取帮助

如果问题仍然存在，请提供以下信息：

1. **CSV文件的前几行**（包括列名）
2. **完整的错误信息**
3. **您使用的列映射配置**
4. **操作系统和Python版本**

### 联系信息
- 创建issue时请包含上述信息
- 提供可重现的步骤

## 预防措施

1. **数据准备**:
   - 确保CSV文件格式正确
   - 使用UTF-8编码
   - 检查数据完整性

2. **列名规范**:
   - 避免使用特殊字符
   - 保持列名简洁
   - 使用标准命名

3. **定期备份**:
   - 备份原始数据
   - 保存成功的配置

---

**最后更新**: 2024-01-01  
**版本**: v1.1.0