import json
import re
from templated_generation import gen_templated_string

def load_templates():
    with open("config/templates.json", "r", encoding="utf-8") as f:
        return json.load(f)

def run_test(name, templates, subgoal, ai_player, target, scenario_string, expected_patterns=None):
    print(f"\n测试：{name}")
    print(f"输入参数：")
    print(f"  - subgoal: {subgoal}")
    print(f"  - ai_player: {ai_player}")
    print(f"  - target: {target}")
    print(f"  - scenario_string: {scenario_string}")
    
    # 运行多次以验证随机性
    results = set()
    for i in range(10):
        result = gen_templated_string(templates, subgoal, ai_player, target, scenario_string)
        results.add(result)
        print(f"第{i+1}次结果: {result}")
    
    if expected_patterns:
        for result in results:
            matched = False
            for pattern in expected_patterns:
                if re.match(pattern, result):
                    matched = True
                    break
            assert matched, f"结果 '{result}' 不符合任何预期模式: {expected_patterns}"
    
    print(f"得到 {len(results)} 种不同的结果：")
    for result in sorted(results):
        print(f"  - {result}")

def main():
    templates = load_templates()
    
    # 测试1：基本兜底模板
    run_test(
        "兜底模板测试",
        templates,
        "抓人",
        "倾雨",
        "小明",
        "",
        [
            r"抓小明[！|。]",
            r"打小明，一起上！"
        ]
    )
    
    # 测试2：玩家近情况
    run_test(
        "玩家近情况测试",
        templates,
        "抓人",
        "倾雨",
        "小明",
        "玩家近",  # 这个参数目前在代码中没有使用，但保留以备后续实现
        [
            r"我来抓小明。",
            r"我来抓小明，看我位置。",
            r"我来抓小明，注意我位置。",
            r"我来抓小明，拖住他。"
        ]
    )
    
    # 测试3：不存在的AI角色
    run_test(
        "不存在的AI角色测试",
        templates,
        "抓人",
        "不存在的角色",
        "小明",
        "",
        [r"抓小明。"]  # 应该返回默认字符串
    )
    
    # 测试4：不存在的子目标
    run_test(
        "不存在的子目标测试",
        templates,
        "不存在的子目标",
        "倾雨",
        "小明",
        "",
        [""]  # 应该返回空字符串
    )

if __name__ == "__main__":
    main()
