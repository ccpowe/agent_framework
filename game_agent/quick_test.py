"""
快速测试递归限制修复
"""
import asyncio
import logging
from agent_system import create_doudizhu_agent_system

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_recursion_limit():
    """测试递归限制问题是否解决"""
    print("🔧 测试递归限制修复")
    print("=" * 50)
    
    try:
        system = create_doudizhu_agent_system()
        print("✅ 系统创建成功")
        
        step_count = 0
        game_over_detected = False
        
        async for chunk in system.stream_game():
            step_count += 1
            print(f"步骤 {step_count}: {list(chunk.keys())}")
            
            # 检查是否有game_over状态
            for node_name, node_data in chunk.items():
                if isinstance(node_data, dict):
                    if node_data.get("game_over"):
                        print(f"🏁 游戏结束检测到在步骤 {step_count}")
                        print(f"获胜方: {node_data.get('winner', '未知')}")
                        game_over_detected = True
                        break
                    
                    # 检查游戏对象状态
                    if "game" in node_data and node_data["game"]:
                        game_obj = node_data["game"]
                        if game_obj.state.game_over:
                            print(f"🏁 游戏对象显示游戏结束在步骤 {step_count}")
                            print(f"获胜方: {game_obj.state.winner}")
                            game_over_detected = True
                            break
            
            if game_over_detected:
                break
            
            # 安全限制
            if step_count > 30:
                print("⏰ 达到安全步数限制，游戏可能仍在运行")
                break
        
        if game_over_detected:
            print("✅ 游戏正常结束，递归限制问题已解决")
        else:
            print("⚠️ 游戏未正常结束，可能仍有问题")
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        if "recursion limit" in str(e).lower():
            print("💥 仍然存在递归限制问题")
        else:
            print(f"其他错误: {e}")

if __name__ == "__main__":
    asyncio.run(test_recursion_limit()) 