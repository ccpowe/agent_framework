# 背景：我使用langgraph构建了一个斗地主agent 本来按照@AGENT_SYSTEM_DESIGN.md 的设计文档进行的开发。我但是在实际过程中可能已经发生了偏移。
#任务：
## 1.你帮我全面分析当前的代码文件。生成一份全新的文档。包含代码的架构，主要的模块。等等
## 2.当前的代码存在一些问题，
- 在运行测试脚本@debug_critical.py存在下面的问题.无法初始化运行测试。
    ```
    PS D:\Code_vs\agent_framework\game_agent> uv run .\debug_critical.py
    🚨 斗地主系统 - 关键问题调试
    专门针对：AI决策丢失、玩家不切换问题
    ============================================================
    ✅ 服务器正常
    🎮 创建测试游戏...
    ❌ 游戏创建失败: 500 - {"detail":"创建游戏失败: 'player_decision' is already being used as a state key"}
    ```

    ```
    (agent-framwork) PS D:\Code_vs\agent_framework\game_agent> uv run .\main.py
    INFO:     Will watch for changes in these directories: ['D:\\Code_vs\\ageINFO:     Will watch for changes in these directories: ['D:\\Code_vs\\ageINFO:     Will watch for changes in these directories: ['D:\\Code_vs\\ageINFO:     Will watch for changes in these directories: ['D:\\Code_vs\\agent_framework\\game_agent']
    INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)  
    INFO:     Started reloader process [8544] using WatchFiles
    INFO:     Started server process [22516]
    INFO:     Waiting for application startup.
    INFO:main:斗地主多智能体系统启动
    INFO:main:API文档: http://localhost:8000/docs
    INFO:     Application startup complete.
    INFO:watchfiles.main:5 changes detected
    INFO:     127.0.0.1:61737 - "GET /api/health HTTP/1.1" 200 OK
    ERROR:main:创建游戏失败: 'player_decision' is already being used as a state key
    INFO:     127.0.0.1:61739 - "POST /api/game/start HTTP/1.1" 500 Internal Server Error
    INFO:watchfiles.main:1 change detected
    INFO:watchfiles.main:1 change detected
    ```
- 出牌角色切换存在问题。一直存在的BUg.当玩家1出牌后。因该切换到下一位玩家，但是一直是玩家1.导致游戏逻辑卡死。重点排查相关的部分。分析问题在哪里。

## 要求：
- 先进行任务1，对当前的agent进行全面的了解，生成agent_analysis.md 
- 任务2：若是无法准确得出问题2的出错节点。不要瞎猜，先修复问题1，无法测试的问题，反馈给我，我来进行测试，获取更多的调试信息。
- 生成的文件：
    - 任务1：agent_analysis.md  
    - 任务2：角色切换bug分析.md 
## 代码文件：
- @D:\Code_vs\agent_framework\game_agent\agent_system.py
- @D:\Code_vs\agent_framework\game_agent\game_logic.py
- @D:\Code_vs\agent_framework\game_agent\prompts.py