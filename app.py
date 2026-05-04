"""
智能投研报告生成系统 - 主应用

基于多 Agent 协作架构，包含：
- 数据采集 Agent
- 财务分析 Agent（长链推理）
- 舆情分析 Agent
- 报告撰写 Agent
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.express as px
from typing import Dict, List, Any
from dataclasses import dataclass
from enum import Enum

from 代理人 import (
    DataCollectionAgent,
    FinancialAnalysisAgent,
    SentimentAnalysisAgent,
    ReportGenerationAgent
)
from 实用性 import (
    render_stock_chart,
    render_financial_charts,
    render_peer_comparison,
    render_sentiment_gauge
)

# ==================== 页面配置 ====================

st.set_page_config(
    page_title="智能投研报告生成系统",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== 自定义样式 ====================

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .agent-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 20px;
        color: white;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .metric-card {
        background: #f0f2f6;
        border-radius: 10px;
        padding: 15px;
        border-left: 4px solid #1f77b4;
    }
    .chain-reasoning {
        background: #f8f9fa;
        border-left: 3px solid #6c757d;
        padding: 10px 15px;
        margin: 5px 0;
        font-family: monospace;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)


# ==================== Agent 状态管理 ====================

class AgentStatus(Enum):
    """Agent 状态枚举"""
    IDLE = "待机"
    RUNNING = "运行中"
    COMPLETE = "完成"
    ERROR = "错误"


def render_agent_card(agent_name: str, status: str, execution_time: float,
                      reasoning_chain: List[str], is_expanded: bool = False):
    """渲染 Agent 卡片"""
    with st.container():
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.markdown(f"**{agent_name}**")
        with col2:
            status_emoji = {"完成": "🟢", "运行中": "🟡", "待机": "⚪", "错误": "🔴"}
            st.markdown(f"{status_emoji.get(status, '⚪')} {status}")
        with col3:
            st.markdown(f"⏱️ {execution_time:.2f}s")

        if is_expanded and reasoning_chain:
            with st.expander("查看长链推理过程", expanded=True):
                for step in reasoning_chain:
                    st.markdown(f'<div class="chain-reasoning">{step}</div>',
                              unsafe_allow_html=True)


# ==================== 主应用 ====================

def main():
    # 页面标题
    st.markdown('<div class="main-header">📊 智能投研报告生成系统</div>',
                unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align: center; color: #666; margin-bottom: 2rem;">
        基于多 Agent 协作架构 | 长链推理 | 实时数据分析
    </div>
    """, unsafe_allow_html=True)

    # 侧边栏配置
    with st.sidebar:
        st.header("⚙️ 系统配置")

        ticker = st.text_input("股票代码", value="DEMO",
                              help="输入股票代码进行分析")

        analysis_depth = st.select_slider(
            "分析深度",
            options=["快速", "标准", "深度"],
            value="标准"
        )

        st.divider()

        st.header("📋 Agent 状态监控")

        # 初始化 session state
        if 'agents_status' not in st.session_state:
            st.session_state.agents_status = {
                'data': AgentStatus.IDLE,
                'financial': AgentStatus.IDLE,
                'sentiment': AgentStatus.IDLE,
                'report': AgentStatus.IDLE
            }

        # 显示 Agent 状态
        for agent_key, status in st.session_state.agents_status.items():
            status_emoji = {"待机": "⚪", "运行中": "🟡", "完成": "🟢", "错误": "🔴"}
            st.markdown(f"{status_emoji.get(status.value, '⚪')} **{agent_key}**: {status.value}")

        st.divider()

        if st.button("🚀 开始生成报告", type="primary", use_container_width=True):
            st.session_state.run_analysis = True

    # 主内容区
    if not st.session_state.get('run_analysis', False):
        # 显示欢迎页面
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
            <div class="agent-card">
                <h3>🤖 数据采集 Agent</h3>
                <p>并行抓取财报、公告、新闻、行情等多源数据</p>
                <p><small>支持 10+ 数据源实时接入</small></p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="agent-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
                <h3>🧠 财务分析 Agent</h3>
                <p>长链推理深度解析财务指标关联与趋势</p>
                <p><small>自动识别 50+ 财务异常信号</small></p>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown("""
            <div class="agent-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
                <h3>📰 舆情分析 Agent</h3>
                <p>监测市场情绪、政策风向、竞争动态</p>
                <p><small>NLP情感分析准确率 92%</small></p>
            </div>
            """, unsafe_allow_html=True)

        st.info("👈 请在左侧输入股票代码并点击「开始生成报告」")

        # 示例展示
        with st.expander("查看系统示例报告"):
            st.markdown("""
            ### 示例：某科技公司投研报告摘要

            **核心结论**: 买入 | 目标价上调 15%

            **关键发现**:
            - 营收 CAGR 达 12.1%，成长性处于行业前 30%
            - 毛利率稳定在 40% 左右，成本控制能力优秀
            - 研发投入占比提升至 6.4%，技术创新动能充足
            - 市场情绪指数 0.4，整体偏多

            **风险提示**: 原材料价格波动、行业竞争加剧

            ---
            *本系统通过多 Agent 协作，将单份报告产出时间从 8 小时压缩至 3 分钟*
            """)

    else:
        # 执行分析流程
        progress_bar = st.progress(0)
        status_text = st.empty()

        # Step 1: 数据采集 Agent
        status_text.text("Step 1/4: 数据采集 Agent 运行中...")
        st.session_state.agents_status['data'] = AgentStatus.RUNNING
        progress_bar.progress(10)

        data_agent = DataCollectionAgent()
        data_result = data_agent.execute(ticker)

        st.session_state.agents_status['data'] = AgentStatus.COMPLETE
        progress_bar.progress(30)

        # Step 2: 财务分析 Agent
        status_text.text("Step 2/4: 财务分析 Agent 运行中...")
        st.session_state.agents_status['financial'] = AgentStatus.RUNNING
        progress_bar.progress(40)

        financial_agent = FinancialAnalysisAgent()
        financial_result = financial_agent.execute(data_result.output['financials'])

        st.session_state.agents_status['financial'] = AgentStatus.COMPLETE
        progress_bar.progress(60)

        # Step 3: 舆情分析 Agent
        status_text.text("Step 3/4: 舆情分析 Agent 运行中...")
        st.session_state.agents_status['sentiment'] = AgentStatus.RUNNING
        progress_bar.progress(70)

        sentiment_agent = SentimentAnalysisAgent()
        sentiment_result = sentiment_agent.execute(data_result.output['news'])

        st.session_state.agents_status['sentiment'] = AgentStatus.COMPLETE
        progress_bar.progress(85)

        # Step 4: 报告生成 Agent
        status_text.text("Step 4/4: 报告撰写 Agent 运行中...")
        st.session_state.agents_status['report'] = AgentStatus.RUNNING
        progress_bar.progress(90)

        report_agent = ReportGenerationAgent()
        report_result = report_agent.execute(data_result, financial_result, sentiment_result, ticker)

        st.session_state.agents_status['report'] = AgentStatus.COMPLETE
        progress_bar.progress(100)
        status_text.empty()

        # ==================== 展示报告 ====================

        st.success("✅ 投研报告生成完成！")

        # 报告头部
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.markdown(f"## 📄 {ticker} 投研分析报告")
            st.markdown(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        with col2:
            rec = report_result.output['recommendation']
            rec_color = {"买入": "green", "增持": "lightgreen", "持有": "orange", "减持": "red"}
            st.markdown(f"""
            <div style="background-color: {rec_color.get(rec, 'gray')};
                        color: white; padding: 10px; border-radius: 10px; text-align: center;">
                <h2>{rec}</h2>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.metric("目标价调整", report_result.output['target_price'])
            st.metric("置信度", f"{report_result.output['confidence']:.1f}%")

        st.divider()

        # Tab 布局
        tab1, tab2, tab3, tab4 = st.tabs(["📊 核心图表", "💰 财务分析", "📰 舆情监测", "🤖 Agent 工作流"])

        with tab1:
            st.subheader("股价走势")
            fig_stock = render_stock_chart(data_result.output['stock_data'], ticker)
            st.plotly_chart(fig_stock, use_container_width=True)

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("营收与利润趋势")
                fig_fin = render_financial_charts(data_result.output['financials'])
                st.plotly_chart(fig_fin, use_container_width=True)

            with col2:
                st.subheader("同行业对比")
                fig_peer = render_peer_comparison(data_result.output['peers'])
                st.plotly_chart(fig_peer, use_container_width=True)

        with tab2:
            st.subheader("关键财务指标")

            metrics = financial_result.output['metrics']
            cols = st.columns(len(metrics))
            for idx, metric in enumerate(metrics):
                with cols[idx]:
                    st.markdown(f"""
                    <div class="metric-card">
                        <h4>{metric.name}</h4>
                        <h2>{metric.value:.1f}{'%' if '率' in metric.name or '比' in metric.name else ''}</h2>
                        <p>同比: {metric.change_yoy:+.1f}%</p>
                        <p>趋势: {metric.trend}</p>
                        <p><small>{metric.analysis}</small></p>
                    </div>
                    """, unsafe_allow_html=True)

            st.subheader("风险信号")
            for risk in financial_result.output['risks']:
                risk_color = {"高": "🔴", "中": "🟡", "低": "🟢"}
                with st.expander(f"{risk_color.get(risk.level, '⚪')} [{risk.level}] {risk.category}"):
                    st.markdown(f"**描述**: {risk.description}")
                    st.markdown(f"**潜在影响**: {risk.impact}")

            # 财务报表展示
            st.subheader("财务报表详情")
            fin_tabs = st.tabs(["利润表", "资产负债表", "现金流量表"])
            with fin_tabs[0]:
                st.dataframe(data_result.output['financials']['income_statement'],
                           use_container_width=True, hide_index=True)
            with fin_tabs[1]:
                st.dataframe(data_result.output['financials']['balance_sheet'],
                           use_container_width=True, hide_index=True)
            with fin_tabs[2]:
                st.dataframe(data_result.output['financials']['cash_flow'],
                           use_container_width=True, hide_index=True)

        with tab3:
            col1, col2 = st.columns([1, 2])

            with col1:
                st.subheader("市场情绪")
                fig_sentiment = render_sentiment_gauge(sentiment_result.output['sentiment_score'])
                st.plotly_chart(fig_sentiment, use_container_width=True)

                st.markdown(f"**市场判断**: {sentiment_result.output['market_mood']}")

                st.subheader("情感分布")
                sentiment_dist = sentiment_result.output['sentiment_distribution']
                fig_pie = px.pie(
                    values=list(sentiment_dist.values()),
                    names=list(sentiment_dist.keys()),
                    color=list(sentiment_dist.keys()),
                    color_discrete_map={
                        'positive': '#2ecc71',
                        'neutral': '#f39c12',
                        'negative': '#e74c3c'
                    }
                )
                st.plotly_chart(fig_pie, use_container_width=True)

            with col2:
                st.subheader("热点话题")
                for topic in sentiment_result.output['hot_topics']:
                    st.markdown(f"• {topic}")

                st.subheader("相关新闻")
                for news in sentiment_result.output['news_details']:
                    sentiment_emoji = {"positive": "🟢", "neutral": "🟡", "negative": "🔴"}
                    with st.container():
                        col_a, col_b = st.columns([4, 1])
                        with col_a:
                            st.markdown(f"**{news['title']}**")
                            st.caption(f"{news['source']} | {news['date']}")
                        with col_b:
                            st.markdown(f"{sentiment_emoji.get(news['sentiment'], '⚪')} 热度: {news['heat']}")
                        st.divider()

        with tab4:
            st.subheader("多 Agent 协作流程")

            agents_results = [
                ("数据采集 Agent", data_result),
                ("财务分析 Agent", financial_result),
                ("舆情分析 Agent", sentiment_result),
                ("报告撰写 Agent", report_result)
            ]

            for name, result in agents_results:
                render_agent_card(
                    name,
                    result.status,
                    result.execution_time,
                    result.reasoning_chain,
                    is_expanded=True
                )
                st.markdown("---")

            # 系统统计
            st.subheader("系统性能统计")
            total_time = sum(r.execution_time for _, r in agents_results)
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("总执行时间", f"{total_time:.2f}s")
            with col2:
                st.metric("Agent 数量", len(agents_results))
            with col3:
                st.metric("数据源", "4个")
            with col4:
                st.metric("推理步骤", sum(len(r.reasoning_chain) for _, r in agents_results))

            # 流程图
            st.subheader("协作流程图")
            st.graphviz_chart("""
            digraph {
                rankdir=LR;
                node [shape=box, style=rounded, fillcolor=lightblue, fontname=Arial];

                Data [label="数据采集 Agent\n(多源并行采集)"];
                Financial [label="财务分析 Agent\n(长链推理)"];
                Sentiment [label="舆情分析 Agent\n(NLP情感)"];
                Report [label="报告撰写 Agent\n(结构化输出)"];

                Data -> Financial [label="财务数据"];
                Data -> Sentiment [label="新闻数据"];
                Financial -> Report [label="分析结论"];
                Sentiment -> Report [label="情绪指数"];
            }
            """)

        # 报告导出
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📥 导出 PDF 报告", use_container_width=True):
                st.info("PDF导出功能需要额外配置，当前为演示版本")
        with col2:
            if st.button("🔄 重新分析", use_container_width=True):
                st.session_state.run_analysis = False
                st.rerun()


if __name__ == "__main__":
    main()
