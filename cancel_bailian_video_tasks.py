#!/usr/bin/env python3
"""
批量取消 bailian 供应商的视频生成任务
"""

import asyncio
import sys

from lib.generation_queue import get_generation_queue


async def main():
    queue = get_generation_queue()

    # 获取所有 queued 状态的任务
    result = await queue.list_tasks(
        status="queued",
        page=1,
        page_size=500,
    )

    tasks = result.get("items", [])
    print(f"找到 {len(tasks)} 个排队中的任务")

    # 筛选出 bailian 供应商的视频任务
    bailian_video_tasks = []
    for task in tasks:
        payload = task.get("payload", {})
        provider = payload.get("provider")
        media_type = task.get("media_type")

        if provider == "bailian" and media_type == "video":
            bailian_video_tasks.append(task)

    print(f"\n找到 {len(bailian_video_tasks)} 个 bailian 视频任务:")
    for task in bailian_video_tasks:
        print(f"  - {task['task_id']}: {task['task_type']} | {task['resource_id']}")

    if not bailian_video_tasks:
        print("\n没有找到需要取消的任务")
        return

    # 确认取消
    print(f"\n准备取消 {len(bailian_video_tasks)} 个任务")
    confirm = input("确认取消? (yes/no): ")

    if confirm.lower() != "yes":
        print("已取消操作")
        return

    # 批量取消
    cancelled_count = 0
    failed_count = 0

    for task in bailian_video_tasks:
        task_id = task["task_id"]
        try:
            result = await queue.cancel_task(task_id)
            cancelled = result.get("cancelled", [])
            cancelled_count += len(cancelled)
            print(f"✓ 已取消任务 {task_id} (连带取消 {len(cancelled)} 个)")
        except Exception as e:
            failed_count += 1
            print(f"✗ 取消任务 {task_id} 失败: {e}")

    print(f"\n完成! 成功取消 {cancelled_count} 个任务, 失败 {failed_count} 个")


if __name__ == "__main__":
    asyncio.run(main())
