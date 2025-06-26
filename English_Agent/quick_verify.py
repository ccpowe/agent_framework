#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
快速验证优化效果
"""

import os
import sys
from pathlib import Path

# 确保能找到模块
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def quick_test():
    """快速测试几个关键案例"""
    print("⚡ 快速验证优化效果")
    print("=" * 40)
    
    # 检查环境
    from dotenv import load_dotenv
    load_dotenv()
    
    try:
        from new_EnglishAgent import process_text
        print("✅ 模块导入成功")
    except ImportError as e:
        print(f"❌ 模块导入失败: {e}")
        return False
    
    # 关键测试案例
    test_cases = [
        {
            "name": "缺少标点符号",
            "input": "She is an university student",
            "expected": "She is an[a] university student<.>"
        },
        {
            "name": "大小写+标点",
            "input": "what is your name",
            "expected": "what[What] is your name<.>"
        },
        {
            "name": "问号纠正",
            "input": "What is your name.",
            "expected": "What is your name<?>"
        },
        {
            "name": "你的问题案例",
            "input": "hello, my neme are cc ,what is you name？",
            "expected": "hello[Hello], my neme[name] are[is] cc, what[What] is you[your] name<?>"
        }
    ]
    
    passed = 0
    for i, case in enumerate(test_cases, 1):
        print(f"\n🧪 测试 {i}: {case['name']}")
        print(f"输入: \"{case['input']}\"")
        
        try:
            result = process_text(case['input'], verbose=False)
            actual = result['corrected_text']
            approved = result['approved']
            
            print(f"期望: \"{case['expected']}\"")
            print(f"实际: \"{actual}\"")
            print(f"通过: {'是' if approved else '否'}")
            
            if actual == case['expected'] and approved:
                print("✅ 成功")
                passed += 1
            else:
                print("❌ 失败")
                if not approved:
                    print(f"反馈: {result['check_result']}")
            
        except Exception as e:
            print(f"❌ 错误: {e}")
    
    print(f"\n📊 结果: {passed}/{len(test_cases)} 通过")
    return passed > 0

if __name__ == "__main__":
    try:
        quick_test()
    except Exception as e:
        print(f"❌ 测试出错: {e}")
    
    input("\n按回车键退出...")