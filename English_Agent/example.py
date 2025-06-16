import os
import asyncio
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.openai import OpenAILike
from agno.team.team import Team
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.reasoning import ReasoningTools
from agno.tools.yfinance import YFinanceTools
from agno.tools.mcp import MultiMCPTools # 导入 MultiMCPTools

# 加载环境变量
load_dotenv()

# 主异步函数
async def main():
    """
    演示如何构建一个使用外部MCP工具和内置工具的多智能体团队。
    """
    # 1. 使用 async with 统一管理所有外部 MCP 工具
    #    所有需要这些工具的操作都必须在这个代码块内完成
    async with MultiMCPTools(
        [
            "npx -y firecrawl-mcp"  # 启动 firecrawl 工具
        ],
        env={"FIRECRAWL_API_KEY": os.getenv("FIRECRAWL_API_KEY")},
        timeout_seconds=60
    ) as mcp_tools:
        # 2. 在 with 块内部定义你的 Agent
        #    这个 Agent 现在可以使用 firecrawl 和 DuckDuckGo
        web_research_agent = Agent(
            name="Web Research Agent",
            role="使用网络爬虫和搜索引擎处理网页抓取和综合研究请求",
            model=OpenAILike(id=os.getenv("MODEL_NAME"), api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("MODEL_BASE_URL")),
            # 3. 将 mcp_tools 和其他内置工具一起传给 Agent
            tools=[mcp_tools, DuckDuckGoTools()],
            instructions="优先使用 firecrawl 爬取具体网址。如果只是泛泛的搜索，则使用 DuckDuckGo。总是要包含信息来源。",
            add_datetime_to_instructions=True,
        )

        # 这个 Agent 专注于金融数据
        finance_agent = Agent(
            name="Finance Agent",
            role="处理金融数据请求和市场分析",
            model=OpenAILike(id=os.getenv("MODEL_NAME"), api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("MODEL_BASE_URL")),
            tools=[YFinanceTools(stock_price=True, stock_fundamentals=True, analyst_recommendations=True, company_info=True)],
            instructions=[
                "使用表格展示股价、基本面（市盈率、市值）和分析师建议。",
                "清晰地标出公司名称和股票代码。",
            ],
            add_datetime_to_instructions=True,
        )

        # 4. 在 with 块内部定义你的 Team
        reasoning_finance_team = Team(
            name="Reasoning Finance Team",
            mode="coordinate",
            model=OpenAILike(id=os.getenv("MODEL_NAME"), api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("MODEL_BASE_URL")),
            members=[web_research_agent, finance_agent], # 使用我们刚刚定义的 Agent
            tools=[ReasoningTools(add_instructions=True)],
            instructions=[
                "协作提供全面的金融和投资见解。",
                "综合基本面分析和市场情绪。",
                "只输出最终的综合分析，而不是单个智能体的回应。",
            ],
            markdown=True,
            show_members_responses=True,
            add_datetime_to_instructions=True,
        )

        # 5. 在 with 块内部运行你的 Team
        #    这里的调用会触发整个团队协作流程
        print("--- 团队开始执行任务 ---")
        await reasoning_finance_team.aprint_response(
            """
            对比分析一下特斯拉(TSLA)和英伟达(NVDA)的投资价值:
            1. 从雅虎财经获取两家公司的核心财务数据。
            2. 使用网页爬虫和搜索，查找并总结最近影响这两家公司股价的重大新闻。
            3. 综合以上信息，给出一个投资建议。
            """,
            stream=True,
            show_full_reasoning=True,
            stream_intermediate_steps=True,
        )
        print("\n--- 团队任务执行完毕 ---")


# 运行主函数
if __name__ == "__main__":
    asyncio.run(main())
