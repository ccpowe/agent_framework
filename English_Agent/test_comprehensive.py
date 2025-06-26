#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
使用comprehensive_test.json测试LangGraph英语纠错系统
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List

# 确保能找到模块
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def load_test_cases() -> Dict:
    """加载测试案例"""
    test_file = current_dir / "comprehensive_test.json"
    
    try:
        with open(test_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ 测试文件不存在: {test_file}")
        return {}
    except json.JSONDecodeError as e:
        print(f"❌ JSON格式错误: {e}")
        return {}

def test_category(category_name: str, test_cases: List[Dict], process_text_func) -> Dict:
    """测试特定类别的案例"""
    print(f"\n📋 测试类别: {category_name}")
    print("-" * 50)
    
    results = {
        "total": len(test_cases),
        "passed": 0,
        "failed": 0,
        "details": []
    }
    
    for i, case in enumerate(test_cases, 1):
        input_text = case["input"]
        expected_output = case["expected_output"]
        
        print(f"\n🧪 案例 {i}/{len(test_cases)}")
        print(f"输入: \"{input_text}\"")
        print(f"期望: \"{expected_output}\"")
        
        try:
            result = process_text_func(input_text, verbose=False)
            actual_output = result['corrected_text']
            approved = result['approved']
            iterations = result['iterations']
            
            print(f"实际: \"{actual_output}\"")
            print(f"通过: {'是' if approved else '否'} (迭代: {iterations})")
            
            # 检查输出是否匹配期望
            if actual_output == expected_output and approved:
                print("✅ 测试通过")
                results["passed"] += 1
                status = "PASS"
            else:
                print("❌ 测试失败")
                results["failed"] += 1
                status = "FAIL"
                if not approved:
                    print(f"反馈: {result['check_result']}")
            
            results["details"].append({
                "input": input_text,
                "expected": expected_output,
                "actual": actual_output,
                "approved": approved,
                "iterations": iterations,
                "status": status
            })
            
        except Exception as e:
            print(f"❌ 处理错误: {e}")
            results["failed"] += 1
            results["details"].append({
                "input": input_text,
                "expected": expected_output,
                "actual": f"ERROR: {e}",
                "approved": False,
                "iterations": 0,
                "status": "ERROR"
            })
    
    return results

def generate_report(all_results: Dict) -> None:
    """生成测试报告"""
    print("\n" + "=" * 80)
    print("📊 测试报告总结")
    print("=" * 80)
    
    total_cases = 0
    total_passed = 0
    total_failed = 0
    
    for category, results in all_results.items():
        total_cases += results["total"]
        total_passed += results["passed"]
        total_failed += results["failed"]
        
        pass_rate = (results["passed"] / results["total"] * 100) if results["total"] > 0 else 0
        
        print(f"\n📋 {category}:")
        print(f"   总计: {results['total']} | 通过: {results['passed']} | 失败: {results['failed']} | 通过率: {pass_rate:.1f}%")
    
    overall_pass_rate = (total_passed / total_cases * 100) if total_cases > 0 else 0
    
    print(f"\n🎯 总体结果:")
    print(f"   总计: {total_cases} | 通过: {total_passed} | 失败: {total_failed} | 通过率: {overall_pass_rate:.1f}%")
    
    if overall_pass_rate >= 90:
        print("🎉 优秀！系统表现很好")
    elif overall_pass_rate >= 70:
        print("👍 良好！还有改进空间")
    else:
        print("⚠️ 需要改进！存在较多问题")

def save_detailed_report(all_results: Dict) -> None:
    """保存详细报告到文件"""
    report_file = current_dir / "test_report.json"
    
    try:
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(all_results, f, indent=2, ensure_ascii=False)
        print(f"\n📄 详细报告已保存到: {report_file}")
    except Exception as e:
        print(f"❌ 保存报告失败: {e}")

def main():
    """主测试函数"""
    print("🧪 LangGraph英语纠错系统 - 综合测试")
    print("=" * 80)
    
    # 检查环境
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = ["MODEL_NAME", "OPENAI_API_KEY", "MODEL_BASE_URL"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ 缺少环境变量: {', '.join(missing_vars)}")
        return False
    
    print("✅ 环境配置检查通过")
    
    # 导入模块
    try:
        from new_EnglishAgent import process_text
        print("✅ 模块导入成功")
    except ImportError as e:
        print(f"❌ 模块导入失败: {e}")
        return False
    
    # 加载测试案例
    test_cases = load_test_cases()
    if not test_cases:
        print("❌ 无法加载测试案例")
        return False
    
    print(f"✅ 加载了 {len(test_cases)} 个测试类别")
    
    # 运行测试
    all_results = {}
    
    for category_name, cases in test_cases.items():
        if cases:  # 确保类别不为空
            results = test_category(category_name, cases, process_text)
            all_results[category_name] = results
    
    # 生成报告
    generate_report(all_results)
    save_detailed_report(all_results)
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n👋 测试中断")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 测试过程出错: {e}")
        sys.exit(1)