"use client"

import { useEffect, useState } from "react"
import { motion, AnimatePresence } from "framer-motion"
import { Loader2 } from "lucide-react"

interface WritingPaperProps {
  inputText: string
  setInputText: (text: string) => void
  correctedText: string
  isChecked: boolean
  isLoading: boolean
}

interface ParsedError {
  type: "word" | "punctuation" | "grammar"
  originalText: string
  correction: string
  startIndex: number
  endIndex: number
  id: string
}

export default function WritingPaper({
  inputText,
  setInputText,
  correctedText,
  isChecked,
  isLoading,
}: WritingPaperProps) {
  const [parsedErrors, setParsedErrors] = useState<ParsedError[]>([])
  const [displayText, setDisplayText] = useState("")
  const [showAnnotations, setShowAnnotations] = useState(false)

  useEffect(() => {
    if (isChecked && correctedText) {
      const cleanText = removeMarkup(correctedText)
      const errors = parseCorrections(correctedText, cleanText)
      setParsedErrors(errors)
      setDisplayText(cleanText)

      const timer = setTimeout(() => {
        setShowAnnotations(true)
      }, 800)

      return () => clearTimeout(timer)
    } else {
      setShowAnnotations(false)
      setParsedErrors([])
      setDisplayText("")
    }
  }, [correctedText, isChecked])

  const removeMarkup = (text: string): string => {
    return text
      .replace(/\w+\[([^\]]+)\]/g, (match, correction) => {
        const word = match.split("[")[0]
        return word
      })
      .replace(/<([^>]+)>/g, "$1")
      .replace(/\{([^}]+)\}/g, "")
  }

  const parseCorrections = (originalText: string, cleanText: string): ParsedError[] => {
    const errors: ParsedError[] = []

    // Parse word errors [correction]
    const wordRegex = /(\w+)\[([^\]]+)\]/g
    let wordMatch
    while ((wordMatch = wordRegex.exec(originalText)) !== null) {
      const wordInCleanText = cleanText.indexOf(wordMatch[1])
      if (wordInCleanText !== -1) {
        errors.push({
          type: "word",
          originalText: wordMatch[1],
          correction: wordMatch[2],
          startIndex: wordInCleanText,
          endIndex: wordInCleanText + wordMatch[1].length,
          id: `word-${errors.length}`,
        })
      }
    }

    // Parse punctuation errors <>
    const punctRegex = /<([^>]+)>/g
    let punctMatch
    while ((punctMatch = punctRegex.exec(originalText)) !== null) {
      errors.push({
        type: "punctuation",
        originalText: "",
        correction: punctMatch[1],
        startIndex: punctMatch.index,
        endIndex: punctMatch.index,
        id: `punct-${errors.length}`,
      })
    }

    // Parse grammar errors {correction}
    const grammarRegex = /\{([^}]+)\}/g
    let grammarMatch
    while ((grammarMatch = grammarRegex.exec(originalText)) !== null) {
      errors.push({
        type: "grammar",
        originalText: "",
        correction: grammarMatch[1],
        startIndex: 0,
        endIndex: cleanText.length,
        id: `grammar-${errors.length}`,
      })
    }

    return errors
  }

  const renderContent = () => {
    if (isLoading) {
      return (
        <div className="min-h-[400px] flex items-center justify-center">
          <div className="text-center">
            <Loader2 className="w-8 h-8 animate-spin mx-auto mb-4 text-indigo-600" />
            <p className="text-gray-600 text-lg">Teacher is reviewing your writing...</p>
          </div>
        </div>
      )
    }

    if (!isChecked) {
      return (
        <textarea
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder="Start writing your sentences here... For example: 'my name are Cc, nice to meet you! i will graduate from university at July 5.'"
          className="w-full min-h-[400px] p-6 text-lg leading-8 bg-transparent border-none outline-none resize-none font-handwriting"
          style={{
            backgroundImage: `repeating-linear-gradient(
              transparent,
              transparent 31px,
              #e5e7eb 31px,
              #e5e7eb 32px
            )`,
            lineHeight: "32px",
          }}
        />
      )
    }

    return <CorrectedText text={displayText} errors={parsedErrors} showAnnotations={showAnnotations} />
  }

  return (
    <div className="relative bg-gradient-to-br from-yellow-50 to-orange-50 rounded-lg border-2 border-yellow-200 min-h-[450px] overflow-hidden">
      {/* Paper texture */}
      <div className="absolute inset-0 opacity-10 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZGVmcz48cGF0dGVybiBpZD0iZ3JpZCIgd2lkdGg9IjEwIiBoZWlnaHQ9IjEwIiBwYXR0ZXJuVW5pdHM9InVzZXJTcGFjZU9uVXNlIj48cGF0aCBkPSJNIDEwIDAgTCAwIDAgMCAxMCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjMDAwIiBzdHJva2Utd2lkdGg9IjAuNSIvPjwvcGF0dGVybj48L2RlZnM+PHJlY3Qgd2lkdGg9IjEwMCUiIGhlaWdodD0iMTAwJSIgZmlsbD0idXJsKCNncmlkKSIvPjwvc3ZnPg==')]"></div>

      {/* Red margin line */}
      <div className="absolute left-16 top-0 bottom-0 w-0.5 bg-red-300 opacity-60"></div>

      <div className="relative z-10">{renderContent()}</div>
    </div>
  )
}

interface CorrectedTextProps {
  text: string
  errors: ParsedError[]
  showAnnotations: boolean
}

function CorrectedText({ text, errors, showAnnotations }: CorrectedTextProps) {
  return (
    <div className="relative p-6 text-lg leading-8 min-h-[400px] font-handwriting">
      <AnnotatedText text={text} errors={errors} showAnnotations={showAnnotations} />

      {/* Grammar corrections */}
      <AnimatePresence>
        {errors
          .filter((error) => error.type === "grammar")
          .map((error, index) => (
            <motion.div
              key={error.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 2 + index * 0.5 }}
              className="mt-8 p-4 bg-green-50 border-l-4 border-green-500 rounded-r-lg shadow-md"
            >
              <div className="text-sm text-green-700 font-medium mb-2">✏️ Teacher's Grammar Suggestion:</div>
              <div className="text-green-800 italic font-medium">"{error.correction}"</div>
            </motion.div>
          ))}
      </AnimatePresence>
    </div>
  )
}

interface AnnotatedTextProps {
  text: string
  errors: ParsedError[]
  showAnnotations: boolean
}

function AnnotatedText({ text, errors, showAnnotations }: AnnotatedTextProps) {
  const renderTextWithAnnotations = () => {
    const words = text.split(/(\s+)/)
    let currentIndex = 0

    return words.map((word, wordIndex) => {
      const wordStart = currentIndex
      const wordEnd = currentIndex + word.length
      currentIndex = wordEnd

      const wordErrors = errors.filter(
        (error) => error.type !== "grammar" && error.startIndex >= wordStart && error.endIndex <= wordEnd,
      )

      if (wordErrors.length > 0) {
        const error = wordErrors[0]
        return (
          <AnnotatedWord
            key={wordIndex}
            word={word}
            error={error}
            index={wordIndex}
            showAnnotations={showAnnotations}
          />
        )
      }

      return <span key={wordIndex}>{word}</span>
    })
  }

  return <>{renderTextWithAnnotations()}</>
}

interface AnnotatedWordProps {
  word: string
  error: ParsedError
  index: number
  showAnnotations: boolean
}

function AnnotatedWord({ word, error, index, showAnnotations }: AnnotatedWordProps) {
  const [showCorrection, setShowCorrection] = useState(false)

  useEffect(() => {
    if (showAnnotations) {
      const timer = setTimeout(
        () => {
          setShowCorrection(true)
        },
        500 + index * 150,
      )

      return () => clearTimeout(timer)
    }
  }, [index, showAnnotations])

  return (
    <span className="relative inline-block">
      <motion.span
        initial={{ backgroundColor: "transparent" }}
        animate={
          showCorrection
            ? {
                backgroundColor: error.type === "word" ? "#fee2e2" : "#dbeafe",
              }
            : {}
        }
        transition={{ duration: 0.6 }}
        className={`relative ${showCorrection ? "rounded px-1" : ""}`}
      >
        {word}

        {/* Circle annotation */}
        <AnimatePresence>
          {showCorrection && (
            <motion.div
              initial={{ scale: 0, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ delay: 0.3, type: "spring", stiffness: 200 }}
              className="absolute -inset-2 border-2 rounded-full pointer-events-none z-10"
              style={{
                borderColor: error.type === "word" ? "#dc2626" : "#2563eb",
                borderStyle: "solid",
              }}
            />
          )}
        </AnimatePresence>
      </motion.span>

      {/* Correction annotation */}
      <AnimatePresence>
        {showCorrection && error.correction && (
          <motion.div
            initial={{ opacity: 0, scale: 0, y: -10 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            transition={{ delay: 0.8, type: "spring", stiffness: 150 }}
            className="absolute -top-16 left-1/2 transform -translate-x-1/2 z-20"
          >
            {/* Arrow */}
            <svg
              className="absolute top-8 left-1/2 transform -translate-x-1/2"
              width="20"
              height="20"
              viewBox="0 0 20 20"
            >
              <path
                d="M10 2 Q15 8 10 14"
                stroke={error.type === "word" ? "#dc2626" : "#2563eb"}
                strokeWidth="2"
                fill="none"
                strokeLinecap="round"
              />
              <polygon points="8,12 10,14 12,12" fill={error.type === "word" ? "#dc2626" : "#2563eb"} />
            </svg>

            {/* Correction bubble */}
            <div
              className={`px-3 py-2 rounded-lg text-sm font-medium whitespace-nowrap shadow-lg transform rotate-1 ${
                error.type === "word" ? "bg-red-500 text-white" : "bg-blue-500 text-white"
              }`}
              style={{ fontFamily: "cursive" }}
            >
              {error.correction}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </span>
  )
}
