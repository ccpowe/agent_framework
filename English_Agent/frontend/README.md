# 英语语法助手 - 前端

本项目是英语语法助手的前端部分，使用 Next.js, React, 和 Tailwind CSS 构建。

## 功能

- 用户输入英文句子。
- 调用后端 API进行语法分析和纠错。
- 以“魔法书”的形式展示用户输入和 AI 的批改建议。
- 针对不同类型的错误（拼写、标点、语法）显示不同的批注动画效果。

## 技术栈

- Next.js (App Router)
- React
- TypeScript
- Tailwind CSS

## 目录结构

- `app/`: Next.js App Router 核心目录
  - `globals.css`: 全局样式和 Tailwind 指令
  - `layout.tsx`: 根布局组件
  - `page.tsx`: 主页面组件
- `components/`: React 组件
  - `MagicBook.tsx`: 魔法书 UI 组件
  - `CorrectionRenderer.tsx`: 批改渲染逻辑组件
- `utils/`: 工具函数
  - `parseCorrections.ts`: 解析后端返回的批改数据
- `public/`: 静态资源

## 开发

1. 确保已安装 Node.js 和 npm/yarn/pnpm。

2. 进入 `frontend` 目录。

3. 安装依赖：

   ```bash
   npm install
   # 或者
   # yarn install
   # pnpm install
   ```

4. 启动开发服务器：

   ```bash
   npm run dev
   # 或者
   # yarn dev
   # pnpm dev
   ```

5. 在浏览器中打开 `http://localhost:3000`。

## 后端 API 格式约定

后端返回的批改字符串遵循以下格式：

- **语法错误**: 在原句末尾用 `{}` 包裹正确的句子。
  - 例如: `... original sentence {Corrected sentence.}`
- **拼写/词语错误**: 在错误单词后用 `[]` 写入正确的单词。
  - 例如: `wrongword[correctword]`
- **标点错误**: 在需要修正的位置用 `<>` 插入正确的标点。
  - 例如: `word1 <>word2` (表示 word1 和 word2 间应有标点), `word1<correct_punctuation>`

**示例输入:**
`my name are Cc, nice to meet you! i will graduate from university at July 5. when i graduated i will trivial around word`

**示例模型输出:**
`my name are[is] Cc, nice to meet you<,>! i[I] will graduate from university at[on] July 5<.> when i[I] graduate[graduated] i[I] will trivial[travel] around[around the] word[world]{My name is Cc. Nice to meet you! I will graduate from university on July 5. When I graduate, I will travel around the world. OR My name is Cc. Nice to meet you! I will graduate from university on July 5. After I graduate, I will travel around the world.}`
