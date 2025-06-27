"""
斗地主多智能体系统 - FastAPI 后端服务
提供游戏管理和实时状态查询的REST API接口
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional
import asyncio
import uuid
import logging
from datetime import datetime

from agent_system import create_doudizhu_agent_system, DoudizhuAgentSystem
from game_logic import Game

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title="斗地主多智能体系统",
    description="基于LangGraph的AI斗地主游戏后端",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境中应该设置具体的前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局游戏管理
game_sessions: Dict[str, Dict[str, Any]] = {}
agent_systems: Dict[str, DoudizhuAgentSystem] = {}


# ========== 请求/响应模型 ==========

class CreateGameRequest(BaseModel):
    """创建游戏请求"""
    model_name: Optional[str] = "gpt-3.5-turbo"
    player_names: Optional[Dict[str, str]] = None


class GameStateResponse(BaseModel):
    """游戏状态响应"""
    game_id: str
    game_state: Dict[str, Any]
    status: str
    created_at: str
    last_updated: str


class GameActionRequest(BaseModel):
    """游戏动作请求"""
    action: str  # "step", "reset", "pause"
    params: Optional[Dict[str, Any]] = None


# ========== API 路由 ==========

@app.get("/")
async def root():
    """API根路径"""
    return {
        "message": "斗地主多智能体系统 API",
        "version": "1.0.0",
        "status": "运行中",
        "active_games": len(game_sessions)
    }


@app.post("/api/game/start", response_model=GameStateResponse)
async def start_game(request: CreateGameRequest, background_tasks: BackgroundTasks):
    """
    创建并启动新游戏
    """
    try:
        # 生成游戏ID
        game_id = str(uuid.uuid4())
        
        # 创建智能体系统
        model_name = request.model_name or "gpt-3.5-turbo"
        agent_system = create_doudizhu_agent_system(model_name)
        agent_systems[game_id] = agent_system
        
        # 初始化游戏会话
        game_sessions[game_id] = {
            "game_id": game_id,
            "status": "initializing",
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "model_name": request.model_name,
            "player_names": request.player_names or {
                "player_1": "AI地主",
                "player_2": "AI农民1", 
                "player_3": "AI农民2"
            },
            "game_state": {},
            "error": None
        }
        
        # 在后台启动游戏
        background_tasks.add_task(run_game_async, game_id, agent_system)
        
        logger.info(f"创建新游戏: {game_id}")
        
        return GameStateResponse(
            game_id=game_id,
            game_state=game_sessions[game_id]["game_state"],
            status="starting",
            created_at=game_sessions[game_id]["created_at"],
            last_updated=game_sessions[game_id]["last_updated"]
        )
        
    except Exception as e:
        logger.error(f"创建游戏失败: {e}")
        raise HTTPException(status_code=500, detail=f"创建游戏失败: {str(e)}")


@app.get("/api/game/{game_id}/state", response_model=GameStateResponse)
async def get_game_state(game_id: str):
    """
    获取游戏状态
    前端通过轮询此接口获取实时游戏状态
    """
    if game_id not in game_sessions:
        raise HTTPException(status_code=404, detail="游戏不存在")
    
    session = game_sessions[game_id]
    
    return GameStateResponse(
        game_id=game_id,
        game_state=session["game_state"],
        status=session["status"],
        created_at=session["created_at"],
        last_updated=session["last_updated"]
    )


@app.post("/api/game/{game_id}/action")
async def game_action(game_id: str, request: GameActionRequest):
    """
    执行游戏动作
    支持暂停、重置等操作
    """
    if game_id not in game_sessions:
        raise HTTPException(status_code=404, detail="游戏不存在")
    
    session = game_sessions[game_id]
    
    try:
        if request.action == "reset":
            # 重置游戏
            await reset_game(game_id)
            return {"message": "游戏重置成功", "game_id": game_id}
            
        elif request.action == "pause":
            # 暂停游戏（更新状态）
            session["status"] = "paused"
            session["last_updated"] = datetime.now().isoformat()
            return {"message": "游戏已暂停", "game_id": game_id}
            
        elif request.action == "resume":
            # 恢复游戏
            if session["status"] == "paused":
                session["status"] = "running"
                session["last_updated"] = datetime.now().isoformat()
            return {"message": "游戏已恢复", "game_id": game_id}
            
        else:
            raise HTTPException(status_code=400, detail=f"不支持的动作: {request.action}")
            
    except Exception as e:
        logger.error(f"执行游戏动作失败: {e}")
        raise HTTPException(status_code=500, detail=f"动作执行失败: {str(e)}")


@app.get("/api/games")
async def list_games():
    """
    获取所有游戏列表
    """
    games = []
    for game_id, session in game_sessions.items():
        games.append({
            "game_id": game_id,
            "status": session["status"],
            "created_at": session["created_at"],
            "last_updated": session["last_updated"],
            "player_names": session["player_names"]
        })
    
    return {
        "total": len(games),
        "games": games
    }


@app.delete("/api/game/{game_id}")
async def delete_game(game_id: str):
    """
    删除游戏会话
    """
    if game_id not in game_sessions:
        raise HTTPException(status_code=404, detail="游戏不存在")
    
    # 清理资源
    if game_id in agent_systems:
        del agent_systems[game_id]
    
    del game_sessions[game_id]
    
    logger.info(f"删除游戏: {game_id}")
    
    return {"message": "游戏删除成功", "game_id": game_id}


@app.get("/api/health")
async def health_check():
    """
    健康检查接口
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "active_games": len(game_sessions),
        "memory_usage": {
            "game_sessions": len(game_sessions),
            "agent_systems": len(agent_systems)
        }
    }


# ========== 后台任务函数 ==========

async def run_game_async(game_id: str, agent_system: DoudizhuAgentSystem):
    """
    异步运行游戏的后台任务（已更新为流式处理）
    """
    session = game_sessions[game_id]
    session["status"] = "running"
    session["last_updated"] = datetime.now().isoformat()
    logger.info(f"开始以流式方式运行游戏: {game_id}")

    final_state = None
    step_count = 0
    max_steps = 500  # 防止无限循环
    
    try:
        # 使用 async for 循环处理 stream_game() 返回的每一个完整的 GraphState
        async for current_state_chunk in agent_system.stream_game():
            step_count += 1
            logger.info(f"[{game_id}] 步骤 {step_count}: {list(current_state_chunk.keys())}")
            
            # 防止无限循环
            if step_count > max_steps:
                logger.warning(f"[{game_id}] 达到最大步数限制，强制结束")
                session["status"] = "error"
                session["error"] = "游戏步数超限"
                break
            
            # 处理不同步骤的状态更新
            for node_name, node_state in current_state_chunk.items():
                if isinstance(node_state, dict):
                    # 如果节点返回了游戏对象，更新状态
                    if "game" in node_state and node_state["game"] is not None:
                        game_obj = node_state["game"]
                        game_state_dict = game_obj.state.to_dict()
                        session["game_state"] = game_state_dict
                        logger.info(f"[{game_id}] 从节点 {node_name} 更新游戏状态")
                        logger.info(f"[{game_id}] 当前玩家: {game_obj.state.current_player}")
                        
                        # 确保API状态同步
                        session["current_player"] = game_obj.state.current_player
                        session["landlord"] = game_obj.state.landlord
                        
                        # 检查游戏是否结束
                        if game_obj.state.game_over:
                            session["status"] = "finished"
                            session["winner"] = game_obj.state.winner
                            session["last_updated"] = datetime.now().isoformat()
                            logger.info(f"[{game_id}] 游戏结束，获胜方: {session['winner']}")
                            return
                    
                    # 更新当前玩家
                    if "current_player_id" in node_state:
                        session["current_player"] = node_state["current_player_id"]
                        logger.info(f"[{game_id}] 更新当前玩家: {node_state['current_player_id']}")
                    
                    # 更新游戏阶段
                    if "game_phase" in node_state:
                        if node_state["game_phase"] == "playing":
                            session["status"] = "playing"
                        else:
                            session["status"] = node_state["game_phase"]
            
            session["last_updated"] = datetime.now().isoformat()
            final_state = current_state_chunk

        # 流式处理结束但游戏可能还没结束
        if final_state:
            logger.info(f"[{game_id}] 流式处理完成，最后状态: {list(final_state.keys())}")
            # 检查是否有最终的游戏状态
            for node_name, node_state in final_state.items():
                if isinstance(node_state, dict) and "game" in node_state and node_state["game"]:
                    game_obj = node_state["game"]
                    session["game_state"] = game_obj.state.to_dict()
                    session["current_player"] = game_obj.state.current_player
                    session["landlord"] = game_obj.state.landlord
                    
                    if game_obj.state.game_over:
                        session["status"] = "finished"
                        session["winner"] = game_obj.state.winner
                    break

    except Exception as e:
        logger.error(f"[{game_id}] 游戏运行异常: {e}", exc_info=True)
        session["status"] = "error"
        session["error"] = str(e)
        session["last_updated"] = datetime.now().isoformat()


async def reset_game(game_id: str):
    """
    重置指定游戏
    """
    if game_id not in game_sessions:
        return
    
    session = game_sessions[game_id]
    model_name = session["model_name"]
    
    # 重新创建智能体系统
    agent_system = create_doudizhu_agent_system(model_name)
    agent_systems[game_id] = agent_system
    
    # 重置会话状态
    session["status"] = "initializing"
    session["last_updated"] = datetime.now().isoformat()
    session["game_state"] = {}
    session["error"] = None
    
    # 重新启动游戏
    asyncio.create_task(run_game_async(game_id, agent_system))


# ========== WebSocket支持（可选扩展）==========

@app.websocket("/ws/game/{game_id}")
async def websocket_endpoint(websocket, game_id: str):
    """
    WebSocket端点，用于实时推送游戏状态
    这是可选功能，用于替代HTTP轮询
    """
    await websocket.accept()
    
    try:
        while True:
            if game_id in game_sessions:
                session = game_sessions[game_id]
                await websocket.send_json({
                    "type": "game_state",
                    "data": {
                        "game_id": game_id,
                        "status": session["status"],
                        "game_state": session["game_state"],
                        "last_updated": session["last_updated"]
                    }
                })
            
            # 每秒推送一次状态
            await asyncio.sleep(1)
            
    except Exception as e:
        logger.error(f"WebSocket连接错误: {e}")
    finally:
        await websocket.close()


# ========== 应用启动和关闭事件 ==========

@app.on_event("startup")
async def startup_event():
    """应用启动事件"""
    logger.info("斗地主多智能体系统启动")
    logger.info("API文档: http://localhost:8000/docs")


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭事件"""
    logger.info("斗地主多智能体系统关闭")
    
    # 清理所有会话
    game_sessions.clear()
    agent_systems.clear()


# ========== 开发和调试工具 ==========

@app.get("/api/debug/game/{game_id}")
async def debug_game(game_id: str):
    """
    调试接口：获取详细的游戏信息
    仅在开发环境使用
    """
    if game_id not in game_sessions:
        raise HTTPException(status_code=404, detail="游戏不存在")
    
    session = game_sessions[game_id]
    
    return {
        "game_id": game_id,
        "full_session": session,
        "has_agent_system": game_id in agent_systems
    }


if __name__ == "__main__":
    import uvicorn
    
    # 启动开发服务器
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 