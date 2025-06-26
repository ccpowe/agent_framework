from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langgraph.graph import END, StateGraph
from typing import TypedDict, Annotated, Sequence
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from pydantic import SecretStr

load_dotenv()

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], lambda x, y: x + y]
    original_text: str
    corrected_text: str
    check_result: str
    is_approved: bool

llm = ChatOpenAI(
    model=os.getenv("MODEL_NAME") or "gpt-4-turbo",
    api_key=SecretStr(os.getenv("OPENAI_API_KEY") or "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"),
    base_url=os.getenv("MODEL_BASE_URL") or "https://openrouter.ai/api/v1",
)

def spelling_grammar_agent(state: AgentState) -> AgentState:
    """Agent 1: Fixes only spelling and basic grammar using [correction] tags."""
    
    text_to_correct = state["original_text"]
    
    system_prompt = """You are a specialized English correction agent. Your ONLY job is to fix spelling and basic grammatical errors (like subject-verb agreement, plurals, and articles).
    
    - Use ONLY the `word[correction]` format.
    - Do NOT add, remove, or change punctuation.
    - Do NOT change sentence structure.
    - Do NOT correct capitalization.
    - Focus exclusively on single-word corrections.
    """
    
    prompt = f"""Please correct the spelling and grammar in the following text using only `word[correction]` markup:\n\n{text_to_correct}
    """
    
    response = llm.invoke([SystemMessage(content=system_prompt), HumanMessage(content=prompt)])
    corrected_text = str(response.content).strip()
    
    return {**state, "corrected_text": corrected_text}

def capitalization_agent(state: AgentState) -> AgentState:
    """Agent 2: Fixes capitalization."""
    
    text_to_correct = state["corrected_text"]
    
    system_prompt = """You are a specialized English capitalization agent. Your ONLY job is to fix capitalization errors.
    
    - Use ONLY the `word[Correction]` format.
    - Do NOT change any words, spelling, grammar, or punctuation.
    - Preserve all existing `[correction]` tags exactly as they are.
    """
    
    prompt = f"""The following text has been corrected for spelling and grammar. Please fix the capitalization using only `word[Correction]` markup:\n\n{text_to_correct}
    """
    
    response = llm.invoke([SystemMessage(content=system_prompt), HumanMessage(content=prompt)])
    corrected_text = str(response.content).strip()
    
    return {**state, "corrected_text": corrected_text}

def punctuation_agent(state: AgentState) -> AgentState:
    """Agent 3: Takes text with grammar and capitalization corrections and adds/fixes punctuation using <correction> tags."""
    
    text_to_correct = state["corrected_text"]
    
    system_prompt = """You are a specialized English punctuation agent. Your ONLY job is to add or correct punctuation.
    
    - Use ONLY the `<.>`, `<?>`, `<,>`, etc. tags.
    - Do NOT change any words or their corrections.
    - Preserve all existing `[correction]` tags exactly as they are.
    """
    
    prompt = f"""The following text has already been corrected for spelling, grammar, and capitalization. Please add or fix the punctuation using only `<tag>` markup:\n\n{text_to_correct}
    """
    
    response = llm.invoke([SystemMessage(content=system_prompt), HumanMessage(content=prompt)])
    corrected_text = str(response.content).strip()
    
    return {**state, "corrected_text": corrected_text}

def structural_agent(state: AgentState) -> AgentState:
    """Agent 4: Takes fully punctuated text and checks for structural issues, applying {correction} if needed."""
    
    text_to_correct = state["corrected_text"]
    
    system_prompt = """You are a specialized English structural editor. Your ONLY job is to identify and fix deep sentence structure problems (like dangling modifiers or run-on sentences).
    
    - If a structural problem exists, rewrite the entire sentence using `{The corrected sentence.}`.
    - If the structure is already okay, output the text exactly as you received it.
    - Do NOT change any existing `[]` or `<>` tags if you are not applying a structural fix.
    """
    
    prompt = f"""The following text has been corrected for grammar and punctuation. Review it for structural errors. If you find any, rewrite the sentence using {{...}}. Otherwise, return the text unchanged.\n\n{text_to_correct}
    """
    
    response = llm.invoke([SystemMessage(content=system_prompt), HumanMessage(content=prompt)])
    response_text = str(response.content).strip()
    
    # If the agent didn't suggest a structural change, it might just return the text.
    # We only want to update if a {} correction is present.
    if '{' in response_text and '}' in response_text:
        return {**state, "corrected_text": response_text}
    else:
        # Otherwise, keep the text from the previous step
        return {**state, "corrected_text": text_to_correct}

def final_check_agent(state: AgentState) -> AgentState:
    """Final Check Agent: Verifies the final output from the assembly line."""
    
    check_prompt = """You are a **Rule Verifier**. Your only goal is to determine if the `corrected_text` is a valid and accurate correction of the `original_text` according to the rules.\n\n**PRIMARY DIRECTIVE: You MUST approve any correction that is accurate.** Do not be overly strict. If the corrected text fixes the errors from the original text using the allowed markup, it is correct.\n\n**Verification Steps:**\n1.  **Check for Accuracy:** Does the `corrected_text` correctly fix all the grammatical, spelling, and punctuation errors from the `original_text`?\n2.  **Check for Valid Markup:** Are all corrections made using only the allowed formats (`word[correction]`, `<.>`, `<?>`, `{sentence}`) and without any mistakes?\n3.  **Check for Over-Correction:** Were any unnecessary changes made to words that were already correct?\n\n**Decision Logic:**\n- If the answer to all three questions above is YES, you **MUST** respond with "APPROVED: [brief reason why it's correct]".\n- If the answer to any question is NO, you **MUST** respond with "REJECTED: [specific, actionable reason]""" 
    
    original_text = state["original_text"]
    corrected_text = state["corrected_text"]
    
    user_message = HumanMessage(content=f"""Evaluate this correction:\n\nOriginal text: {original_text}\nCorrected text: {corrected_text}\n\nProvide a simple APPROVED or REJECTED response based on the rules.\n""")
    
    system_prompt = SystemMessage(content=check_prompt)
    
    response = llm.invoke([system_prompt, user_message])
    check_result = str(response.content).strip()
    
    is_approved = "APPROVED" in check_result
    
    return {
        **state,
        "messages": [response],
        "check_result": check_result,
        "is_approved": is_approved
    }

def create_english_correction_graph():
    """Creates the multi-agent "assembly line" workflow."""
    
    workflow = StateGraph(AgentState)
    
    # Add the new specialized agent nodes
    workflow.add_node("spelling_grammar_agent", spelling_grammar_agent)
    workflow.add_node("capitalization_agent", capitalization_agent)
    workflow.add_node("punctuation_agent", punctuation_agent)
    workflow.add_node("structural_agent", structural_agent)
    workflow.add_node("final_check_agent", final_check_agent)
    
    # Set the entry point
    workflow.set_entry_point("spelling_grammar_agent")
    
    # Define the linear flow of the assembly line
    workflow.add_edge("spelling_grammar_agent", "capitalization_agent")
    workflow.add_edge("capitalization_agent", "punctuation_agent")
    workflow.add_edge("punctuation_agent", "structural_agent")
    workflow.add_edge("structural_agent", "final_check_agent")
    
    # The check agent is the final step, so it leads to the end.
    workflow.add_edge("final_check_agent", END)
    
    app = workflow.compile()
    return app

def process_text(text: str, verbose: bool = True) -> dict:
    """处理文本的主函数"""
    
    initial_state = {
        "messages": [],
        "original_text": text,
        "corrected_text": text, # Start with original text
        "check_result": "",
        "is_approved": False
    }
    
    app = create_english_correction_graph()
    
    if verbose:
        print(f"🚀 开始处理文本: \"{text}\"")
        print("-" * 50)
    
    try:
        final_state = app.invoke(initial_state)
        
        result = {
            "original_text": final_state["original_text"],
            "corrected_text": final_state.get("corrected_text", ""),
            "check_result": final_state.get("check_result", ""),
            "approved": final_state.get("is_approved", False)
        }
        
        if verbose:
            print("-" * 50)
            print("🎉 处理完成!")
            print(f"📝 原始文本: {result['original_text']}")
            print(f"✏️  纠正文本: {result['corrected_text']}")
            print(f"🔍 检查结果: {result['check_result']}")
            print(f"✅ 是否通过: {'是' if result['approved'] else '否'}")
        
        return result
        
    except Exception as e:
        if verbose:
            print(f"❌ 处理过程中出现错误: {e}")
        raise e

if __name__ == "__main__":
    print("🔧 英语语法纠错系统 (v2.0 - Multi-Agent)")
    print("=" * 60)
    print("输入英文文本进行语法检查和纠错")
    print("输入 'exit' 或 'quit' 退出程序")
    print("=" * 60)
    
    while True:
        try:
            user_input = input("\n📝 请输入英文文本: ").strip()
            
            if user_input.lower() in ["exit", "quit", "退出"]:
                print("👋 感谢使用，再见！")
                break
            
            if not user_input:
                print("⚠️  请输入有效的文本")
                continue
            
            process_text(user_input)
            
        except KeyboardInterrupt:
            print("\n👋 感谢使用，再见！")
            break
        except Exception as e:
            print(f"❌ 处理过程中出现错误: {e}")
            continue