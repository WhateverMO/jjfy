import numpy as np



def calculate_weights(questionnaires):
    """
    计算多份问卷各板块权重
    - 使用固定 SECTION_COUNTS 和 SCORES
    - 若题目数不匹配或存在多选题，报错并终止程序
    - 返回三层嵌套列表 [[[板块1],[板块2],...], ...]
    """
    results = []
    section_total = sum(SECTION_COUNTS)

    for idx, answers in enumerate(questionnaires, 1):
        # 检查题目数
        if len(answers) != section_total:
            raise ValueError(f"第{idx}份问卷题目数为{len(answers)}与板块划分总数目{section_total}不一致，请检查。")

        pointer = 0
        section_weights = []

        for count in SECTION_COUNTS:
            section = answers[pointer:pointer + count]
            pointer += count

            # 检查多选题
            for q_idx, q in enumerate(section, 1):
                if sum(q) > 1:
                    raise ValueError(f"第{idx}份问卷第{q_idx}题存在多选题：{q}")

            # 计算板块中每题得分
            section_scores = []
            for q in section:
                if q == [0, 0, 0]:
                    section_scores.append(0)
                else:
                    section_scores.append(sum(np.array(q) * np.array(SCORES)))

            section_scores = np.array(section_scores, dtype=float)
            total = np.sum(section_scores)
            if total > 0:
                weights = section_scores / total
            else:
                weights = np.zeros_like(section_scores)

            # 保留三位小数
            section_weights.append([round(w, 3) for w in weights])

        results.append(section_weights)

    return results


def transpose_by_section(weight_results):
    """
    将每份问卷的板块结果按板块汇总
    - 输入：calculate_weights 返回的三层列表
    - 输出：三层列表，每个板块汇总各份问卷对应的权重
    """
    if not weight_results:
        return []

    num_sections = len(weight_results[0])
    transposed = []

    for sec_idx in range(num_sections):
        sec_list = [weight_results[q_idx][sec_idx] for q_idx in range(len(weight_results))]
        transposed.append(sec_list)

    return transposed


"""-----------------------------------拆分----------------------------------------"""
def split_questionnaire_counts_random(questionnaire_counts, seed=None):
    """
    将汇总问卷统计随机拆分为每份单独问卷
    输入：
        questionnaire_counts: [[重要人数, 一般人数, 不重要人数], ...]
        seed: 随机种子，可选
    输出：
        每份问卷列表 [[题1选项, 题2选项, ...], ...]
    规则：
        - 最大人数总和为拆分份数
        - 不足的题用 [0,0,0] 补齐
        - 每道题的选项顺序随机分布
    """
    if seed is not None:
        np.random.seed(seed)

    # 每道题总人数
    total_per_question = [sum(q) for q in questionnaire_counts]
    max_count = max(total_per_question)  # 最大问卷份数

    num_questions = len(questionnaire_counts)
    split_questionnaires = [[] for _ in range(max_count)]

    for q_idx, q in enumerate(questionnaire_counts):
        counts = q.copy()
        # 构造该题的所有选项列表
        options_list = []
        options_list.extend([[1,0,0]] * counts[0])
        options_list.extend([[0,1,0]] * counts[1])
        options_list.extend([[0,0,1]] * counts[2])
        # 补齐不足的份数
        if len(options_list) < max_count:
            options_list.extend([[0,0,0]] * (max_count - len(options_list)))
        # 随机打乱顺序
        np.random.shuffle(options_list)
        # 分配到每份问卷
        for i in range(max_count):
            split_questionnaires[i].append(options_list[i])

    return split_questionnaires


def delete_elements(lst):
    """
    删除二维列表中第20-22、27-30、33-35个元素（按数数习惯从1开始）

    参数:
    lst: 二维列表

    返回:
    新的二维列表（原列表不会被修改）
    """
    # 要删除的范围（1-based索引）
    ranges_to_delete = [(9, 10), (18, 18), (21, 21), (23, 23), (58, 60), (65, 68), (71, 73)]

    # 转换为0-based索引
    ranges_0_based = []
    for start, end in ranges_to_delete:
        ranges_0_based.append((start - 1, end - 1))

    # 创建要删除的索引集合
    indices_to_delete = set()
    for start, end in ranges_0_based:
        indices_to_delete.update(range(start, end + 1))

    # 创建新列表，跳过要删除的索引
    result = [element for i, element in enumerate(lst) if i not in indices_to_delete]

    return result

# 固定板块题目数
SECTION_COUNTS = [8, 3, 4, 2, 2, 4, 4, 3, 3]
list2 = [3, 2, 3, 3, 3, 2, 3, 3, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 3, 3, 2, 2, 3]
SECTION_COUNTS.extend(list2)
# print(SECTION_COUNTS)
# 固定各选项分数
SCORES = [5, 2.9, 1.7]
