from typing import Dict, Any
from agents.base_agent import BaseAgent
from tools.chart_generator import generate_chart
import json


class WriterAgent(BaseAgent):
    """报告作家：撰写最终报告和生成图表"""

    def __init__(self):
        system_prompt = """你是专业报告作家。你的职责：
        1. 整合数据、新闻和分析
        2. 撰写结构化的 Markdown 报告
        3. 生成可视化图表
        4. 确保逻辑连贯、数据准确

        报告结构：摘要、数据概览、市场情绪、深度分析、战略建议、风险提示
        """
        super().__init__(
            name="Writer",
            role="Report Writer",
            system_prompt=system_prompt
        )

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        query = input_data.get("query", "")
        data = input_data.get("data", {})
        news = input_data.get("news", [])
        analysis = input_data.get("analysis", {})

        # 生成图表
        chart_path = self._create_charts(data)

        # 撰写报告
        report = self._write_report(query, data, news, analysis, chart_path)

        return {
            "agent": self.name,
            "report": report,
            "chart_path": chart_path,
            "status": "completed"
        }

    def _create_charts(self, data: Dict) -> str:
        """生成数据图表"""
        sales_data = data.get("data", {}).get("sales", {})
        if sales_data:
            return generate_chart(sales_data)
        return ""

    def _write_report(self, query: str, data: Dict, news: list,
                      analysis: Dict, chart_path: str) -> str:
        """撰写最终报告"""

        report = f"""# {query} 深度研究报告

## 📊 执行摘要

基于多维度数据分析，本报告呈现 {query} 的最新市场格局和战略建议。

## 📈 数据概览

**关键指标：**
- 总销量：{data.get('statistics', {}).get('total_sales', 'N/A')}
- 增长率：{data.get('statistics', {}).get('growth_rate', 'N/A')}
- 平均价格：{data.get('statistics', {}).get('avg_price', 'N/A')}

{chr(10).join([f"![数据图表]({chart_path})" if chart_path else ""])}

## 📰 市场情绪分析

共分析 {len(news)} 条关键新闻：

{self._format_news(news)}

情感分布：{self._format_sentiment(news)}

## 🔍 深度战略分析

### SWOT 分析
{self._format_swot(analysis.get('analysis', {}).get('swot', {}))}

### 关键洞察
{self._format_insights(analysis.get('analysis', {}).get('key_insights', []))}

## 💡 战略建议

{self._format_recommendations(analysis.get('analysis', {}).get('recommendations', []))}

## ⚠️ 风险提示

1. 市场竞争加剧可能影响市场份额
2. 原材料价格波动风险
3. 政策变化的不确定性

---
*报告生成时间：2026年5月15日*
*数据来源：多智能体研究系统*
"""
        return report

    def _format_news(self, news: list) -> str:
        formatted = ""
        for item in news:
            formatted += f"- **{item.get('title')}** ({item.get('date')})\n"
            formatted += f"  {item.get('summary')} [来源：{item.get('source')}]\n"
        return formatted

    def _format_swot(self, swot: Dict) -> str:
        return f"""
| 维度 | 内容 |
|------|------|
| 优势 | {', '.join(swot.get('strengths', []))} |
| 劣势 | {', '.join(swot.get('weaknesses', []))} |
| 机会 | {', '.join(swot.get('opportunities', []))} |
| 威胁 | {', '.join(swot.get('threats', []))} |
"""

    def _format_insights(self, insights: list) -> str:
        return "\n".join([f"{i + 1}. {insight}" for i, insight in enumerate(insights)])

    def _format_recommendations(self, recs: list) -> str:
        return "\n".join([f"- {rec}" for rec in recs])

    def _format_sentiment(self, news: list) -> str:
        from collections import Counter
        sentiments = [item.get("sentiment", "neutral") for item in news]
        counts = Counter(sentiments)
        return f"正面：{counts['positive']} | 负面：{counts['negative']} | 中性：{counts['neutral']}"