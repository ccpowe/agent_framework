import type { Player } from "@/app/page"
import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { HandDisplay } from "@/components/hand-display"
import { Crown, Users } from "lucide-react"

interface PlayerAreaProps {
  player: Player
  position: "top-left" | "top-right" | "bottom"
  showCards: boolean
}

export function PlayerArea({ player, position, showCards }: PlayerAreaProps) {
  const getRoleIcon = () => {
    if (player.role === "landlord") {
      return <Crown className="h-4 w-4 text-yellow-400" />
    } else if (player.role === "farmer") {
      return <Users className="h-4 w-4 text-green-400" />
    }
    return null
  }

  const getRoleColor = () => {
    if (player.role === "landlord") return "bg-yellow-600"
    if (player.role === "farmer") return "bg-green-600"
    return "bg-gray-600"
  }

  const getPlayerNameColor = () => {
    if (player.name.includes("Gemini")) return "text-blue-400"
    if (player.name.includes("GPT")) return "text-green-400"
    if (player.name.includes("Claude")) return "text-purple-400"
    return "text-white"
  }

  return (
    <Card className={`bg-gray-800 border-gray-700 p-4 ${player.is_turn ? "ring-2 ring-blue-400" : ""}`}>
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center space-x-2">
          <span className={`font-semibold ${getPlayerNameColor()}`}>{player.name}</span>
          {getRoleIcon()}
        </div>
        <div className="flex items-center space-x-2">
          {player.role !== "pending" && (
            <Badge className={getRoleColor()}>{player.role === "landlord" ? "地主" : "农民"}</Badge>
          )}
          <Badge variant="outline" className="text-white border-gray-600">
            {player.hand_count} 张
          </Badge>
        </div>
      </div>

      {player.is_turn && (
        <div className="mb-3">
          <div className="flex items-center text-blue-400 text-sm">
            <div className="w-2 h-2 bg-blue-400 rounded-full mr-2 animate-pulse"></div>
            思考中...
          </div>
        </div>
      )}

      <HandDisplay cards={showCards ? player.hand : []} showCards={showCards} cardCount={player.hand_count} />
    </Card>
  )
}
