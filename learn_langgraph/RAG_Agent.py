from langchain_core.messages import BaseMessage, SystemMessage,HumanMessage,AIMessage
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from typing import TypedDict, Annotated, Sequence
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
import os

# --- 配置加载 ---
load_dotenv()

# --- LLM 和 Embeddings 初始化 ---
# 建议将敏感信息（如API Key）存储在环境变量中
llm = ChatOpenAI(
    model=os.getenv("MODEL_NAME", "gpt-3.5-turbo"),
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("MODEL_BASE_URL", "https://api.openai.com/v1"),
)

embeddings = OpenAIEmbeddings(
    model=os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002"),
    api_key=os.getenv("SILICONFLOW_API_KEY"), # 通常 embedding 和 chat 使用相同的 key
    base_url=os.getenv("SILICONFLOW_EMBEDDING_URL", "https://api.openai.com/v1"),
    # 注意：很多服务不允许在创建Embeddings时一次性处理大量文本
    # 我们将在下面处理这个问题
)

# --- PDF 处理 ---
pdf_path = r"D:\Code_vs\agent_framework\learn_langgraph\1706.03762v7.pdf" # 确认路径是正确的
loader = PyPDFLoader(pdf_path)
documents = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splitted_docs = text_splitter.split_documents(documents)
print(f"文档被分割成了 {len(splitted_docs)} 个块。")

# --- 向量数据库创建（分批处理） ---
print("正在创建向量存储...")
# 先初始化一个空的 Chroma 实例
vector_store = Chroma(
    persist_directory="chroma_db",
    embedding_function=embeddings,
    collection_name="pdf_collection",
)

# 定义批处理大小
batch_size = 32 # 根据API的限制来设置

# 分批添加文档
for i in range(0, len(splitted_docs), batch_size):
    batch = splitted_docs[i:i + batch_size]
    vector_store.add_documents(batch)
    print(f"已添加 {i + len(batch)} / {len(splitted_docs)} 个文档块。")

print("向量存储创建并持久化完成。")

# --- RAG检索器 ---
retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 5}
)

# --- 工具定义 ---
@tool
def search_pdf(query: str) -> str:
    """在PDF中搜索特定查询。"""
    print(f"正在使用检索器搜索: '{query}'")
    docs = retriever.get_relevant_documents(query)
    print("搜索完成。")
    return "\n".join([doc.page_content for doc in docs])

tools = [search_pdf]
llm_with_tools = llm.bind_tools(tools)

# --- Agent 状态定义 ---
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

# --- Agent 节点定义 ---
def should_continue(state: AgentState) -> str:
    """决定是继续调用工具还是结束。"""
    if isinstance(state, list): # 兼容旧版LangGraph的stream输出
        last_message = state[-1]['messages'][-1]
    else:
        last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "continue"
    else:
        return "end"

def call_model(state: AgentState) -> dict:
    """调用LLM的节点。"""
    messages = state['messages']
    # 添加系统提示，确保Agent知道它的能力
    system_prompt = SystemMessage(
        content="You are a helpful assistant that can use tools to retrieve information from the PDF."
    )
    # 调用绑定了工具的LLM
    response = llm_with_tools.invoke([system_prompt] + list(messages))
    chat_history.append(response)
    return {"messages": [response]}

# --- Graph 构建 ---
workflow = StateGraph(AgentState)

workflow.add_node("agent", call_model)
tool_node = ToolNode(tools)
workflow.add_node("tools", tool_node)

workflow.set_entry_point("agent")

workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "continue": "tools",
        "end": END,
    },
)

workflow.add_edge("tools", "agent")

app = workflow.compile()

# --- 聊天历史 ---
chat_history = []

# --- 执行和输出 ---

def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()
inputs = input("\nYou: ")
while inputs.lower() not in ['exit', 'quit', '退出']:
    chat_history.append(HumanMessage(content=inputs))
    print_stream(app.stream({"messages": chat_history}, stream_mode="values"))
    inputs = input("\nYou: ")

