from agno.agent import Agent
from agno.models.openai.like import OpenAILike
from agno.tools.mcp import MultiMCPTools
from agno.embedder.openai import OpenAIEmbedder
from agno.knowledge.markdown import MarkdownKnowledgeBase
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.memory.v2.memory import Memory
from agno.vectordb.lancedb import LanceDb, SearchType
from pathlib import Path # 建议使用 Path 对象处理路径
import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

knowledge = MarkdownKnowledgeBase(
    # urls=["https://docs.agno.com/introduction.md"],
    path=Path("./agno_introduction.md"), # 使用 Path 对象处理路径
    vector_db=LanceDb(
        uri="tmp/lancedb",
        table_name="agno_docs_markdown",
        search_type=SearchType.hybrid,
        embedder=OpenAIEmbedder(
            id="BAAI/bge-large-en-v1.5",
            api_key=os.getenv("SILICONFLOW_API_KEY"),
            base_url=os.getenv("SILICONFLOW_EMBEDDING_URL"),
            dimensions=1024, 
        )
    ),
)

memory = Memory(
    # Use any model for creating and managing memories
    model=OpenAILike(
        id=os.getenv("MODEL_NAME"),
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("MODEL_BASE_URL"),
    ),
    # Store memories in a SQLite database
    db=SqliteMemoryDb(table_name="user_memories", db_file="tmp/agent.db"),
    # We disable deletion by default, enable it if needed
    delete_memories=False,
    clear_memories=False,
)

# Store agent sessions in a SQLite database
# storage = SqliteStorage(table_name="agent_sessions", db_file="tmp/agent.db")

async def run_agent(message: str) -> None:

    """运行agent使用多种工具的官方示例"""
    env = {
        "FIRECRAWL_API_KEY": os.getenv("FIRECRAWL_API_KEY"),
    }

    async with MultiMCPTools(
        [
            "npx -y firecrawl-mcp"
        ],
        env=env,
        timeout_seconds=30
    ) as mcp_tools:
        agent = Agent(
            model=OpenAILike(
                id=os.getenv("MODEL_NAME"),
                api_key=os.getenv("OPENAI_API_KEY"),
                base_url=os.getenv("MODEL_BASE_URL"),
            ),
            tools=[mcp_tools],
            instructions="你可以使用firecrawl-mcp工具来爬取网页获取信息并为用户总结，或者根据你的知识库回答问题",
            markdown=True,
            show_tool_calls=True,
            knowledge=knowledge,
            # storage=storage,
            add_datetime_to_instructions=True,
            # Add the chat history to the messages
            add_history_to_messages=True,
            # Number of history runs
            num_history_runs=3,
            user_id="ava",
            memory=memory,
            # Let the Agent manage its memories
            enable_agentic_memory=True,
        )

        await agent.aprint_response(message, stream=True)

if __name__ == "__main__":
    print("Initializing knowledge base...")
    asyncio.run(knowledge.aload(recreate=False))
    asyncio.run(run_agent("What is Agno?"))
    asyncio.run(run_agent("我之前问过你什么问题"))
