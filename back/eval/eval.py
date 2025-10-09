import numpy as np
import json

from scipy.optimize import linprog

from .weight_utils import (
    calculate_weights,
    transpose_by_section,
    split_questionnaire_counts_random,
    delete_elements,
)

import numpy as np

from .weight_calc_method_main import process_weight_list, split_list_at_indices

from .question_2 import calculate_final_scores

from .model_score_cal_main import calculate_model_score

from .generate_dict_main import build_score_structure
from .generate_dict_main import level1_names, level2_names, level3_names

from .test_case import qa1_case1, qa1_case2, qa1_case3, qa1_case4
from .test_case import qa2_case1, qa2_case2, qa2_case3, qa2_case4


def eval_qa(questionnaire_1_counts, questionnaire_2_counts, method="entropy"):
    questionnaire_1_counts = delete_elements(questionnaire_1_counts)
    split_qs = split_questionnaire_counts_random(questionnaire_1_counts, seed=42)
    # print(split_qs)
    # print(f"拆分后问卷总数: {len(split_qs)}")
    # print("前3份问卷示例:")
    # for i in range(len(split_qs)):
    #     print(split_qs[i])

    print("第一步已完成")

    """-----------------------第二部分，计算问卷一得到的权重-------------------------"""
    # 计算每份问卷板块权重
    orig_weights = calculate_weights(split_qs)

    # 按板块汇总各问卷
    transposed_weights = transpose_by_section(orig_weights)
    # with open('transposed.txt', 'w', encoding='utf-8') as f:
    #     f.write(json.dumps(transposed_weights, ensure_ascii=False, indent=2))
    #     print("transposed.txt写入成功!")

    # # 打印结果
    # print("每份问卷板块权重（原顺序）：")
    # print(orig_weights)

    # print("\n按板块汇总各问卷：")
    # print(transposed_weights)
    print("第二步已完成")

    """-----------------------第三部分，主客观确权（bwm或熵权法）-------------------------"""
    # 调用函数（选择BWM方法）
    # print(transposed_weights)
    weights_results = process_weight_list(transposed_weights, method)
    # print(f"{method}方法计算结果：", weights_results)

    # ---------------------------------
    # 切割列表
    l1_weights, l2_weights, l3_weights = split_list_at_indices(weights_results, 1, 8)

    print("第三步已完成")

    """-----------------------第四部分，从问卷二得到三级指标得分-------------------------"""

    # 调用函数计算结果
    l3_scores = calculate_final_scores(questionnaire_2_counts)
    # 打印输出
    # print("各模块题目得分（二维列表形式）：")
    # print("l3_scores:",l3_scores)
    # print("len(l3_scores):",len(l3_scores))

    # x = [3, 2, 3, 3, 3, 2, 3, 3, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 3, 3, 2, 2, 3]
    # print(len(x))
    # print(sum(x))

    # 对三级指标得分进行模块分割
    l3_scores = split_list_at_indices(
        l3_scores,
        3,
        2,
        3,
        3,
        3,
        2,
        3,
        3,
        1,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        3,
        2,
        3,
        3,
        2,
        2,
        3,
    )

    print("第四步已完成")
    """-----------------------第五部分，计算各级指标得分和模型得分-------------------------"""

    try:
        model_scores, l1_scores, l2_scores = calculate_model_score(
            l1_weights, l2_weights, l3_weights, l3_scores
        )
        # print(f"模型总得分: {model_scores}")
        # print("各级指标得分：")
        # print("一级指标得分：",l1_scores)
        # print("二级指标得分：",l2_scores)
        print("第五步已完成")
    except Exception as e:
        print(f"计算错误: {e}")

    """-----------------------第六部分，输出字典形式-------------------------"""

    level_name = "控制级"

    # 构建字典结构
    score_dict = build_score_structure(
        level1_names,
        level2_names,
        level3_names,
        l1_scores,
        l2_scores,
        l3_scores,
        model_scores,
        level_name,
    )

    # 打印结果
    print(f"模型得分（采用{method}方法）：", model_scores)
    # print(json.dumps(score_dict, ensure_ascii=False, indent=2))

    # with open('output.txt', 'w', encoding='utf-8') as f:
    #     f.write(json.dumps(score_dict, ensure_ascii=False, indent=2))
    #     print("output.txt写入成功!")

    print("第六步已完成")

    return score_dict


if __name__ == "__main__":
    print(eval_qa(qa1_case1, qa2_case1, "bwm"))
    # main(qa1_case2,qa2_case2,"bwm")
    # main(qa1_case3,qa2_case3,"bwm")
    # main(qa1_case4,qa2_case4,"bwm")

    # main(qa1_case1,qa2_case1,"entropy")
    # main(qa1_case2,qa2_case2,"entropy")
    # main(qa1_case3,qa2_case3,"entropy")
    # main(qa1_case4,qa2_case4,"entropy")
