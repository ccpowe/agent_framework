PS D:\Code_vs\agent_framework\game_agent> uv run .\debug_critical.py
🚨 斗地主系统 - 关键问题调试
专门针对：AI决策丢失、玩家不切换问题
============================================================
✅ 服务器正常
🎮 创建测试游戏...
✅ 游戏创建成功! Game ID: d959044d-eda7-408e-8348-c58699075ec9
🔍 监控游戏 d959044d-eda7-408e-8348-c58699075ec9 的关键状态传递...
============================================================

🔎 步骤 1:
   状态: playing
   地主: player_1
   当前玩家: player_1
   手牌: player_1(20) | player_2(17) | player_3(17)

🔎 步骤 2:
   状态: playing
   地主: player_1
   当前玩家: player_1
   手牌: player_1(20) | player_2(17) | player_3(17)

🔎 步骤 3:
   状态: playing
   地主: player_1
   当前玩家: player_2
   手牌: player_1(19) | player_2(17) | player_3(17)
   最后动作: player_1 出牌 ['♥3'] (single)
   总回合: 1

🔎 步骤 4:
   状态: playing
   地主: player_1
   当前玩家: player_2
   手牌: player_1(19) | player_2(17) | player_3(17)
   最后动作: player_1 出牌 ['♥3'] (single)
   总回合: 1

🔎 步骤 5:
   状态: playing
   地主: player_1
   当前玩家: player_3
   手牌: player_1(19) | player_2(17) | player_3(17)
   最后动作: player_2 过牌
   总回合: 2

🔎 步骤 6:
   状态: playing
   地主: player_1
   当前玩家: player_3
   手牌: player_1(19) | player_2(17) | player_3(17)
   最后动作: player_2 过牌
   总回合: 2

🔎 步骤 7:
   状态: playing
   地主: player_1
   当前玩家: player_3
   手牌: player_1(19) | player_2(17) | player_3(17)
   最后动作: player_2 过牌
   总回合: 2

🔎 步骤 8:
   状态: playing
   地主: player_1
   当前玩家: player_3
   手牌: player_1(19) | player_2(17) | player_3(17)
   最后动作: player_2 过牌
   总回合: 2

🔎 步骤 9:
   状态: playing
   地主: player_1
   当前玩家: player_3
   手牌: player_1(19) | player_2(17) | player_3(17)
   最后动作: player_2 过牌
   总回合: 2

🔎 步骤 10:
   状态: playing
   地主: player_1
   当前玩家: player_3
   手牌: player_1(19) | player_2(17) | player_3(17)
   最后动作: player_2 过牌
   总回合: 2

🔎 步骤 11:
   状态: playing
   地主: player_1
   当前玩家: player_1
   手牌: player_1(19) | player_2(17) | player_3(17)
   最后动作: player_3 过牌
   总回合: 3
⚠️ 疑似状态卡死！玩家未切换

🔎 步骤 12:
   状态: playing
   地主: player_1
   当前玩家: player_2
   手牌: player_1(18) | player_2(17) | player_3(17)
   最后动作: player_1 出牌 ['♣3'] (single)
   总回合: 4

🔎 步骤 13:
   状态: playing
   地主: player_1
   当前玩家: player_2
   手牌: player_1(18) | player_2(17) | player_3(17)
   最后动作: player_1 出牌 ['♣3'] (single)
   总回合: 4

🔎 步骤 14:
   状态: playing
   地主: player_1
   当前玩家: player_2
   手牌: player_1(18) | player_2(17) | player_3(17)
   最后动作: player_1 出牌 ['♣3'] (single)
   总回合: 4

🔎 步骤 15:
   状态: playing
   地主: player_1
   当前玩家: player_3
   手牌: player_1(18) | player_2(16) | player_3(17)
   最后动作: player_2 出牌 ['♠6'] (single)
   总回合: 5

🔎 步骤 16:
   状态: playing
   地主: player_1
   当前玩家: player_3
   手牌: player_1(18) | player_2(16) | player_3(17)
   最后动作: player_2 出牌 ['♠6'] (single)
   总回合: 5

🔎 步骤 17:
   状态: playing
   地主: player_1
   当前玩家: player_3
   手牌: player_1(18) | player_2(16) | player_3(17)
   最后动作: player_2 出牌 ['♠6'] (single)
   总回合: 5

🔎 步骤 18:
   状态: playing
   地主: player_1
   当前玩家: player_1
   手牌: player_1(18) | player_2(16) | player_3(16)
   最后动作: player_3 出牌 ['♠7'] (single)
   总回合: 6
⚠️ 疑似状态卡死！玩家未切换

🔎 步骤 19:
   状态: playing
   地主: player_1
   当前玩家: player_1
   手牌: player_1(18) | player_2(16) | player_3(16)
   最后动作: player_3 出牌 ['♠7'] (single)
   总回合: 6
⚠️ 疑似状态卡死！玩家未切换

🔎 步骤 20:
   状态: playing
   地主: player_1
   当前玩家: player_1
   手牌: player_1(18) | player_2(16) | player_3(16)
   最后动作: player_3 出牌 ['♠7'] (single)
   总回合: 6
⚠️ 疑似状态卡死！玩家未切换

🔎 步骤 21:
   状态: playing
   地主: player_1
   当前玩家: player_1
   手牌: player_1(18) | player_2(16) | player_3(16)
   最后动作: player_3 出牌 ['♠7'] (single)
   总回合: 6
⚠️ 疑似状态卡死！玩家未切换

🔎 步骤 22:
   状态: playing
   地主: player_1
   当前玩家: player_1
   手牌: player_1(18) | player_2(16) | player_3(16)
   最后动作: player_3 出牌 ['♠7'] (single)
   总回合: 6
⚠️ 疑似状态卡死！玩家未切换

🔎 步骤 23:
   状态: playing
   地主: player_1
   当前玩家: player_1
   手牌: player_1(18) | player_2(16) | player_3(16)
   最后动作: player_3 出牌 ['♠7'] (single)
   总回合: 6
⚠️ 疑似状态卡死！玩家未切换

🔎 步骤 24:
   状态: playing
   地主: player_1
   当前玩家: player_1
   手牌: player_1(18) | player_2(16) | player_3(16)
   最后动作: player_3 出牌 ['♠7'] (single)
   总回合: 6
⚠️ 疑似状态卡死！玩家未切换

🔎 步骤 25:
   状态: playing
   地主: player_1
   当前玩家: player_1
   手牌: player_1(18) | player_2(16) | player_3(16)
   最后动作: player_3 出牌 ['♠7'] (single)
   总回合: 6
⚠️ 疑似状态卡死！玩家未切换

🔎 步骤 26:
   状态: playing
   地主: player_1
   当前玩家: player_1
   手牌: player_1(18) | player_2(16) | player_3(16)
   最后动作: player_3 出牌 ['♠7'] (single)
   总回合: 6
⚠️ 疑似状态卡死！玩家未切换

🔎 步骤 27:
   状态: playing
   地主: player_1
   当前玩家: player_1
   手牌: player_1(18) | player_2(16) | player_3(16)
   最后动作: player_3 出牌 ['♠7'] (single)
   总回合: 6
⚠️ 疑似状态卡死！玩家未切换

🔎 步骤 28:
   状态: playing
   地主: player_1
   当前玩家: player_1
   手牌: player_1(18) | player_2(16) | player_3(16)
   最后动作: player_3 出牌 ['♠7'] (single)
   总回合: 6
⚠️ 疑似状态卡死！玩家未切换

🔎 步骤 29:
   状态: playing
   地主: player_1
   当前玩家: player_1
   手牌: player_1(18) | player_2(16) | player_3(16)
   最后动作: player_3 出牌 ['♠7'] (single)
   总回合: 6
⚠️ 疑似状态卡死！玩家未切换

🔎 步骤 30:
   状态: playing
   地主: player_1
   当前玩家: player_1
   手牌: player_1(18) | player_2(16) | player_3(16)
   最后动作: player_3 出牌 ['♠7'] (single)
   总回合: 6
⚠️ 疑似状态卡死！玩家未切换

🔎 步骤 31:
   状态: playing
   地主: player_1
   当前玩家: player_1
   手牌: player_1(18) | player_2(16) | player_3(16)
   最后动作: player_3 出牌 ['♠7'] (single)
   总回合: 6
⚠️ 疑似状态卡死！玩家未切换

🔎 步骤 32:
   状态: playing
   地主: player_1
   当前玩家: player_1
   手牌: player_1(18) | player_2(16) | player_3(16)
   最后动作: player_3 出牌 ['♠7'] (single)
   总回合: 6
⚠️ 疑似状态卡死！玩家未切换

🔎 步骤 33:
   状态: playing
   地主: player_1
   当前玩家: player_1
   手牌: player_1(18) | player_2(16) | player_3(16)
   最后动作: player_3 出牌 ['♠7'] (single)
   总回合: 6
⚠️ 疑似状态卡死！玩家未切换

🔎 步骤 34:
   状态: playing
   地主: player_1
   当前玩家: player_1
   手牌: player_1(18) | player_2(16) | player_3(16)
   最后动作: player_3 出牌 ['♠7'] (single)
   总回合: 6
⚠️ 疑似状态卡死！玩家未切换

🔎 步骤 35:
   状态: playing
   地主: player_1
   当前玩家: player_1
   手牌: player_1(18) | player_2(16) | player_3(16)
   最后动作: player_3 出牌 ['♠7'] (single)
   总回合: 6
⚠️ 疑似状态卡死！玩家未切换

🔎 步骤 36:
   状态: playing
   地主: player_1
   当前玩家: player_1
   手牌: player_1(18) | player_2(16) | player_3(16)
   最后动作: player_3 出牌 ['♠7'] (single)
   总回合: 6
⚠️ 疑似状态卡死！玩家未切换

🔎 步骤 37:
   状态: playing
   地主: player_1
   当前玩家: player_1
   手牌: player_1(18) | player_2(16) | player_3(16)
   最后动作: player_3 出牌 ['♠7'] (single)
   总回合: 6
⚠️ 疑似状态卡死！玩家未切换

🔎 步骤 38:
   状态: playing
   地主: player_1
   当前玩家: player_1
   手牌: player_1(18) | player_2(16) | player_3(16)
   最后动作: player_3 出牌 ['♠7'] (single)
   总回合: 6
⚠️ 疑似状态卡死！玩家未切换

🔎 步骤 39:
   状态: playing
   地主: player_1
   当前玩家: player_1
   手牌: player_1(18) | player_2(16) | player_3(16)
   最后动作: player_3 出牌 ['♠7'] (single)
   总回合: 6
⚠️ 疑似状态卡死！玩家未切换

🔎 步骤 40:
   状态: playing
   地主: player_1
   当前玩家: player_1
   手牌: player_1(18) | player_2(16) | player_3(16)
   最后动作: player_3 出牌 ['♠7'] (single)
   总回合: 6
⚠️ 疑似状态卡死！玩家未切换
Traceback (most recent call last):