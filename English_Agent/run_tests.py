"""run_tests.py
测试 English_Agent 智能体的语法纠错能力。

读取 test.json 中的测试用例，调用 englishAgent 中的 `agent` 对象，
保存每个输入句子的模型输出与期望输出到 result.json。
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

# --- 常量配置 ---
TEST_FILE = Path(__file__).with_name("test.json")
RESULT_FILE = Path(__file__).with_name("result_8.json")

# --- 导入智能体 ---
try:
    from englishAgent import agent
except Exception as import_err:  # noqa: BLE001
    raise RuntimeError(
        "无法导入 englishAgent 中的 agent 对象，请确认环境变量和依赖已正确配置。"
    ) from import_err


def evaluate_sentence(sentence: str) -> str:
    """调用智能体，获取模型输出。

    参数:
        sentence: 用户输入句子。
    返回:
        智能体输出字符串。
    """
    # agent.run() 返回一个包含 content 属性的对象
    response = agent.run(sentence)
    return getattr(response, "content", str(response))


def run_tests() -> None:
    """执行所有测试并生成结果文件。"""
    if not TEST_FILE.exists():
        raise FileNotFoundError(f"未找到测试文件: {TEST_FILE}")

    with TEST_FILE.open("r", encoding="utf-8") as f:
        test_data: Dict[str, Any] = json.load(f)

    results: Dict[str, Any] = {}

    # 遍历难度级别
    for level, examples in test_data.items():
        level_results = []
        for case in examples:
            sentence = case["input"]
            expected = case["expected_output"]
            # 获取模型答案
            try:
                model_output = evaluate_sentence(sentence)
            except Exception as call_err:  # noqa: BLE001
                model_output = f"<Error: {call_err}>"

            level_results.append(
                {
                    "input": sentence,
                    "expected_output": expected,
                    "model_output": model_output,
                }
            )
        results[level] = level_results

    # 写入结果文件
    with RESULT_FILE.open("w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"测试完成，结果已保存至 {RESULT_FILE}")


if __name__ == "__main__":
    run_tests()
