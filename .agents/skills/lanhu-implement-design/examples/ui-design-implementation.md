# 示例 1：实现蓝湖 UI 设计稿

用户说："实现这个蓝湖设计稿 https://lanhuapp.com/web/..."

## 操作步骤

1. 解析邀请链接：`lanhu_resolve_invite_link(link="https://lanhuapp.com/web/...")`
2. 获取设计：`lanhu_get_designs(project_id="xxx")`
3. 分析设计：`lanhu_get_ai_analyze_design_result(project_id="xxx", design_id="xxx")`
4. 获取切图：`lanhu_get_design_slices(project_id="xxx", design_id="xxx")`
5. 下载资源（图片、图标、SVG 等）
6. 将蓝湖 HTML+CSS 作为参考，转换为本项目的 Vue/React 框架代码
7. 使用项目的设计系统组件替换蓝湖原始 HTML 元素
8. 对照设计稿进行验证（布局、颜色、字体、交互状态）

## 转换原则

- 蓝湖输出是参考，不是最终代码
- 使用项目框架的组件替换原始 HTML
- 使用项目的设计 token 替换蓝湖的 CSS 变量
- 将蓝湖切图资源放到项目的 static/assets 目录