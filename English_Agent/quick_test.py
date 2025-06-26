#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
快速测试新的多代理英语纠错系统
"""

from new_EnglishAgent import process_text

def test_basic_functionality():
    """测试基本功能"""
    test_cases = [
        "hello world",
        "My freind is comming",
        "the meeting is on monday",
        "If I was rich I would travel"
    ]
    
    print("🧪 快速测试多代理英语纠错系统")
    print("=" * 50)
    
    for i, text in enumerate(test_cases, 1):
        print(f"\n测试 {i}: {text}")
        try:
            result = process_text(text, verbose=False)
            print(f"✅ 成功: {result['corrected_text']}")
            print(f"通过: {result['approved']}")
            print(f"检查: {result['check_result']}")
        except Exception as e:
            print(f"❌ 错误: {e}")

if __name__ == "__main__":
    test_basic_functionality() 