from typing import Dict, Any, List
from agents.base_agent import BaseAgent


class ManagerAgent(BaseAgent):
    """总指挥：负责任务拆解、分发和整合"""

    def __init__(self):
        system_prompt = """你是研究团队的总指挥。你的职责：
        1. 理解用户的研究需求
        2. 拆解任务为：数据收集、新闻搜索、战略分析、报告撰写
        3. 协调各 Agent 工作，确保数据流转
        4. 整合最终输出

        你输出 JSON 格式，包含 task_plan 和 assigned_agent。
        """
        super().__init__(
            name="Manager",
            role="Orchestrator",
            system_prompt=system_prompt
        )

    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        user_query = input_data.get("query", "")

        # 任务拆解
        task_plan = self._decompose_task(user_query)

        return {
            "agent": self.name,
            "task_plan": task_plan,
            "query": user_query,
            "status": "plan_created"
        }

    def _decompose_task(self, query: str) -> List[Dict]:
        """使用 LLM 拆解任务"""
        prompt = f"""
        用户需求: {query}

        请将任务拆解为以下步骤，输出 JSON 数组：
        1. data_collection: 需要什么数据？（如销量、价格）
        2. news_search: 搜索关键词？
        3. analysis: 需要什么分析？（如SWOT）
        4. writing: 报告格式要求？
        """

        response = self.llm_call(prompt)
        # 简化版：手动解析
        # 实际使用中应使用 JSON 解析器
        return [
            {"step": "data_collection", "agent": "DataAnalyst", "query": f"{query} 数据"},
            {"step": "news_search", "agent": "NewsHunter", "query": f"{query} 新闻"},
            {"step": "analysis", "agent": "Strategist", "query": f"分析 {query}"},
            {"step": "writing", "agent": "Writer", "query": f"撰写 {query} 报告"}
        ]

    def integrate_results(self, results: List[Dict]) -> Dict:
        """整合所有 Agent 的结果"""
        integrated = {
            "data": None,
            "news": None,
            "analysis": None,
            "final_report": None
        }

        for result in results:
            agent_name = result.get("agent")
            if agent_name == "DataAnalyst":
                integrated["data"] = result.get("data")
            elif agent_name == "NewsHunter":
                integrated["news"] = result.get("news")
            elif agent_name == "Strategist":
                integrated["analysis"] = result.get("analysis")
            elif agent_name == "Writer":
                integrated["final_report"] = result.get("report")

        return integrated