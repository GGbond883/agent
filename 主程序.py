from agents.manager import ManagerAgent
from agents.data_analyst import DataAnalystAgent
from agents.news_hunter import NewsHunterAgent
from agents.strategist import StrategistAgent
from agents.writer import WriterAgent
import json
from typing import Dict, Any


class MultiAgentSystem:
    """多智能体协作系统"""

    def __init__(self):
        self.manager = ManagerAgent()
        self.data_analyst = DataAnalystAgent()
        self.news_hunter = NewsHunterAgent()
        self.strategist = StrategistAgent()
        self.writer = WriterAgent()

    def run(self, query: str) -> Dict[str, Any]:
        """运行多智能体协作流程"""

        print(f"\n{'=' * 60}")
        print(f"🎯 开始研究任务: {query}")
        print(f"{'=' * 60}\n")

        # Step 1: 任务规划
        print("📋 [Manager] 正在规划任务...")
        plan = self.manager.execute({"query": query})
        print(f"   ✓ 任务规划完成\n")

        # Step 2: 并行执行数据收集和新闻搜索
        print("📊 [Data Analyst] 正在收集数据...")
        data_result = self.data_analyst.execute({"query": query})
        print(f"   ✓ 数据收集完成")

        print("📰 [News Hunter] 正在搜索新闻...")
        news_result = self.news_hunter.execute({"query": query})
        print(f"   ✓ 新闻搜索完成\n")

        # Step 3: 战略分析
        print("💡 [Strategist] 正在进行分析...")
        analysis_input = {
            "query": query,
            "data": data_result,
            "news": news_result.get("news", [])
        }
        analysis_result = self.strategist.execute(analysis_input)
        print(f"   ✓ 战略分析完成\n")

        # Step 4: 报告撰写
        print("✍️  [Writer] 正在撰写报告...")
        writing_input = {
            "query": query,
            "data": data_result,
            "news": news_result.get("news", []),
            "analysis": analysis_result.get("analysis", {})
        }
        final_report = self.writer.execute(writing_input)
        print(f"   ✓ 报告撰写完成\n")

        # Step 5: 整合结果
        results = [data_result, news_result, analysis_result, final_report]
        integrated = self.manager.integrate_results(results)

        print(f"{'=' * 60}")
        print("✅ 任务完成！")
        print(f"{'=' * 60}\n")

        return integrated

    def save_report(self, report_data: Dict, filename: str = "final_report.md"):
        """保存最终报告"""
        report_content = report_data.get("final_report", "")
        chart_path = report_data.get("chart_path", "")

        if report_content:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(report_content)
            print(f"📄 报告已保存至: {filename}")

        if chart_path:
            print(f"📊 图表已保存至: {chart_path}")


def main():
    """主函数"""

    # 初始化系统
    system = MultiAgentSystem()

    # 运行研究任务
    query = "新能源汽车市场2025年竞争格局与增长机会"

    try:
        result = system.run(query)

        # 保存报告
        system.save_report(result)

        # 打印报告预览
        print("\n📖 报告预览：\n")
        print(result.get("final_report", "")[:500] + "...\n")

    except Exception as e:
        print(f"❌ 系统运行出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()