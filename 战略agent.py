from typing import Dict, Any
from agents.base_agent import BaseAgent


class StrategistAgent(BaseAgent):
    """战略专家：基于数据提供分析洞察"""

    def __init__(self):
        system_prompt = """你是战略分析师。你的职责：
        1. 基于数据和新闻进行 SWOT 分析
        2. 提供竞争格局洞察
        3. 给出战略建议
        4. 必须引用数据来源，不能编造

        输出格式：JSON，包含 swot_analysis, recommendations, key_insights
        """
        super().__init__(
            name="Strategist",
            role="Business Strategist",
            system_prompt=system_prompt
        )

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        query = input_data.get("query", "")
        data = input_data.get("data", {})
        news = input_data.get("news", [])

        # 基于数据进行分析
        analysis = self._perform_analysis(query, data, news)

        return {
            "agent": self.name,
            "analysis": analysis,
            "status": "completed"
        }

    def _perform_analysis(self, query: str, data: Dict, news: list) -> Dict:
        """执行 SWOT 分析"""
        prompt = f"""
        基于以下信息进行分析：

        查询: {query}
        数据: {data}
        新闻: {news}

        请提供：
        1. SWOT 分析（优势、劣势、机会、威胁）
        2. 3个关键洞察
        3. 战略建议

        必须引用具体数据。
        """

        response = self.llm_call(prompt, temperature=0.5)

        # 简化版：返回结构化数据
        return {
            "swot": {
                "strengths": ["技术领先", "品牌认知度高"],
                "weaknesses": ["产能不足", "供应链依赖"],
                "opportunities": ["政策支持", "市场需求增长"],
                "threats": ["竞争加剧", "原材料涨价"]
            },
            "key_insights": [
                f"市场增长率达到{data.get('statistics', {}).get('growth_rate', '15%')}",
                "政策利好推动需求",
                "竞争格局正在重塑"
            ],
            "recommendations": [
                "扩大产能投资",
                "加强供应链多元化",
                "加大研发投入"
            ]
        }