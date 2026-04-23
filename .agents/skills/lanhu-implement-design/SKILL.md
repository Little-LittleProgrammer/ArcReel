---
name: lanhu-implement-design
description: 当用户要求"实现蓝湖设计稿"、"根据蓝湖设计生成代码"、"分析蓝湖原型"、"蓝湖设计稿实现"、"蓝湖原型分析"、"蓝湖切图"、"蓝湖资源下载"、"蓝湖协作"、"蓝湖 MCP"、"lanhuapp.com"，或提供蓝湖链接/邀请链接时，应使用此技能。
version: 0.1.0
---

# 蓝湖设计实现

## 概述

此技能提供了一套结构化的工作流程，用于将蓝湖设计稿和 Axure 原型转换为可直接用于生产的代码。它与蓝湖 MCP 服务器集成，可获取设计上下文、分析原型、下载资源、生成代码，并提供团队协作支持。

## 前置条件

- 蓝湖 MCP 服务器已连接且可访问：<http://localhost:8000/mcp>
- 已配置有效的 `LANHU_COOKIE` 环境变量
- 用户必须提供以下之一：
  - 蓝湖邀请链接
  - 项目 ID 和页面设计 ID（直接提供）

**如果 MCP 工具不可用：** 请参考 `references/install-mcp.md` 安装说明。

## 技能边界

- 当交付物是基于蓝湖设计稿的代码实现时，使用此技能
- 对于从 Axure 原型进行需求分析，请使用原型分析工作流程
- 对于团队协作（评论、@提及），请集成 `lanhu_say` 工具
- 如果未安装 MCP 服务器，请引导用户按照 `references/install-mcp.md` 进行安装

## 可用的 MCP 工具

### 设计与原型工具

- `lanhu_resolve_invite_link` - 解析邀请链接以获取项目访问权限
- `lanhu_get_pages` - 获取原型页面列表
- `lanhu_get_ai_analyze_page_result` - 分析原型页面内容（开发/测试/探索模式）
- `lanhu_get_designs` - 获取 UI 设计图列表
- `lanhu_get_ai_analyze_design_result` - 分析 UI 设计并生成 HTML+CSS 代码
- `lanhu_get_design_slices` - 获取切图/导出的资源信息

### 协作工具

- `lanhu_say` - 发布评论/消息
- `lanhu_say_list` - 获取评论列表
- `lanhu_say_detail` - 获取评论详情
- `lanhu_say_edit` - 编辑评论
- `lanhu_say_delete` - 删除评论
- `lanhu_get_members` - 获取团队协作者列表

## 必需工作流程

**请按顺序执行以下步骤，不要跳过任何步骤。**

### 步骤 0：检查 MCP 可用性

在继续之前，验证蓝湖 MCP 工具是否可用：

1. 检查当前环境中是否可以访问 `lanhu_*` 工具
2. 如果工具不可用，请阅读 `references/install-mcp.md` 并引导用户完成安装
3. 确保已设置 `LANHU_COOKIE` 环境变量

### 步骤 1：解析项目访问权限

如果用户提供了邀请链接，请先解析：

```bash
lanhu_resolve_invite_link(link="https://lanhuapp.com/web/...")
```

这将返回后续调用所需的项目信息。

### 步骤 2：识别目标资源

在原型分析和 UI 设计实现之间选择：

#### 选项 A：原型分析（需求分析）

用于 Axure 原型分析以理解需求：

```bash
lanhu_get_pages(project_id="xxx")

lanhu_get_ai_analyze_page_result(
  project_id="xxx",
  page_id="xxx",
  analyze_mode="develop"  // "develop", "test", 或 "explore"
)
```

**分析模式：**

- `develop` - 面向开发的分析，提取技术需求
- `test` - 面向测试的分析，识别测试场景
- `explore` - 探索性分析，全面的功能分解

#### 选项 B：UI 设计实现

用于将 UI 设计转换为代码：

```bash
lanhu_get_designs(project_id="xxx")

lanhu_get_ai_analyze_design_result(
  project_id="xxx",
  design_id="xxx"
)
```

这将返回 HTML+CSS 代码和设计上下文。

### 步骤 3：下载资源

获取图片和图标的切图信息：

```bash
lanhu_get_design_slices(
  project_id="xxx",
  design_id="xxx"
)
```

从切图 URL 下载所有需要的资源（图片、图标、SVG 等）。

### 步骤 4：转换为项目规范

将蓝湖输出（HTML+CSS）转换为本项目的框架：

**核心原则：**

- 将蓝湖 HTML+CSS 作为参考，而非最终代码
- 使用本项目的框架（Vue/React 等）进行替换
- 使用项目的设计系统组件
- 应用项目的样式规范（CSS modules、Tailwind 等）
- 与现有的路由和状态管理集成

### 步骤 5：验证实现

根据原始设计进行验证：

**验证清单：**

- [ ] 布局与设计规范一致
- [ ] 排版一致（字体、大小、粗细）
- [ ] 颜色完全匹配
- [ ] 资源渲染正确
- [ ] 交互状态已实现
- [ ] 响应式行为正确
- [ ] 符合无障碍标准

### 步骤 6：协作（可选）

通过评论分享实现状态或提问：

```bash
lanhu_say(
  project_id="xxx",
  content="前端实现已完成，请查看 @设计师"
)

lanhu_get_members(project_id="xxx")  // 获取成员列表以便 @提及
```

## 实现规则

### 代码组织

- 将组件放置在项目指定的目录结构中
- 遵循项目的命名规范
- 将可复用的模式提取为共享组件

### 设计系统集成

- 将蓝湖设计 token 映射到项目设计 token
- 在有匹配设计时使用现有组件
- 记录新增的组件

### 资源处理

- 从切图 URL 下载资源
- 优化生产环境的图片
- 将资源放置在项目的 static/assets 目录中
- 对图标和图片使用一致的命名

## 示例

### 示例 1：实现蓝湖 UI 设计

用户说："实现这个蓝湖设计稿 https://lanhuapp.com/web/..."

**操作：**

1. 解析邀请链接：`lanhu_resolve_invite_link(link="...")`
2. 获取设计：`lanhu_get_designs(project_id="xxx")`
3. 分析设计：`lanhu_get_ai_analyze_design_result(project_id="xxx", design_id="xxx")`
4. 获取切图：`lanhu_get_design_slices(project_id="xxx", design_id="xxx")`
5. 下载资源
6. 将 HTML+CSS 转换为项目框架
7. 对照设计进行验证
8. 如需要，发布完成评论

**结果：** 与蓝湖设计匹配的组件，已集成到项目中。

### 示例 2：分析原型以获取需求

用户说："分析这个蓝湖原型的需求"

**操作：**

1. 如需要，先解析邀请链接
2. 获取页面：`lanhu_get_pages(project_id="xxx")`
3. 使用开发模式分析：`lanhu_get_ai_analyze_page_result(project_id="xxx", page_id="xxx", analyze_mode="develop")`
4. 提取技术需求
5. 生成实现计划

**结果：** 可直接用于实现的结构化需求分析。

### 示例 3：团队协作

用户说："在蓝湖留言通知设计师已完成"

**操作：**

1. 获取成员：`lanhu_get_members(project_id="xxx")`
2. 找到设计师的成员 ID
3. 发布评论：`lanhu_say(project_id="xxx", content="前端实现已完成，请查看 @设计师ID")`

**结果：** 设计师通过蓝湖评论系统收到通知。

## 最佳实践

### 始终先获取上下文

不要基于假设进行实现。始终先使用 `lanhu_get_ai_analyze_design_result` 或 `lanhu_get_ai_analyze_page_result`。

### 选择正确的分析模式

对于原型分析，选择适当的模式：

- **开发模式**：用于实现规划
- **测试模式**：用于 QA 和测试用例生成
- **探索模式**：用于全面的功能探索

### 使用协作功能

通过蓝湖的评论系统让设计师了解情况。使用 `@提及` 通知特定的团队成员。

### 验证资源

在下载之前检查所有切图 URL 是否可访问。通过评论报告缺失的资源。

## 常见问题

### 问题：邀请链接解析失败

**原因：** Cookie 过期或无效。
**解决方案：** 验证 `LANHU_COOKIE` 环境变量是否正确设置。

### 问题：设计分析返回空结果

**原因：** 设计 ID 不正确或没有访问权限。
**解决方案：** 从 `lanhu_get_designs` 输出中验证 project_id 和 design_id。

### 问题：资源下载失败

**原因：** 切图 URL 过期或不可访问。
**解决方案：** 重新解析邀请链接以刷新访问权限，然后重试获取切图。

## 其他资源

### 参考文件

- **`references/install-mcp.md`** - MCP 服务器安装指南（当工具不可用时使用）

### MCP 服务器文档

- [蓝湖 MCP GitHub](https://github.com/dsphper/lanhu-mcp)
- [蓝湖官方文档](https://lanhuapp.com)

### 相关技能

- 对于 Figma 设计，请使用 `figma-implement-design` 技能
- 对于代码生成工作流程，请查阅项目的开发指南
