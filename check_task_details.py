#!/usr/bin/env python3
"""
查看任务的完整 payload 和错误信息
"""

import asyncio
import json

from lib.generation_queue import get_generation_queue


async def main():
    queue = get_generation_queue()

    # 检查 queued 和 running 状态的任务
    for status in ["queued", "running"]:
        result = await queue.list_tasks(
            status=status,
            page=1,
            page_size=10,
        )

        tasks = result.get("items", [])
        print(f"\n{'=' * 60}")
        print(f"状态: {status} ({len(tasks)} 个任务)")
        print("=" * 60)

        for i, task in enumerate(tasks[:3], 1):
            print(f"\n任务 {i}: {task['task_id']}")
            print(f"  类型: {task['task_type']}")
            print(f"  媒体: {task['media_type']}")
            print(f"  资源: {task['resource_id']}")
            print(f"  项目: {task['project_name']}")

            payload = task.get("payload", {})
            print(f"  Payload: {json.dumps(payload, ensure_ascii=False, indent=4)}")

            error = task.get("error_message")
            if error:
                print(f"  错误: {error[:200]}")


if __name__ == "__main__":
    asyncio.run(main())
