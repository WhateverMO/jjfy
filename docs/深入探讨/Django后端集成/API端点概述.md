数据成熟度评估项目提供了一个基于Django的REST API，具备两大核心功能：数据库模式分析和数据成熟度评估。本概述为初级开发者介绍可用的端点、其用途以及如何有效交互。

## API架构

该API遵循简单的RESTful结构，所有端点均以`/api/`为前缀，如主URL配置[back/mysite/urls.py](/data-maturity-assessment/back/mysite/urls.py#L20)中所定义。端点分为两大类：数据库模式操作和评估功能。

## 数据库模式端点

这些端点提供对SQL Server数据库元数据的访问和可视化功能。所有模式端点都接受可选连接参数，默认值为预配置的AdventureWorks2019数据库。

### 连接参数

所有模式端点都支持这些可选查询参数：

-   `server`: 数据库服务器（默认："localhost"）
-   `database`: 数据库名称（默认："AdventureWorks2019"）
-   `username`: SQL用户名（默认："sa"）
-   `password`: SQL密码（默认："test@123SA"）
-   `driver`: ODBC驱动程序（默认："ODBC Driver 17 for SQL Server"）
-   `schema`: 数据库模式（默认："HumanResources"）

### 可用端点

| 端点 | 方法 | 用途 | 响应格式 |
| --- | --- | --- | --- |
| `/api/get_table_names` | GET | 获取所有表名 | 包含`table_names`和`problem_tables`数组的JSON |
| `/api/get_view_names` | GET | 获取所有视图名 | 包含`view_names`数组的JSON |
| `/api/get_all_relations` | GET | 获取所有数据库关系 | 包含关系的`view_names`的JSON |
| `/api/get_table` | GET | 获取特定表结构 | 包含表模式的JSON（目前限制为Employee表） |
| `/api/er` | GET | 生成ER图为SVG | SVG图像响应 |

> [!NOTE]
> `/api/er`端点在数据库可视化方面特别强大。它支持额外的参数，如`reasoning_FK`、`rankdir`和`render_related`来自定义ER图生成过程。

### ER图生成

`/api/er`端点[back/api/views.py](/data-maturity-assessment/back/api/views.py#L111)是功能最丰富的模式端点，提供广泛的自定义选项：

![[Pasted image 20251104170734.png]]

额外的ER特定参数：

-   `tables`: 要渲染的表的逗号分隔列表
-   `reasoning_FK`: 启用外键推理（默认：true）
-   `reasoning_all_FK`: 推理所有可能的外键（默认：false）
-   `disable_sqlFK`: 禁用SQL外键约束（默认：false）
-   `rankdir`: 布局方向（"LR"或"TB"，默认："LR"）
-   `render_related`: 渲染相关表（默认：true）
-   `field_omission`: 启用图表中的字段省略（默认：false）

## 评估端点

### 数据成熟度评估

`/api/eval`端点[back/api/views.py](/data-maturity-assessment/back/api/views.py#L207)使用预定义的测试用例和评估方法提供数据成熟度评估功能。

| 参数 | 类型 | 默认值 | 描述 |
| --- | --- | --- | --- |
| `method` | string | "entropy" | 评估方法（"entropy"或其他支持的方法） |

该端点使用评估流水线处理问卷响应，并返回结构化结果，包括不同级别和部分的成熟度分数和评估。

## 使用示例

### 基本表列表

```bash
GET /api/get_table_names
```

返回包含所有可用表名和模式分析期间检测到的任何问题表的JSON响应。

### 自定义ER图

```bash
GET /api/er?tables=Employee,Department&reasoning_FK=true&rankdir=TB
```

生成一个从上到下的ER图，仅显示Employee和Department表，并启用外键推理。

### 数据评估

```bash
GET /api/eval?method=entropy
```

使用熵权法处理预定义的测试用例并返回评估结果。

## 实现说明

API实现遵循Django最佳实践，在URL路由[back/api/urls.py](/data-maturity-assessment/back/api/urls.py#L5)和视图逻辑[back/api/views.py](/data-maturity-assessment/back/api/views.py#L27)之间明确分离关注点。所有端点都返回适当的HTTP响应类型（数据为JSON，图表为SVG），并包含数据库连接的错误处理。

> [!NOTE]
> 数据库连接参数在视图模块[back/api/views.py](/data-maturity-assessment/back/api/views.py#L19-L24)中硬编码了默认值。在生产环境中，应将这些参数移至环境变量或Django设置中，以提高安全性和可配置性。

## 后续步骤

要深入理解API实现：

-   探索[数据库连接管理](深入探讨/Django后端集成/数据库连接管理) 页面，了解SQL Server连接的建立方式
-   查看[ER图生成](深入探讨/Django后端集成/ER图生成) 文档，了解可视化功能的详细信息
-   查看[评估流水线架构](深入探讨/核心评估引擎/评估流水线架构) ，了解数据成熟度评估的内部工作原理

该API作为数据库分析和评估功能的基础，是理解整体系统架构的关键组件。