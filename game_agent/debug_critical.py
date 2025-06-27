import requests
import time
import os
import json
from dotenv import load_dotenv

load_dotenv()


def create_test_game():
    """创建测试游戏"""
    print("🎮 创建测试游戏...")
    
    game_config = {
        "model_name": "deepseek/deepseek-chat-v3-0324",
        "player_names": {
            "player_1": "地主AI",
            "player_2": "农民AI_1", 
            "player_3": "农民AI_2"
        }
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/api/game/start",
            json=game_config,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 游戏创建成功! Game ID: {data['game_id']}")
            return data["game_id"]
        else:
            print(f"❌ 游戏创建失败: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ 游戏创建异常: {e}")
        return None


def monitor_critical_steps(game_id):
    """监控关键步骤，专注于状态传递问题"""
    print(f"🔍 监控游戏 {game_id} 的关键状态传递...")
    print("=" * 60)
    
    step_count = 0
    max_steps = 50  # 限制步数，专注于前几轮
    
    while step_count < max_steps:
        step_count += 1
        
        try:
            response = requests.get(
                f"http://localhost:8000/api/game/{game_id}/state",
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                status = data.get("status", "unknown")
                game_state = data.get("game_state", {})
                
                print(f"\n🔎 步骤 {step_count}:")
                print(f"   状态: {status}")
                
                if game_state:
                    current_player = game_state.get("current_player", "未知")
                    landlord = game_state.get("landlord", "未知")
                    
                    print(f"   地主: {landlord}")
                    print(f"   当前玩家: {current_player}")
                    
                    # 手牌数量
                    if "player_hands" in game_state:
                        hands_info = []
                        for player, hand_info in game_state["player_hands"].items():
                            count = hand_info.get("count", 0)
                            hands_info.append(f"{player}({count})")
                        print(f"   手牌: {' | '.join(hands_info)}")
                    
                    # 新的回合
                    if "turn_history" in game_state:
                        turn_count = len(game_state["turn_history"])
                        if turn_count > 0:
                            last_turn = game_state["turn_history"][-1]
                            player = last_turn.get("player", "未知")
                            play = last_turn.get("play", "未知")
                            
                            if play == "pass":
                                print(f"   最后动作: {player} 过牌")
                            elif isinstance(play, dict):
                                cards = play.get("cards", [])
                                card_type = play.get("card_type", "")
                                print(f"   最后动作: {player} 出牌 {cards} ({card_type})")
                            
                            print(f"   总回合: {turn_count}")
                
                # 检查是否有进展（当前玩家切换或新回合）
                if step_count > 10 and current_player == "player_1":
                    print("⚠️ 疑似状态卡死！玩家未切换")
                
                # 检查游戏结束
                if status in ["finished", "error"]:
                    print(f"\n🏁 游戏结束: {status}")
                    if status == "finished" and game_state:
                        winner = game_state.get("winner", "未知")
                        print(f"🎉 获胜方: {winner}")
                    return True
                
            else:
                print(f"❌ 获取状态失败: {response.status_code}")
                
        except Exception as e:
            print(f"❌ 监控异常: {e}")
        
        time.sleep(3)  # 每3秒检查一次
    
    print(f"\n⏰ 监控达到步数限制 ({max_steps})")
    return False


def main():
    """主函数"""
    print("🚨 斗地主系统 - 关键问题调试")
    print("专门针对：AI决策丢失、玩家不切换问题")
    print("=" * 60)
    
    # 检查服务器
    try:
        response = requests.get("http://localhost:8000/api/health", timeout=5)
        if response.status_code != 200:
            print("❌ 服务器异常")
            return
        print("✅ 服务器正常")
    except:
        print("❌ 无法连接服务器")
        return
    
    # 创建游戏并监控
    game_id = create_test_game()
    if game_id:
        success = monitor_critical_steps(game_id)
        
        print("\n" + "=" * 60)
        if success:
            print("✅ 监控完成")
        else:
            print("⚠️ 发现关键问题")
            print("建议检查服务器日志中的详细错误信息")


if __name__ == "__main__":
    main() 