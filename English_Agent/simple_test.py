#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
简单测试脚本 - 验证LangGraph英语纠错系统的基本功能
"""

import os
import sys
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def test_imports():
    """测试模块导入"""
    try:
        from new_EnglishAgent import (
            english_agent, 
            check_agent, 
            create_english_correction_graph,
            process_text,
            AgentState
        )
        print("✅ 所有模块导入成功")
        return True
    except ImportError as e:
        print(f"❌ 模块导入失败: {e}")
        return False

def test_graph_creation():
    """测试图创建"""
    try:
        from new_EnglishAgent import create_english_correction_graph
        app = create_english_correction_graph()
        print("✅ 工作流图创建成功")
        return True
    except Exception as e:
        print(f"❌ 工作流图创建失败: {e}")
        return False

def test_simple_correction():
    """测试简单纠错功能"""
    try:
        from new_EnglishAgent import process_text
        
        # 简单测试用例
        test_text = "hello world"  # 简单的无错误文本
        print(f"🧪 测试文本: \"{test_text}\"")
        
        result = process_text(test_text, verbose=False)
        
        print(f"✅ 纠错测试完成")
        print(f"   原始: {result['original_text']}")
        print(f"   纠正: {result['corrected_text']}")
        print(f"   迭代: {result['iterations']}")
        print(f"   通过: {result['approved']}")
        
        return True
        
    except Exception as e:
        print(f"❌ 纠错测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🔧 LangGraph英语纠错系统 - 简单测试")
    print("=" * 50)
    
    # 检查环境变量
    required_vars = ["MODEL_NAME", "OPENAI_API_KEY", "MODEL_BASE_URL"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print("❌ 缺少环境变量:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n请配置 .env 文件")
        return False
    
    print("✅ 环境变量检查通过")
    
    # 运行测试
    tests = [
        ("模块导入", test_imports),
        ("图创建", test_graph_creation),
        ("简单纠错", test_simple_correction)
    ]
    
    for test_name, test_func in tests:
        print(f"\n🧪 测试: {test_name}")
        if not test_func():
            print(f"❌ {test_name} 测试失败")
            return False
        print(f"✅ {test_name} 测试通过")
    
    print("\n" + "=" * 50)
    print("🎉 所有测试通过！系统运行正常")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)