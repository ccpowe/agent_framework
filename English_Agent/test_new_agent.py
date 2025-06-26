#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试新的LangGraph英语纠错系统
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from new_EnglishAgent import process_text, create_english_correction_graph
    print("✅ 成功导入模块")
except ImportError as e:
    print(f"❌ 导入模块失败: {e}")
    sys.exit(1)

def test_basic_functionality():
    """测试基本功能"""
    print("\n🧪 开始基本功能测试...")
    
    # 测试用例
    test_cases = [
        "what is you're name.",  # 大小写 + 语法错误 + 标点错误
        "She is a amazin person",  # 冠词错误 + 拼写错误 + 缺少标点
        "The data suggest different conclusion",  # 主谓一致错误 + 缺少冠词 + 缺少标点
    ]
    
    for i, test_text in enumerate(test_cases, 1):
        print(f"\n--- 测试用例 {i} ---")
        try:
            result = process_text(test_text)
            print(f"✅ 测试用例 {i} 完成")
        except Exception as e:
            print(f"❌ 测试用例 {i} 失败: {e}")

def test_graph_creation():
    """测试图创建"""
    print("\n🔧 测试工作流图创建...")
    try:
        app = create_english_correction_graph()
        print("✅ 工作流图创建成功")
        return True
    except Exception as e:
        print(f"❌ 工作流图创建失败: {e}")
        return False

if __name__ == "__main__":
    print("🚀 LangGraph英语纠错系统测试")
    print("=" * 50)
    
    # 测试图创建
    if not test_graph_creation():
        print("❌ 基础测试失败，退出")
        sys.exit(1)
    
    # 测试基本功能
    test_basic_functionality()
    
    print("\n" + "=" * 50)
    print("🎉 测试完成！")