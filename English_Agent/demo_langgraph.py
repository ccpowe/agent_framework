#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
LangGraph英语纠错系统演示
展示双代理循环纠错的工作流程
"""

import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 检查必要的环境变量
required_env_vars = ["MODEL_NAME", "OPENAI_API_KEY", "MODEL_BASE_URL"]
missing_vars = [var for var in required_env_vars if not os.getenv(var)]

if missing_vars:
    print("❌ 缺少必要的环境变量:")
    for var in missing_vars:
        print(f"   - {var}")
    print("\n请创建 .env 文件并设置这些变量")
    exit(1)

try:
    from new_EnglishAgent import process_text
    print("✅ 成功导入LangGraph英语纠错系统")
except ImportError as e:
    print(f"❌ 导入失败: {e}")
    exit(1)

def demo_correction_workflow():
    """演示纠错工作流程"""
    
    print("\n🎯 LangGraph双代理英语纠错系统演示")
    print("=" * 60)
    print("系统架构:")
    print("1. 📝 English Agent: 根据严格标记规则纠正文本")
    print("2. 🔍 Check Agent: 验证纠错结果是否符合要求")
    print("3. 🔄 循环机制: 不符合要求时重新纠错，直到通过或达到最大迭代次数")
    print("=" * 60)
    
    # 演示用例
    demo_cases = [
        {
            "text": "what is you're name.",
            "description": "大小写错误 + 语法错误 + 标点错误"
        },
        {
            "text": "She is a amazin person",
            "description": "冠词错误 + 拼写错误 + 缺少标点"
        },
        {
            "text": "The data suggest different conclusion",
            "description": "主谓一致错误 + 缺少冠词 + 缺少标点"
        }
    ]
    
    for i, case in enumerate(demo_cases, 1):
        print(f"\n📋 演示案例 {i}: {case['description']}")
        print(f"输入文本: \"{case['text']}\"")
        print("-" * 40)
        
        try:
            result = process_text(case['text'])
            
            print(f"\n📊 处理结果:")
            print(f"   原始文本: {result['original_text']}")
            print(f"   纠正文本: {result['corrected_text']}")
            print(f"   迭代次数: {result['iterations']}")
            print(f"   是否通过: {'✅ 是' if result['approved'] else '❌ 否'}")
            print(f"   检查反馈: {result['check_result']}")
            
        except Exception as e:
            print(f"❌ 处理失败: {e}")
        
        print("\n" + "=" * 60)

def interactive_mode():
    """交互模式"""
    print("\n🎮 进入交互模式")
    print("输入英文文本进行纠错，输入 'quit' 退出")
    print("-" * 40)
    
    while True:
        try:
            user_input = input("\n📝 请输入英文文本: ").strip()
            
            if user_input.lower() in ['quit', 'exit', '退出']:
                print("👋 再见！")
                break
            
            if not user_input:
                print("⚠️ 请输入有效文本")
                continue
            
            result = process_text(user_input)
            
        except KeyboardInterrupt:
            print("\n👋 再见！")
            break
        except Exception as e:
            print(f"❌ 处理错误: {e}")

if __name__ == "__main__":
    print("🚀 LangGraph英语纠错系统")
    
    # 运行演示
    demo_correction_workflow()
    
    # 询问是否进入交互模式
    while True:
        choice = input("\n是否进入交互模式？(y/n): ").strip().lower()
        if choice in ['y', 'yes', '是']:
            interactive_mode()
            break
        elif choice in ['n', 'no', '否']:
            print("👋 感谢使用！")
            break
        else:
            print("请输入 y 或 n")