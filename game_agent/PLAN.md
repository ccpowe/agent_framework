# 斗地主 (Dou Dizhu) 多智能体游戏系统 - 详细计划文档

## 1. 项目愿景

本项目旨在创建一个基于大型语言模型（LLM）的多智能体“斗地主”游戏系统。该系统由三个智能体（Agent）组成，模拟一局完整的斗地主游戏。核心是使用 LangGraph 构建一个可循环、可中断的智能体交互框架。

系统将包含一个独立的后端服务和一个前端界面。后端使用 FastAPI 搭建，负责运行游戏逻辑和 LangGraph 智能体系统。前端负责可视化游戏进程，实时展示牌局状态和智能体的决策过程。最终目标是打造一个可以接入不同 LLM 进行策略比拼的、可交互的 AI 游戏平台。

## 2. 系统架构

系统分为三个核心部分：

1.  **前端 (Frontend)**: 基于 Web 技术的用户界面，用于展示游戏画面、玩家手牌、出牌记录等。
2.  **后端 API (Backend API)**: 使用 FastAPI 构建的轻量级 Web 服务，作为前端和智能体系统之间的桥梁。
3.  **智能体系统 (Agent System)**: 使用 LangGraph 构建的核心决策系统，负责管理游戏状态和驱动三个智能体进行游戏。

**交互流程:**

`前端 (React/Vue)` <--> `HTTP 请求` <--> `后端 (FastAPI)` <--> `函数调用` <--> `智能体系统 (LangGraph)`

![Architecture Diagram](https://i.imgur.com/gZ3oXyF.png) (*这是一个概念图，用于说明架构*)

## 3. 技术选型

-   **后端框架**: Python, FastAPI
-   **智能体框架**: LangChain, LangGraph
-   **LLM 集成**: LangChain 的 LLM 接口 (可灵活接入 OpenAI, Anthropic, Google Gemini, 或本地模型)
-   **前端框架**: React (使用 Vite) 或 Vue.js
-   **UI 库**: Ant Design 或 Tailwind CSS，用于快速构建美观的界面
-   **通信协议**: HTTP/REST (未来可升级为 WebSocket 实现实时通信)

## 4. 模块设计

### 4.1. 后端 (Backend)

#### a. 游戏核心逻辑 (`game_logic.py`)

这个模块独立于智能体，负责实现斗地主的所有规则。

-   **`Card` 类**: 定义单张扑克牌（花色、点数）。
-   **`Hand` 类**: 代表一个玩家的手牌，包含出牌、验证牌型等方法。
-   **`Game` 类**:
    -   `state`: 存储整个游戏的状态，包括：
        -   `deck`: 牌堆
        -   `players`: 三个玩家的实例
        -   `landlord`: 地主玩家
        -   `player_hands`: 每个玩家的手牌
        -   `current_turn`: 当前轮到哪个玩家
        -   `last_play`: 上一个出牌的玩家和牌
        -   `history`: 游戏历史记录
        -   `winner`: 游戏获胜者
    -   `deal()`: 发牌方法。
    -   `determine_landlord()`: 叫地主逻辑。
    -   `validate_move(player, move)`: 验证玩家的出牌是否符合规则。
    -   `update_state(player, move)`: 更新游戏状态。
    -   `check_winner()`: 检查是否有玩家胜出。

#### b. 智能体系统 (`agent_system.py`)

使用 LangGraph 构建游戏流程图。

-   **Graph State**: 定义一个贯穿整个图的状态对象，它将包含 `Game` 类的实例。
-   **Nodes (节点)**:
    -   `start_game_node`: 初始化游戏、洗牌、发牌。
    -   `determine_landlord_node`: 模拟叫地主过程，可以由一个或多个 Agent 节点完成。
    -   `player_agent_node`: 这是核心的决策节点。它会：
        1.  接收当前游戏状态。
        2.  根据当前玩家的角色（地主/农民）和手牌，构建一个 Prompt。
        3.  调用该玩家绑定的 LLM 进行决策（出牌或过）。
        4.  解析 LLM 的输出，格式化为游戏动作。
    -   `game_logic_node`: 调用 `game_logic.py` 中的方法，验证 `player_agent_node` 的决策是否有效，并更新游戏状态。如果无效，可以将状态反馈给 Agent 重新决策。
    -   `end_game_node`: 宣布获胜方，结束游戏。
-   **Edges (边)**:
    -   **Conditional Edges**: 主要的逻辑流转方式。例如，在 `game_logic_node` 之后，根据 `check_winner()` 的结果，决定是流向下一个玩家的 `player_agent_node` 还是 `end_game_node`。

#### c. API 接口 (`main.py`)

使用 FastAPI 提供以下接口：

-   `POST /game/start`: 创建一个新游戏。
    -   触发 LangGraph 的 `start_game_node`。
    -   返回初始的游戏状态和游戏 ID。
-   `GET /game/{game_id}/state`: 获取指定游戏的当前状态。
    -   前端通过轮询此接口来刷新界面。
-   `POST /game/{game_id}/next_move`: （可选，用于手动控制）触发下一个智能体的行动。
    -   在自动循环模式下，此接口可能不需要。
-   `POST /game/run`: (推荐) 启动一个完整的自动化游戏循环。
    -   后端自动运行 LangGraph 的循环，直到游戏结束。
    -   前端只需要轮询 `/state` 接口。

### 4.2. 前端 (Frontend)

-   **`GameBoard` 组件**: 整个游戏桌面的容器。
-   **`Player` 组件**: 显示每个玩家的头像、角色（地主/农民）、剩余手牌数量。
-   **`Hand` 组件**: 显示当前玩家的手牌。
-   **`DiscardPile` 组件**: 显示上一手出的牌。
-   **`ActionLog` 组件**: 显示游戏日志，如 "玩家A 出 3个J", "玩家B Pass"。
-   **`GameControls` 组件**: 包含 "开始新游戏" 等按钮。

## 5. 开发路线图

### **第一阶段: 核心逻辑与后端搭建 (Week 1)**

1.  **[完成]** 实现 `game_logic.py`，包含完整的斗地主规则，并编写单元测试确保其正确性。
2.  **[完成]** 搭建基础的 FastAPI 服务 (`main.py`)。
3.  **[完成]** 定义 `/start` 和 `/state` 接口的初步形态。
4.  **[完成]** 构建基础的 LangGraph 结构，只包含节点和状态定义，暂不集成 LLM。可以使用基于规则的简单机器人作为 Agent 的临时替代。

### **第二阶段: 智能体集成与循环 (Week 2)**

1.  **[完成]** 设计并实现 `player_agent_node` 的 Prompt 工程，使其能清晰地向 LLM 描述游戏状态。
2.  **[完成]** 集成第一个 LLM (例如 `gpt-3.5-turbo`) 到 Agent 中。
3.  **[完成]** 实现 LangGraph 的条件边，让三个智能体能够根据游戏规则循环交互。
4.  **[完成]** 实现完整的从开始到结束的游戏循环，并通过日志和测试验证其正确性。

### **第三阶段: 前端开发与对接 (Week 3-4)**

1.  **[完成]** 使用 Vite 初始化 React/Vue 项目。
2.  **[完成]** 开发所有前端组件 (`GameBoard`, `Player`, `Hand` 等)。
3.  **[完成]** 实现前端与后端的 API 对接，通过轮询 `GET /game/{game_id}/state` 来渲染游戏状态。
4.  **[完成]** 实现 "开始新游戏" 功能。
5.  **[完成]** 对 UI 进行初步美化。

### **第四阶段: 优化与扩展**

1.  **[探索]** 实现可插拔的 LLM 配置，允许在开始游戏前为每个 Agent 选择不同的 LLM。
2.  **[探索]** 将通信方式从 HTTP 轮询升级为 WebSocket，实现更流畅的实时更新。
3.  **[探索]** 优化 Prompt 和 Agent 的决策逻辑，提高 AI 的游戏水平。
4.  **[探索]** 增加游戏历史回放功能。

## 6. 建议文件结构

```
/game_agent
|-- backend/
|   |-- venv/
|   |-- app/
|   |   |-- __init__.py
|   |   |-- main.py             # FastAPI 应用入口
|   |   |-- agent_system.py     # LangGraph 定义
|   |   |-- game_logic.py       # 斗地主核心规则
|   |   |-- prompts.py          # 存放 Agent 的 Prompt 模板
|   |   |-- utils.py            # 工具函数
|   |-- requirements.txt
|   |-- Dockerfile
|
|-- frontend/
|   |-- node_modules/
|   |-- public/
|   |-- src/
|   |   |-- components/
|   |   |   |-- GameBoard.jsx
|   |   |   |-- Player.jsx
|   |   |   |-- Hand.jsx
|   |   |   |-- Card.jsx
|   |   |-- App.jsx
|   |   |-- index.css
|   |   |-- main.jsx
|   |-- package.json
|   |-- vite.config.js
|
|-- PLAN.md                     # 本计划文档
|-- README.md
```
