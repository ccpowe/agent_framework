import type { GameState } from "@/app/page"
import { PlayerArea } from "@/components/player-area"
import { GameStatus } from "@/components/game-status"
import { ActionLog } from "@/components/action-log"

interface GameBoardProps {
  gameState: GameState
}

export function GameBoard({ gameState }: GameBoardProps) {
  const [player1, player2, player3] = gameState.players

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <div className="container mx-auto p-4 h-screen flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between mb-4">
          <h1 className="text-2xl font-bold text-blue-400">AI 斗地主观察室</h1>
          <div className="text-sm text-gray-400">游戏 ID: {gameState.game_id.slice(-8)}</div>
        </div>

        <div className="flex-1 grid grid-cols-4 gap-4">
          {/* Main Game Area */}
          <div className="col-span-3 flex flex-col">
            {/* Top Players */}
            <div className="grid grid-cols-2 gap-4 mb-4">
              <PlayerArea player={player2} position="top-left" showCards={false} />
              <PlayerArea player={player3} position="top-right" showCards={false} />
            </div>

            {/* Center Game Status */}
            <div className="flex-1 flex items-center justify-center mb-4">
              <GameStatus gameState={gameState} />
            </div>

            {/* Bottom Player */}
            <div className="mt-auto">
              <PlayerArea player={player1} position="bottom" showCards={true} />
            </div>
          </div>

          {/* Action Log Sidebar */}
          <div className="col-span-1">
            <ActionLog logEntries={gameState.action_log} />
          </div>
        </div>
      </div>
    </div>
  )
}
