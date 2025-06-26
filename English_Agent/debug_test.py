#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
调试测试新的多代理英语纠错系统
"""

import os
from dotenv import load_dotenv

def test_environment():
    """测试环境配置"""
    load_dotenv()
    
    print("🔍 环境检查:")
    required_vars = ["MODEL_NAME", "OPENAI_API_KEY", "MODEL_BASE_URL"]
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: {'*' * 10}")  # 隐藏敏感信息
        else:
            print(f"❌ {var}: 未设置")
    
    return all(os.getenv(var) for var in required_vars)

def test_import():
    """测试模块导入"""
    try:
        from new_EnglishAgent import process_text
        print("✅ 模块导入成功")
        return True, process_text
    except Exception as e:
        print(f"❌ 模块导入失败: {e}")
        return False, None

def test_simple_case(process_text_func):
    """测试简单案例"""
    test_text = "hello world"
    print(f"\n🧪 测试文本: '{test_text}'")
    
    try:
        result = process_text_func(test_text, verbose=True)
        print(f"\n📊 结果:")
        print(f"  原文: {result['original_text']}")
        print(f"  修正: {result['corrected_text']}")
        print(f"  检查: {result['check_result']}")
        print(f"  通过: {result['approved']}")
        return True
    except Exception as e:
        print(f"❌ 处理失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔧 调试测试多代理英语纠错系统")
    print("=" * 50)
    
    # 测试环境
    if not test_environment():
        print("\n❌ 环境配置有问题，请检查 .env 文件")
        exit(1)
    
    # 测试导入
    success, process_text = test_import()
    if not success:
        exit(1)
    
    # 测试简单案例
    if test_simple_case(process_text):
        print("\n✅ 基础测试通过")
    else:
        print("\n❌ 基础测试失败")
        exit(1) 