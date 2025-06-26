// components/MagicBook.tsx
'use client';

import React, { useState, useRef, useEffect } from 'react';
import CorrectionRenderer from '@/components/CorrectionRenderer';
import { BookOpen, Sparkles, Send, Loader2 } from 'lucide-react';
import { motion } from 'framer-motion';

interface MagicBookProps {
  onSubmit: (text: string) => Promise<void>;
  originalText: string;
  correctedText: string;
  isLoading: boolean;
}

const MagicBook: React.FC<MagicBookProps> = ({ onSubmit, originalText, correctedText, isLoading }) => {
  const [currentText, setCurrentText] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSubmit = () => {
    if (currentText.trim() && !isLoading) {
      onSubmit(currentText.trim());
    }
  };

  useEffect(() => {
    // 自动调整文本框高度
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = textareaRef.current.scrollHeight + 'px';
    }
  }, [currentText, correctedText]);

  return (
    <div className="w-full max-w-4xl h-[600px] bg-book-cover shadow-2xl rounded-lg p-2 flex perspective-[1500px]">
      {/* 书脊 */}
      <div className="w-10 bg-book-cover shadow-inner rounded-l-md" /> {/* Use book-cover for spine, consider a darker shade or texture later */}

      {/* 左页 - 输入页 */}
      <motion.div 
        className="flex-1 bg-book-page p-8 rounded-l-none rounded-r-md magic-book-page relative overflow-y-auto shadow-lg shadow-inner border border-black/10"
        style={{ transformOrigin: 'right center' }} // Pivot from the spine
        whileHover={{ rotateY: -2, scale: 1.01, zIndex: 10 }}
        transition={{ type: "spring", stiffness: 300, damping: 20 }}
      >
        <h2 className="text-2xl font-semibold text-book-text mb-4 border-b-2 border-book-text/30 pb-2 flex items-center font-magic-script">
          <Sparkles className="w-6 h-6 mr-2 text-amber-500" />
          在此处书写你的句子...
        </h2>
        <textarea
          ref={textareaRef}
          className="w-full min-h-[300px] p-4 bg-transparent text-lg text-book-text focus:outline-none resize-none placeholder-book-text/50 leading-relaxed font-magic-script tracking-wide"
          placeholder="例如: My name are Cascade..."
          value={currentText}
          onChange={(e) => setCurrentText(e.target.value)}
          disabled={isLoading}
          rows={10}
        />
        <button
          onClick={handleSubmit}
          disabled={isLoading || !currentText.trim()}
          className={`mt-6 px-6 py-3 bg-book-cover text-book-page font-semibold rounded-lg shadow-md hover:opacity-90 hover:shadow-lg active:scale-95 transition-all duration-150 disabled:bg-gray-400 disabled:text-gray-200 disabled:cursor-not-allowed flex items-center justify-center float-right`}
        >
          {isLoading ? (
            <><Loader2 className="w-5 h-5 mr-2 animate-spin" /> 正在施法...</>
          ) : (
            <><Send className="w-5 h-5 mr-2" /> 祈求魔法批改</>
          )}
        </button>
      </motion.div>

      {/* 右页 - 批改页 */}
      <motion.div 
        className="flex-1 bg-book-page p-8 rounded-r-none rounded-l-md magic-book-page relative overflow-y-auto shadow-lg shadow-inner border border-black/10"
        style={{ transformOrigin: 'left center' }} // Pivot from the spine
        whileHover={{ rotateY: 2, scale: 1.01, zIndex: 10 }}
        transition={{ type: "spring", stiffness: 300, damping: 20 }}
      >
        <h2 className="text-2xl font-semibold text-book-text mb-4 border-b-2 border-book-text/30 pb-2 flex items-center font-magic-script">
          <BookOpen className="w-6 h-6 mr-2 text-book-text opacity-75" />
          魔法批改结果
        </h2>
        {isLoading && !correctedText && (
          <div className="flex items-center justify-center h-full">
            <Loader2 className="w-12 h-12 text-amber-500 animate-spin" /> {/* Changed yellow to amber for consistency */}
            <p className="ml-4 text-xl text-book-text/80">魔法正在汇聚...</p>
          </div>
        )}
        {!isLoading && !correctedText && !originalText && (
          <p className="text-gray-500 text-center mt-10 text-lg">请在左侧书写内容并提交，批改结果将在此处展现。</p>
        )}
        {(correctedText || originalText) && !isLoading && ( // Ensure not to render CorrectionRenderer while loading
          <CorrectionRenderer 
            originalText={originalText} 
            correctedText={correctedText} 
          />
        )}
      </motion.div>
    </div>
  );
};

export default MagicBook;
