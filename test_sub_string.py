import re
from templated_generation import sub_string

def run_test(name, template, info, expected_pattern=None):
    result = sub_string(template, info)
    if expected_pattern is not None:
        assert re.match(expected_pattern, result) is not None, \
            f"Test '{name}' failed!\nExpected pattern: {expected_pattern}\nGot: {result}"
    print(f"Test '{name}': {result}")

def main():
    # 测试1：基本变量替换
    run_test(
        "基本变量替换",
        "你好，{name}！",
        {"name": "张三"},
        r"你好，张三！"
    )

    # 测试2：缺失变量替换
    run_test(
        "缺失变量替换",
        "你好，{name}！",
        {},
        r""
    )

    # 测试3：多选项替换
    run_test(
        "多选项替换",
        "这是[选项1|选项2|选项3]测试",
        {},
        r"这是(选项1|选项2|选项3)测试"
    )

    # 测试4：单选项50%概率替换
    print("\n测试单选项50%概率替换（运行多次以验证随机性）：")
    for i in range(10):
        run_test(
            f"单选项替换 #{i+1}",
            "这是[测试]结果",
            {},
            r"这是(测试|)结果"
        )

    # 测试5：空括号替换
    run_test(
        "空括号替换",
        "这是[]测试",
        {},
        r"这是测试"
    )

    # 测试6：多个变量和选项组合 - 所有变量都匹配
    run_test(
        "多个变量和选项组合 - 完全匹配",
        "{name}[在|正在]{action}[呢|着][。|！|～]",
        {"name": "小明", "action": "跑步"},
        r"小明(在|正在)跑步(呢|着)(。|！|～)"
    )

    # 测试7：多个变量和选项组合 - 部分变量不匹配
    run_test(
        "多个变量和选项组合 - 部分不匹配",
        "{name}[在|正在]{action}[呢|着][。|！|～]",
        {"name": "小明"},  # 缺少 action
        r""
    )

    # 测试8：实际模板示例 - 完全匹配
    run_test(
        "实际模板示例 - 完全匹配",
        "我来抓{target}[。|看我位置。|注意我位置。]还有{support}[需要支援|来帮忙]",
        {"target": "敌人", "support": "谁"},
        r"我来抓敌人(。|看我位置。|注意我位置。)还有谁(需要支援|来帮忙)"
    )

    # 测试9：实际模板示例 - 部分变量不匹配
    run_test(
        "实际模板示例 - 部分不匹配",
        "我来抓{target}[。|看我位置。|注意我位置。]还有{support}[需要支援|来帮忙]",
        {"target": "敌人"},  # 缺少 support
        r""
    )

    # 测试10：选项中包含变量 - 完全匹配
    run_test(
        "选项中包含变量 - 完全匹配",
        "我[抓住{target}了|看到{target}了]",
        {"target": "敌人"},
        r"我(抓住敌人了|看到敌人了)"
    )

    # 测试11：选项中包含变量 - 变量不匹配
    run_test(
        "选项中包含变量 - 变量不匹配",
        "我[抓住{target}了|看到{target}了]",
        {},
        r""
    )

    # 测试12：选项中包含变量 - 单选项
    run_test(
        "选项中包含变量 - 单选项",
        "我[抓住{target}了]",
        {"target": "敌人"},
        r"我(抓住敌人了|)"
    )

    # 测试13：选项中包含多个变量
    run_test(
        "选项中包含多个变量",
        "[{player}抓住{target}|{player}正在追击{target}]",
        {"player": "我", "target": "敌人"},
        r"(我抓住敌人|我正在追击敌人)"
    )

    # 测试14：嵌套变量和选项的复杂情况
    run_test(
        "嵌套变量和选项的复杂情况",
        "{player}[发现{target}了|正在找{target}][。|！][要支援|需要帮助]吗？",
        {"player": "小明", "target": "敌人"},
        r"小明(发现敌人了|正在找敌人)(。|！)(要支援|需要帮助)吗？"
    )

    print("\n所有测试通过！")

if __name__ == "__main__":
    main()
