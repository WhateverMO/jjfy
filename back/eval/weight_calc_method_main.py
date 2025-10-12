import numpy as np
from .weight_calc_method import bwm_method
from .weight_calc_method import entropy_method

import numpy as np  # 若原始数据含np.float64，需导入numpy

from .test_case import qa1_case1, qa1_case2, qa1_case3, qa1_case4
from .test_case import qa2_case1, qa2_case2, qa2_case3, qa2_case4


def process_weight_list(input_list, method="bwm"):
    """
    处理嵌套权重列表，调用指定方法计算并返回所有结果

    参数：
        input_list: list - 输入的3层嵌套列表（外层含多个a级别的二级子列表）
        method: str - 选择调用的方法，"bwm"调用bwm_method()，"entropy"调用entropy_method()，默认"bwm"

    返回：
        result_list: list - 所有a级别子列表的计算结果，顺序与输入外层列表一致
    """
    # 1. 初始化结果列表，用于存储每个a级别的计算结果
    result_list = []

    # 2. 循环处理输入列表中的每个a级别子列表（即外层列表的每个元素）
    for a_level_data in input_list:
        # print(a_level_data)
        # （可选）将np.float64类型转为普通float（避免潜在类型问题，若方法支持np.float64可跳过）
        # 处理逻辑：遍历a级别子列表的每一行，将np.float64转为float
        a_level_data_converted = [
            [float(num) for num in row]  # 行内元素转float
            for row in a_level_data  # 遍历a级别子列表的每一行
        ]

        # 3. 根据选择的方法调用对应函数，计算结果
        if method == "bwm":
            # current_result = bwm_method(a_level_data_converted)  # 调用BWM方法
            bwm_weights, bwm_CR = bwm_method(a_level_data_converted)
            result_list.append(bwm_weights)

        elif method == "entropy":
            # current_result = entropy_method(a_level_data_converted)  # 调用熵权法
            entropy_weights, info = entropy_method(a_level_data_converted)
            result_list.append(entropy_weights)

        else:
            raise ValueError("方法选择错误！请传入 'bwm' 或 'entropy'")

    return result_list


def split_list_at_indices(lst, *split_sizes):
    """
    将列表按照指定的大小分割成多个子列表

    参数:
    lst: 要分割的列表
    *split_sizes: 可变参数，表示每个子列表的大小

    返回:
    分割后的嵌套列表

    规则:
    - 如果分割大小总和等于列表长度：按指定大小分割
    - 如果分割大小总和小于列表长度：剩余元素自动组成最后一个子列表
    - 如果分割大小总和大于列表长度：抛出错误
    """
    if len(split_sizes) == 1 and isinstance(split_sizes[0], list):
        split_sizes = split_sizes[0]

    total_split_size = sum(split_sizes)

    # 检查分割大小总和是否大于列表长度
    if total_split_size > len(lst):
        raise ValueError(f"分割大小总和({total_split_size})大于列表长度({len(lst)})")

    result = []
    start_index = 0

    # 按指定大小分割
    for size in split_sizes:
        sublist = lst[start_index : start_index + size]
        result.append(sublist)
        start_index += size

    # 如果还有剩余元素，添加到结果中
    if start_index < len(lst):
        remaining_sublist = lst[start_index:]
        result.append(remaining_sublist)

    return result


def main():
    input_data_pre = [
        [[0.342, 0.199, 0.116, 0.342], [0.269, 0.463, 0.0, 0.269]],
        [[0.0, 0.5, 0.5], [0.427, 0.145, 0.427]],
        [[0.746, 0.254], [0.63, 0.37]],
        [[0.342, 0.199, 0.116, 0.342], [0.269, 0.463, 0.0, 0.269]],
        [[0.0, 0.5, 0.5], [0.427, 0.145, 0.427]],
        [[0.746, 0.254], [0.63, 0.37]],
        [[0.342, 0.199, 0.116, 0.342], [0.269, 0.463, 0.0, 0.269]],
        [[0.0, 0.5, 0.5], [0.427, 0.145, 0.427]],
        [[0.746, 0.254], [0.63, 0.37]],
        [
            [
                np.float64(0.292),
                np.float64(0.099),
                np.float64(0.17),
                np.float64(0.17),
                np.float64(0.17),
                np.float64(0.0),
                np.float64(0.099),
                np.float64(0.0),
            ],
            [
                np.float64(0.21),
                np.float64(0.123),
                np.float64(0.123),
                np.float64(0.0),
                np.float64(0.21),
                np.float64(0.123),
                np.float64(0.21),
                np.float64(0.0),
            ],
            [
                np.float64(0.092),
                np.float64(0.27),
                np.float64(0.092),
                np.float64(0.27),
                np.float64(0.092),
                np.float64(0.0),
                np.float64(0.092),
                np.float64(0.092),
            ],
        ],
    ]
    # 调用函数（选择BWM方法）
    bwm_results = process_weight_list(input_data_pre, method="bwm")
    print("BWM方法计算结果：", bwm_results)

    # 调用函数（选择熵权法）
    # entropy_results = process_weight_list(input_data_pre, method="entropy")
    # print("熵权法计算结果：", entropy_results)

    # ---------------------------------
    # 切割列表
    l1_bwm, l2_bwm, l3_bwm = split_list_at_indices(bwm_results, 1, 8)
    print("---------------")
    print(
        "一级指标权重：",
        l1_bwm,
        "\n",
        "二级指标权重：",
        l2_bwm,
        "\n",
        "三级指标权重：",
        l3_bwm,
    )

    # l1_entropy,l2_entropy,l3_entropy = split_list_at_indices(entropy_results, 1, 3)
    # print("---------------")
    # print("一级指标权重：",l1_entropy,"\n","二级指标权重：",l2_entropy,"\n","三级指标权重：",l3_entropy)


if __name__ == "__main__":
    main()
