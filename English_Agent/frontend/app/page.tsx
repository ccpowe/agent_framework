// app/page.tsx
'use client';

import { useState, useEffect } from 'react';
import MagicBook from '@/components/MagicBook';

export default function HomePage() {
  const [userInput, setUserInput] = useState<string>('');
  const [apiResponse, setApiResponse] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const handleSubmit = async (text: string) => {
    setIsLoading(true);
    setUserInput(text); // 保存原始输入用于显示
    setApiResponse(''); // 清除之前的API响应

    try {
      const response = await fetch('http://127.0.0.1:8000/chat', { 
        method: 'POST', 
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text, stream: false })
      });

      if (!response.ok) {
        // 如果HTTP状态码不是2xx，则抛出错误
        // 尝试解析JSON错误体，如果失败则使用状态文本
        let errorMessage = response.statusText;
        try {
          const errorData = await response.json();
          errorMessage = errorData.detail || errorData.message || errorMessage;
        } catch (e) {
          // 无法解析JSON，继续使用statusText
        }
        throw new Error(`API Error ${response.status}: ${errorMessage}`);
      }

      const data = await response.json();
      if (data && typeof data.response === 'string') {
        setApiResponse(data.response);
      } else {
        console.error('API响应格式不正确或缺少 response 字段:', data);
        setApiResponse("Error: API响应格式不正确。请检查后端。");
      }
    } catch (error) {
      console.error('调用API时出错:', error);
      let errorMessage = '调用API时出错，请检查网络连接或稍后再试。';
      if (error instanceof Error) {
        errorMessage = error.message;
      }
      setApiResponse(`Error: ${errorMessage}`);
    }
    
    setIsLoading(false);
  };

  return (
    <main className="min-h-screen flex flex-col items-center justify-center p-4 bg-gradient-to-br from-purple-200 via-pink-200 to-orange-200">
      <h1 className="text-4xl font-bold text-gray-800 mb-8 font-magic-script">
        魔法英语练习册
      </h1>
      <MagicBook 
        onSubmit={handleSubmit} 
        originalText={userInput}
        correctedText={apiResponse} 
        isLoading={isLoading} 
      />
    </main>
  );
}
