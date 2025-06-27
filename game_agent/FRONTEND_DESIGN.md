# 斗地主 AI 观察室 - 前端设计文档

## 1. 设计哲学与目标

前端的核心目标是**清晰地、实时地可视化 AI 智能体之间的游戏过程**。用户作为“观察者”，应该能一目了然地看到牌局的每一个变化、每一个智能体的决策。界面应追求现代化、简洁、响应迅速，并带有一定的科技感，以匹配“AI 对战”的主题。

-   **核心用户体验**: 观察、学习、分析 AI 的决策。
-   **交互性**: 最小化用户交互，主要集中在开始游戏和查看信息上。
-   **信息层次**: 关键信息（如谁是地主、当前轮到谁、剩余牌数）必须最突出。

## 2. 视觉风格与主题

-   **主题**: 采用**深色主题 (Dark Mode)**。这有助于减少视觉疲劳，让彩色的扑克牌和高亮元素更突出，也符合游戏和科技应用的常用风格。
-   **色彩方案**:
    -   背景: 深灰或近黑 (e.g., `#1A1A1A`)
    -   主面板/容器: 略亮的灰色 (e.g., `#2C2C2C`)
    -   主色调: 科技蓝或紫色 (e.g., `#4A90E2`)，用于按钮、高亮、标题等。
    -   强调色 (成功/胜利): 绿色 (e.g., `#7ED321`)
    -   强调色 (警告/失败): 红色 (e.g., `#D0021B`)
-   **字体**: 使用无衬线字体，如 `Inter`, `Roboto`, 或 `Helvetica Neue`，以保证在各种屏幕上的可读性。
-   **动画**: 使用微妙、快速的动画来提升体验，例如：
    -   卡牌移动的过渡效果。
    -   当前玩家高亮的淡入淡出效果。
    -   出牌时的缩放效果。

## 3. 页面与视图设计

本项目本质上是一个**单页面应用 (Single-Page Application)**。所有内容都在一个主视图中根据游戏状态动态展示。

### 视图状态 (View States)

1.  **欢迎/启动视图 (Welcome View)**
    -   **内容**: 页面中央显示游戏标题 “AI 斗地主竞技场”，下方有一个醒目的 “开始新对局” 按钮。
    -   **交互**: 点击按钮后，向后端发送开始游戏请求，并过渡到游戏视图。

2.  **游戏进行时视图 (Game View)**
    -   这是核心界面，布局如下：
        -   **顶部区域**: 显示 “对手1” (左) 和 “对手2” (右) 的信息区。每个区域包含：
            -   玩家名称 (e.g., "Agent 2")
            -   角色标识 (地主图标或农民图标)
            -   剩余手牌数量 (一个数字角标)
            -   手牌的背面视图 (表示隐藏的手牌)
        -   **中央区域 (牌桌)**:
            -   显示地主的三张底牌（游戏开始时短暂显示后覆盖）。
            -   显示上一手打出的牌。
            -   如果轮到某玩家思考，可以显示一个 “思考中...” 的指示器。
        -   **底部区域**: 显示 “主视角玩家” (Agent 1) 的信息和手牌。
            -   玩家名称、角色、剩余牌数。
            -   **完整、正面朝上**显示其所有手牌。
        -   **右侧或左侧边栏**: **行动日志 (Action Log)**
            -   滚动列表，显示游戏中的每一个动作，例如：
                -   `[系统] 游戏开始，正在发牌...`
                -   `[Agent 2] 叫地主`
                -   `[Agent 3] 不叫`
                -   `[Agent 1] 抢地主`
                -   `[Agent 1] 打出 [♠️3, ♥️3]`
                -   `[Agent 2] Pass`

3.  **游戏结束视图 (End Game View)**
    -   **形式**: 在游戏视图之上弹出一个**模态框 (Modal)**。
    -   **内容**: 
        -   清晰的标题，如 “地主胜利！” 或 “农民胜利！”
        -   （可选）显示本局的简单统计。
        -   一个 “再来一局” 的按钮。
    -   **交互**: 点击按钮将关闭模态框，并重置为欢迎视图。

## 4. 组件化设计

-   `GameBoard.jsx`: 游戏主容器，负责整体布局。
-   `PlayerArea.jsx`: 玩家信息展示区。接收 `player` 对象作为 props，动态显示名称、角色、牌数等。
-   `HandDisplay.jsx`: 手牌展示区。接收一个卡牌数组 `cards` 作为 props 并渲染它们。
-   `Card.jsx`: 单张扑克牌。接收 `suit`, `rank`, `isFaceUp` 等 props。
-   `ActionLog.jsx`: 行动日志。接收一个日志条目数组 `logEntries` 并渲染。
-   `GameStatus.jsx`: 显示当前回合、上一手牌等中央信息。
-   `EndGameModal.jsx`: 游戏结束的模态框。接收 `winner` 和 `onRestart` 函数作为 props。

## 5. 与后端的 API 结构规范

前端通过**轮询 (Polling)** 机制与后端通信。前端定期向后端请求最新的游戏状态，然后根据返回的数据更新 UI。这是一个简单而可靠的实现方式。

### Endpoints

1.  **`POST /api/game/start`**
    -   **用途**: 开始一局新游戏。
    -   **请求体 (Request Body)**: (可选) 可以传入 LLM 配置。
        ```json
        {
          "llm_config": {
            "player_1": "gemini-1.5-pro",
            "player_2": "gpt-4o",
            "player_3": "claude-3-opus"
          }
        }
        ```
    -   **成功响应 (Response Body)**: `200 OK`，返回初始的 `GameState` 对象。

2.  **`GET /api/game/{game_id}/state`**
    -   **用途**: 获取指定 `game_id` 的当前完整游戏状态。
    -   **成功响应 (Response Body)**: `200 OK`，返回最新的 `GameState` 对象。

### 数据结构 (Data Structures)

**`GameState` 对象 (后端返回给前端的核心对象)**

```json
{
  "game_id": "unique-game-identifier-12345",
  "game_status": "bidding" | "in_progress" | "finished", // 游戏阶段：叫地主中、游戏中、已结束
  "turn_player_id": "player_2", // 当前轮到谁出牌
  "last_move": { // 上一个成功的出牌动作
    "player_id": "player_1",
    "move_type": "play" | "pass", // "play" 表示出牌, "pass" 表示过
    "cards_played": ["S3", "H3", "D4", "C4"] // 卡牌数组，pass 时为空
  } | null,
  "players": [
    {
      "id": "player_1",
      "name": "Agent 1 (Gemini)",
      "role": "farmer" | "landlord" | "pending", // 角色：农民、地主、未定
      "hand": ["S3", "S4", "S5", "..."], // 该玩家的完整手牌
      "hand_count": 17, // 剩余手牌数量
      "is_turn": false // 是否正轮到该玩家
    },
    {
      "id": "player_2",
      "name": "Agent 2 (GPT-4o)",
      "role": "farmer",
      "hand": ["H3", "H4", "H5", "..."],
      "hand_count": 17,
      "is_turn": true
    },
    {
      "id": "player_3",
      "name": "Agent 3 (Claude)",
      "role": "landlord",
      "hand": ["D3", "D4", "D5", "..."],
      "hand_count": 20,
      "is_turn": false
    }
  ],
  "landlord_extra_cards": ["SA", "HK", "C2"], // 三张地主底牌
  "winner": "landlord" | "farmers" | null, // 胜利者，游戏未结束时为 null
  "action_log": [ // 游戏过程的文字记录
    "游戏开始，正在发牌...",
    "玩家 player_2 叫地主",
    "玩家 player_3 选择不叫",
    "玩家 player_1 打出方块3"
  ]
}
```

**卡牌表示法**: 推荐使用 `花色`+`点数` 的字符串表示。例如: `S` (Spades), `H` (Hearts), `D` (Diamonds), `C` (Clubs)。点数可以是 `3-10, J, Q, K, A, 2`。小王 `BJ` (Black Joker), 大王 `RJ` (Red Joker)。示例: `H3` (红桃3), `DA` (方片A), `S2` (黑桃2), `RJ` (大王)。
