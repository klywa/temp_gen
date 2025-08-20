import re
import random


class TemplatedStringGenerator:
    def __init__(self, templates):
        self.templates = templates

    def gen_templated_string(self, subgoal, ai_player, target, scenario_string):

        candidates = []

        if subgoal == "抓人":
            candidates = self.get_gank_candidates(ai_player, target, scenario_string)
        elif subgoal == "打龙":
            candidates = self.get_take_dragon_candidates(ai_player, target, scenario_string)
        elif subgoal == "推塔":
            candidates = self.get_push_tower_candidates(ai_player, target, scenario_string)

        # random choose one candidate
        if len(candidates) > 0: 
            final_result = random.choice(candidates)
        else:
            final_result = ""
        
        return final_result

    def get_gank_candidates(self, ai_player, target, scenario_string):
        candidates = []
        info = {}
        template_list = []
        tags = []

        # 解析所有有用的信息到 info
        info = {
            "target": target,
        }

        # 根据信息判断是否满足“TAG”，并将“TAG”中的所有模板加入 template_list。
        
        # 将所有命中 tag 的template 加入 template_list
        for tag in tags:
            template_list.extend(self.get_tempaltes_with_subgoal_and_tag("抓人", tag, ai_player))
        if len(template_list) == 0:
            template_list.extend(self.get_tempaltes_with_subgoal_and_tag("抓人", "兜底", ai_player))

        # generate string candidates
        for template in template_list:
            candidate = sub_string(template, info)
            if len(candidate) > 0:
                candidates.append(candidate)

        if len(candidates) == 0:
            candidates.append(f"抓{target}。")

        return candidates
    
    def get_take_dragon_candidates(self, ai_player, target, scenario_string):
        candidates = []
        info = {}
        template_list = []
        tags = []

        # 解析所有有用的信息到 info
        info = {
            "target": target,
        }

        # 根据信息判断是否满足“TAG”，并将“TAG”中的所有模板加入 template_list。
        
        # 将所有命中 tag 的template 加入 template_list
        for tag in tags:
            template_list.extend(self.get_tempaltes_with_subgoal_and_tag("打龙", tag, ai_player))
        if len(template_list) == 0:
            template_list.extend(self.get_tempaltes_with_subgoal_and_tag("打龙", "兜底", ai_player))

        # generate string candidates
        for template in template_list:
            candidate = sub_string(template, info)
            if len(candidate) > 0:
                candidates.append(candidate)

        if len(candidates) == 0:
            candidates.append(f"打{target}。")

        return candidates
    
    def get_push_tower_candidates(self, ai_player, target, scenario_string):
        candidates = []
        info = {}
        template_list = []
        tags = []

        # 解析所有有用的信息到 info
        info = {
            "target": target,
        }

        # 根据信息判断是否满足“TAG”，并将“TAG”中的所有模板加入 template_list。
        
        # 将所有命中 tag 的template 加入 template_list
        for tag in tags:
            template_list.extend(self.get_tempaltes_with_subgoal_and_tag("推塔", tag, ai_player))
        if len(template_list) == 0:
            template_list.extend(self.get_tempaltes_with_subgoal_and_tag("推塔", "兜底", ai_player))

        # generate string candidates
        for template in template_list:
            candidate = sub_string(template, info)
            if len(candidate) > 0:
                candidates.append(candidate)

        if len(candidates) == 0:
            candidates.append(f"推塔。")

        return candidates
    
    def get_tempaltes_with_subgoal_and_tag(self, subgoal, tag, ai_player):
        result = self.templates.get(subgoal, {}).get(tag, {}).get(ai_player, [])
        if len(result) == 0:
            result = self.templates.get(subgoal, {}).get(tag, {}).get("兜底", [])
        return result
    

def get_all_candidates(template_list, info):
    candidates = []
    for template in template_list:
        candidate = sub_string(template, info)
        if len(candidate) > 0:
            candidates.append(candidate)
    return candidates

def sub_string(template, info):
    """
    处理模板字符串，支持两种替换：
    1. {XX} - 从info字典中获取值，如果任何一个变量没有匹配则返回空字符串
    2. [选项1|选项2] - 随机选择一个选项
       如果只有一个选项（没有|），则50%概率保留该选项
       选项中也可以包含 {XX} 变量

    Args:
        template (str): 模板字符串
        info (dict): 替换信息字典

    Returns:
        str: 处理后的字符串，如果任何变量未匹配则返回空字符串
    """
    if not template:
        return ""

    # 首先检查所有的变量是否都能匹配
    var_pattern = r'\{(\w+)\}'
    variables = re.findall(var_pattern, template)
    for var in variables:
        if var not in info:
            return ""

    # 处理 {XX} 替换
    def replace_var(match):
        key = match.group(1)
        return info[key]  # 这里可以直接使用 info[key]，因为已经检查过所有变量都存在
    
    result = re.sub(var_pattern, replace_var, template)
    
    # 处理 [选项1|选项2] 替换
    def replace_choice(match):
        content = match.group(1)
        if not content:  # 空括号 []
            return ""
        
        options = [opt.strip() for opt in content.split("|")]
        if len(options) == 1:  # 只有一个选项，没有 |
            return options[0] if random.random() < 0.5 else ""
        return random.choice(options)
    
    result = re.sub(r'\[(.*?)\]', replace_choice, result)
    
    return result


# 单元测试
if __name__ == "__main__":
    def run_test(name, template, info, expected_pattern=None):
        result = sub_string(template, info)
        if expected_pattern is not None:
            assert re.match(expected_pattern, result) is not None, \
                f"Test '{name}' failed!\nExpected pattern: {expected_pattern}\nGot: {result}"
        print(f"Test '{name}': {result}")

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