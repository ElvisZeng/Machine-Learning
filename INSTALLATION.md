# 📦 安装说明

## 🔧 系统要求

- **操作系统**: Windows 10+, macOS 10.14+, Ubuntu 18.04+
- **Python版本**: 3.8 或更高版本
- **内存**: 建议 4GB 或更多
- **存储空间**: 至少 1GB 可用空间

## 🚀 快速安装

### 方法1: 一键安装（推荐）

```bash
# 1. 克隆或下载项目
git clone <repository-url>
cd futures-strategy-analyzer

# 2. 运行安装脚本
./start.sh
```

### 方法2: 手动安装

```bash
# 1. 检查Python版本
python3 --version

# 2. 安装依赖包
pip3 install --break-system-packages --user -r requirements.txt

# 3. 检查安装
python3 check_dependencies.py

# 4. 生成示例数据
python3 sample_data.py

# 5. 启动应用
python3 -m streamlit run app.py
```

## 📋 详细安装步骤

### 步骤1: 环境准备

#### Linux/Ubuntu
```bash
# 更新系统包
sudo apt update

# 安装Python3和pip
sudo apt install python3 python3-pip python3-venv

# 验证安装
python3 --version
pip3 --version
```

#### macOS
```bash
# 使用Homebrew安装Python
brew install python3

# 验证安装
python3 --version
pip3 --version
```

#### Windows
```bash
# 下载并安装Python 3.8+ from python.org
# 确保勾选"Add Python to PATH"

# 验证安装
python --version
pip --version
```

### 步骤2: 安装依赖包

#### 方法A: 直接安装（推荐）
```bash
# 安装所有依赖包
pip3 install --break-system-packages --user -r requirements.txt
```

#### 方法B: 虚拟环境安装
```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
# Linux/macOS:
source venv/bin/activate
# Windows:
# venv\Scripts\activate

# 安装依赖包
pip install -r requirements.txt
```

### 步骤3: 验证安装

```bash
# 运行依赖检查
python3 check_dependencies.py
```

预期输出：
```
📈 期货交易策略分析系统 - 依赖检查
============================================================
🐍 Python版本: 3.8.x
✅ Python版本符合要求 (>= 3.8)

🔍 检查依赖包...
==================================================
✅ streamlit
✅ pandas
✅ numpy
✅ scikit-learn
✅ plotly
✅ matplotlib
✅ seaborn
✅ ta
✅ joblib
✅ xgboost
✅ lightgbm
✅ catboost
==================================================

✅ 所有依赖包已安装 (12/12)

============================================================
🎉 环境检查通过！可以启动应用程序
============================================================
```

### 步骤4: 生成示例数据

```bash
# 生成示例期货数据
python3 sample_data.py
```

### 步骤5: 启动应用程序

```bash
# 方法1: 使用启动脚本
./start.sh

# 方法2: 手动启动
python3 -m streamlit run app.py
```

## 🔍 故障排除

### 问题1: Python版本过低
```bash
# 错误信息: Python版本过低，需要3.8或更高版本

# 解决方案: 升级Python
# Ubuntu/Debian:
sudo apt update
sudo apt install python3.8 python3.8-pip

# macOS:
brew install python@3.8

# Windows: 从python.org下载最新版本
```

### 问题2: 依赖包安装失败
```bash
# 错误信息: No module named 'xxx'

# 解决方案1: 使用--break-system-packages
pip3 install --break-system-packages --user -r requirements.txt

# 解决方案2: 使用虚拟环境
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 解决方案3: 升级pip
pip3 install --upgrade pip
```

### 问题3: 权限问题
```bash
# 错误信息: Permission denied

# 解决方案1: 使用--user标志
pip3 install --user -r requirements.txt

# 解决方案2: 使用sudo（不推荐）
sudo pip3 install -r requirements.txt

# 解决方案3: 使用虚拟环境（推荐）
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 问题4: 网络连接问题
```bash
# 错误信息: Connection timeout

# 解决方案1: 使用国内镜像源
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# 解决方案2: 使用阿里云镜像
pip3 install -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt
```

### 问题5: 特定包安装失败

#### scikit-learn安装失败
```bash
# 解决方案: 先安装编译依赖
# Ubuntu/Debian:
sudo apt install build-essential python3-dev

# 然后安装scikit-learn
pip3 install --break-system-packages --user scikit-learn
```

#### XGBoost安装失败
```bash
# 解决方案: 使用预编译版本
pip3 install --break-system-packages --user xgboost
```

#### LightGBM安装失败
```bash
# 解决方案: 先安装编译依赖
# Ubuntu/Debian:
sudo apt install cmake build-essential

# 然后安装LightGBM
pip3 install --break-system-packages --user lightgbm
```

## 📊 依赖包说明

| 包名 | 版本 | 用途 |
|------|------|------|
| streamlit | 1.28.1 | Web应用框架 |
| pandas | 2.1.3 | 数据处理 |
| numpy | 1.24.3 | 数值计算 |
| scikit-learn | 1.3.2 | 机器学习算法 |
| plotly | 5.17.0 | 交互式图表 |
| matplotlib | 3.8.2 | 静态图表 |
| seaborn | 0.13.0 | 统计图表 |
| ta | 0.10.2 | 技术指标 |
| joblib | 1.3.2 | 并行计算 |
| xgboost | 2.0.2 | 梯度提升 |
| lightgbm | 4.1.0 | 轻量级梯度提升 |
| catboost | 1.2.2 | 类别特征处理 |

## ✅ 安装验证

安装完成后，运行以下命令验证：

```bash
# 1. 检查依赖
python3 check_dependencies.py

# 2. 运行系统测试
python3 test_system.py

# 3. 启动应用
python3 -m streamlit run app.py
```

如果所有测试都通过，说明安装成功！

## 🆘 获取帮助

如果遇到安装问题，请：

1. 查看本文档的故障排除部分
2. 运行 `python3 check_dependencies.py` 检查具体问题
3. 查看错误日志信息
4. 联系技术支持

---

**安装完成后，请阅读 README.md 了解如何使用系统。**