// utils/parseCorrections.ts

export interface ParsedSegment {
  id: string;
  type: 'original' | 'spelling' | 'punctuation' | 'full_sentence';
  originalText: string; // 对于 'original' 类型，这是实际文本。
                        // 对于 'spelling' 类型，这是原始的错误单词。
                        // 对于 'punctuation' 类型，这通常为空，表示插入位置，或代表被替换的原始标点（如果能识别）。
                        // 对于 'full_sentence' 类型，这是完整的正确句子。
  correctedText?: string; // 对于 'spelling' 和 'punctuation'，这是建议的修正。
}

export const parseCorrectionString = (rawText: string): ParsedSegment[] => {
  if (!rawText) return [];

  const segments: ParsedSegment[] = [];
  let segmentIdCounter = 0;
  let textToParse = rawText;
  let fullSentenceCorrectionText: string | undefined;

  // 1. Extract full sentence correction from the end, if it exists
  const fullSentenceMatch = textToParse.match(/^(.*){([^}]*)}$/s);
  if (fullSentenceMatch) {
    textToParse = fullSentenceMatch[1];
    fullSentenceCorrectionText = fullSentenceMatch[2];
  }

  let i = 0;
  let currentText = '';

  const flushCurrentText = () => {
    if (currentText) {
      segments.push({
        id: `seg-${segmentIdCounter++}-original`,
        type: 'original',
        originalText: currentText,
      });
      currentText = '';
    }
  };

  while (i < textToParse.length) {
    const char = textToParse[i];
    const nextChar = textToParse[i + 1];

    if (char === '[' && i > 0) {
      const closingBracketIndex = textToParse.indexOf(']', i);
      if (closingBracketIndex > -1) {
        const originalWordMatch = currentText.match(/(\w+)$/);
        if (originalWordMatch) {
          const originalWord = originalWordMatch[1];
          const correctedText = textToParse.substring(i + 1, closingBracketIndex);
          
          // Rewind currentText to remove the original word
          currentText = currentText.substring(0, currentText.length - originalWord.length);
          flushCurrentText();

          segments.push({
            id: `seg-${segmentIdCounter++}-spelling`,
            type: 'spelling',
            originalText: originalWord,
            correctedText: correctedText,
          });

          i = closingBracketIndex + 1;
          continue;
        }
      }
    } else if (char === '<') {
      const closingBracketIndex = textToParse.indexOf('>', i);
      if (closingBracketIndex > -1) {
        flushCurrentText();
        const correctedText = textToParse.substring(i + 1, closingBracketIndex);
        segments.push({
          id: `seg-${segmentIdCounter++}-punctuation`,
          type: 'punctuation',
          originalText: '', // Punctuation is an insertion
          correctedText: correctedText,
        });
        i = closingBracketIndex + 1;
        continue;
      }
    }

    currentText += char;
    i++;
  }

  flushCurrentText();

  if (fullSentenceCorrectionText) {
    segments.push({
      id: `seg-${segmentIdCounter++}-fullsentence`,
      type: 'full_sentence',
      originalText: fullSentenceCorrectionText,
    });
  }

  return segments;
};

// // 示例用法:
// const exampleOutput = "my name are[is] Cc, nice to meet you<,>! i[I] will graduate from university at[on] July 5<.> when i[I] graduate[graduated] i[I]  will trivial[travel] around[around the] word[world]{My name is Cc. Nice to meet you! I will graduate from university on July 5. When I graduate, I will travel around the world. OR My name is Cc. Nice to meet you! I will graduate from university on July 5. After I graduate, I will travel around the world.}";
// const parsed = parseCorrectionString(exampleOutput);
// console.log(JSON.stringify(parsed, null, 2));

// const example2 = "Helo[Hello] wrld[world]<.>{Hello world.}";
// const parsed2 = parseCorrectionString(example2);
// console.log(JSON.stringify(parsed2, null, 2));

// const example3 = "This is a test sentence."; // No corrections
// const parsed3 = parseCorrectionString(example3);
// console.log(JSON.stringify(parsed3, null, 2));

// const example4 = "{This is a fully corrected sentence only.}"; // Only full correction
// const parsed4 = parseCorrectionString(example4);
// console.log(JSON.stringify(parsed4, null, 2));

// const example5 = "wordA[wordB]<puncC>"; // Adjacent corrections
// const parsed5 = parseCorrectionString(example5);
// console.log(JSON.stringify(parsed5, null, 2));
