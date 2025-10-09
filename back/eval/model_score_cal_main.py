'''
该文件用于计算数据成熟都模型得分
输入：一、二、三级权重，三级得分
输出：模型得分
过程包含了一、二、三级得分
'''
# 映射函数
def map(score_pre):
    score_mapped = score_pre
    return score_mapped

# 专门给三级指标计算加权和的，因为三级指标需要map
def multiply_weights_scores_l3(weights, scores):
    """
    三级指标权重与评分逐元素相乘并求和
    
    参数:
        weights: 权重列表 [[w1, w2, ...], ...]
        scores: 评分列表 [[s1, s2, ...], ...]
    
    返回:
        list: 每个维度的加权和分数
    """
    # 输入验证
    if not weights or not scores:
        raise ValueError("权重和评分列表不能为空")
    
    if len(weights) != len(scores):
        raise ValueError(f"权重和评分的样本数量不匹配: 权重有{len(weights)}个样本, 评分有{len(scores)}个样本")
    
    weighted_scores_list = []
    for i, (weight_list, score_list) in enumerate(zip(weights, scores)):
        # 检查每个样本内部的维度匹配
        if len(weight_list) != len(score_list):
            raise ValueError(f"第{i+1}个样本的权重和评分维度不匹配: 权重有{len(weight_list)}个维度, 评分有{len(score_list)}个维度")
        
        # 逐元素相乘
        weighted_scores = [map(weight * score) for weight, score in zip(weight_list, score_list)]
        weighted_scores_list.append(weighted_scores)
    
    # 计算加权和
    result = []
    for weighted_scores in weighted_scores_list:
        weighted_sum = sum(weighted_scores)
        result.append(round(weighted_sum, 4))

    return result

# 给一、二级指标计算加权和的
def multiply_weights_scores(weights, scores):
    """
    权重与评分逐元素相乘并求和
    
    参数:
        weights: 权重列表 [[w1, w2, ...], ...]
        scores: 评分列表 [[s1, s2, ...], ...]
    
    返回:
        list: 每个维度的加权和分数
    """
    # 输入验证
    if not weights or not scores:
        raise ValueError("权重和评分列表不能为空")
    
    if len(weights) != len(scores):
        raise ValueError(f"权重和评分的样本数量不匹配: 权重有{len(weights)}个样本, 评分有{len(scores)}个样本")
    
    weighted_scores_list = []
    for i, (weight_list, score_list) in enumerate(zip(weights, scores)):
        # 检查每个样本内部的维度匹配
        if len(weight_list) != len(score_list):
            raise ValueError(f"第{i+1}个样本的权重和评分维度不匹配: 权重有{len(weight_list)}个维度, 评分有{len(score_list)}个维度")
        
        # 逐元素相乘
        weighted_scores = [weight * score for weight, score in zip(weight_list, score_list)]
        weighted_scores_list.append(weighted_scores)
    
    # 计算加权和
    result = []
    for weighted_scores in weighted_scores_list:
        weighted_sum = sum(weighted_scores)
        result.append(round(weighted_sum, 4))

    return result

# 用于分割列表
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
    total_split_size = sum(split_sizes)
    
    # 检查分割大小总和是否大于列表长度
    if total_split_size > len(lst):
        raise ValueError(f"分割大小总和({total_split_size})大于列表长度({len(lst)})")
    
    result = []
    start_index = 0
    
    # 按指定大小分割
    for size in split_sizes:
        sublist = lst[start_index:start_index + size]
        result.append(sublist)
        start_index += size
    
    # 如果还有剩余元素，添加到结果中
    if start_index < len(lst):
        remaining_sublist = lst[start_index:]
        result.append(remaining_sublist)
    
    return result

def calculate_model_score(level1_weights, level2_weights, level3_weights, level3_scores):
    """
    计算模型得分（三级指标加权汇总）
    
    参数:
        level1_weights: 一级指标权重列表 [w1, w2, ...]
        level2_weights: 二级指标权重列表 [[w1, w2, ...], [w3, w4, ...], ...]
        level3_weights: 三级指标权重列表 [[w1, w2, ...], [w3, w4, ...], ...]
        level3_scores: 三级指标得分列表 [[s1, s2, ...], [s3, s4, ...], ...]
    
    返回:
        float: 模型总得分
    """

    # 第一步：计算三级指标加权得分
    level2_scores_from_level3 = multiply_weights_scores_l3(level3_weights, level3_scores)
    # print("level2_scores_from_level3:",level2_scores_from_level3)
    # 第二步：根据二级指标结构分割三级加权得分
    # 计算每个二级指标对应的三级指标数量
    level2_split_sizes = [len(weights) for weights in level2_weights]
    # print("level2_split_sizes:",level2_split_sizes)
    # 分割三级加权得分为二级结构
    level2_scores_split = split_list_at_indices(level2_scores_from_level3, *level2_split_sizes)
    # print("tttt")
    # print("level2_scores_split:",level2_scores_split)

    # 第三步：计算二级指标加权得分
    level1_scores_from_level2 = multiply_weights_scores(level2_weights, level2_scores_split)
    # print("level1_scores_from_level2:",level1_scores_from_level2)

    # 第四步：计算一级指标加权得分
    # print("level1_weights：",level1_weights)
    # print(level1_scores_from_level2)
    result = sum(a * b for a, b in zip(level1_weights[0], level1_scores_from_level2))
    return result,level1_scores_from_level2,level2_scores_split
    
    # 由于一级权重只有一个列表对应一个得分列表，所以返回第一个（也是唯一一个）得分
    # return model_total_score[0]

# 测试你的例子
if __name__ == "__main__":
    # 你的测试数据
    level1_weights = [[0.6, 0.4]]
    level2_weights = [[0.2, 0.3, 0.5], [0.4, 0.6]]
    level3_weights = [[0.3, 0.7], [0.3, 0.7], [0.3, 0.7], [0.3, 0.7], [0.3, 0.7]]
    level3_scores = [[2, 3], [3, 2], [2, 3], [3, 2], [1, 3]]
    
    try:
        result,l2_scores,l1_scores = calculate_model_score(level1_weights, level2_weights, level3_weights, level3_scores)
        print(f"模型总得分: {result}")
        
        # 验证中间步骤
        # print("\n验证中间步骤:")
        # # 三级加权得分
        # level2_scores_from_level3 = multiply_weights_scores(level3_weights, level3_scores)
        # print(f"三级加权得分: {level2_scores_from_level3}")
        
        # # 分割为二级结构
        # level2_split_sizes = [len(weights) for weights in level2_weights]
        # level2_scores_split = split_list_at_indices(level2_scores_from_level3, *level2_split_sizes)
        # print(f"二级结构得分: {level2_scores_split}")
        
        # # 二级加权得分
        # level1_scores_from_level2 = multiply_weights_scores(level2_weights, level2_scores_split)
        # print(f"二级加权得分: {level1_scores_from_level2}")
        
        # # 分割为一级结构
        # level1_split_sizes = [len(weights) for weights in level1_weights]
        # level1_scores_split = split_list_at_indices(level1_scores_from_level2, *level1_split_sizes)
        # print(f"一级结构得分: {level1_scores_split}")
        
        # # 最终得分
        # final_score = multiply_weights_scores(level1_weights, level1_scores_split)
        # print(f"最终模型得分: {final_score[0]}")
        
    except Exception as e:
        print(f"计算错误: {e}")

