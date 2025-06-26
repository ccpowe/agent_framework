#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
代码验证脚本 - 检查语法和基本功能
"""

import ast
import sys
from pathlib import Path

def validate_syntax(file_path):
    """验证Python文件语法"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
        
        # 解析AST
        ast.parse(source)
        print(f"✅ {file_path.name} - 语法正确")
        return True
        
    except SyntaxError as e:
        print(f"❌ {file_path.name} - 语法错误: {e}")
        return False
    except Exception as e:
        print(f"❌ {file_path.name} - 读取错误: {e}")
        return False

def check_imports():
    """检查导入是否正确"""
    print("\n🔍 检查导入...")
    
    try:
        # 检查基本导入
        from typing import TypedDict, Annotated, Sequence, Literal
        print("✅ typing 模块导入成功")
        
        from dotenv import load_dotenv
        print("✅ dotenv 模块导入成功")
        
        # 检查LangChain相关导入
        from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage
        print("✅ langchain_core.messages 导入成功")
        
        from langgraph.graph import END, START, StateGraph
        print("✅ langgraph.graph 导入成功")
        
        from langgraph.graph.message import add_messages
        print("✅ langgraph.graph.message 导入成功")
        
        # 检查OpenAI导入
        from langchain_openai import ChatOpenAI
        print("✅ langchain_openai 导入成功")
        
        return True
        
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False

def validate_environment():
    """验证环境配置"""
    print("\n🔧 检查环境配置...")
    
    import os
    load_dotenv()
    
    required_vars = ["MODEL_NAME", "OPENAI_API_KEY", "MODEL_BASE_URL"]
    all_present = True
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            # 隐藏敏感信息
            if "API_KEY" in var and len(value) > 10:
                display_value = value[:8] + "..." + value[-4:]
            else:
                display_value = value
            print(f"✅ {var}: {display_value}")
        else:
            print(f"❌ {var}: 未设置")
            all_present = False
    
    return all_present

def main():
    """主验证函数"""
    print("🔧 LangGraph英语纠错系统 - 代码验证")
    print("=" * 50)
    
    current_dir = Path(__file__).parent
    
    # 验证Python文件语法
    print("📝 验证Python文件语法...")
    python_files = [
        "new_EnglishAgent.py",
        "demo_langgraph.py", 
        "quick_demo.py",
        "simple_test.py"
    ]
    
    syntax_ok = True
    for file_name in python_files:
        file_path = current_dir / file_name
        if file_path.exists():
            if not validate_syntax(file_path):
                syntax_ok = False
        else:
            print(f"⚠️ {file_name} - 文件不存在")
    
    if not syntax_ok:
        print("\n❌ 语法验证失败")
        return False
    
    # 检查导入
    if not check_imports():
        print("\n❌ 导入检查失败")
        return False
    
    # 验证环境
    if not validate_environment():
        print("\n⚠️ 环境配置不完整")
    
    print("\n" + "=" * 50)
    print("✅ 代码验证完成！")
    print("\n📋 运行建议:")
    print("1. 使用 uv 管理依赖: uv sync")
    print("2. 运行演示: uv run python English_Agent/quick_demo.py")
    print("3. 或直接运行: python English_Agent/new_EnglishAgent.py")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ 验证过程出错: {e}")
        sys.exit(1)