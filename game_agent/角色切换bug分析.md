# 角色切换 Bug 分析与调试计划

本文档记录了对斗地主 Agent 系统中关键 Bug 的分析和修复过程。

## 1. 已完成的工作：修复初始化失败问题

- **问题**：运行 `debug_critical.py` 或通过 API 启动游戏时，系统抛出 `500 - {"detail":"创建游戏失败: 'player_decision' is already being used as a state key"}` 错误。
- **分析**：该问题是由于 LangGraph 中的一个状态键（`player_decision`）与一个节点名（`player_decision`）发生了命名冲突，导致图无法正确初始化。
- **解决方案**：我已经修改了 `agent_system.py` 文件，将冲突的节点名从 `player_decision` 重命名为 `get_player_decision`，并更新了所有相关的图连接边。此举解决了状态键与节点名的冲突。

## 2. 下一步计划：调试玩家不切换的 Bug

现在，初始化的问题已经解决，我们可以开始处理核心的逻辑 Bug：**玩家1出牌后，当前玩家（`current_player`）没有正确切换到下一位玩家，导致游戏卡死。**

### 你的任务 (User Action):

1.  请在你的终端中，**运行测试脚本**：
    ```sh
    uv run .\debug_critical.py
    ```
2.  脚本会开始创建并监控游戏。请等待它运行一段时间（大约1分钟，或者直到你看到它明显卡在某个玩家的回合）。
3.  请将该脚本在终端中输出的**全部内容**复制并发送给我。

### 我的任务 (My Task):

1.  收到你提供的完整日志后，我将仔细分析其中记录的每一步游戏状态。
2.  我的分析重点将是追踪 `current_player` 字段的变化，以及 `turn_history` 中的玩家动作。
3.  通过对比游戏逻辑（`game_logic.py`）中的预期行为和日志中的实际状态流转，我将精确定位在 `agent_system.py` 的哪个环节（很可能是在 `_process_move_node` 或 `_route_game_flow` 中）导致了玩家切换失败。
4.  定位问题后，我将提出具体的代码修复方案。
