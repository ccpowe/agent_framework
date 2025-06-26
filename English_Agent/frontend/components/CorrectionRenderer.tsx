// components/CorrectionRenderer.tsx
'use client';

import React, { useState, useRef, createRef, useEffect } from 'react';
import { ParsedSegment, parseCorrectionString } from '@/utils/parseCorrections';
import AnnotationArrow from './AnnotationArrow'; // 导入箭头组件
import { motion, AnimatePresence } from 'framer-motion';

interface CorrectionRendererProps {
  originalText: string; // 原始用户输入
  correctedText: string; // 后端返回的带标记的文本
}

interface SegmentRefsType {
  [key: string]: {
    from: React.RefObject<HTMLSpanElement>;
    to: React.RefObject<HTMLDivElement>; // All tooltips are now divs
  };
}

const CorrectionRenderer: React.FC<CorrectionRendererProps> = ({
  originalText,
  correctedText,
}) => {
  const segments = parseCorrectionString(correctedText);
  const containerRef = useRef<HTMLDivElement>(null); // Ref for the main container

  // State to manage which arrow/tooltip is visible
  const [activeAnnotationId, setActiveAnnotationId] = useState<string | null>(null);

  // Refs for each segment (from: error, to: correction tooltip)
  const segmentRefs = useRef<SegmentRefsType>({});

  // Initialize refs for segments that need annotations
  segments.forEach(segment => {
    if ((segment.type === 'spelling' || segment.type === 'punctuation') && !segmentRefs.current[segment.id]) {
      segmentRefs.current[segment.id] = {
        from: createRef<HTMLSpanElement>(),
        to: createRef<HTMLDivElement>(), // All tooltips are now divs
      };
    }
  });

  const getArrowColor = (type: ParsedSegment['type']) => {
    switch (type) {
      case 'spelling':
        return '#EF4444'; // red-500
      case 'punctuation':
        return '#3B82F6'; // blue-500
      default:
        return '#6B7280'; // gray-500
    }
  };
  
  // Handler to show annotation
  const handleMouseEnter = (segmentId: string) => {
    setActiveAnnotationId(segmentId);
  };

  // Handler to hide annotation
  const handleMouseLeave = () => {
    setActiveAnnotationId(null);
  };

  return (
    <div className="p-4 max-w-2xl mx-auto font-serif relative" ref={containerRef}>
      <div className="text-lg leading-relaxed text-gray-800 bg-yellow-50 p-6 rounded-md shadow-lg relative min-h-[150px]">
        {segments.map((segment) => {
          const currentRefs = segmentRefs.current[segment.id];
          switch (segment.type) {
            case 'spelling':
              return (
                <span
                  key={segment.id}
                  ref={currentRefs?.from}
                  className="relative group cursor-pointer"
                  onMouseEnter={() => handleMouseEnter(segment.id)}
                  onMouseLeave={handleMouseLeave}
                >
                  <span className="line-through text-book-annotation bg-book-annotation/10 px-1 rounded-sm">
                    {segment.originalText}
                  </span>
                  <AnimatePresence>
                    {activeAnnotationId === segment.id && segment.correctedText && (
                      <motion.div
                        ref={currentRefs?.to}
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: 10 }}
                        transition={{ duration: 0.2 }}
                        className="absolute left-1/2 -translate-x-1/2 bottom-full mb-2 w-max max-w-xs px-3 py-1.5 bg-book-annotation text-white text-sm rounded-lg shadow-lg z-20"
                      >
                        {segment.correctedText}
                      </motion.div>
                    )}
                  </AnimatePresence>
                </span>
              );
            case 'punctuation':
              // Punctuation is treated as an insertion at a specific point.
              return (
                <span
                  key={segment.id}
                  ref={currentRefs?.from}
                  className="relative group cursor-pointer inline-flex items-center justify-center mx-px"
                  onMouseEnter={() => handleMouseEnter(segment.id)}
                  onMouseLeave={handleMouseLeave}
                >
                  {/* Visual marker for the insertion point */}
                  <span className="text-book-annotation font-bold bg-book-annotation/10 rounded-sm w-4 h-5 flex items-center justify-center leading-none">^</span>
                  <AnimatePresence>
                    {activeAnnotationId === segment.id && segment.correctedText && (
                      <motion.div
                        ref={currentRefs?.to}
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: 10 }}
                        transition={{ duration: 0.2 }}
                        className="absolute left-1/2 -translate-x-1/2 bottom-full mb-2 w-max max-w-xs px-3 py-1.5 bg-book-annotation text-white text-sm rounded-lg shadow-lg z-20"
                      >
                        建议插入: <span className="font-bold text-base">{segment.correctedText}</span>
                      </motion.div>
                    )}
                  </AnimatePresence>
                </span>
              );
            case 'full_sentence':
              // Full sentence corrections are displayed separately, no inline arrow needed for now.
              return null; // Will be rendered below
            case 'original':
            default:
              return <span key={segment.id}>{segment.originalText}</span>;
          }
        })}

        {/* Render Arrows: Iterate over active annotations that have refs */}
        {segments.map(segment => {
          if ((segment.type === 'spelling' || segment.type === 'punctuation') && activeAnnotationId === segment.id) {
            const currentRefs = segmentRefs.current[segment.id];
            if (currentRefs?.from?.current && currentRefs?.to?.current && containerRef.current) {
              return (
                <AnnotationArrow
                  key={`arrow-${segment.id}`}
                  fromRef={currentRefs.from}
                  toRef={currentRefs.to}
                  containerRef={containerRef}
                  color={getArrowColor(segment.type)}
                  visible={true} // Arrow is visible when activeAnnotationId matches
                />
              );
            }
          }
          return null;
        })}
      </div>

      {/* Display full sentence corrections separately */}
      {segments.filter(s => s.type === 'full_sentence' && s.correctedText).length > 0 && (
        <div className="mt-6 p-4 border-2 border-solid border-book-annotation bg-book-annotation/10 rounded-md shadow">
          <h3 className="text-md font-semibold text-book-annotation mb-2">教师批注:</h3>
          {segments.map(
            (segment) =>
              segment.type === 'full_sentence' &&
              segment.correctedText && (
                <p key={`fs-${segment.id}`} className="text-book-text">
                  {segment.correctedText}
                </p>
              )
          )}
        </div>
      )}
    </div>
  );
};

export default CorrectionRenderer;

