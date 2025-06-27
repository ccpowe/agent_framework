import { Card } from "@/components/ui/card"
import { ScrollArea } from "@/components/ui/scroll-area"

interface ActionLogProps {
  logEntries: string[]
}

export function ActionLog({ logEntries }: ActionLogProps) {
  return (
    <Card className="bg-gray-800 border-gray-700 h-full">
      <div className="p-4 border-b border-gray-700">
        <h3 className="font-semibold text-white">行动日志</h3>
      </div>
      <ScrollArea className="h-[calc(100%-60px)] p-4">
        <div className="space-y-2">
          {logEntries.map((entry, index) => (
            <div key={index} className="text-sm text-gray-300 p-2 bg-gray-900/50 rounded">
              <span className="text-gray-500 text-xs">{String(index + 1).padStart(2, "0")}:</span>
              <span className="ml-2">{entry}</span>
            </div>
          ))}
        </div>
      </ScrollArea>
    </Card>
  )
}
