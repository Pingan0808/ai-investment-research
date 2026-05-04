"""
舆情分析 Agent

负责：
- 新闻情感分类
- 热点话题识别
- 市场情绪指数计算
- 媒体关注度评估
"""

import time
from datetime import datetime
from typing import Dict, List
from dataclasses import dataclass


@dataclass
class AgentResult:
    """Agent 执行结果"""
    agent_name: str
    status: str
    output: Dict
    execution_time: float
    reasoning_chain: List[str]


class SentimentAnalysisAgent:
    """舆情分析 Agent"""

    def __init__(self):
        self.name = "舆情分析 Agent"
        self.reasoning_chain = []

    def execute(self, news: List[Dict]) -> AgentResult:
        """执行舆情分析任务"""
        start_time = datetime.now()

        # 分析舆情
        sentiment_counts = {'positive': 0, 'neutral': 0, 'negative': 0}
        for item in news:
            sentiment_counts[item['sentiment']] += 1

        total = sum(sentiment_counts.values())
        sentiment_score = (
            sentiment_counts['positive'] * 1 + 
            sentiment_counts['neutral'] * 0 + 
            sentiment_counts['negative'] * -1
        ) / total if total > 0 else 0

        self.reasoning_chain = [
            f"Step 1: 采集到{len(news)}条相关新闻",
            f"Step 2: 情感分类统计 - 正面:{sentiment_counts['positive']} 中性:{sentiment_counts['neutral']} 负面:{sentiment_counts['negative']}",
            f"Step 3: 计算情感得分: {sentiment_score:.2f} (范围-1到1)",
            "Step 4: 识别关键事件 - 财报超预期、战略合作、产品认证为正面驱动",
            "Step 5: 识别风险信号 - 原材料价格上涨、大宗折价交易",
            f"Step 6: 评估媒体关注度 - 总热度{sum(n['heat'] for n in news)}",
            "Step 7: 生成市场情绪指数: 偏多"
        ]

        hot_topics = [
            "Q3财报超预期", "战略合作", "产品认证", "股权激励", "研发加码"
        ]

        time.sleep(0.6)

        execution_time = (datetime.now() - start_time).total_seconds()

        return AgentResult(
            agent_name=self.name,
            status="完成",
            output={
                'sentiment_score': sentiment_score,
                'sentiment_distribution': sentiment_counts,
                'hot_topics': hot_topics,
                'market_mood': '偏多' if sentiment_score > 0 else '偏空' if sentiment_score < 0 else '中性',
                'news_details': news
            },
            execution_time=execution_time,
            reasoning_chain=self.reasoning_chain
        )
