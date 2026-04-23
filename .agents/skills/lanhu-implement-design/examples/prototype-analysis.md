# 示例 2：分析蓝湖原型获取需求

用户说："分析这个蓝湖原型的需求"

## 操作步骤

1. 如用户提供邀请链接，先解析：`lanhu_resolve_invite_link(link="...")`
2. 获取页面：`lanhu_get_pages(project_id="xxx")`
3. 使用开发模式分析：`lanhu_get_ai_analyze_page_result(project_id="xxx", page_id="xxx", analyze_mode="develop")`
4. 提取技术需求（数据结构、交互流程、API 需求）
5. 生成实现计划

## 分析模式选择

- `develop` — 面向开发的分析，提取技术需求
- `test` — 面向测试的分析，识别测试场景
- `explore` — 探索性分析，全面的功能分解