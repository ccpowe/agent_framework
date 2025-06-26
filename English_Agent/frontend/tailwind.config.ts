import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      backgroundImage: {
        "gradient-radial": "radial-gradient(var(--tw-gradient-stops))",
        "gradient-conic":
          "conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))",
      },
      // 可以在这里为魔法书主题添加自定义颜色、字体等
      colors: {
        book: {
          cover: '#8B4513',      // 棕色书皮
          page: '#F5F5DC',       // 米色书页
          text: '#3A3A3A',       // 深灰色文字
          annotation: '#D22B2B', // 红色批注
        },
      },
      fontFamily: {
        "magic-script": ["'Dancing Script'", "cursive"], // 一个手写风格的字体示例
      },
    },
  },
  plugins: [],
};
export default config;
