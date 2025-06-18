"use client"

import { useState, useRef } from "react"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { BookOpen, Loader2, PenTool, Menu, Plus, Save } from "lucide-react"
import CorrectionDisplay from "@/components/correction-display"
import Sidebar from "@/components/sidebar"

interface TextEntry {
  id: string
  originalText: string
  correctedText: string
  isChecked: boolean
  isLoading: boolean
}

interface Session {
  id: string
  title: string
  entries: TextEntry[]
  currentInput: string
  timestamp: Date
}

interface SavedEntry {
  id: string
  originalText: string
  correctedText: string
  timestamp: Date
  title: string
}

export default function GrammarAssistant() {
  const [sessions, setSessions] = useState<Session[]>([
    {
      id: "1",
      title: "Session 1",
      entries: [],
      currentInput: "",
      timestamp: new Date(),
    },
  ])
  const [currentSessionId, setCurrentSessionId] = useState("1")
  const [savedEntries, setSavedEntries] = useState<SavedEntry[]>([])
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const bottomRef = useRef<HTMLDivElement>(null)

  const currentSession = sessions.find((s) => s.id === currentSessionId)!

  const scrollToBottom = () => {
    setTimeout(() => {
      bottomRef.current?.scrollIntoView({ behavior: "smooth" })
    }, 100)
  }

  const handleCheckGrammar = async () => {
    if (!currentSession.currentInput.trim()) return

    const inputText = currentSession.currentInput
    const newEntryId = Date.now().toString()

    setSessions((prev) =>
      prev.map((session) =>
        session.id === currentSessionId
          ? {
              ...session,
              entries: [
                ...session.entries,
                {
                  id: newEntryId,
                  originalText: inputText,
                  correctedText: "",
                  isChecked: false,
                  isLoading: true,
                },
              ],
              currentInput: "",
            }
          : session,
      ),
    )

    try {
      const response = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-User-ID": "user-123",
          "X-Session-ID": `session-${Date.now()}`,
        },
        body: JSON.stringify({
          message: inputText,
          stream: false,
        }),
      })

      if (!response.ok) {
        throw new Error("Failed to get correction")
      }

      const data = await response.json()

      setSessions((prev) =>
        prev.map((session) =>
          session.id === currentSessionId
            ? {
                ...session,
                entries: session.entries.map((entry) =>
                  entry.id === newEntryId
                    ? {
                        ...entry,
                        correctedText: data.response,
                        isChecked: true,
                        isLoading: false,
                      }
                    : entry,
                ),
              }
            : session,
        ),
      )

      scrollToBottom()
    } catch (error) {
      console.error("Error:", error)

      const demoCorrection = `my name are[is] Cc, nice to meet you<,>! i[I] will graduate from university at[on] July 5<.> when i[I] graduate[graduated] i[I] will trivial[travel] around[around the] word[world]{My name is Cc. Nice to meet you! I will graduate from university on July 5. When I graduate, I will travel around the world.}`

      setSessions((prev) =>
        prev.map((session) =>
          session.id === currentSessionId
            ? {
                ...session,
                entries: session.entries.map((entry) =>
                  entry.id === newEntryId
                    ? {
                        ...entry,
                        correctedText: demoCorrection,
                        isChecked: true,
                        isLoading: false,
                      }
                    : entry,
                ),
              }
            : session,
        ),
      )

      scrollToBottom()
    }
  }

  const handleNewSession = () => {
    const newSessionId = Date.now().toString()
    const newSession: Session = {
      id: newSessionId,
      title: `Session ${sessions.length + 1}`,
      entries: [],
      currentInput: "",
      timestamp: new Date(),
    }

    setSessions((prev) => [...prev, newSession])
    setCurrentSessionId(newSessionId)
    scrollToBottom()
  }

  const handleSaveSession = () => {
    const checkedEntries = currentSession.entries.filter((entry) => entry.isChecked)

    checkedEntries.forEach((entry) => {
      const newSavedEntry: SavedEntry = {
        id: `${currentSessionId}-${entry.id}`,
        originalText: entry.originalText,
        correctedText: entry.correctedText,
        timestamp: new Date(),
        title: entry.originalText.slice(0, 30) + (entry.originalText.length > 30 ? "..." : ""),
      }
      setSavedEntries((prev) => {
        if (prev.some((saved) => saved.id === newSavedEntry.id)) {
          return prev
        }
        return [newSavedEntry, ...prev]
      })
    })
  }

  const handleLoadEntry = (entry: SavedEntry) => {
    const newEntryId = Date.now().toString()
    setSessions((prev) =>
      prev.map((session) =>
        session.id === currentSessionId
          ? {
              ...session,
              entries: [
                ...session.entries,
                {
                  id: newEntryId,
                  originalText: entry.originalText,
                  correctedText: entry.correctedText,
                  isChecked: true,
                  isLoading: false,
                },
              ],
            }
          : session,
      ),
    )
    setSidebarOpen(false)
    scrollToBottom()
  }

  const updateCurrentInput = (text: string) => {
    setSessions((prev) =>
      prev.map((session) => (session.id === currentSessionId ? { ...session, currentInput: text } : session)),
    )
  }

  const hasCheckedEntries = currentSession.entries.some((entry) => entry.isChecked)

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex">
      {/* Main Content */}
      <div className="flex-1">
        {/* Header */}
        <div className="sticky top-0 bg-gradient-to-br from-blue-50 to-indigo-100 z-30 p-4 border-b border-white/20 backdrop-blur-sm">
          <div className="max-w-4xl mx-auto">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <BookOpen className="w-8 h-8 text-indigo-600" />
                <h1 className="text-3xl font-bold text-gray-800">English Grammar Assistant</h1>
              </div>
              <div className="flex gap-2">
                <Button onClick={handleNewSession} variant="outline" className="bg-white/80">
                  <Plus className="w-4 h-4 mr-2" />
                  New Session
                </Button>
                <Button onClick={() => setSidebarOpen(true)} variant="outline" className="bg-white/80">
                  <Menu className="w-4 h-4 mr-2" />
                  Saved ({savedEntries.length})
                </Button>
              </div>
            </div>
            <p className="text-gray-600 mt-2">
              {currentSession.title} - Write continuously and get instant corrections
            </p>
          </div>
        </div>

        {/* Single Card Container */}
        <div className="max-w-4xl mx-auto p-4">
          <div className="bg-white/90 backdrop-blur-sm rounded-lg shadow-2xl border border-yellow-200">
            {/* Card Header */}
            <div className="flex items-center justify-between p-4 border-b border-yellow-200">
              <h3 className="flex items-center gap-2 text-lg font-semibold text-gray-700">
                <PenTool className="w-5 h-5" />
                {currentSession.title}
              </h3>
              <div className="flex items-center gap-4">
                <div className="text-sm text-gray-500">
                  {currentSession.entries.length} correction{currentSession.entries.length !== 1 ? "s" : ""}
                </div>
                {hasCheckedEntries && (
                  <Button onClick={handleSaveSession} className="bg-green-600 hover:bg-green-700 text-white" size="sm">
                    <Save className="w-4 h-4 mr-2" />
                    Save Session
                  </Button>
                )}
              </div>
            </div>

            {/* Card Content */}
            <div className="relative bg-gradient-to-br from-yellow-50 to-orange-50 min-h-[500px]">
              {/* Notebook paper lines - 调整为80px行高 */}
              <div
                className="absolute inset-0 opacity-20"
                style={{
                  backgroundImage: `repeating-linear-gradient(
                    transparent,
                    transparent 79px,
                    #e5e7eb 79px,
                    #e5e7eb 80px
                  )`,
                }}
              />

              {/* Red margin line */}
              <div className="absolute left-16 top-0 bottom-0 w-0.5 bg-red-300 opacity-60"></div>

              <div className="relative z-10 p-6">
                {/* All Previous Entries */}
                {currentSession.entries.map((entry, index) => (
                  <div key={entry.id} className="mb-16">
                    {entry.isLoading ? (
                      <div className="flex items-center justify-center py-8">
                        <div className="text-center">
                          <Loader2 className="w-6 h-6 animate-spin mx-auto mb-2 text-indigo-600" />
                          <p className="text-gray-600 text-sm">Checking grammar...</p>
                        </div>
                      </div>
                    ) : entry.isChecked ? (
                      <div>
                        <CorrectionDisplay originalText={entry.originalText} correctedText={entry.correctedText} />
                      </div>
                    ) : (
                      <div className="text-lg font-handwriting" style={{ lineHeight: "50px" }}> {/* 与输入区域保持一致的行间距 */}
                        {entry.originalText}
                      </div>
                    )}
                  </div>
                ))}

                {/* Current Input Area */}
                <div className="relative">
                  <Textarea
                    value={currentSession.currentInput}
                    onChange={(e) => updateCurrentInput(e.target.value)}
                    placeholder={
                      currentSession.entries.length === 0
                        ? "Start writing your sentences here... For example: 'my name are Cc, nice to meet you! i will graduate from university at July 5.'"
                        : "Continue writing your next sentences here..."
                    }
                    className="w-full min-h-[200px] text-lg bg-transparent border-none outline-none resize-none font-handwriting relative z-10"
                    style={{ lineHeight: "50px" }} /* 将行间距从80px减小到50px，使文本更加紧凑但保持可读性 */
                  />

                  {/* Check Grammar Button */}
                  <div className="mt-4 flex justify-end">
                    <Button
                      onClick={handleCheckGrammar}
                      disabled={!currentSession.currentInput.trim()}
                      className="bg-purple-600 hover:bg-purple-700 text-white shadow-lg disabled:opacity-50"
                    >
                      Check Grammar
                    </Button>
                  </div>
                </div>

                {/* Bottom reference for scrolling */}
                <div ref={bottomRef} className="h-4" />
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Sidebar */}
      <Sidebar
        isOpen={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
        entries={savedEntries}
        onLoadEntry={handleLoadEntry}
        onDeleteEntry={(id) => setSavedEntries((prev) => prev.filter((entry) => entry.id !== id))}
      />
    </div>
  )
}
