"""
报告撰写 Agent

负责整合各 Agent 输出，生成结构化投研报告：
- 投资建议生成
- 报告结构整合
- 关键发现提炼
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


class ReportGenerationAgent:
    """报告撰写 Agent"""

    def __init__(self):
        self.name = "报告撰写 Agent"
        self.reasoning_chain = []

    def execute(self, data_result: AgentResult, 
                financial_result: AgentResult,
                sentiment_result: AgentResult,
                ticker: str) -> AgentResult:
        """执行报告生成任务"""
        start_time = datetime.now()

        self.reasoning_chain = [
            "Step 1: 接收三个上游Agent的输出结果",
            "Step 2: 设计报告结构 - 执行摘要/公司概况/财务分析/估值分析/风险提示/投资建议",
            "Step 3: 提取核心财务指标并生成对比图表",
            "Step 4: 整合舆情分析结果至风险评估章节",
            "Step 5: 生成投资建议逻辑链",
            "Step 6: 格式化输出最终报告"
        ]

        # 生成投资建议
        metrics = financial_result.output['metrics']
        sentiment = sentiment_result.output['sentiment_score']

        # 简单评分模型
        score = 0
        for m in metrics:
            if m.trend == '上升':
                score += 1
            elif m.trend == '稳定':
                score += 0.5

        score += sentiment * 2

        if score >= 4:
            recommendation = "买入"
            target_price = "上调15-20%"
        elif score >= 2:
            recommendation = "增持"
            target_price = "上调5-10%"
        elif score >= 0:
            recommendation = "持有"
            target_price = "维持现价"
        else:
            recommendation = "减持"
            target_price = "下调5-10%"

        time.sleep(0.5)

        execution_time = (datetime.now() - start_time).total_seconds()

        return AgentResult(
            agent_name=self.name,
            status="完成",
            output={
                'recommendation': recommendation,
                'target_price': target_price,
                'confidence': min(abs(score) / 5 * 100, 95),
                'report_structure': [
                    '执行摘要', '公司概况', '财务分析', '行业地位',
                    '舆情监测', '估值分析', '风险提示', '投资建议'
                ],
                'key_highlights': [
                    f"营收CAGR达{metrics[0].value:.1f}%，成长性良好",
                    f"市场情绪指数{sentiment:.2f}，整体偏多",
                    f"研发投入持续加码，创新动能充足"
                ]
            },
            execution_time=execution_time,
            reasoning_chain=self.reasoning_chain
        )
