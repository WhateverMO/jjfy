import numpy as np
from scipy.optimize import linprog

def bwm_method(comparison_matrix_list):
    """
    BWM确权方法 - 对外暴露的接口
    参数: list[list] 
    返回: 权重向量和一致性比率
    """
    # 处理输入数据格式
    if not comparison_matrix_list:
        raise ValueError("输入数据不能为空")

    if isinstance(comparison_matrix_list[0], list) and isinstance(comparison_matrix_list[0][0], (int, float)):
        return _experts_bwm(comparison_matrix_list)
    else:
        raise ValueError("不支持的输入格式")

def _weights_to_bwm_vectors(weights):
    """
    将归一化权重转换为BWM的比较向量（内部函数）
    """
    n = len(weights)
    
    # 检查权重是否全为零
    if all(w == 0 for w in weights):
        return {
            "best_to_others": [1] * len(weights),
            "others_to_worst": [1] * len(weights)
        }        

    
    # 确定最佳和最劣准则的索引
    best_idx = np.argmax(weights)
    worst_idx = np.argmin(weights)
    
    # 生成最佳向量
    best_to_others = []
    for i in range(n):
        if i == best_idx:
            best_to_others.append(1)
        else:
            # 防止除零错误
            if weights[i] == 0:
                # 如果当前权重为0，最佳权重非0，比值为最大值9
                best_to_others.append(9)
            else:
                ratio = weights[best_idx] / weights[i]
                scaled = max(1, min(9, int(round(ratio))))
                best_to_others.append(scaled)
    
    # 生成最劣向量
    others_to_worst = []
    for i in range(n):
        if i == worst_idx:
            others_to_worst.append(1)
        else:
            # 防止除零错误
            if weights[worst_idx] == 0:
                # 如果最劣权重为0，当前权重非0，比值为最大值9
                others_to_worst.append(9)
            else:
                ratio = weights[i] / weights[worst_idx]
                scaled = max(1, min(9, int(round(ratio))))
                others_to_worst.append(scaled)
    
    return {
        "best_to_others": best_to_others,
        "others_to_worst": others_to_worst
    }

def _calculate_bwm_weights(best_to_others, others_to_worst):
    """
    BWM权重计算（内部函数）
    """


    n = len(best_to_others)
    if (n==1):
        return [1],0
    if 1 not in best_to_others or 1 not in others_to_worst:
        raise ValueError("最佳或最差准则标识错误：必须包含值1")
    
    # 构建线性规划问题
    c = np.zeros(n + 1)
    c[-1] = 1
    
    A_ub = []
    b_ub = []
    
    best_idx = np.argmin(best_to_others)
    worst_idx = np.argmin(others_to_worst)
    
    # 添加最佳准则约束
    for j in range(n):
        if j != best_idx:
            a_bj = best_to_others[j]
            # 约束1
            row1 = np.zeros(n + 1)
            row1[best_idx] = -1
            row1[j] = a_bj
            row1[-1] = -1
            A_ub.append(row1)
            b_ub.append(0)
            
            # 约束2
            row2 = np.zeros(n + 1)
            row2[best_idx] = 1
            row2[j] = -a_bj
            row2[-1] = -1
            A_ub.append(row2)
            b_ub.append(0)
    
    # 添加最差准则约束
    for j in range(n):
        if j != worst_idx:
            a_jw = others_to_worst[j]
            # 约束3
            row3 = np.zeros(n + 1)
            row3[j] = -1
            row3[worst_idx] = a_jw
            row3[-1] = -1
            A_ub.append(row3)
            b_ub.append(0)
            
            # 约束4
            row4 = np.zeros(n + 1)
            row4[j] = 1
            row4[worst_idx] = -a_jw
            row4[-1] = -1
            A_ub.append(row4)
            b_ub.append(0)
    
    # 权重和为1的约束
    A_eq = np.ones((1, n + 1))
    A_eq[0, -1] = 0
    b_eq = [1]
    
    # 变量边界
    bounds = [(1e-6, None) for _ in range(n)] + [(0, None)]
    
    # 求解线性规划
    res = linprog(c, A_ub=np.array(A_ub), b_ub=np.array(b_ub),
                 A_eq=A_eq, b_eq=b_eq, bounds=bounds)
    
    if not res.success:
        raise ValueError(f"求解失败: {res.message}")
    
    weights = res.x[:-1]
    xi = res.x[-1]
    
    # 计算一致性比率
    a_bw = best_to_others[worst_idx]
    consistency_index = {1:0, 2:0.44, 3:1.00, 4:1.63, 5:2.30, 6:3.00, 7:3.73, 8:4.47, 9:5.23}
    CI = consistency_index.get(a_bw, 1.45)
    CR = xi / CI if CI > 0 else 0
    
    return weights, CR

def _experts_bwm(weights_list):
    bwm_data_list = []
    for weights in weights_list:
        bwm_data_list.append(_weights_to_bwm_vectors(weights))
    
    all_weights = []
    all_CR = []
    
    for i, expert in enumerate(bwm_data_list):
        try:
            weights, CR = _calculate_bwm_weights(
                expert["best_to_others"], 
                expert["others_to_worst"]
            )
            all_weights.append(weights)
            all_CR.append(CR)
        except Exception as e:
            print(f"专家{i+1}计算失败: {e}")
            continue
    
    if not all_weights:
        raise ValueError("所有专家数据均无效")
    
    # 聚合权重（算术平均）
    aggregated_weights = np.mean(all_weights, axis=0)
    aggregated_weights = aggregated_weights / np.sum(aggregated_weights)  # 重新归一化
    avg_CR = np.mean(all_CR) if all_CR else 0
    
    return aggregated_weights.tolist(), avg_CR


# ------------------------------------------------------
# ------------------------------------------------------
# ------------------------------------------------------


def entropy_method(data_matrix):
    """
    熵权法确权方法 - 统一接口
    参数: data_matrix - list[list]，决策矩阵，行代表方案，列代表指标
    返回: (权重向量, 附加信息)
    """
    if not data_matrix or not all(data_matrix):
        raise ValueError("输入数据不能为空")
    
    # 转换为numpy数组
    matrix = np.array(data_matrix)
    
    # 1. 数据归一化
    normalized_matrix = _normalize_columns(matrix)
    
    # 2. 计算占比
    proportion_matrix = _calculate_proportion(normalized_matrix)
    
    # 3. 计算信息熵
    entropy = _calculate_entropy(proportion_matrix)
    
    # 4. 计算权重
    weights = _calculate_entropy_weights(entropy)
    
    # 5. 计算信息效用值（作为附加信息）
    information_utility = 1 - entropy
    
    additional_info = {
        "entropy": entropy.tolist(),
        "information_utility": information_utility.tolist(),
        "normalized_matrix": normalized_matrix.tolist()
    }
    
    return weights.tolist(), additional_info

def _normalize_columns(matrix):
    """对每一列进行归一化：r_ij = (x_ij - min(x_j)) / (max(x_j) - min(x_j))"""
    min_vals = matrix.min(axis=0)
    max_vals = matrix.max(axis=0)
    range_vals = max_vals - min_vals
    # 处理max=min的情况（避免除以0）
    range_vals[range_vals == 0] = 1
    normalized = (matrix - min_vals) / range_vals
    return normalized

def _calculate_proportion(normalized_matrix):
    """计算每个元素在列中的占比：p_ij = r_ij / sum(r_j)"""
    column_sums = normalized_matrix.sum(axis=0)
    # 处理sum=0的情况（避免除以0）
    column_sums[column_sums == 0] = 1
    proportion = normalized_matrix / column_sums
    return proportion

def _calculate_entropy(proportion_matrix):
    """计算每一列的信息熵"""
    m = proportion_matrix.shape[0]  # 行数
    # 避免log2(0)的情况，用很小的数替换0
    epsilon = 1e-10
    modified_p = np.where(proportion_matrix == 0, epsilon, proportion_matrix)
    entropy = -np.sum(proportion_matrix * np.log2(modified_p), axis=0) / np.log2(m)
    return entropy

def _calculate_entropy_weights(entropy):
    """计算权重：w_j = (1 - e_j) / sum(1 - e_j)"""
    d_j = 1 - entropy
    sum_d = d_j.sum()
    weights = d_j / sum_d
    return weights