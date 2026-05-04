"""
模拟数据生成器

用于生成演示用的财务和市场数据。
实际生产环境可替换为真实 API 数据源。
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List


class DataGenerator:
    """生成模拟的财务和市场数据"""

    @staticmethod
    def generate_stock_data(ticker: str, days: int = 252) -> pd.DataFrame:
        """生成股票历史数据"""
        np.random.seed(hash(ticker) % 2**32)
        dates = pd.date_range(end=datetime.now(), periods=days, freq='B')

        # 生成随机游走价格
        returns = np.random.normal(0.0005, 0.02, days)
        price = 100 * np.exp(np.cumsum(returns))
        volume = np.random.lognormal(15, 0.5, days)

        df = pd.DataFrame({
            'date': dates,
            'open': price * (1 + np.random.normal(0, 0.01, days)),
            'high': price * (1 + abs(np.random.normal(0, 0.02, days))),
            'low': price * (1 - abs(np.random.normal(0, 0.02, days))),
            'close': price,
            'volume': volume.astype(int)
        })
        return df

    @staticmethod
    def generate_financial_statements(ticker: str) -> Dict[str, pd.DataFrame]:
        """生成模拟财务报表"""
        np.random.seed(hash(ticker) % 2**32)

        years = ['2021', '2022', '2023', '2024']

        # 资产负债表
        balance_sheet = pd.DataFrame({
            '科目': ['货币资金', '应收账款', '存货', '流动资产合计', '固定资产', 
                    '无形资产', '资产总计', '短期借款', '应付账款', '流动负债合计', 
                    '长期借款', '负债合计', '股东权益合计'],
            '2021': [5000, 3000, 2000, 12000, 8000, 2000, 25000, 2000, 3000, 8000, 5000, 15000, 10000],
            '2022': [5500, 3500, 2200, 13500, 8500, 2200, 27000, 1800, 3200, 8500, 4800, 15200, 11800],
            '2023': [4800, 4000, 2500, 14000, 9000, 2500, 28500, 2200, 3500, 9000, 4500, 15500, 13000],
            '2024': [6000, 3800, 2300, 14500, 9200, 2800, 30000, 1500, 3800, 8800, 4200, 15000, 15000]
        })

        # 利润表
        income_statement = pd.DataFrame({
            '科目': ['营业收入', '营业成本', '毛利润', '销售费用', '管理费用', 
                    '研发费用', '营业利润', '净利润'],
            '2021': [20000, 12000, 8000, 2000, 1500, 1000, 2500, 2000],
            '2022': [22000, 13200, 8800, 2200, 1600, 1200, 2800, 2240],
            '2023': [25000, 15500, 9500, 2500, 1800, 1500, 2700, 2160],
            '2024': [28000, 16800, 11200, 2800, 2000, 1800, 3600, 2880]
        })

        # 现金流量表
        cash_flow = pd.DataFrame({
            '科目': ['经营活动现金流', '投资活动现金流', '筹资活动现金流', '现金净增加额'],
            '2021': [3000, -1500, -500, 1000],
            '2022': [3500, -2000, -800, 700],
            '2023': [2800, -1800, -300, 700],
            '2024': [4000, -2200, -500, 1300]
        })

        return {
            'balance_sheet': balance_sheet,
            'income_statement': income_statement,
            'cash_flow': cash_flow
        }

    @staticmethod
    def generate_news_sentiment(ticker: str) -> List[Dict]:
        """生成模拟新闻舆情"""
        news_templates = [
            {"title": f"{ticker}发布Q3财报，营收超预期增长15%", "sentiment": "positive", "source": "财经网"},
            {"title": f"{ticker}宣布新一轮股权激励计划", "sentiment": "positive", "source": "证券时报"},
            {"title": f"行业分析：{ticker}所在赛道竞争加剧", "sentiment": "neutral", "source": "券商研报"},
            {"title": f"{ticker}核心产品通过欧盟认证", "sentiment": "positive", "source": "产业新闻"},
            {"title": f"大宗交易：{ticker}出现折价成交", "sentiment": "negative", "source": "交易所公告"},
            {"title": f"{ticker}与头部客户签订战略合作协议", "sentiment": "positive", "source": "公司公告"},
            {"title": f"原材料价格上涨或对{ticker}毛利率产生压力", "sentiment": "negative", "source": "行业观察"},
            {"title": f"{ticker}研发投入占比持续提升", "sentiment": "positive", "source": "科技媒体"}
        ]

        np.random.seed(hash(ticker) % 2**32)
        selected = np.random.choice(len(news_templates), size=5, replace=False)
        news = []
        for idx in selected:
            item = news_templates[idx].copy()
            item['date'] = (datetime.now() - timedelta(days=int(np.random.randint(1, 30)))).strftime('%Y-%m-%d')
            item['heat'] = int(np.random.randint(100, 10000))
            news.append(item)

        return sorted(news, key=lambda x: x['date'], reverse=True)

    @staticmethod
    def generate_peer_comparison(ticker: str) -> pd.DataFrame:
        """生成同行业对比数据"""
        peers = [ticker, '竞争对手A', '竞争对手B', '竞争对手C', '行业平均']

        np.random.seed(hash(ticker) % 2**32)
        base_roe = np.random.uniform(10, 20)
        base_pe = np.random.uniform(15, 30)

        data = {
            '公司': peers,
            'ROE(%)': [base_roe, base_roe-2, base_roe+1, base_roe-3, base_roe-1],
            'PE(倍)': [base_pe, base_pe+5, base_pe-3, base_pe+8, base_pe+2],
            '毛利率(%)': [35, 32, 38, 30, 33],
            '营收增速(%)': [20, 15, 25, 10, 17],
            '研发占比(%)': [8, 6, 10, 5, 7]
        }

        return pd.DataFrame(data)
