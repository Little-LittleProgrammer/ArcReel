#!/usr/bin/env python3
"""
批量取消当前默认视频后端对应的所有排队视频任务
"""

import asyncio

from sqlalchemy import select

from lib.db import safe_session_factory
from lib.db.models.config import SystemSetting
from lib.generation_queue import get_generation_queue


async def main():
    # 获取当前默认视频后端
    async with safe_session_factory() as session:
        result = await session.execute(select(SystemSetting).where(SystemSetting.key == "default_video_backend"))
        setting = result.scalar_one_or_none()
        backend = setting.value if setting else "unknown"

    print(f"当前默认视频后端: {backend}")

    queue = get_generation_queue()

    # 获取所有 queued 状态的任务
    result = await queue.list_tasks(
        status="queued",
        page=1,
        page_size=500,
    )

    tasks = result.get("items", [])
    video_tasks = [t for t in tasks if t.get("media_type") == "video"]

    print(f"找到 {len(video_tasks)} 个排队中的视频任务")

    if not video_tasks:
        print("没有找到需要取消的任务")
        return

    cancelled_count = 0
    failed_count = 0

    for task in video_tasks:
        task_id = task["task_id"]
        try:
            result = await queue.cancel_task(task_id)
            cancelled = result.get("cancelled", [])
            if cancelled:
                cancelled_count += 1
                print(f"✓ 已取消任务 {task_id}: {task['resource_id']}")
        except Exception as e:
            failed_count += 1
            print(f"✗ 取消任务 {task_id} 失败: {e}")

    print(f"\n完成! 成功取消 {cancelled_count} 个任务, 失败 {failed_count} 个")


if __name__ == "__main__":
    asyncio.run(main())
