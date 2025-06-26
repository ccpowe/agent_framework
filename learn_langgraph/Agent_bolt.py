from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import END, START, StateGraph
from typing import List, TypedDict
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()


class AgentState(TypedDict):
    messages: List[HumanMessage | AIMessage]


# 自定义llm
llm = ChatOpenAI(
    model=os.getenv("MODEL_NAME") or "gpt-3.5-turbo",
    api_key=os.getenv("OPENAI_API_KEY")
    or "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    base_url=os.getenv("MODEL_BASE_URL") or "https://openrouter.ai/api/v1",
)


def process(state: AgentState) -> AgentState:
    """this node will solve the request you input"""
    response = llm.invoke(state["messages"])# messages is chat history list
    print(response)
    state["messages"].append(AIMessage(content=response.content))# append ai response to chat history,eq to chat history.append(AIMessage(content=response.content))
    print(state["messages"])
    print(f"\nAI:{response.content}")# output ai response
    return state


graph = StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END)
agent = graph.compile()

chat_history = [] # 保存对话历史
with open("chat_history.txt", encoding="utf-8") as f:
    for line in f:
        if line.strip():
            if line.startswith("User:"):
                chat_history.append(HumanMessage(content=line[5:].strip()))# line[5:] is remove "User: "
            elif line.startswith("AI:"):
                chat_history.append(AIMessage(content=line[3:].strip()))# line[3:] is remove "AI: "
    
user_input = input("Enter: ")
while user_input != "exit":
    chat_history.append(HumanMessage(content=user_input))
    response = agent.invoke({"messages": chat_history})
    # chat_history.append(AIMessage(content=response["messages"][-1].content))# so this append AIMessage again,is errors
    # chat_history = response["messages"]
    print(chat_history)
    user_input = input("\nEnter: ")

with open("chat_history.txt", "w", encoding="utf-8") as f:
    for message in chat_history:
        if isinstance(message, HumanMessage):
            f.write(f"User: {message.content}\n\n")
        elif isinstance(message, AIMessage):
            f.write(f"AI: {message.content}\n\n")
        
print("chat_history.txt has been saved.")

history_for_json = []
for message in chat_history:
    if isinstance(message, HumanMessage):
        history_for_json.append({"role": "user", "content": message.content})
    elif isinstance(message, AIMessage):
        history_for_json.append({"role": "assistant", "content": message.content})

with open("chat_history.json", "w", encoding="utf-8") as f:
    json.dump(history_for_json, f, ensure_ascii=False, indent=2)
    
print("chat_history.json has been saved.")
