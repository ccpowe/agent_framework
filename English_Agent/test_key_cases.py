#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试关键案例 - 验证修复效果
"""

import os
import sys
from pathlib import Path

# 确保能找到模块
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def test_key_cases():
    """测试关键案例"""
    print("🔑 测试关键案例")
    print("=" * 60)
    
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
    key_cases = [
        {
            "name": "你提到的问题案例",
            "input": "hello, my neme are cc ,what is you name？",
            "expected": "hello[Hello], my neme[name] are[is] cc, what[What] is you[your] name<?>"
        },
        {
            "name": "原始示例1 - 大小写+语法+标点",
            "input": "what is you're name.",
            "expected": "what[What] is you're[your] name<?>"
        },
        {
            "name": "原始示例2 - 冠词+拼写+标点",
            "input": "She is a amazin person",
            "expected": "She is a[an] amazin[amazing] person<.>"
        },
        {
            "name": "主谓一致错误",
            "input": "The data suggest different conclusions",
            "expected": "The data suggest[suggests] different conclusions<.>"
        },
        {
            "name": "无错误文本",
            "input": "The quick brown fox jumps over the lazy dog.",
            "expected": "✅ No errors found."
        }
    ]
    
    passed = 0
    total = len(key_cases)
    
    for i, case in enumerate(key_cases, 1):
        print(f"\n🧪 案例 {i}: {case['name']}")
        print(f"输入: \"{case['input']}\"")
        print(f"期望: \"{case['expected']}\"")
        print("处理中...")
        
        try:
            result = process_text(case['input'], verbose=False)
            actual = result['corrected_text']
            approved = result['approved']
            iterations = result['iterations']
            
            print(f"实际: \"{actual}\"")
            print(f"迭代: {iterations} 次")
            print(f"通过: {'是' if approved else '否'}")
            
            # 检查结果
            if actual == case['expected'] and approved:
                print("✅ 测试通过")
                passed += 1
            else:
                print("❌ 测试失败")
                if not approved:
                    print(f"反馈: {result['check_result']}")
            
        except Exception as e:
            print(f"❌ 处理错误: {e}")
        
        print("-" * 40)
    
    # 总结
    pass_rate = (passed / total * 100) if total > 0 else 0
    print(f"\n📊 测试结果: {passed}/{total} 通过 ({pass_rate:.1f}%)")
    
    if pass_rate >= 80:
        print("🎉 系统运行良好！")
        return True
    else:
        print("⚠️ 系统需要进一步调优")
        return False

def main():
    """主函数"""
    try:
        success = test_key_cases()
        
        if success:
            print("\n🚀 你可以运行完整测试:")
            print("   python test_comprehensive.py")
            print("\n🎮 或者运行交互演示:")
            print("   python run_fixed_demo.py")
        
        return success
        
    except Exception as e:
        print(f"❌ 测试出错: {e}")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n👋 测试中断")
        sys.exit(0)