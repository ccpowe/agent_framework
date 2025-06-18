"use client"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { X, Trash2, Clock } from "lucide-react"
import { motion, AnimatePresence } from "framer-motion"

interface SavedEntry {
  id: string
  originalText: string
  correctedText: string
  timestamp: Date
  title: string
}

interface SidebarProps {
  isOpen: boolean
  onClose: () => void
  entries: SavedEntry[]
  onLoadEntry: (entry: SavedEntry) => void
  onDeleteEntry: (id: string) => void
}

export default function Sidebar({ isOpen, onClose, entries, onLoadEntry, onDeleteEntry }: SidebarProps) {
  const formatDate = (date: Date) => {
    return date.toLocaleDateString() + " " + date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
  }

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/20 z-40"
            onClick={onClose}
          />

          {/* Sidebar */}
          <motion.div
            initial={{ x: "100%" }}
            animate={{ x: 0 }}
            exit={{ x: "100%" }}
            transition={{ type: "spring", damping: 25, stiffness: 200 }}
            className="fixed right-0 top-0 h-full w-96 bg-white shadow-2xl z-50 overflow-y-auto"
          >
            <div className="p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold text-gray-800">Saved Writings</h2>
                <Button onClick={onClose} variant="ghost" size="sm">
                  <X className="w-5 h-5" />
                </Button>
              </div>

              {entries.length === 0 ? (
                <div className="text-center py-12 text-gray-500">
                  <Clock className="w-12 h-12 mx-auto mb-4 opacity-50" />
                  <p>No saved writings yet</p>
                  <p className="text-sm">Complete a correction and save it to see it here</p>
                </div>
              ) : (
                <div className="space-y-4">
                  {entries.map((entry) => (
                    <Card key={entry.id} className="hover:shadow-md transition-shadow cursor-pointer">
                      <CardHeader className="pb-2">
                        <div className="flex items-start justify-between">
                          <CardTitle className="text-sm font-medium text-gray-700 line-clamp-2">
                            {entry.title}
                          </CardTitle>
                          <Button
                            onClick={(e) => {
                              e.stopPropagation()
                              onDeleteEntry(entry.id)
                            }}
                            variant="ghost"
                            size="sm"
                            className="text-red-500 hover:text-red-700 hover:bg-red-50"
                          >
                            <Trash2 className="w-4 h-4" />
                          </Button>
                        </div>
                        <p className="text-xs text-gray-500">{formatDate(entry.timestamp)}</p>
                      </CardHeader>
                      <CardContent className="pt-0">
                        <div
                          onClick={() => onLoadEntry(entry)}
                          className="text-sm text-gray-600 line-clamp-3 hover:text-gray-800 transition-colors"
                        >
                          {entry.originalText}
                        </div>
                        <Button onClick={() => onLoadEntry(entry)} variant="outline" size="sm" className="w-full mt-3">
                          Load Writing
                        </Button>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              )}
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  )
}
