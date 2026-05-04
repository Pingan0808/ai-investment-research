"""
工具模块

包含：
- DataGenerator: 模拟数据生成器
- Visualizations: 图表渲染组件
"""

from .data_generator import DataGenerator
from .visualizations import (
    render_stock_chart,
    render_financial_charts,
    render_peer_comparison,
    render_sentiment_gauge
)

__all__ = [
    'DataGenerator',
    'render_stock_chart',
    'render_financial_charts',
    'render_peer_comparison',
    'render_sentiment_gauge'
]
