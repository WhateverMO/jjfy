最优最劣方法（BWM）是一种多准则决策方法，通过将各准则与最优准则和最劣准则进行比较来确定权重。本实现提供了一个稳健的权重计算框架，具备一致性验证和多专家聚合能力。

## 核心架构

BWM实现采用模块化设计，在公共接口和内部计算逻辑之间具有清晰的分离：

![[Pasted image 20251104164700.png]]

## 公共接口

主入口点是`bwm_method`函数[weight\_calc\_method.py#L4-L18](/data-maturity-assessment/back/eval/weight_calc_method.py#L4-L18)，作为BWM权重计算的公共API。该函数处理输入验证，并根据数据结构路由到相应的处理流程。

**主要功能：**

-   接受单专家和多专家比较矩阵
-   返回标准化权重和一致性比率（CR）
-   处理零权重和无效输入等边缘情况

## 内部处理流程

### 专家数据处理

对于多专家场景，`_experts_bwm`函数[weight\_calc\_method.py#L160-L188](/data-maturity-assessment/back/eval/weight_calc_method.py#L160-L188)通过算术平均聚合各专家的权重：

1.  将每个专家的权重转换为BWM比较向量
2.  独立计算每个专家的权重
3.  使用均值聚合结果
4.  计算平均一致性比率

### 权重到向量转换

`_weights_to_bwm_vectors`函数[weight\_calc\_method.py#L19-L70](/data-maturity-assessment/back/eval/weight_calc_method.py#L19-L70)将标准化权重转换为BWM比较向量：

-   识别最优（最高权重）和最劣（最低权重）准则
-   生成`best_to_others`和`others_to_worst`比较向量
-   应用1-9标度进行实际比较值计算
-   通过分配最大比率处理零权重边缘情况

### 线性规划核心

计算核心位于`_calculate_bwm_weights`[weight\_calc\_method.py#L72-L158](/data-maturity-assessment/back/eval/weight_calc_method.py#L72-L158)，该函数构建并求解线性规划问题：

**目标函数：** 最小化 ξ（一致性偏差）

**约束条件：**

-   |w\_best/a\_bj - w\_j| ≤ ξ 对所有准则j
-   |w\_j - w\_worst × a\_jw| ≤ ξ 对所有准则j
-   Σw\_j = 1（权重和为1）
-   w\_j ≥ 0（非负性）

> [!NOTE]
> 实现使用scipy.optimize.linprog求解线性规划问题，确保数值稳定性和最优解的获取。

## 一致性验证

该方法包含使用一致性比率（CR）的内置一致性检查：

**CR = ξ/CI**

其中CI是基于比较标度的一致性指数：

| max(a\_bw) | CI 值 |
| --- | --- |
| 1 | 0.00 |
| 2 | 0.44 |
| 3 | 1.00 |
| 4 | 1.63 |
| 5 | 2.30 |
| 6 | 3.00 |
| 7 | 3.73 |
| 8 | 4.47 |
| 9 | 5.23 |

> [!NOTE]
> CR值小于0.1通常表示可接受的一致性，但阈值可能因应用需求而异。

## 与主处理的集成

BWM方法通过`process_weight_list`[weight\_calc\_method\_main.py#L11-L49](/data-maturity-assessment/back/eval/weight_calc_method_main.py#L11-L49)与更广泛的权重计算系统集成，该函数：

-   处理嵌套输入数据结构
-   转换数据类型以确保兼容性
-   支持BWM和熵值法
-   保持一致的输出格式

## 错误处理

实现包含全面的错误处理机制，针对：

-   空输入验证
-   不支持的数据格式
-   线性规划求解失败
-   零权重边缘情况
-   无效的比较矩阵结构

## 使用模式

```python
weights, CR = bwm_method(comparison_matrix_list)
 
# 输入结构应遵循测试用例中的格式
# 参见：test_case.py#L1-L30中的示例配置
```

BWM实现提供了一种数学上严谨的权重确定方法，具备内置的一致性验证，适用于需要系统处理和验证专家判断的多准则决策应用。