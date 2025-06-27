# 斗地主 AI - LangGraph 智能体系统设计文档

## 1. 系统概述

本文档详细描述了“斗地主 AI 观察室”项目后端的核心部分——基于 LangGraph 的多智能体系统的设计与实现。本系统旨在创建一个由三个大型语言模型（LLM）驱动的智能体，它们能够根据斗地主的游戏规则进行交互，完成一整局游戏。

该设计遵循 `PLAN.md` 中定义的总体架构，并为 `FRONTEND_DESIGN.md` 中描述的前端接口提供数据支持。

## 2. LangGraph 设计理念

我们将游戏流程构建为一个**有状态的循环图 (Stateful, Cyclic Graph)**。LangGraph 的核心优势在于其管理状态和通过条件边（Conditional Edges）进行复杂逻辑路由的能力，这与棋牌游戏的流程天然契合。

-   **统一状态管理**: 整个游戏的状态，包括牌局信息、玩家手牌、历史记录等，都封装在一个 `GraphState` 对象中。这个状态对象在图的节点之间流动，确保了数据的一致性和可追溯性。
-   **节点作为功能单元**: 图中的每个节点（Node）代表游戏流程中的一个具体步骤，例如“玩家决策”、“处理出牌”或“检查游戏是否结束”。这使得逻辑单元高度内聚、易于测试和维护。
-   **边作为游戏规则**: 节点之间的连接（Edge），特别是条件边，充当了游戏规则的执行者。例如，在一个玩家出牌后，条件边会根据出牌是否有效、游戏是否结束来决定下一个应该执行哪个节点，从而驱动游戏流程。

## 3. 核心数据结构: GraphState

`GraphState` 是贯穿整个 LangGraph 图的单一数据源。它被定义为一个 `TypedDict`，以利用 LangChain 的类型化编程优势。

```python
from typing import List, Tuple, TypedDict, Annotated
from langgraph.graph.message import add_messages

# game_logic.py 需定义 Game 类
from .game_logic import Game

class GraphState(TypedDict):
    """
    代表整个游戏生命周期的状态。

    Attributes:
        game: 游戏核心逻辑的实例，包含所有规则和牌局状态。
        current_player_id: 当前轮到行动的玩家ID ("player_1", "player_2", "player_3")。
        messages: 用于驱动 Agent 对话和决策的消息列表。
        turn_history: 记录每个回合的玩家及其动作。
        game_over: 游戏是否结束的标志。
        winner: 胜利者的角色 ("landlord" 或 "farmers")。
        last_valid_move: 上一个合法的出牌，用于下一位玩家决策。
        invalid_move_feedback: 当玩家做出无效决策时，向其提供的反馈信息。
    """
    game: Game
    current_player_id: str
    messages: Annotated[List[BaseMessage], add_messages]
    turn_history: List[Tuple[str, str]]
    game_over: bool
    winner: str
    last_valid_move: List[str] | None
    invalid_move_feedback: str | None
```

## 4. 节点 (Nodes) 设计

图由以下几个关键节点组成：

1.  **`start_game_node` (游戏初始化节点)**
    -   **职责**: 创建 `Game` 实例，洗牌并发牌给三位玩家。
    -   **输出**: 更新 `GraphState` 中的 `game` 和 `current_player_id`。

2.  **`player_agent_node` (玩家决策节点)**
    -   **职责**: 这是智能体与 LLM 交互的核心。
    -   **流程**:
        1.  从 `GraphState` 中获取当前玩家 (`current_player_id`)。
        2.  构建一个详细的 **Prompt**，包含公共信息（地主、底牌、每家剩余牌数、历史出牌）、当前玩家的私有信息（手牌）、游戏规则以及可选的 `invalid_move_feedback`。
        3.  调用与当前玩家关联的 LLM Agent 来获取决策（出牌或 Pass）。
        4.  将 LLM 的输出（例如，`"play 3 3 4 4 5 5"` 或 `"pass"`）添加到 `messages` 列表中。

3.  **`process_decision_node` (决策处理与裁判节点)**
    -   **职责**: 验证玩家的决策并更新游戏状态。
    -   **流程**:
        1.  从 `messages` 中解析出玩家的最新决策。
        2.  调用 `game.validate_move()` 验证牌是否符合规则（例如，是否比上家大，牌型是否正确）。
        3.  **如果有效**:
            -   调用 `game.play_move()` 更新玩家手牌。
            -   更新 `GraphState` 的 `last_valid_move`。
            -   清空 `invalid_move_feedback`。
            -   调用 `game.check_winner()` 检查是否产生胜利者，并相应更新 `game_over` 和 `winner` 状态。
        4.  **如果无效**:
            -   不更新游戏状态。
            -   在 `invalid_move_feedback` 中生成一条错误提示信息（例如，“您出的牌不符合规则，请重新出牌”）。

## 5. 边 (Edges) 与逻辑路由

条件边是驱动游戏流程的关键。我们将定义一个 `route_after_processing` 函数来处理所有主要的逻辑分支。

-   **`conditional_edge` (条件路由函数)**
    -   **输入**: `GraphState`。
    -   **逻辑**:
        1.  检查 `state['game_over']`：如果为 `True`，则路由到 `END` 节点。
        2.  检查 `state['invalid_move_feedback']`：如果存在反馈信息（意味着上一步出牌无效），则路由回 `player_agent_node`，让**同一位玩家**根据反馈重新决策。
        3.  如果以上都不是，则代表是一次成功的出牌或 Pass。此时，更新 `current_player_id` 为下一位玩家，并路由到 `player_agent_node`。

## 6. 图结构定义

使用 `langgraph.StateGraph` 来组装整个流程。

```python
from langgraph.graph import StateGraph, END

# ... (导入节点函数和状态定义)

# 1. 初始化图
workflow = StateGraph(GraphState)

# 2. 添加节点
workflow.add_node("start_game", start_game_node)
workflow.add_node("player_agent", player_agent_node)
workflow.add_node("process_decision", process_decision_node)

# 3. 设置入口点
workflow.set_entry_point("start_game")

# 4. 添加边
workflow.add_edge("start_game", "player_agent")
workflow.add_edge("player_agent", "process_decision")

# 5. 添加条件边
workflow.add_conditional_edges(
    "process_decision",
    route_after_processing, # 这是我们的路由函数
    {
        "continue": "player_agent", # 继续游戏
        "end_game": END              # 结束游戏
    }
)

# 6. 编译图
app = workflow.compile()
```

## 7. 与 FastAPI 的集成

编译后的 `app` 对象可以被 FastAPI 服务直接调用。

-   **`POST /api/game/start`**:
    -   调用 `app.invoke()` 来启动一个新的游戏图实例。
    -   将返回的初始 `GraphState` 转化为前端所需的 `GameState` JSON 格式并响应。
    -   启动一个后台任务，使用 `app.stream()` 持续运行游戏，直到 `END` 状态。

-   **`GET /api/game/{game_id}/state`**:
    -   前端通过此接口轮询。
    -   后端维护一个字典，存储 `game_id` 与其对应的最新 `GraphState`。
    -   每次被请求时，从该字典中读取最新状态，格式化后返回。当图运行结束时，后端更新对应 `game_id` 的最终状态。
```