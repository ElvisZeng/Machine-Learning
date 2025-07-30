import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import StandardScaler
import xgboost as xgb
import lightgbm as lgb
from catboost import CatBoostClassifier
import ta
import joblib
import os
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# 设置页面配置
st.set_page_config(
    page_title="期货交易策略分析系统",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #c3e6cb;
    }
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #f5c6cb;
    }
</style>
""", unsafe_allow_html=True)

class FuturesStrategyAnalyzer:
    def __init__(self):
        self.data = None
        self.features = None
        self.target = None
        self.model = None
        self.scaler = StandardScaler()
        self.column_mapping = {}
        
    def load_data(self, file, column_mapping):
        """加载并处理CSV数据"""
        try:
            df = pd.read_csv(file)
            
            # 重命名列
            df = df.rename(columns=column_mapping)
            
            # 确保必要的列存在
            required_columns = ['date', 'contract', 'open', 'high', 'low', 'close', 'volume', 'open_interest']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                raise ValueError(f"缺少必要的列: {missing_columns}")
            
            # 处理日期列
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')
            
            # 确保数值列为数值类型
            numeric_columns = ['open', 'high', 'low', 'close', 'volume', 'open_interest']
            for col in numeric_columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # 删除缺失值
            df = df.dropna()
            
            self.data = df
            return True, "数据加载成功！"
            
        except Exception as e:
            return False, f"数据加载失败: {str(e)}"
    
    def create_features(self):
        """创建技术指标特征"""
        if self.data is None:
            return False, "请先加载数据"
        
        try:
            df = self.data.copy()
            
            # 基础价格特征
            df['price_change'] = df['close'].pct_change()
            df['high_low_ratio'] = df['high'] / df['low']
            df['open_close_ratio'] = df['open'] / df['close']
            
            # 移动平均线
            df['ma_5'] = df['close'].rolling(window=5).mean()
            df['ma_10'] = df['close'].rolling(window=10).mean()
            df['ma_20'] = df['close'].rolling(window=20).mean()
            df['ma_50'] = df['close'].rolling(window=50).mean()
            
            # 价格相对于移动平均线的位置
            df['price_vs_ma5'] = df['close'] / df['ma_5'] - 1
            df['price_vs_ma10'] = df['close'] / df['ma_10'] - 1
            df['price_vs_ma20'] = df['close'] / df['ma_20'] - 1
            df['price_vs_ma50'] = df['close'] / df['ma_50'] - 1
            
            # 技术指标
            df['rsi'] = ta.momentum.RSIIndicator(df['close']).rsi()
            df['macd'] = ta.trend.MACD(df['close']).macd()
            df['macd_signal'] = ta.trend.MACD(df['close']).macd_signal()
            df['bb_upper'] = ta.volatility.BollingerBands(df['close']).bollinger_hband()
            df['bb_lower'] = ta.volatility.BollingerBands(df['close']).bollinger_lband()
            df['bb_width'] = df['bb_upper'] - df['bb_lower']
            
            # 成交量指标
            df['volume_ma'] = df['volume'].rolling(window=20).mean()
            df['volume_ratio'] = df['volume'] / df['volume_ma']
            
            # 波动率指标
            df['volatility'] = df['close'].rolling(window=20).std()
            df['atr'] = ta.volatility.AverageTrueRange(df['high'], df['low'], df['close']).average_true_range()
            
            # 趋势指标
            df['adx'] = ta.trend.ADXIndicator(df['high'], df['low'], df['close']).adx()
            df['cci'] = ta.trend.CCIIndicator(df['high'], df['low'], df['close']).cci()
            
            # 删除包含NaN的行
            df = df.dropna()
            
            self.features = df
            return True, "特征创建成功！"
            
        except Exception as e:
            return False, f"特征创建失败: {str(e)}"
    
    def create_target(self, lookforward_days=5, profit_threshold=0.02, loss_threshold=-0.01):
        """创建目标变量（未来价格变动）"""
        if self.features is None:
            return False, "请先创建特征"
        
        try:
            df = self.features.copy()
            
            # 计算未来价格变动
            df['future_return'] = df['close'].shift(-lookforward_days) / df['close'] - 1
            
            # 创建目标变量
            # 1: 做多信号 (未来上涨超过阈值)
            # 0: 持有 (未来变动在阈值内)
            # -1: 做空信号 (未来下跌超过阈值)
            
            conditions = [
                df['future_return'] > profit_threshold,
                df['future_return'] < loss_threshold
            ]
            choices = [1, -1]
            df['target'] = np.select(conditions, choices, default=0)
            
            # 删除最后几行（没有未来数据）
            df = df.dropna()
            
            self.target = df
            return True, "目标变量创建成功！"
            
        except Exception as e:
            return False, f"目标变量创建失败: {str(e)}"
    
    def train_model(self, model_type='random_forest', test_size=0.2):
        """训练机器学习模型"""
        if self.target is None:
            return False, "请先创建目标变量"
        
        try:
            df = self.target.copy()
            
            # 选择特征列
            feature_columns = [
                'price_change', 'high_low_ratio', 'open_close_ratio',
                'price_vs_ma5', 'price_vs_ma10', 'price_vs_ma20', 'price_vs_ma50',
                'rsi', 'macd', 'macd_signal', 'bb_width', 'volume_ratio',
                'volatility', 'atr', 'adx', 'cci'
            ]
            
            # 确保所有特征列都存在
            available_features = [col for col in feature_columns if col in df.columns]
            
            X = df[available_features]
            y = df['target']
            
            # 分割数据
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=42, stratify=y
            )
            
            # 标准化特征
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            # 选择模型
            if model_type == 'random_forest':
                self.model = RandomForestClassifier(n_estimators=100, random_state=42)
            elif model_type == 'gradient_boosting':
                self.model = GradientBoostingClassifier(random_state=42)
            elif model_type == 'logistic_regression':
                self.model = LogisticRegression(random_state=42, max_iter=1000)
            elif model_type == 'xgboost':
                self.model = xgb.XGBClassifier(random_state=42)
            elif model_type == 'lightgbm':
                self.model = lgb.LGBMClassifier(random_state=42)
            elif model_type == 'catboost':
                self.model = CatBoostClassifier(random_state=42, verbose=False)
            
            # 训练模型
            self.model.fit(X_train_scaled, y_train)
            
            # 评估模型
            y_pred = self.model.predict(X_test_scaled)
            accuracy = accuracy_score(y_test, y_pred)
            
            return True, f"模型训练成功！测试集准确率: {accuracy:.4f}"
            
        except Exception as e:
            return False, f"模型训练失败: {str(e)}"
    
    def predict_strategy(self, latest_data):
        """预测交易策略"""
        if self.model is None:
            return False, "请先训练模型"
        
        try:
            # 使用相同的特征创建方法处理最新数据
            df = latest_data.copy()
            
            # 创建特征（使用与训练时相同的方法）
            # 这里简化处理，实际应用中需要与create_features方法保持一致
            feature_columns = [
                'price_change', 'high_low_ratio', 'open_close_ratio',
                'price_vs_ma5', 'price_vs_ma10', 'price_vs_ma20', 'price_vs_ma50',
                'rsi', 'macd', 'macd_signal', 'bb_width', 'volume_ratio',
                'volatility', 'atr', 'adx', 'cci'
            ]
            
            available_features = [col for col in feature_columns if col in df.columns]
            X_latest = df[available_features].iloc[-1:].values
            
            # 标准化
            X_latest_scaled = self.scaler.transform(X_latest)
            
            # 预测
            prediction = self.model.predict(X_latest_scaled)[0]
            probabilities = self.model.predict_proba(X_latest_scaled)[0]
            
            # 获取当前价格
            current_price = df['close'].iloc[-1]
            
            # 计算止损止盈价格（基于ATR）
            atr = df['atr'].iloc[-1] if 'atr' in df.columns else current_price * 0.02
            
            if prediction == 1:  # 做多
                stop_loss = current_price - atr * 2
                take_profit = current_price + atr * 3
                action = "做多"
            elif prediction == -1:  # 做空
                stop_loss = current_price + atr * 2
                take_profit = current_price - atr * 3
                action = "做空"
            else:  # 持有
                stop_loss = None
                take_profit = None
                action = "持有"
            
            # 计算成功率（基于概率）
            success_rate = max(probabilities) * 100
            
            # 计算盈亏比
            if stop_loss and take_profit:
                if prediction == 1:
                    risk = current_price - stop_loss
                    reward = take_profit - current_price
                else:
                    risk = stop_loss - current_price
                    reward = current_price - take_profit
                profit_loss_ratio = reward / risk if risk > 0 else 0
            else:
                profit_loss_ratio = 0
            
            result = {
                'action': action,
                'current_price': current_price,
                'stop_loss': stop_loss,
                'take_profit': take_profit,
                'success_rate': success_rate,
                'profit_loss_ratio': profit_loss_ratio,
                'prediction': prediction,
                'probabilities': probabilities
            }
            
            return True, result
            
        except Exception as e:
            return False, f"策略预测失败: {str(e)}"

# 初始化分析器
if 'analyzer' not in st.session_state:
    st.session_state.analyzer = FuturesStrategyAnalyzer()

# 主界面
st.markdown('<h1 class="main-header">📈 期货交易策略分析系统</h1>', unsafe_allow_html=True)

# 侧边栏
st.sidebar.title("功能菜单")

# 数据导入部分
st.sidebar.header("📊 数据导入")
uploaded_file = st.sidebar.file_uploader("选择CSV文件", type=['csv'])

if uploaded_file is not None:
    # 读取CSV文件的前几行来显示列名
    df_preview = pd.read_csv(uploaded_file, nrows=5)
    st.sidebar.write("CSV文件列名:")
    st.sidebar.write(list(df_preview.columns))
    
    # 列映射配置
    st.sidebar.header("列映射配置")
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        date_col = st.selectbox("日期列", df_preview.columns, index=0)
        contract_col = st.selectbox("合约列", df_preview.columns, index=1)
        open_col = st.selectbox("开盘价列", df_preview.columns, index=2)
        high_col = st.selectbox("最高价列", df_preview.columns, index=3)
    
    with col2:
        low_col = st.selectbox("最低价列", df_preview.columns, index=4)
        close_col = st.selectbox("收盘价列", df_preview.columns, index=5)
        volume_col = st.selectbox("成交量列", df_preview.columns, index=6)
        oi_col = st.selectbox("持仓量列", df_preview.columns, index=7)
    
    # 创建列映射
    column_mapping = {
        date_col: 'date',
        contract_col: 'contract',
        open_col: 'open',
        high_col: 'high',
        low_col: 'low',
        close_col: 'close',
        volume_col: 'volume',
        oi_col: 'open_interest'
    }
    
    if st.sidebar.button("导入数据", type="primary"):
        success, message = st.session_state.analyzer.load_data(uploaded_file, column_mapping)
        
        if success:
            st.sidebar.markdown(f'<div class="success-message">{message}</div>', unsafe_allow_html=True)
            st.session_state.data_loaded = True
        else:
            st.sidebar.markdown(f'<div class="error-message">{message}</div>', unsafe_allow_html=True)

# 主内容区域
tab1, tab2, tab3, tab4 = st.tabs(["📊 数据概览", "🔧 特征工程", "🤖 模型训练", "📈 策略分析"])

with tab1:
    st.header("数据概览")
    
    if hasattr(st.session_state, 'data_loaded') and st.session_state.data_loaded:
        analyzer = st.session_state.analyzer
        
        if analyzer.data is not None:
            # 显示基本信息
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("数据行数", len(analyzer.data))
            
            with col2:
                st.metric("合约数量", analyzer.data['contract'].nunique())
            
            with col3:
                st.metric("日期范围", f"{analyzer.data['date'].min().strftime('%Y-%m-%d')} 至 {analyzer.data['date'].max().strftime('%Y-%m-%d')}")
            
            with col4:
                st.metric("数据完整性", f"{(1 - analyzer.data.isnull().sum().sum() / (len(analyzer.data) * len(analyzer.data.columns))) * 100:.1f}%")
            
            # 显示数据表格
            st.subheader("数据预览")
            st.dataframe(analyzer.data.head(10))
            
            # 价格走势图
            st.subheader("价格走势图")
            fig = go.Figure()
            
            # 按合约分组显示
            for contract in analyzer.data['contract'].unique()[:5]:  # 只显示前5个合约
                contract_data = analyzer.data[analyzer.data['contract'] == contract]
                fig.add_trace(go.Scatter(
                    x=contract_data['date'],
                    y=contract_data['close'],
                    mode='lines',
                    name=contract
                ))
            
            fig.update_layout(
                title="收盘价走势",
                xaxis_title="日期",
                yaxis_title="价格",
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # 统计信息
            st.subheader("统计信息")
            st.dataframe(analyzer.data.describe())
            
        else:
            st.warning("请先导入数据")
    else:
        st.info("请先导入CSV数据文件")

with tab2:
    st.header("特征工程")
    
    if hasattr(st.session_state, 'data_loaded') and st.session_state.data_loaded:
        analyzer = st.session_state.analyzer
        
        if analyzer.data is not None:
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("创建技术指标特征", type="primary"):
                    success, message = analyzer.create_features()
                    if success:
                        st.success(message)
                        st.session_state.features_created = True
                    else:
                        st.error(message)
            
            with col2:
                if st.button("创建目标变量", type="primary"):
                    if hasattr(st.session_state, 'features_created') and st.session_state.features_created:
                        lookforward = st.slider("预测天数", 1, 10, 5)
                        profit_threshold = st.slider("盈利阈值", 0.01, 0.05, 0.02, 0.01)
                        loss_threshold = st.slider("亏损阈值", -0.05, -0.01, -0.01, 0.01)
                        
                        success, message = analyzer.create_target(lookforward, profit_threshold, loss_threshold)
                        if success:
                            st.success(message)
                            st.session_state.target_created = True
                        else:
                            st.error(message)
                    else:
                        st.warning("请先创建特征")
            
            # 显示特征信息
            if hasattr(st.session_state, 'features_created') and st.session_state.features_created:
                if analyzer.features is not None:
                    st.subheader("特征概览")
                    
                    # 显示特征统计
                    feature_stats = analyzer.features.describe()
                    st.dataframe(feature_stats)
                    
                    # 特征相关性热力图
                    st.subheader("特征相关性")
                    numeric_features = analyzer.features.select_dtypes(include=[np.number])
                    correlation_matrix = numeric_features.corr()
                    
                    fig, ax = plt.subplots(figsize=(12, 8))
                    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, ax=ax)
                    plt.title("特征相关性热力图")
                    st.pyplot(fig)
                    
                    # 目标变量分布
                    if hasattr(st.session_state, 'target_created') and st.session_state.target_created:
                        if analyzer.target is not None:
                            st.subheader("目标变量分布")
                            
                            target_counts = analyzer.target['target'].value_counts()
                            fig = px.pie(
                                values=target_counts.values,
                                names=['做空', '持有', '做多'],
                                title="目标变量分布"
                            )
                            st.plotly_chart(fig, use_container_width=True)
                            
                            st.write("目标变量统计:")
                            st.write(target_counts)
        else:
            st.warning("请先导入数据")
    else:
        st.info("请先导入数据")

with tab3:
    st.header("模型训练")
    
    if hasattr(st.session_state, 'target_created') and st.session_state.target_created:
        analyzer = st.session_state.analyzer
        
        if analyzer.target is not None:
            # 模型选择
            model_type = st.selectbox(
                "选择模型类型",
                ['random_forest', 'gradient_boosting', 'logistic_regression', 'xgboost', 'lightgbm', 'catboost'],
                format_func=lambda x: {
                    'random_forest': '随机森林',
                    'gradient_boosting': '梯度提升',
                    'logistic_regression': '逻辑回归',
                    'xgboost': 'XGBoost',
                    'lightgbm': 'LightGBM',
                    'catboost': 'CatBoost'
                }[x]
            )
            
            test_size = st.slider("测试集比例", 0.1, 0.5, 0.2, 0.05)
            
            if st.button("训练模型", type="primary"):
                with st.spinner("正在训练模型..."):
                    success, message = analyzer.train_model(model_type, test_size)
                    
                    if success:
                        st.success(message)
                        st.session_state.model_trained = True
                        
                        # 显示模型性能指标
                        if analyzer.model is not None:
                            st.subheader("模型性能")
                            
                            # 这里可以添加更多的模型评估指标
                            st.info(f"模型类型: {model_type}")
                            st.info(f"测试集比例: {test_size}")
                            
                    else:
                        st.error(message)
        else:
            st.warning("请先创建目标变量")
    else:
        st.info("请先完成特征工程和目标变量创建")

with tab4:
    st.header("策略分析")
    
    if hasattr(st.session_state, 'model_trained') and st.session_state.model_trained:
        analyzer = st.session_state.analyzer
        
        if analyzer.model is not None and analyzer.target is not None:
            # 策略预测
            st.subheader("实时策略预测")
            
            if st.button("生成交易策略", type="primary"):
                with st.spinner("正在分析..."):
                    success, result = analyzer.predict_strategy(analyzer.target)
                    
                    if success:
                        # 显示策略结果
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.metric("操作建议", result['action'])
                        
                        with col2:
                            st.metric("当前价格", f"{result['current_price']:.2f}")
                        
                        with col3:
                            st.metric("成功率", f"{result['success_rate']:.1f}%")
                        
                        with col4:
                            st.metric("盈亏比", f"{result['profit_loss_ratio']:.2f}")
                        
                        # 详细策略信息
                        st.subheader("详细策略信息")
                        
                        if result['action'] != "持有":
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.info(f"**止损价格**: {result['stop_loss']:.2f}")
                            
                            with col2:
                                st.info(f"**止盈价格**: {result['take_profit']:.2f}")
                            
                            # 风险收益分析
                            st.subheader("风险收益分析")
                            
                            if result['profit_loss_ratio'] > 0:
                                risk_reward_color = "green" if result['profit_loss_ratio'] > 2 else "orange"
                                st.markdown(f"""
                                <div style="color: {risk_reward_color}; font-size: 1.2em;">
                                    <strong>风险收益比: {result['profit_loss_ratio']:.2f}</strong>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                if result['profit_loss_ratio'] > 2:
                                    st.success("✅ 优秀的风险收益比，建议执行交易")
                                elif result['profit_loss_ratio'] > 1.5:
                                    st.warning("⚠️ 风险收益比一般，谨慎考虑")
                                else:
                                    st.error("❌ 风险收益比偏低，不建议交易")
                            
                            # 成功率分析
                            if result['success_rate'] > 70:
                                st.success(f"✅ 高成功率 ({result['success_rate']:.1f}%)，建议执行")
                            elif result['success_rate'] > 50:
                                st.warning(f"⚠️ 中等成功率 ({result['success_rate']:.1f}%)，谨慎考虑")
                            else:
                                st.error(f"❌ 低成功率 ({result['success_rate']:.1f}%)，不建议执行")
                        else:
                            st.info("当前市场条件不适合交易，建议持有观望")
                        
                        # 预测概率分布
                        st.subheader("预测概率分布")
                        prob_df = pd.DataFrame({
                            '操作': ['做空', '持有', '做多'],
                            '概率': result['probabilities']
                        })
                        
                        fig = px.bar(prob_df, x='操作', y='概率', title="模型预测概率")
                        st.plotly_chart(fig, use_container_width=True)
                        
                    else:
                        st.error(result)
            
            # 历史回测
            st.subheader("历史回测分析")
            
            if st.button("运行历史回测"):
                with st.spinner("正在回测..."):
                    # 这里可以添加历史回测逻辑
                    st.info("历史回测功能正在开发中...")
        else:
            st.warning("请先训练模型")
    else:
        st.info("请先完成模型训练")

# 页脚
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>期货交易策略分析系统 | 基于机器学习的智能交易决策支持</p>
    <p>⚠️ 免责声明：本系统仅供学习和研究使用，不构成投资建议。投资有风险，入市需谨慎。</p>
</div>
""", unsafe_allow_html=True)