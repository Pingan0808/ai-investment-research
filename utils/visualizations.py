"""
图表渲染组件

使用 Plotly 生成交互式图表
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Dict


def render_stock_chart(stock_data: pd.DataFrame, ticker: str) -> go.Figure:
    """渲染股票K线图"""
    fig = go.Figure(data=[go.Candlestick(
        x=stock_data['date'],
        open=stock_data['open'],
        high=stock_data['high'],
        low=stock_data['low'],
        close=stock_data['close'],
        name='K线'
    )])

    fig.update_layout(
        title=f'{ticker} 股价走势',
        yaxis_title='价格',
        xaxis_title='日期',
        template='plotly_white',
        height=400
    )

    return fig


def render_financial_charts(financials: Dict[str, pd.DataFrame]) -> go.Figure:
    """渲染财务图表"""
    income = financials['income_statement']

    years = ['2021', '2022', '2023', '2024']
    revenue = [income[y].iloc[0] for y in years]
    profit = [income[y].iloc[-1] for y in years]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=years, y=revenue, name='营业收入', marker_color='#1f77b4'))
    fig.add_trace(go.Scatter(
        x=years, y=profit, name='净利润',
        mode='lines+markers', 
        line=dict(color='#ff7f0e', width=3),
        yaxis='y2'
    ))

    fig.update_layout(
        title='营收与利润趋势',
        yaxis_title='营业收入 (万元)',
        yaxis2=dict(title='净利润 (万元)', overlaying='y', side='right'),
        template='plotly_white',
        height=350,
        legend=dict(orientation='h', yanchor='bottom', y=1.02)
    )

    return fig


def render_peer_comparison(peers: pd.DataFrame) -> go.Figure:
    """渲染同业对比雷达图"""
    categories = ['ROE(%)', '毛利率(%)', '营收增速(%)', '研发占比(%)']

    fig = go.Figure()
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

    for idx, row in peers.iterrows():
        values = [row[cat] for cat in categories]
        values += [values[0]]  # 闭合

        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories + [categories[0]],
            fill='toself',
            name=row['公司'],
            line_color=colors[idx % len(colors)]
        ))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 50])),
        showlegend=True,
        title='同行业关键指标对比',
        height=400
    )

    return fig


def render_sentiment_gauge(score: float) -> go.Figure:
    """渲染情感仪表盘"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "市场情绪指数"},
        gauge={
            'axis': {'range': [-1, 1]},
            'bar': {'color': "#1f77b4"},
            'steps': [
                {'range': [-1, -0.3], 'color': "#ffcccc"},
                {'range': [-0.3, 0.3], 'color': "#ffffcc"},
                {'range': [0.3, 1], 'color': "#ccffcc"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': score
            }
        }
    ))

    fig.update_layout(height=300)
    return fig
