from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from typing import TypedDict, Annotated, Sequence, Literal
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode
from dotenv import load_dotenv
import os
from pydantic import SecretStr

load_dotenv()

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    original_text: str  # 保存原始输入文本
    corrected_text: str  # 保存纠错后的文本
    check_result: str  # 保存检查结果
    iteration_count: int  # 迭代次数，防止无限循环
    is_approved: bool  # 是否通过检查

llm = ChatOpenAI(
    model=os.getenv("MODEL_NAME") or "gpt-3.5-turbo",
    api_key=SecretStr(os.getenv("OPENAI_API_KEY") or "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"),
    base_url=os.getenv("MODEL_BASE_URL") or "https://openrouter.ai/api/v1",
)

def english_agent(state: AgentState) -> AgentState:
    """英语语法纠错代理 - 根据严格的标记规则纠正文本"""
    
    # 获取要处理的文本
    if state.get("iteration_count", 0) == 0:
        # 第一次处理，使用原始文本
        text_to_correct = state["original_text"]
        user_message = HumanMessage(content=text_to_correct)
    else:
        # 后续处理，基于检查反馈重新纠正
        text_to_correct = state["original_text"]
        feedback = state.get("check_result", "")
        user_message = HumanMessage(content=f"""
Original text: {text_to_correct}
Previous correction: {state.get('corrected_text', '')}
Feedback from checker: {feedback}

Please correct the original text again, taking the feedback into account. Pay special attention to:
1. Adding missing punctuation with <.> <,> <?> tags
2. Proper capitalization for sentence beginnings
3. Exact formatting requirements
""")
    
    # 添加系统描述，与原始agent保持一致，并强调关键规则
    system_description = """You are a **Text Formatting Linter (Text-Formatting-Linter)**. Your only function is to receive input text and re-render it based on a set of absolute strict markup language rules. You are not a teacher, you are not an assistant, you are a **strictly rule-following machine**. Do not output any explanation, greeting, or comments unrelated to the rules.

**CRITICAL REMINDERS**:
- ALWAYS add <.> at the end if the sentence lacks proper ending punctuation
- ALWAYS use <?> when a question mark is needed but missing or incorrect
- ALWAYS correct capitalization for the first word of a sentence if it is lowercase: what -> what[What]
- ALWAYS follow the exact format: word[correction] for replacements
- NEVER leave sentences without proper ending punctuation"""
    
    system_prompt = SystemMessage(content=f"{system_description}\n\n{instructions}")
    
    response = llm.invoke([system_prompt, user_message])
    corrected_text = str(response.content).strip()
    
    return {
        **state,  # 保留所有现有状态
        "messages": [response],
        "corrected_text": corrected_text,
        "iteration_count": state.get("iteration_count", 0) + 1
    }

def check_agent(state: AgentState) -> AgentState:
    """检查代理 - 验证纠错结果是否符合标记规则要求"""
    
    corrected_text = state.get("corrected_text", "")
    original_text = state.get("original_text", "")
    
    check_prompt = """You are a **Rule Verifier**. Your only goal is to determine if the `corrected_text` is a valid and accurate correction of the `original_text` according to the rules.

**PRIMARY DIRECTIVE: You MUST approve any correction that is accurate.** Do not be overly strict. If the corrected text fixes the errors from the original text using the allowed markup, it is correct.

**Verification Steps:**
1.  **Check for Accuracy:** Does the `corrected_text` correctly fix all the grammatical, spelling, and punctuation errors from the `original_text`?
2.  **Check for Valid Markup:** Are all corrections made using only the allowed formats (`word[correction]`, `<.>`, `<?>`, `{sentence}`) and without any mistakes?
3.  **Check for Over-Correction:** Were any unnecessary changes made to words that were already correct? (e.g., changing "Hello" to "hello[Hello]")

**Decision Logic:**
- If the answer to all three questions above is YES, you **MUST** respond with "APPROVED: [brief reason why it's correct]".
- If the answer to any question is NO, you **MUST** respond with "REJECTED: [specific, actionable reason]". For example, "REJECTED: The word 'My' was already capitalized and should not have been changed.""""
    
    user_message = HumanMessage(content=f"""
Evaluate this correction with balanced assessment:

Original text: {original_text}
Corrected text: {corrected_text}

Please analyze:
1. Were there actual errors in the original text that needed correction?
2. If corrections were made, are they accurate and properly formatted?
3. If no corrections were made, was the original text already correct?
4. Are the markup tags used appropriately and accurately?

Provide a fair evaluation - approve good corrections and "✅ No errors found." responses.
""")
    
    system_prompt = SystemMessage(content=check_prompt)
    
    response = llm.invoke([system_prompt, user_message])
    check_result = str(response.content).strip()
    
    # 判断是否通过检查
    is_approved = check_result.startswith("APPROVED")
    
    return {
        **state,  # 保留所有现有状态
        "messages": [response],
        "check_result": check_result,
        "is_approved": is_approved
    }

instructions = """
### **Core Markup Language Definition**
You can only use the following three types of tags: `[correction]`, `<correction>`, `{correction}`.

### **Mandatory Processing Flow**
You must follow the three steps below in order to internally think and construct the final output.

**Step 1: Token-Level Scan -> Use `[]`**

1.  **Scan every word (token) one by one**, focusing on the following basic grammatical errors:

    **a) Spelling Error Check**:
    - `freind` -> `[friend]`, `libary` -> `[library]`, `imediately` -> `[immediately]`

    **b) Article Usage Errors (Emphasis)**:
    - `a amazing` -> `a[an] amazing` (Use "an" before a vowel sound)
    - `an book` -> `an[a] book` (Use "a" before a consonant sound)
    - Check if all uses of a/an are correct

    **c) Pluralization Errors (Emphasis)**:
    - `apple` (singular, but context requires plural) -> `apple[apples]`
    - `books` (plural, but context requires singular) -> `books[book]`
    - Irregular plurals like `mouse` -> `mouse[mice]`, `child` -> `child[children]`

    **d) Capitalization Errors (Emphasis)**:
    - Lowercase at the beginning of a sentence: `what` -> `what[What]`
    - Proper nouns: `china` -> `china[China]`
    - Names of people, places, etc.

    **e) Basic Grammar Replacements**:
    - **Subject-verb disagreement (Enhanced check)**: `is` -> `[are]`, `have` -> `[has]`, `suggest` -> `[suggests]`
    - **Pay special attention to collective nouns**: `data suggest` -> `data[data] suggest[suggests]`
    - **Long-distance subject-verb agreement**: Check subject-verb relationships across modifiers
    - Pronoun errors: `me` -> `[I]`, `him` -> `[he]`
    - Verb form: `dont` -> `[doesn't]`, `goed` -> `[went]`
    - Part-of-speech errors: `affect` -> `[effect]`, `its` -> `[it's]`
    - Subjunctive mood: `was` -> `[were]` (in conditional sentences)

2.  **Absolute Rules**:
    - There **must** be only one word inside `[]`.
    - `[]` is used to replace one **complete** input token.
    - **Forbidden**: `however[; however,]` (Error: more than one word inside)
    - **Forbidden**: `re['re]` (Error: `re` is not an independent token)
    - **Correct**: `dont[doesn't]` (Correct: replacing one token with another)

**Step 2: Structural Scan -> Use `{}`**

1.  After completing Step 1, review the entire sentence structure.

2.  **Only** when you encounter a deeper **structural problem** that **cannot** be fixed with the `[]` from Step 1, append `{the complete correct sentence}` at the end of the sentence.

3.  **Applicable Scenarios (Strictly Limited)**:
    - **Word order rearrangement**: `a car red` -> `a red car`
    - **Dangling modifiers**: `Published last month the report...` -> `{The report, published last month, details...}`
    - **Sentences that require adding or deleting multiple words to be correct**
    - **Severe sentence structure problems**, such as run-on sentences that need to be split.

4.  **Important Rules**:
    - If an error **can be** corrected by `[]` and **also seems** to be correctable by `{}`, you **must** choose `[]`.
    - `{}` is the last and only option.
    - **The content inside `{}` is a complete, correct sentence and does not require any `<>` tags.**

**Step 3: Punctuation & Spacing Scan -> Use `<>`**

1.  After completing the first two steps, handle punctuation and spacing last.

2.  **Punctuation Handling Principles**:
    - **Only use the `<>` tag for punctuation that needs to be modified or added.**
    - **If existing punctuation is correct in position and type, do not tag it.**
    - **Only tag existing punctuation if its type is incorrect.**

3.  **Common Punctuation Error Checks**:
    - Missing period at the end of a sentence: Add `<.>`
    - Missing comma in a compound sentence: Add `<,>`
    - Incorrect punctuation for a question: `.` -> `<?>` (Only when the original is a period but should be a question mark)
    - Missing semicolon in a compound sentence: Add `<;>`
    - Punctuation for an exclamation: Add `<!>`

4.  **Absolute Rules**:
    - When the original sentence has a punctuation error and a period needs to be added at the end, you **must** output the literal three characters `<.>`.
    - When the original sentence has a punctuation error and a comma needs to be added in the middle, you **must** output the literal three characters `<,>`.
    - When the original sentence has a punctuation error and a question mark needs to be corrected, you **must** output the literal three characters `<?>`.
    - **Do not** use punctuation like `.`, `,`, `?` directly in the output as corrections, unless they are part of the original input.

### **Markup Conflict Avoidance Rules**

1.  **Conflict between `{}` and `<>` usage**:
    - `{}` contains a complete sentence reconstruction and **absolutely never** uses `<>` tags inside it.
    - `<>` tags are only used when modifying the original text.
    - **Incorrect Example**: `{Having finished the assignment, I turned on the TV.<.>}`
    - **Correct Example**: `{Having finished the assignment, I turned on the TV.}`

2.  **Punctuation Tagging Consistency**:
    - If existing punctuation is correct, leave it as is; do not add `<>` tags.
    - Only incorrect or missing punctuation requires `<>` tags.

### **Reinforced Checklist**

**Each sentence must be checked one by one**:
1.  ✅ Is the first letter of every sentence capitalized?
2.  ✅ Is every use of a/an correct (based on the pronunciation of the following word)?
3.  ✅ Does the singular/plural form of every noun match the context?
4.  ✅ Does every verb agree with its subject (especially watch for long-distance subject-verb agreement)?
5.  ✅ Does every sentence have appropriate ending punctuation?
6.  ✅ Is the subjunctive mood used correctly?
7.  ✅ Is subject-verb agreement for collective nouns (data, team, etc.) correct?

### **Final Output Construction**
Merge the results of the three steps above into the final output string. If the text is flawless and requires no tags, only output: `✅ No errors found.`

### **Examples Walkthrough**

**Input**: `what is you're name.`

**Internal Thought Process**:
1.  **Step 1**: `what` -> `what[What]` (Capitalization), `you're` -> `you're[your]` (Part-of-speech error)
2.  **Step 2**: No structural issues.
3.  **Step 3**: `.` -> `<?>` (A question should end with a question mark; existing punctuation needs correction)

**Output**: `what[What] is you're[your] name<?>`

**Input**: `She is a amazin person`

**Internal Thought Process**:
1.  **Step 1**: `a` -> `a[an]` (Use "an" before a vowel sound), `amazin` -> `amazin[amazing]` (Spelling error)
2.  **Step 2**: No structural issues.
3.  **Step 3**: Missing period at the end of the sentence, add `<.>`

**Output**: `She is a[an] amazin[amazing] person<.>`

**Input**: `The data suggest a different conclusion`

**Internal Thought Process**:
1.  **Step 1**: `suggest` -> `suggest[suggests]` (The collective noun "data" as subject takes a singular verb)
2.  **Step 2**: No structural issues.
3.  **Step 3**: Add a period `<.>` at the end of the sentence.

**Output**: `The data suggest[suggests] a different conclusion<.>`

**Input**: `Having finished the assignment the TV was turned on.`

**Internal Thought Process**:
1.  **Step 1**: No token-level errors.
2.  **Step 2**: Dangling modifier issue, requires reconstruction: `{Having finished the assignment, I turned on the TV.}`
3.  **Step 3**: Already handled in Step 2, no additional punctuation tagging needed.

**Output**: `{Having finished the assignment, I turned on the TV.}`

**Input**: `My cat name is Fluffy. She are very playful.`

**Internal Thought Process**:
1.  **Step 1**: `are` -> `are[is]` (Subject-verb disagreement)
2.  **Step 2**: No structural issues.
3.  **Step 3**: The period in the first sentence is correct and needs no tag. Add `<.>` to the end of the second sentence.

**Output**: `My cat name is Fluffy. She are[is] very playful<.>`
"""

def should_continue(state: AgentState) -> Literal["check_agent", "end"]:
    """决定English Agent之后是否继续到Check Agent"""
    # 检查是否达到最大迭代次数（防止无限循环）
    max_iterations = 5
    if state.get("iteration_count", 0) >= max_iterations:
        print(f"⚠️ 达到最大迭代次数 ({max_iterations})，停止处理")
        return "end"
    
    # 总是先去检查代理验证结果
    return "check_agent"

def should_retry(state: AgentState) -> Literal["english_agent", "end"]:
    """决定Check Agent之后是否需要重新纠错"""
    # 如果通过检查，结束流程
    if state.get("is_approved", False):
        print("✅ 检查通过，处理完成")
        return "end"
    
    # 检查是否达到最大迭代次数
    max_iterations = 5
    if state.get("iteration_count", 0) >= max_iterations:
        print(f"⚠️ 达到最大迭代次数 ({max_iterations})，停止处理")
        return "end"
    
    # 否则返回英语代理重新处理
    print(f"🔄 检查未通过，进行第 {state.get('iteration_count', 0) + 1} 次纠错")
    return "english_agent"

def create_english_correction_graph():
    """创建英语纠错工作流图"""
    
    # 创建状态图
    workflow = StateGraph(AgentState)
    
    # 添加节点
    workflow.add_node("english_agent", english_agent)
    workflow.add_node("check_agent", check_agent)
    
    # 设置入口点
    workflow.set_entry_point("english_agent")
    
    # 添加条件边
    workflow.add_conditional_edges(
        "english_agent",
        should_continue,
        {
            "check_agent": "check_agent",
            "end": END
        }
    )
    
    workflow.add_conditional_edges(
        "check_agent", 
        should_retry,
        {
            "english_agent": "english_agent",
            "end": END
        }
    )
    
    # 编译图
    app = workflow.compile()
    return app

def process_text(text: str, verbose: bool = True) -> dict:
    """处理文本的主函数"""
    
    # 初始化状态
    initial_state = {
        "messages": [],
        "original_text": text,
        "corrected_text": "",
        "check_result": "",
        "iteration_count": 0,
        "is_approved": False
    }
    
    # 创建并运行工作流
    app = create_english_correction_graph()
    
    if verbose:
        print(f"🚀 开始处理文本: \"{text}\"")
        print("-" * 50)
    
    try:
        # 运行工作流
        final_state = app.invoke(initial_state)
        
        # 返回结果
        result = {
            "original_text": final_state["original_text"],
            "corrected_text": final_state.get("corrected_text", ""),
            "check_result": final_state.get("check_result", ""),
            "iterations": final_state.get("iteration_count", 0),
            "approved": final_state.get("is_approved", False)
        }
        
        if verbose:
            print("-" * 50)
            print("🎉 处理完成!")
            print(f"📝 原始文本: {result['original_text']}")
            print(f"✏️  纠正文本: {result['corrected_text']}")
            print(f"🔍 检查结果: {result['check_result']}")
            print(f"🔄 迭代次数: {result['iterations']}")
            print(f"✅ 是否通过: {'是' if result['approved'] else '否'}")
        
        return result
        
    except Exception as e:
        if verbose:
            print(f"❌ 处理过程中出现错误: {e}")
        raise e

if __name__ == "__main__":
    print("🔧 英语语法纠错系统 (基于 LangGraph)")
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
            
            # 处理文本
            result = process_text(user_input)
            
        except KeyboardInterrupt:
            print("\n👋 感谢使用，再见！")
            break
        except Exception as e:
            print(f"❌ 处理过程中出现错误: {e}")
            continue

