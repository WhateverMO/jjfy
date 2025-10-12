# score_functions.py

def calculate_final_scores(questionnaire_counts, q2_section, module_total=100):
    """
    输入：
        questionnaire_counts: 二维列表，每题是选项计数，如 [[10,5], [20,1,6,5], ...]
        q2_section: 每个模块包含题目索引的列表，如 [[0,2,3], [1,4,5]]
        module_total: 每个模块的总分（默认100）
    输出：
        二维列表：每个模块中每道题的得分（保留两位小数）
    """
    results = []

    # 检查题目索引是否有效
    max_index = len(questionnaire_counts) - 1
    for sec_idx, indices in enumerate(q2_section, 1):
        for idx in indices:
            if idx < 0 or idx > max_index:
                print(f"⚠️ 第{sec_idx}模块包含的题目索引 {idx} 超出题目总数 {len(questionnaire_counts)}，请检查。")
                return []

    # 计算单选题（长度为2）的最大答卷数
    single_totals = [sum(q) for q in questionnaire_counts if len(q) == 2]
    if not single_totals:
        print("⚠️ 未检测到单选题，无法确定问卷总份数。")
        return []
    total_forms = max(single_totals)

    for indices in q2_section:
        count = len(indices)
        base_score = module_total / count  # 每题基础分
        section_scores = []

        for idx in indices:
            q = questionnaire_counts[idx]
            if len(q) == 2:
                # 单选题
                score = base_score * (q[0] / total_forms)
            else:
                # 多选题（按选项总数平均）
                score = (base_score * (sum(q) / len(q))) / total_forms

            section_scores.append(round(score, 2))

        results.append(section_scores)

    result = [sum(lst) for lst in results]

    return result


# 模块划分示例（可以乱序）
# 比如总共有6题，模块1包含第1、3、4题，模块2包含第2、5、6题
SECTION_INDICES = []

# 前45题，3题一个模块 -> 15个模块
for i in range(0, 45, 3):
    SECTION_INDICES.append([i, i+1, i+2])

# 46-62，每题一个模块 -> 17个模块
for i in range(45, 62):
    SECTION_INDICES.append([i])

# 后面的特殊模块
SECTION_INDICES.extend([
    [62, 67, 65],  # 对应【63,68,66】，注意索引减1
    [63, 66],      # 对应【64,67】
    [64, 70, 69],  # 对应【65,71,70】
    [68],          # 对应【69】
    [71, 74],      # 对应【72,75】
    [72],          # 对应【73】
    [73],          # 对应【74】
    [75, 76],      # 对应【76,77】
])

# 78-79为一个模块
SECTION_INDICES.append([77, 78])  # 索引从0开始

# 80-121，每三题一个模块 -> 14个模块
for i in range(79, 121, 3):
    SECTION_INDICES.append([i, i+1, i+2])

# 122-123一个模块
SECTION_INDICES.append([121, 122])

# 124-132，每三题一个模块 -> 3个模块
for i in range(123, 132, 3):
    SECTION_INDICES.append([i, i+1, i+2])

# print(SECTION_INDICES)

a = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11], [12, 13, 14], [15, 16, 17], [18, 19, 20], [21, 22, 23], [24, 25, 26], [27, 28, 29], [30, 31, 32], [33, 34, 35], [36, 37, 38], [39, 40, 41], [42, 43, 44], [45], [46], [47], [48], [49], [50], [51], [52], [53], [54], [55], [56], [57], [58], [59], [60], [61], [62, 67, 65], [63, 66], [64, 70, 69], [68], [71, 74], [72], [73], [75, 76], [77, 78], [79, 80, 81], [82, 83, 84], [85, 86, 87], [88, 89, 90], [91, 92, 93], [94, 95, 96], [97, 98, 99], [100, 101, 102], [103, 104, 105], [106, 107, 108], [109, 110, 111], [112, 113, 114], [115, 116, 117], [118, 119, 120], [121, 122], [123, 124, 125], [126, 127, 128], [129, 130, 131]]
