"""
测试修复后的斗地主Agent系统
"""
import asyncio
import logging
from agent_system import create_doudizhu_agent_system

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_fixed_system():
    """测试修复后的系统是否正常运行"""
    print("🚀 测试修复后的斗地主Agent系统")
    print("=" * 60)
    
    try:
        # 创建系统
        system = create_doudizhu_agent_system()
        print("✅ 系统创建成功")
        
        # 测试游戏流程
        print("\n🎮 开始测试游戏流程...")
        step_count = 0
        player_switches = []
        
        async for chunk in system.stream_game():
            step_count += 1
            
            # 记录关键信息
            for node_name, node_data in chunk.items():
                print(f"步骤 {step_count}: 节点 {node_name}")
                
                # 如果有游戏状态，记录当前玩家
                if isinstance(node_data, dict) and "game" in node_data and node_data["game"]:
                    current_player = node_data["game"].state.current_player
                    player_switches.append((step_count, node_name, current_player))
                    print(f"  当前玩家: {current_player}")
                
                # 如果有玩家决策，显示出来
                if isinstance(node_data, dict) and "player_decision" in node_data:
                    decision = node_data["player_decision"]
                    print(f"  AI决策: {decision}")
                
                # 如果有移动结果，显示出来
                if isinstance(node_data, dict) and "move_result" in node_data:
                    move_result = node_data["move_result"]
                    print(f"  移动结果: {move_result}")
                
                # 如果游戏结束，退出
                if isinstance(node_data, dict) and node_data.get("game_over"):
                    print("🏁 游戏结束")
                    break
            
            # 限制测试步数，避免无限运行
            if step_count > 20:
                print("⏹️ 达到测试步数限制，停止测试")
                break
        
        # 分析玩家切换情况
        print(f"\n📊 玩家切换分析 (总共 {len(player_switches)} 次):")
        for i, (step, node, player) in enumerate(player_switches):
            if i > 0:
                prev_player = player_switches[i-1][2]
                if prev_player != player:
                    print(f"  ✅ 步骤 {step}: {prev_player} -> {player} (节点: {node})")
                else:
                    print(f"  ⚠️ 步骤 {step}: {player} (无切换, 节点: {node})")
            else:
                print(f"  📍 步骤 {step}: 初始玩家 {player} (节点: {node})")
        
        print("\n✅ 测试完成")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_fixed_system()) 