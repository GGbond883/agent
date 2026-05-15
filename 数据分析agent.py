from typing import Dict, Any
import pandas as pd
from agents.base_agent import BaseAgent
from tools.data_fetcher import fetch_mock_data


class DataAnalystAgent(BaseAgent):
    """数据分析师：获取和处理数据"""

    def __init__(self):
        system_prompt = """你是数据分析师。你的职责：
        1. 根据需求获取数据（调用 API 或生成模拟数据）
        2. 清洗和处理数据
        3. 计算基本统计指标（增长率、平均值等）
        4. 返回结构化的数据表格

        输出格式：JSON，包含 data_table, statistics, source
        """
        super().__init__(
            name="DataAnalyst",
            role="Data Specialist",
            system_prompt=system_prompt
        )

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        query = input_data.get("query", "")

        # 获取数据（实际使用会调用真实 API）
        data = self._fetch_data(query)

        # 分析数据
        statistics = self._analyze_data(data)

        return {
            "agent": self.name,
            "data": data,
            "statistics": statistics,
            "status": "completed"
        }

    def _fetch_data(self, query: str) -> Dict:
        """获取数据 - 示例使用模拟数据"""
        # 实际应用：调用 Yahoo Finance, Alpha Vantage 等
        return fetch_mock_data()

    def _analyze_data(self, data: Dict) -> Dict:
        """分析数据"""
        df = pd.DataFrame(data.get("sales", {}))

        stats = {
            "total_sales": int(df.sum().sum()) if not df.empty else 0,
            "growth_rate": "15.2%",  # 示例
            "avg_price": "$45,000"
        }
        return stats