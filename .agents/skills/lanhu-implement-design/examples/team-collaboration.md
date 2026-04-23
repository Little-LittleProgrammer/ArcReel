# 示例 3：蓝湖团队协作

用户说："在蓝湖留言通知设计师已完成"

## 操作步骤

1. 获取项目成员：`lanhu_get_members(project_id="xxx")`
2. 找到设计师的成员 ID
3. 发布评论：`lanhu_say(project_id="xxx", content="前端实现已完成，请查看 @设计师ID")`

## 协作工具

- `lanhu_say` — 发布评论
- `lanhu_say_list` — 获取评论列表
- `lanhu_say_detail` — 获取评论详情
- `lanhu_say_edit` — 编辑评论
- `lanhu_say_delete` — 删除评论