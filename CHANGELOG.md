# 📝 更新日志

## v1.1.0 (2024-01-01) - 新CSV格式支持

### 🆕 新增功能

#### 1. 智能列映射系统
- **自动列名识别**: 系统现在可以自动识别中文和英文列名
- **支持的中文列名**: 交易日、合约、开盘价、最高价、最低价、收盘价、成交量、持仓量
- **支持的可选列**: 成交金额、结算价、前结算价、品种
- **智能映射提示**: 界面会显示自动检测的列映射，用户可以确认或调整

#### 2. 扩展的数据字段支持
- **成交金额字段**: 支持成交金额数据，用于计算平均成交价
- **结算价字段**: 支持结算价和前结算价，用于结算价分析
- **品种字段**: 支持期货品种分类
- **自动特征生成**: 基于新字段自动生成额外的技术指标

#### 3. 新增技术指标
- **成交金额指标**:
  - 成交金额移动平均
  - 成交金额比率
  - 平均成交价
- **结算价指标**:
  - 结算价变动率
  - 收盘价相对结算价位置
  - 结算价相对前结算价变动

### 🔧 技术改进

#### 1. 数据预处理优化
- **智能缺失值处理**: 只删除关键列的缺失值，可选列用0填充
- **数据完整性保护**: 避免因可选列缺失导致数据丢失
- **更好的错误处理**: 提供更详细的错误信息和解决建议

#### 2. 特征工程增强
- **动态特征选择**: 根据可用数据自动选择特征
- **可选特征集成**: 将新的可选特征集成到机器学习模型中
- **特征验证**: 确保所有特征都有效且可用

#### 3. 用户界面改进
- **智能列映射界面**: 自动检测并显示列映射
- **更好的用户提示**: 提供清晰的操作指导
- **错误信息优化**: 更友好的错误提示

### 📊 支持的CSV格式

#### 格式1: 完整中文列名（推荐）
```csv
合约,交易日,开盘价,最高价,最低价,收盘价,成交量,持仓量,成交金额,结算价,前结算价,品种
IF2401,2023-01-01,3500.0,3520.0,3480.0,3510.0,5000,100000,17550000.0,3510.0,3500.0,IF
```

#### 格式2: 标准英文列名
```csv
contract,date,open,high,low,close,volume,open_interest
IF2401,2023-01-01,3500.0,3520.0,3480.0,3510.0,5000,100000
```

#### 格式3: 混合格式
```csv
symbol,交易日,open,high,low,close,volume,open_interest,turnover,settle,pre_settle,variety
IF2401,2023-01-01,3500.0,3520.0,3480.0,3510.0,5000,100000,17550000.0,3510.0,3500.0,IF
```

### 🧪 测试验证

#### 新增测试文件
- `sample_data_new.py`: 生成符合新格式的示例数据
- `test_new_data.py`: 测试新数据结构的完整流程
- 验证了从数据导入到策略预测的完整功能

#### 测试结果
- ✅ 数据加载: 支持中文列名和可选字段
- ✅ 特征工程: 自动生成新的技术指标
- ✅ 模型训练: 集成新特征进行训练
- ✅ 策略预测: 基于增强特征进行预测

### 📈 性能提升

#### 1. 数据处理效率
- **更快的列映射**: 自动检测减少手动配置时间
- **更少的数据丢失**: 智能缺失值处理保留更多有效数据
- **更好的内存使用**: 优化了大数据集的处理

#### 2. 模型性能
- **更多特征**: 新增5个可选特征提升模型表现
- **更好的泛化**: 基于更多数据字段的模型更稳定
- **更准确的预测**: 结算价和成交金额信息提供额外信号

### 🔄 向后兼容

- **完全兼容**: 原有的英文列名格式仍然支持
- **渐进升级**: 用户可以选择使用新功能或保持原有格式
- **平滑迁移**: 无需修改现有数据，系统自动适配

### 📋 使用建议

#### 1. 数据准备
- 推荐使用完整的中文列名格式
- 包含成交金额和结算价数据以获得最佳效果
- 确保数据质量和完整性

#### 2. 特征选择
- 系统会自动选择可用的特征
- 可选特征会增强模型性能
- 用户可以在界面中查看所有生成的特征

#### 3. 模型优化
- 新特征可能需要调整模型参数
- 建议进行交叉验证确保模型稳定性
- 定期更新模型以适应市场变化

### 🚀 升级指南

#### 自动升级
1. 下载最新版本
2. 替换现有文件
3. 重启应用程序

#### 数据迁移
- 无需修改现有数据
- 系统会自动检测和适配
- 可以逐步添加新的数据字段

### 🐛 已知问题

- 无已知问题

### 🔮 未来计划

#### v1.2.0 计划功能
- 实时数据接口
- 多时间框架支持
- 历史回测系统
- 风险管理模块

---

**注意**: 本版本完全向后兼容，现有用户可以无缝升级。