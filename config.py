"""
期货交易策略分析系统配置文件
"""

# 数据配置
DATA_CONFIG = {
    'required_columns': ['date', 'contract', 'open', 'high', 'low', 'close', 'volume', 'open_interest'],
    'date_format': '%Y-%m-%d',
    'default_encoding': 'utf-8'
}

# 特征工程配置
FEATURE_CONFIG = {
    'moving_averages': [5, 10, 20, 50],
    'rsi_period': 14,
    'macd_fast': 12,
    'macd_slow': 26,
    'macd_signal': 9,
    'bb_period': 20,
    'bb_std': 2,
    'atr_period': 14,
    'adx_period': 14,
    'cci_period': 20,
    'volume_ma_period': 20,
    'volatility_period': 20
}

# 目标变量配置
TARGET_CONFIG = {
    'default_lookforward_days': 5,
    'default_profit_threshold': 0.02,  # 2%
    'default_loss_threshold': -0.01,   # -1%
    'target_mapping': {
        1: '做多',
        0: '持有',
        -1: '做空'
    }
}

# 机器学习模型配置
MODEL_CONFIG = {
    'random_forest': {
        'n_estimators': 100,
        'max_depth': None,
        'min_samples_split': 2,
        'min_samples_leaf': 1,
        'random_state': 42
    },
    'gradient_boosting': {
        'n_estimators': 100,
        'learning_rate': 0.1,
        'max_depth': 3,
        'random_state': 42
    },
    'logistic_regression': {
        'max_iter': 1000,
        'random_state': 42
    },
    'xgboost': {
        'n_estimators': 100,
        'learning_rate': 0.1,
        'max_depth': 3,
        'random_state': 42
    },
    'lightgbm': {
        'n_estimators': 100,
        'learning_rate': 0.1,
        'max_depth': 3,
        'random_state': 42
    },
    'catboost': {
        'iterations': 100,
        'learning_rate': 0.1,
        'depth': 3,
        'random_state': 42,
        'verbose': False
    }
}

# 策略配置
STRATEGY_CONFIG = {
    'atr_multiplier_stop_loss': 2.0,
    'atr_multiplier_take_profit': 3.0,
    'success_rate_thresholds': {
        'high': 70,      # 高成功率阈值
        'medium': 50     # 中等成功率阈值
    },
    'profit_loss_ratio_thresholds': {
        'excellent': 2.0,  # 优秀盈亏比阈值
        'good': 1.5        # 良好盈亏比阈值
    }
}

# 界面配置
UI_CONFIG = {
    'page_title': '期货交易策略分析系统',
    'page_icon': '📈',
    'layout': 'wide',
    'initial_sidebar_state': 'expanded',
    'max_upload_size': 200,  # MB
    'supported_file_types': ['csv']
}

# 可视化配置
VISUALIZATION_CONFIG = {
    'plot_height': 500,
    'color_scheme': {
        'primary': '#1f77b4',
        'success': '#2ca02c',
        'warning': '#ff7f0e',
        'danger': '#d62728',
        'info': '#17a2b8'
    },
    'chart_colors': [
        '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
        '#9467bd', '#8c564b', '#e377c2', '#7f7f7f'
    ]
}

# 风险控制配置
RISK_CONFIG = {
    'max_position_size': 0.1,  # 最大仓位比例
    'max_daily_loss': 0.05,    # 最大日亏损比例
    'max_drawdown': 0.2,       # 最大回撤比例
    'stop_loss_atr_multiplier': 2.0,
    'take_profit_atr_multiplier': 3.0
}

# 日志配置
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': 'futures_strategy.log'
}

# 性能配置
PERFORMANCE_CONFIG = {
    'max_data_rows': 100000,  # 最大数据行数
    'chunk_size': 1000,       # 数据处理块大小
    'cache_ttl': 3600,        # 缓存过期时间（秒）
    'parallel_processing': True
}

# 导出配置
EXPORT_CONFIG = {
    'supported_formats': ['csv', 'xlsx', 'json'],
    'default_format': 'csv',
    'include_timestamp': True,
    'compression': False
}

# 系统消息
MESSAGES = {
    'data_import_success': '数据导入成功！',
    'data_import_failed': '数据导入失败',
    'feature_creation_success': '特征创建成功！',
    'feature_creation_failed': '特征创建失败',
    'target_creation_success': '目标变量创建成功！',
    'target_creation_failed': '目标变量创建失败',
    'model_training_success': '模型训练成功！',
    'model_training_failed': '模型训练失败',
    'strategy_prediction_success': '策略预测成功！',
    'strategy_prediction_failed': '策略预测失败',
    'no_data_loaded': '请先加载数据',
    'no_features_created': '请先创建特征',
    'no_target_created': '请先创建目标变量',
    'no_model_trained': '请先训练模型'
}

# 错误代码
ERROR_CODES = {
    'MISSING_COLUMNS': 'E001',
    'INVALID_DATA_FORMAT': 'E002',
    'FEATURE_CREATION_ERROR': 'E003',
    'MODEL_TRAINING_ERROR': 'E004',
    'PREDICTION_ERROR': 'E005',
    'FILE_UPLOAD_ERROR': 'E006',
    'DATA_PROCESSING_ERROR': 'E007'
}