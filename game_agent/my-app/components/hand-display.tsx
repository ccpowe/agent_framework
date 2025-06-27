import { CardComponent } from "@/components/card-component"

interface HandDisplayProps {
  cards: string[]
  showCards: boolean
  cardCount: number
}

export function HandDisplay({ cards, showCards, cardCount }: HandDisplayProps) {
  if (!showCards) {
    // Show card backs
    return (
      <div className="flex flex-wrap gap-1">
        {Array.from({ length: Math.min(cardCount, 10) }).map((_, index) => (
          <CardComponent key={index} cardCode="" isFaceUp={false} />
        ))}
        {cardCount > 10 && (
          <div className="flex items-center justify-center w-12 h-16 bg-gray-700 rounded text-xs text-gray-400">
            +{cardCount - 10}
          </div>
        )}
      </div>
    )
  }

  return (
    <div className="flex flex-wrap gap-1">
      {cards.map((cardCode, index) => (
        <CardComponent key={index} cardCode={cardCode} isFaceUp={true} />
      ))}
    </div>
  )
}
