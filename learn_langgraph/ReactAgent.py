from langchain_core.messages import BaseMessage, SystemMessage # type: ignore
from langgraph.graph import END, START, StateGraph # type: ignore
from langgraph.graph.message import add_messages 
from typing import TypedDict, Annotated, Sequence # type: ignore
from langchain_core.tools import tool # type: ignore
from langchain_openai import ChatOpenAI # type: ignore
from langgraph.prebuilt import ToolNode # type: ignore
from dotenv import load_dotenv # type: ignore
import os

load_dotenv()


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


@tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    print("add:\n") 
    return a + b


@tool
def subtract(a: int, b: int) -> int:
    """Subtract two numbers."""
    return a - b


tools = [add, subtract]

llm = ChatOpenAI(
    model=os.getenv("MODEL_NAME") or "gpt-3.5-turbo",
    api_key=os.getenv("OPENAI_API_KEY")
    or "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    base_url=os.getenv("MODEL_BASE_URL") or "https://openrouter.ai/api/v1",
).bind_tools(tools)


def react_agent(state: AgentState) -> AgentState:
    """this node will solve the request you input"""
    system_prompt = SystemMessage(
        content="You are a helpful assistant that can use tools."
    )
    response = llm.invoke([system_prompt]+state["messages"])
    return {"messages": [response]}


def loop_node(state: AgentState) -> str:
    """this node will loop until the request is solved"""
    print("loop_node:\n")
    print(state["messages"])
    if not state["messages"][-1].tool_calls:
        return "end"
    else:
        return "tool_node"


graph = StateGraph(AgentState)
graph.add_node("react_agent", react_agent)

tool_node = ToolNode(tools)
graph.add_node("tool_node", tool_node)

graph.add_edge(START, "react_agent")
graph.add_conditional_edges(
    "react_agent", loop_node, {"end": END, "tool_node": "tool_node"}
)
graph.add_edge("tool_node", "react_agent")

app = graph.compile()

def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()

inputs = {"messages": [("user", "Add 40 + 12 . Also tell me a joke please.")]}
print_stream(app.stream(inputs, stream_mode="values"))