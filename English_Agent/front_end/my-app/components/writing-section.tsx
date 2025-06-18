"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Loader2, PenTool, RotateCcw, Save, Plus } from "lucide-react"
import WritingPaper from "@/components/writing-paper"

interface WritingSectionProps {
  onSave: (originalText: string, correctedText: string) => void
  onNewEntry: () => void
  loadedEntry: { originalText: string; correctedText: string } | null
}

interface WritingEntry {
  id: string
  inputText: string
  correctedText: string
  isChecked: boolean
  isLoading: boolean
}

export default function WritingSection({ onSave, onNewEntry, loadedEntry }: WritingSectionProps) {
  const [entries, setEntries] = useState<WritingEntry[]>([
    {
      id: "1",
      inputText: "",
      correctedText: "",
      isChecked: false,
      isLoading: false,
    },
  ])

  useEffect(() => {
    if (loadedEntry) {
      setEntries([
        {
          id: Date.now().toString(),
          inputText: loadedEntry.originalText,
          correctedText: loadedEntry.correctedText,
          isChecked: true,
          isLoading: false,
        },
      ])
    }
  }, [loadedEntry])

  const handleCheck = async (entryId: string) => {
    const entry = entries.find((e) => e.id === entryId)
    if (!entry || !entry.inputText.trim()) return

    setEntries((prev) => prev.map((e) => (e.id === entryId ? { ...e, isLoading: true } : e)))

    try {
      const response = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-User-ID": "user-123",
          "X-Session-ID": `session-${Date.now()}`,
        },
        body: JSON.stringify({
          message: entry.inputText,
          stream: false,
        }),
      })

      if (!response.ok) {
        throw new Error("Failed to get correction")
      }

      const data = await response.json()
      setEntries((prev) =>
        prev.map((e) =>
          e.id === entryId ? { ...e, correctedText: data.response, isChecked: true, isLoading: false } : e,
        ),
      )
    } catch (error) {
      console.error("Error:", error)
      // Demo correction
      const demoCorrection = `my name are[is] Cc, nice to meet you<,>! i[I] will graduate from university at[on] July 5<.> when i[I] graduate[graduated] i[I] will trivial[travel] around[around the] word[world]{My name is Cc. Nice to meet you! I will graduate from university on July 5. When I graduate, I will travel around the world.}`

      setEntries((prev) =>
        prev.map((e) =>
          e.id === entryId ? { ...e, correctedText: demoCorrection, isChecked: true, isLoading: false } : e,
        ),
      )
    }
  }

  const handleSave = (entryId: string) => {
    const entry = entries.find((e) => e.id === entryId)
    if (entry && entry.isChecked) {
      onSave(entry.inputText, entry.correctedText)
    }
  }

  const handleAddNewEntry = () => {
    const newEntry: WritingEntry = {
      id: Date.now().toString(),
      inputText: "",
      correctedText: "",
      isChecked: false,
      isLoading: false,
    }
    setEntries((prev) => [...prev, newEntry])
  }

  const handleReset = (entryId: string) => {
    setEntries((prev) =>
      prev.map((e) =>
        e.id === entryId ? { ...e, inputText: "", correctedText: "", isChecked: false, isLoading: false } : e,
      ),
    )
  }

  const updateInputText = (entryId: string, text: string) => {
    setEntries((prev) => prev.map((e) => (e.id === entryId ? { ...e, inputText: text } : e)))
  }

  return (
    <div className="space-y-6">
      {entries.map((entry, index) => (
        <Card key={entry.id} className="shadow-2xl border-0 bg-white/90 backdrop-blur-sm">
          <CardHeader className="pb-4">
            <div className="flex items-center justify-between">
              <CardTitle className="flex items-center gap-2 text-gray-700">
                <PenTool className="w-5 h-5" />
                {entry.isChecked ? "Teacher's Corrections" : "Your Writing"} #{index + 1}
              </CardTitle>
              <div className="flex gap-2">
                {!entry.isChecked ? (
                  <Button
                    onClick={() => handleCheck(entry.id)}
                    disabled={!entry.inputText.trim() || entry.isLoading}
                    className="bg-indigo-600 hover:bg-indigo-700 text-white"
                  >
                    {entry.isLoading ? (
                      <>
                        <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                        Checking...
                      </>
                    ) : (
                      "Check Grammar"
                    )}
                  </Button>
                ) : (
                  <>
                    <Button onClick={() => handleSave(entry.id)} className="bg-green-600 hover:bg-green-700 text-white">
                      <Save className="w-4 h-4 mr-2" />
                      Save
                    </Button>
                    <Button onClick={() => handleReset(entry.id)} variant="outline">
                      <RotateCcw className="w-4 h-4 mr-2" />
                      Reset
                    </Button>
                  </>
                )}
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <WritingPaper
              inputText={entry.inputText}
              setInputText={(text) => updateInputText(entry.id, text)}
              correctedText={entry.correctedText}
              isChecked={entry.isChecked}
              isLoading={entry.isLoading}
            />
          </CardContent>
        </Card>
      ))}

      {/* Add New Entry Button */}
      <div className="text-center">
        <Button
          onClick={handleAddNewEntry}
          variant="outline"
          className="bg-white/80 hover:bg-white border-2 border-dashed border-indigo-300 hover:border-indigo-500 text-indigo-600 py-6 px-8 text-lg"
        >
          <Plus className="w-5 h-5 mr-2" />
          Continue Writing Below
        </Button>
      </div>
    </div>
  )
}
