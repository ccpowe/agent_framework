#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
快速演示脚本 - 测试LangGraph英语纠错系统
"""

import os
import sys
from pathlib import Path

# 确保能找到模块
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def check_environment():
    """检查环境配置"""
    print("🔧 检查环境配置...")
    
    required_vars = ["MODEL_NAME", "OPENAI_API_KEY", "MODEL_BASE_URL"]
    missing_vars = []
    
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing_vars.append(var)
        else:
            # 隐藏API密钥的部分内容
            if "API_KEY" in var and len(value) > 10:
                display_value = value[:10] + "..." + value[-4:]
            else:
                display_value = value
            print(f"  ✅ {var}: {display_value}")
    
    if missing_vars:
        print(f"  ❌ 缺少环境变量: {', '.join(missing_vars)}")
        return False
    
    return True

def test_import():
    """测试模块导入"""
    print("\n📦 测试模块导入...")
    
    try:
        from new_EnglishAgent import process_text, create_english_correction_graph
        print("  ✅ 成功导入 new_EnglishAgent 模块")
        return True
    except ImportError as e:
        print(f"  ❌ 导入失败: {e}")
        return False

def run_simple_demo():
    """运行简单演示"""
    print("\n🚀 运行简单演示...")
    
    try:
        from new_EnglishAgent import process_text
        
        # 简单测试用例
        test_cases = [
            "hello world",  # 无错误文本
            "what is you're name.",  # 多种错误
        ]
        
        for i, text in enumerate(test_cases, 1):
            print(f"\n--- 测试用例 {i} ---")
            print(f"输入: \"{text}\"")
            
            try:
                result = process_text(text, verbose=False)
                print(f"输出: \"{result['corrected_text']}\"")
                print(f"迭代: {result['iterations']} 次")
                print(f"通过: {'是' if result['approved'] else '否'}")
                
                if not result['approved']:
                    print(f"反馈: {result['check_result']}")
                    
            except Exception as e:
                print(f"❌ 处理失败: {e}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ 演示失败: {e}")
        return False

def main():
    """主函数"""
    print("🎯 LangGraph英语纠错系统 - 快速演示")
    print("=" * 50)
    
    # 检查环境
    if not check_environment():
        print("\n❌ 环境配置有问题，请检查 .env 文件")
        return False
    
    # 测试导入
    if not test_import():
        print("\n❌ 模块导入失败，请检查依赖")
        return False
    
    # 运行演示
    if not run_simple_demo():
        print("\n❌ 演示运行失败")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 演示完成！系统运行正常")
    
    # 询问是否运行完整演示
    try:
        choice = input("\n是否运行完整演示？(y/n): ").strip().lower()
        if choice in ['y', 'yes', '是']:
            print("\n🚀 启动完整演示...")
            from demo_langgraph import demo_correction_workflow
            demo_correction_workflow()
    except KeyboardInterrupt:
        print("\n👋 再见！")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n👋 再见！")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 意外错误: {e}")
        sys.exit(1)