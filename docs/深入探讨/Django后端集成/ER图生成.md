ER 图生成模块提供了一个全面的系统，用于从现有数据库架构自动生成实体关系图。该模块结合了数据库内省功能和高级图表渲染功能，创建数据库结构的可视化表示，包括表、视图、关系和约束。

## 架构概述

ER 图生成系统围绕三个核心组件构建，它们协同工作，将数据库元数据转换为可视化图表：

![[Pasted image 20251104180131.png]]

系统采用管道架构，数据库元数据流经分析、转换和渲染阶段。每个组件都有特定的职责：数据库连接、架构分析、图表构建和可视化渲染。

## 数据库连接管理

`dbConnection` 类是数据库内省的基础，提供上下文管理器接口以安全的进行数据库操作 [connection.py#L7-L25](/data-maturity-assessment/back/sqlER/connection/connection.py#L7-L25)。该类通过 pyodbc 支持 Microsoft SQL Server 连接，并实现自动架构检测。

**关键连接特性：**

-   **自动连接字符串构建**：根据提供的参数构建连接字符串
-   **数据库元数据检测**：自动识别数据库名称、类型和架构
-   **架构枚举**：使用 `INFORMATION_SCHEMA.SCHEMATA` 检索可用架构 [connection.py#L35-L42](/data-maturity-assessment/back/sqlER/connection/connection.py#L35-L42)
-   **表发现**：枚举表，可选择排除系统表 [connection.py#L43-L55](/data-maturity-assessment/back/sqlER/connection/connection.py#L43-L55)

> [!NOTE]
> 连接类实现了 Python 的上下文管理器协议，确保即使在发生异常时也能自动清理连接和管理资源。

## 表和视图表示

`Table` 类为数据库实体提供了丰富的抽象，支持表和视图的不同功能 [ERDiagram.py#L9-L152](/data-maturity-assessment/back/sqlER/ERDiagram/ERDiagram.py#L9-L152)。每个表维护详细的字段信息、约束和关系。

**表管理特性：**

-   **字段定义**：添加带有类型规范和约束的字段 [ERDiagram.py#L61-L73](/data-maturity-assessment/back/sqlER/ERDiagram/ERDiagram.py#L61-L73)
-   **主键管理**：定义带有自定义约束的主键 [ERDiagram.py#L74-L82](/data-maturity-assessment/back/sqlER/ERDiagram/ERDiagram.py#L74-L82)
-   **外键关系**：建立具有引用完整性的关系 [ERDiagram.py#L96-L129](/data-maturity-assessment/back/sqlER/ERDiagram/ERDiagram.py#L96-L129)
-   **注释支持**：添加文档和注释 [ERDiagram.py#L130-L138](/data-maturity-assessment/back/sqlER/ERDiagram/ERDiagram.py#L130-L138)

该类区分表和视图，为每种实体类型应用适当的约束和渲染逻辑。

## 高级架构分析

`ERGenerator` 类协调整个 ER 图生成过程，结合数据库内省和智能关系发现 [ERDiagram.py#L546-L846](/data-maturity-assessment/back/sqlER/ERDiagram/ERDiagram.py#L546-L846)。系统支持多种外键发现策略：

**外键发现方法：**

-   **SQL 外键**：直接从数据库元数据中提取
-   **基于推理的发现**：对未记录关系进行智能模式匹配
-   **全面分析**：分析所有潜在关系的选项

`_analysis_database_mssql` 方法实现了关系发现的复杂算法，包括字段相似性分析和命名约定模式识别 [ERDiagram.py#L585-L802](/data-maturity-assessment/back/sqlER/ERDiagram/ERDiagram.py#L585-L802)。

> [!NOTE]
> 基于推理的外键发现可以识别数据库架构中未明确定义的关系，对于约束定义不完整的遗留数据库非常有价值。

## 图表渲染和自定义

`ERDiagram` 类使用 Graphviz 处理数据库结构的可视化表示，以生成高质量图表 [ERDiagram.py#L158-L545](/data-maturity-assessment/back/sqlER/ERDiagram/ERDiagram.py#L158-L545)。系统支持多种输出格式和广泛的自定义选项。

**渲染功能：**

-   **多种输出格式**：SVG、PNG 及其他 Graphviz 支持的格式
-   **质量控制**：可调节的 DPI、字体设置和单元格内边距 [ERDiagram.py#L179-L207](/data-maturity-assessment/back/sqlER/ERDiagram/ERDiagram.py#L179-L207)
-   **选择性渲染**：包含特定表或相关实体 [ERDiagram.py#L284-L394](/data-maturity-assessment/back/sqlER/ERDiagram/ERDiagram.py#L284-L394)
-   **布局控制**：从上到下或从左到右的图表方向

渲染系统使用 Graphviz 的 DOT 语言进行布局，提供具有适当间距、对齐和关系可视化的专业质量图表。

## 集成和使用

ER 图生成系统与更广泛的 Django 应用程序架构无缝集成。面向服务的设计使其易于与 Web 界面和 API 端点集成。

**使用模式：**

-   **直接文件生成**：`render_file()` 用于立即导出图表 [ERDiagram.py#L825-L846](/data-maturity-assessment/back/sqlER/ERDiagram/ERDiagram.py#L825-L846)
-   **内存渲染**：`render_diagrams()` 用于生成 Web 响应 [ERDiagram.py#L806-L824](/data-maturity-assessment/back/sqlER/ERDiagram/ERDiagram.py#L806-L824)
-   **自定义过滤**：选择性表渲染用于聚焦文档

有关详细的 API 集成模式，请参阅 [API 端点概述](深入探讨/Django后端集成/API端点概述) 。有关数据库连接配置，请参考 [数据库连接管理](深入探讨/Django后端集成/数据库连接管理) 。

## 配置选项

| 参数 | 类型 | 默认值 | 描述 |
| --- | --- | --- | --- |
| `reasoning_FK` | bool | False | 启用智能外键发现 |
| `reasoning_all_FK` | bool | False | 分析所有潜在关系 |
| `disable_sql_FK` | bool | False | 跳过 SQL 定义的外键 |
| `rankdir` | TypeRankdir | TB | 图表布局方向 (TB/LR) |
| `dpi` | int | 1300 | 栅格格式的输出分辨率 |
| `field_omission` | bool | False | 从图表中排除字段详情 |

系统提供了灵活的配置以平衡图表细节和视觉清晰度，使其适用于技术文档和高级架构概述。