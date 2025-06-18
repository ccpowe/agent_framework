"use client"

import { useEffect, useState, useRef } from "react"
import { motion, AnimatePresence } from "framer-motion"

interface CorrectionDisplayProps {
  originalText: string
  correctedText: string
}

interface ParsedError {
  type: "word" | "punctuation" | "grammar"
  originalText: string
  correction: string
  startIndex: number
  endIndex: number
  id: string
}

export default function CorrectionDisplay({ originalText, correctedText }: CorrectionDisplayProps) {
  const [parsedErrors, setParsedErrors] = useState<ParsedError[]>([])
  const [displayText, setDisplayText] = useState("")
  const [showAnnotations, setShowAnnotations] = useState(false)

  useEffect(() => {
    const cleanText = removeMarkup(correctedText)
    const errors = parseCorrections(correctedText, cleanText)
    setParsedErrors(errors)
    setDisplayText(cleanText)

    const timer = setTimeout(() => {
      setShowAnnotations(true)
    }, 500)

    return () => clearTimeout(timer)
  }, [correctedText])

  const removeMarkup = (text: string): string => {
    return text
      .replace(/\w+\[([^\]]+)\]/g, (match) => {
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

        // Parse punctuation errors <> and accurately map to cleanText indices
    const punctRegex = /<([^>]+)>/g
    let punctMatch
    let searchPos = 0 // 用于在 cleanText 中增量搜索，避免找到错误的相同符号
    while ((punctMatch = punctRegex.exec(originalText)) !== null) {
      const punctChar = punctMatch[1]
      // 在 cleanText 中从 searchPos 开始查找对应的符号位置
      const punctInCleanText = cleanText.indexOf(punctChar, searchPos)
      if (punctInCleanText !== -1) {
        errors.push({
          type: "punctuation",
          originalText: "",
          correction: punctChar,
          startIndex: punctInCleanText,
          endIndex: punctInCleanText + punctChar.length,
          id: `punct-${errors.length}`,
        })
        searchPos = punctInCleanText + punctChar.length
      }
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

  return (
    <div className="relative w-full">
      {/* Corrected Text with Interlinear Annotations */}
      <div className="text-lg font-handwriting w-full" style={{ lineHeight: "60px" }}>
        <AnnotatedText text={displayText} errors={parsedErrors} showAnnotations={showAnnotations} />
      </div>

      {/* Grammar Suggestions */}
      <div className="w-full mt-8">
        <AnimatePresence>
          {parsedErrors
            .filter((error) => error.type === "grammar")
            .map((error, index) => (
              <motion.div
                key={error.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 2 + index * 0.5 }}
                className="p-4 bg-green-50 border-l-4 border-green-500 rounded-r-lg shadow-md w-full mb-4"
              >
                <div className="text-sm text-green-700 font-medium mb-2">✏️ Teacher's Grammar Suggestion:</div>
                <div className="text-green-800 italic font-medium break-words">"{error.correction}"</div>
              </motion.div>
            ))}
        </AnimatePresence>
      </div>
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
    // 拆分时将常见标点作为独立 token，避免“Hello,”被当作一个单词
    const words = text.split(/(\s+|[,.!?;:])/)
    let currentIndex = 0

    return words.map((word, wordIndex) => {
      const wordStart = currentIndex
      const wordEnd = currentIndex + word.length
      currentIndex = wordEnd

      const wordErrors = errors.filter(
        (error) =>
          error.type !== "grammar" &&
          // 允许端点在 wordEnd 处（针对紧跟在单词后的标点）
          error.startIndex >= wordStart &&
          error.endIndex <= wordEnd,
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

      // 忽略空字符串 token
      if (word === "") {
        return <span key={wordIndex}></span>
      }
      return <span key={wordIndex}>{word}</span>
    })
  }

  return <div className="w-full break-words">{renderTextWithAnnotations()}</div>
}

interface AnnotatedWordProps {
  word: string
  error: ParsedError
  index: number
  showAnnotations: boolean
}

function AnnotatedWord({ word, error, index, showAnnotations }: AnnotatedWordProps) {
  const [showCorrection, setShowCorrection] = useState(false)
  const containerRef = useRef<HTMLSpanElement>(null)  // 整个组件的容器引用
  const wordRef = useRef<HTMLSpanElement>(null)       // 单词元素引用
  const correctionRef = useRef<HTMLDivElement>(null)  // 批注元素引用

  useEffect(() => {
    if (showAnnotations) {
      const timer = setTimeout(
        () => {
          setShowCorrection(true)
        },
        300 + index * 100,
      )

      return () => clearTimeout(timer)
    }
  }, [index, showAnnotations])

  // 调整批注的相对位置，确保它直接位于单词正上方
  // 不再使用像素偏移计算，而是直接用top: 0和transform来控制位置
  const annotationStyles: React.CSSProperties = {
    position: 'absolute',
    top: '0',          // 与单词顶部对齐
    left: '0',         // 与单词左侧对齐
    width: '100%',     // 占满整个单词宽度
    height: '0',       // 高度为0确保不占用空间
    zIndex: 20,
    display: 'flex',
    justifyContent: 'center',  // 水平居中
    alignItems: 'flex-end',    // 在底部(刚好与单词顶部对齐)
    transform: 'translateY(-250%)',  // 显著增加向上移动的距离，确保批注与圆框之间有明显间隔
  }
  
  // 批注样式
  const bubbleStyles: React.CSSProperties = {
    fontFamily: "system-ui, -apple-system, sans-serif",
    lineHeight: 1.2,
    fontSize: '14px',  // 增大字体大小
    padding: '2px 6px',  // 增加内边距
    whiteSpace: 'nowrap',
    textAlign: 'center' as const,
    boxShadow: '0 2px 3px rgba(0,0,0,0.1)',
    borderRadius: '3px',
    fontWeight: 500,  // 增加字体权重使其更加醒目
  }

  return (
    <span ref={containerRef} className="relative inline-block">
      <motion.span
        ref={wordRef}
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
              transition={{ delay: 0.2, type: "spring", stiffness: 200 }}
              className="absolute pointer-events-none z-10"
              style={{
                borderColor: error.type === "word" ? "#dc2626" : "#2563eb",
                borderStyle: "solid",
                borderWidth: "2px",
                borderRadius: "9999px",
                // 缩小圆框大小，以便给批注留出更多空间
                ...(error.type === "word"
                  ? { inset: "-3px" }
                  : { 
                      top: "-2px", 
                      bottom: "-2px", 
                      left: "-2px", 
                      right: "-2px" 
                    }),
              }}
            />
          )}
        </AnimatePresence>
        
        {/* 批注直接放在单词内部，确保完美居中 */}
        <AnimatePresence>
          {showCorrection && error.correction && (
            <motion.div
              initial={{ opacity: 0, scale: 0 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0 }}
              transition={{ delay: 0.3, type: "spring", stiffness: 120 }}
              style={annotationStyles}
            >
              <div
                ref={correctionRef}
                className={`border ${error.type === "word" ? "bg-red-50 text-red-700 border-red-200" : "bg-blue-50 text-blue-700 border-blue-200"}`}
                style={bubbleStyles}
              >
                {error.correction}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </motion.span>
    </span>
  )
}
