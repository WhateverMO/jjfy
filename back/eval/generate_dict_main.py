def build_score_structure_old(level1_names, level2_names, level3_names, 
                         level1_scores, level2_scores, level3_scores,
                         total_score, level_name):
    """
    构建嵌套的得分字典结构
    
    参数:
        level1_names: 一级指标名称列表 [name1, name2, ...]
        level2_names: 二级指标名称嵌套列表 [[name1, name2, ...], [name3, name4, ...], ...]
        level3_names: 三级指标名称嵌套列表 [[name1, name2, ...], [name3, name4, ...], ...]
        level1_scores: 一级指标得分列表 [score1, score2, ...]
        level2_scores: 二级指标得分嵌套列表 [[score1, score2, ...], [score3, score4, ...], ...]
        level3_scores: 三级指标得分嵌套列表 [[score1, score2, ...], [score3, score4, ...], ...]
        total_score: 模型总得分
        level_name: 等级名称
    
    返回:
        dict: 嵌套的得分字典结构
    """
    result = {
        'score': round(total_score, 4),
        'level': level_name
    }
    
    # 构建一级指标
    level1_index = 0
    level2_global_index = 0
    level3_global_index = 0
    
    for i, level1_name in enumerate(level1_names):
        level1_data = {
            'score': round(level1_scores[i], 4)
        }
        
        # 获取该一级指标下的二级指标数量
        level2_count = len(level2_names[i])
        
        # 构建二级指标
        for j in range(level2_count):
            level2_name = level2_names[i][j]
            level2_data = {
                'score': round(level2_scores[i][j], 4)
            }
            
            # 获取该二级指标下的三级指标数量
            level3_count = len(level3_names[level2_global_index])
            
            # 构建三级指标
            for k in range(level3_count):
                level3_name = level3_names[level2_global_index][k]
                level3_data = {
                    'score': round(level3_scores[level2_global_index][k], 4)
                }
                level2_data[level3_name] = level3_data
                level3_global_index += 1
            
            level1_data[level2_name] = level2_data
            level2_global_index += 1
        
        result[level1_name] = level1_data
        level1_index += 1
    
    return result


level1_names = [
    "数据战略","数据生命周期","数据治理","数据架构","数据质量","数据标准","数据安全","数据应用"
    ]
level2_names = [
    # 旧的二级指标
    # ["数据战略规划","数据战略实施","数据战略评估"],
    # ["数据需求管理","数据设计和开发","数据运维","数据退役"],
    # ["数据治理组织","数据制度建设","数据治理沟通"],
    # ["数据模型","数据分布","数据集成与共享","元数据管理"],
    # ["数据质量需求","数据质量检查","数据质量分析","数据质量提升"],
    # ["业务术语","参考数据与主数据","数据元","指标数据"],
    # ["数据安全策略","数据安全管理","数据安全审计"],
    # ["数据分析","数据开放共享","数据服务"]


    # 新的二级指标
    ["数据战略规划","数据战略实施","数据战略评估"],

    ["数据需求管理","数据设计和开发","数据运维","数据退役"],

    ["数据制度建设","数据治理沟通"],

    ["数据分布","元数据管理"],

    ["数据质量需求","数据质量检查","数据质量分析","数据质量提升"],

    ["业务术语","参考数据与主数据","数据元","指标数据"],

    ["数据安全策略","数据安全管理","数据安全审计"],

    ["数据分析","数据开放共享","数据服务"]
]
level3_names = [
    # 旧的（105个三级指标）
    # ["明确利益相关者","数据战略制定","数据战略修订"],
    # ["战略实施计划制定","战略实施过程"],
    # ["战略实施现状和差距评估","战略评估模型建立","战略评估模型应用"],
    # ["需求管理制度","定义数据需求","业务一致性"],
    # ["数据解决方案设计","数据解决方案质量管理","数据解决方案实施"],
    # ["数据运维方案制定","数据平台的运维"],
    # ["数据退役设计","数据退役执行","数据退役跟踪"],
    # ["治理组织就绪度","岗位职责明确率","绩效评价机制完备性"],
    # ["数据分级分类覆盖率","数据访问权限规范率","数据安全规范更新及时率"],
    # ["协作效率指数","​数据安全培训覆盖率","​​数据文化认知度"],
    # ["模型规范覆盖率","核心模型落地率"],
    # ["核心数据溯源能力","​​跨系统协同效率"],
    # ["标准接口采用率","平台服务稳定性"],
    # ["元模型实施完整度","元数据变更响应时效","血缘追溯可用率"],
    # ["数据质量规则覆盖率","数据质量需求更新及时性"],
    # ["数据准确率","数据质量问题发现率"],
    # ["数据质量问题根因定位准确率","问题根因分析机制完善度"],
    # ["数据质量问题解决率","质量问题闭环率"],
    # ["业务术语字典完整性","业务术语变更管理规范性"],
    # ["系统一致性达标率","数据元目录完整性"],
    # ["数据元标准一致性","数据元问题处理及时率"],
    # ["指标字典完整性","指标口径一致性","指标数据更新及时性"],
    # ["数据安全策略制定","数据安全策略实施"],
    # ["数据安全等级","数据安全限制","数据安全监控"],
    # ["过程、规范、合规审计","供应商审计","审计报告发布及建议"],
    # ["高级分析工具和方法","数据分析应用"],
    # ["数据目录","数据开放共享"],
    # ["数据服务需求","数据服务部署","数据服务监控"]


    # 新的（95个三级指标）
    ["明确利益相关者","数据战略制定","数据战略修订"],
    ["战略实施计划制定","战略实施过程"],
    ["战略实施现状和差距评估","战略评估模型建立","战略评估模型应用"],
    ["需求管理制度","定义数据需求","业务一致性"],
    ["数据解决方案设计","数据解决方案质量管理","数据解决方案实施"],
    ["数据运维方案制定","数据平台的运维"],
    ["数据退役设计","数据退役执行","数据退役跟踪"],
    ["数据分级分类覆盖率","数据访问权限规范率​​","数据安全培训覆盖率​​"],
    ["​​跨部门协作效率指数​​"],
    ["核心数据分布集中度​​","跨系统关联复杂度​​"],
    ["元数据一致性达标率","血缘关系完整度"],
    ["数据质量规则覆盖率","数据质量需求更新及时性"],
    ["数据准确率","数据质量问题发现率"],
    ["数据质量问题根因定位准确率","问题根因分析机制完善度"],
    ["数据质量问题解决率","质量问题闭环率"],
    ["业务术语字典完整性","业务术语变更管理规范性"],
    ["系统一致性达标率","数据元目录完整性"],
    ["数据元标准一致性","数据元问题处理及时率"],
    ["指标字典完整性","指标口径一致性","指标数据更新及时性"],
    ["数据安全策略制定","数据安全策略实施"],
    ["数据安全等级","数据安全限制","数据安全监控"],
    ["过程、规范、合规审计","供应商审计","审计报告发布及建议"],
    ["高级分析工具和方法","数据分析应用"],
    ["数据目录","数据开放共享"],
    ["数据服务需求","数据服务部署","数据服务监控"]
]


# print(len(level1_names))
# print(len(level2_names))
# print(len(level3_names))

def build_score_structure(level1_names, level2_names, level3_names, 
                         level1_scores, level2_scores, level3_scores,
                         level1_weights, level2_weights, level3_weights,
                         total_score, level_name):
    """
    构建嵌套的得分字典结构
    
    参数:
        level1_names: 一级指标名称列表 [name1, name2, ...]
        level2_names: 二级指标名称嵌套列表 [[name1, name2, ...], [name3, name4, ...], ...]
        level3_names: 三级指标名称嵌套列表 [[name1, name2, ...], [name3, name4, ...], ...]
        level1_scores: 一级指标得分列表 [score1, score2, ...]
        level2_scores: 二级指标得分嵌套列表 [[score1, score2, ...], [score3, score4, ...], ...]
        level3_scores: 三级指标得分嵌套列表 [[score1, score2, ...], [score3, score4, ...], ...]
        level1_weights: 一级指标权重列表 [weight1, weight2, ...]
        level2_weights: 二级指标权重嵌套列表 [[weight1, weight2, ...], [weight3, weight4, ...], ...]
        level3_weights: 三级指标权重嵌套列表 [[weight1, weight2, ...], [weight3, weight4, ...], ...]
        total_score: 模型总得分
        level_name: 等级名称
    
    返回:
        dict: 嵌套的得分字典结构
    """
    # 参数验证
    if not all([
        len(level1_names) == len(level1_scores) == len(level1_weights),
        len(level2_names) == len(level1_names),
        len(level2_scores) == len(level1_names),
        len(level2_weights) == len(level1_names),
        len(level3_names) == sum(len(level2) for level2 in level2_names),
        len(level3_scores) == sum(len(level2) for level2 in level2_scores),
        len(level3_weights) == sum(len(level2) for level2 in level2_weights)
    ]):
        raise ValueError("输入参数长度不匹配")
    
    result = {
        'score': round(total_score, 4),
        'level': level_name
    }
    
    level3_start_index = 0
    
    for i, (level1_name, level1_score, level1_weight) in enumerate(zip(level1_names, level1_scores, level1_weights)):
        level1_data = {
            'score': round(level1_score, 4),
            'weight': round(level1_weight, 4)
        }
        
        for j, (level2_name, level2_score, level2_weight) in enumerate(zip(level2_names[i], level2_scores[i], level2_weights[i])):
            level2_data = {
                'score': round(level2_score, 4),
                'weight': round(level2_weight, 4)
            }
            
            # 处理当前二级指标下的三级指标
            level3_count = len(level3_names[level3_start_index])
            for k in range(level3_count):
                level3_name = level3_names[level3_start_index][k]
                level3_score = level3_scores[level3_start_index][k]
                level3_weight = level3_weights[level3_start_index][k]
                level2_data[level3_name] = {
                    'score': round(level3_score, 4),
                    'weight': round(level3_weight, 4)
                }
            
            level1_data[level2_name] = level2_data
            level3_start_index += 1
        
        result[level1_name] = level1_data
    
    return result

# 使用示例
if __name__ == "__main__":
    level1_names = [
        "数据战略","数据生命周期","数据治理","数据架构","数据质量","数据标准","数据安全","数据应用"
        ]
    level2_names = [
        ["数据战略规划","数据战略实施","数据战略评估"],

        ["数据需求管理","数据设计和开发","数据运维","数据退役"],

        ["数据治理组织","数据制度建设","数据治理沟通"],

        ["数据模型","数据分布","数据集成与共享","元数据管理"],

        ["数据质量需求","数据质量检查","数据质量分析","数据质量提升"],

        ["业务术语","参考数据与主数据","数据元","指标数据"],

        ["数据安全策略","数据安全管理","数据安全审计"],

        ["数据分析","数据开放共享","数据服务"]

    ]
    level3_names = [
        ["明确利益相关者","数据战略制定","数据战略修订"],

        ["战略实施计划制定","战略实施过程"],

        ["战略实施现状和差距评估","战略评估模型建立","战略评估模型应用"],

        ["需求管理制度","定义数据需求","业务一致性"],

        ["数据解决方案设计","数据解决方案质量管理","数据解决方案实施"],

        ["数据运维方案制定","数据平台的运维"],

        ["数据退役设计","数据退役执行","数据退役跟踪"],

        ["治理组织就绪度","岗位职责明确率","绩效评价机制完备性"],

        ["数据分级分类覆盖率","数据访问权限规范率","数据安全规范更新及时率"],

        ["协作效率指数","​数据安全培训覆盖率","​​数据文化认知度"],

        ["模型规范覆盖率","核心模型落地率"],

        ["核心数据溯源能力","​​跨系统协同效率"],

        ["标准接口采用率","平台服务稳定性"],

        ["元模型实施完整度","元数据变更响应时效","血缘追溯可用率"],

        ["数据质量规则覆盖率","数据质量需求更新及时性"],

        ["数据准确率","数据质量问题发现率"],

        ["数据质量问题根因定位准确率","问题根因分析机制完善度"],

        ["数据质量问题解决率","质量问题闭环率"],

        ["业务术语字典完整性","业务术语变更管理规范性"],

        ["系统一致性达标率","数据元目录完整性"],

        ["数据元标准一致性","数据元问题处理及时率"],

        ["指标字典完整性","指标口径一致性","指标数据更新及时性"],

        ["数据安全策略制定","数据安全策略实施"],

        ["数据安全等级","数据安全限制","数据安全监控"],

        ["过程、规范、合规审计","供应商审计","审计报告发布及建议"],

        ["高级分析工具和方法","数据分析应用"],

        ["数据目录","数据开放共享"],
        
        ["数据服务需求","数据服务部署","数据服务监控"]
    ]
    # print(len(level3_names))
    
    # 假设的三级得分数据
    level3_scores = [
        [3, 2, 4],
        [1, 5],
        [4, 3, 2],
        [2, 5, 1],
        [3, 4, 2],
        [1, 5],
        [4, 3, 2],
        [2, 5, 1],
        [3, 4, 2],
        [1, 5, 3],
        [4, 2],
        [3, 5],
        [2, 4],
        [1, 3, 5],
        [4, 2],
        [3, 1],
        [5, 2],
        [4, 3],
        [1, 5],
        [2, 4],
        [3, 1],
        [5, 2, 4],
        [3, 1],
        [2, 4, 5],
        [1, 3, 2],
        [4, 5],
        [3, 1],
        [2, 4, 5]
    ]
    
    level2_scores = [
        [3, 2, 4],
        [1, 5, 3, 2],
        [4, 2, 1],
        [3, 5, 2, 4],
        [1, 3, 5, 2],
        [4, 1, 3, 5],
        [2, 4, 1],
        [3, 5, 2]
    ]
    
    level1_scores = [3, 2, 4, 1, 5, 3, 2, 4]
     
    total_score = 84.42
    level_name = "控制级"
    
    # 构建字典结构
    score_dict = build_score_structure_old(
        level1_names, level2_names, level3_names,
        level1_scores, level2_scores, level3_scores,
        total_score, level_name
    )
    
    # 打印结果
    # import json
    # print(json.dumps(score_dict, ensure_ascii=False, indent=2))

    import json

    # 字典数据(没有权重数据的)
    with open('output.txt', 'w', encoding='utf-8') as f:
        f.write(json.dumps(score_dict, ensure_ascii=False, indent=2))   



