import re
import random


def gen_templated_string(templates, subgoal, ai_player, target, scenario_string):

    candidates = []

    if subgoal == "抓人":
        candidates = get_gank_candidates(templates, ai_player, target, scenario_string)

    # random choose one candidate
    if len(candidates) > 0: 
        final_result = random.choice(candidates)
    else:
        final_result = ""
    
    return final_result

def get_gank_candidates(templates, ai_player, target, scenario_string):
    candidates = []
    info = {}
    template_list = []
    tags = []

    # 解析所有有用的信息到 info
    info = {
        "target": target,
    }

    # 根据信息判断是否满足“TAG”，并将“TAG”中的所有模板加入 template_list。
    if "玩家近" in scenario_string:
        tags.append("玩家近")
    
    # 将所有命中 tag 的template 加入 template_list
    for tag in tags:
        template_list.extend(get_tempaltes_with_subgoal_and_tag(templates, "抓人", tag, ai_player))
    if len(template_list) == 0:
        template_list.extend(get_tempaltes_with_subgoal_and_tag(templates, "抓人", "兜底", ai_player))

    # generate string candidates
    for template in template_list:
        candidate = sub_string(template, info)
        if len(candidate) > 0:
            candidates.append(candidate)

    if len(candidates) == 0:
        candidates.append(f"抓{target}。")

    return candidates

    
def get_tempaltes_with_subgoal_and_tag(templates, subgoal, tag, ai_player):
    result = templates.get(subgoal, {}).get(tag, {}).get(ai_player, [])
    if len(result) == 0:
        result = templates.get(subgoal, {}).get(tag, {}).get("兜底", [])
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

    template = template.replace("｜", "|")

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