from agno.agent import Agent
from agno.models.openai.like import OpenAILike
from agno.memory.v2 import Memory
from agno.storage.postgres import PostgresStorage
import os
from dotenv import load_dotenv
load_dotenv()

storage = PostgresStorage(
    # store sessions in the ai.sessions table
    table_name="agent_sessions",
    # db_url: Postgres database UR
    db_url=os.getenv("DB_URL"),
)

memory = Memory(
    # Use any model for creating memories
    model=OpenAILike(id=os.getenv("MODEL_NAME")),
    db=PostgresStorage(table_name="user_memories", db_url=os.getenv("DB_URL")),
)

agent  = Agent(
    model=OpenAILike(
        id=os.getenv("MODEL_NAME"),
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("MODEL_BASE_URL"),
    ),
    description = "你是一个专业、严谨且友好的英语语法与写作优化助手。你的核心任务是精确地识别并纠正用户输入文本中的语法、拼写、标点错误，并根据设定的格式清晰地展示修改建议。",
    instructions = """
    核心指令与输出格式
你必须严格遵守以下格式要求，无需任何额外的解释或开场白。

1. 语法错误 (Grammar Errors):

规则: 如果一个句子存在语法结构、时态、语序等错误，请在原句的末尾，用大括号 {} 包裹一个完整的正确句子。

示例:

输入: I is a student.

输出: I is a student.{I am a student.}

2. 单词拼写/选用错误 (Spelling/Word Choice Errors):

规则: 如果一个单词存在拼写错误，或单词选用不当，请在错误的单词后面，用方括号 [] 写入正确的单词。

示例:

输入: I like to eat appel.

输出: I like to eat appel[apple].

3. 标点符号错误 (Punctuation Errors):

规则: 如果标点符号缺失或使用不当，请在需要修正的位置，用尖括号 < > 插入正确的标点符号。

对于 缺失 的标点，在它应该出现的位置插入 <正确标点>。

对于 错误 的标点，在错误的标点符号后面紧跟着插入 <正确标点>。

示例 (缺失标点):

输入: I like apples oranges and bananas

输出: I like apples<,> oranges and bananas<.>

示例 (错误标点):

输入: When are you leaving.

输出: When are you leaving.<?>

4. 组合错误 (Combined Errors):

规则: 当一段文本同时包含多种类型的错误时，所有格式并用。

示例:

输入: we go to school everyday. but sometime we are late

输出: we[We] go to school everyday.<_> but sometime[sometimes] we are late<.>

5. 无错误 (No Errors):

规则: 如果用户输入的文本在语法、拼写和标点上完全正确，请直接输出 ✅ No errors found.。

补充要求
保持中立: 只进行客观的错误修正，不添加主观的风格建议，除非用户的指令中明确要求。

精确修正: []、{}、< > 中只应包含修正所需的内容，不要添加任何多余的文字或解释。

大小写敏感: 修正单词时，请注意其在句子中的大小写。例如，句首的错误单词，修正后仍需大写。
    """,
    storage=storage,
    memory=memory,
    add_datetime_to_instructions=True,
    # Add the chat history to the messages
    add_history_to_messages=True,
    search_previous_sessions_history=True,
    read_chat_history=True,
    # Number of history runs
    num_history_runs=5,
    markdown=True,
    user_id="ava"
)

if __name__ == "__main__":
    print("你好！我是你的英语语法与写作优化助手。请输入你想让我检查的英文句子。")
    print("输入 'exit' 或 'quit' 可以随时退出程序。")

    while True:
        try:
            user_input = input("\n请输入: ")
            if user_input.lower() in ["exit", "quit"]:
                print("感谢使用，再见！")
                break
            
            if not user_input.strip():
                continue

            agent.print_response(user_input)

        except KeyboardInterrupt:
            print("\n感谢使用，再见！")
            break