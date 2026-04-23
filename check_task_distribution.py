#!/usr/bin/env python3
"""
查看当前队列中任务的供应商和媒体类型分布
"""

import asyncio
from collections import Counter

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
    print(f"找到 {len(tasks)} 个排队中的任务\n")

    # 统计供应商和媒体类型
    provider_counter = Counter()
    media_type_counter = Counter()
    provider_media_counter = Counter()

    for task in tasks:
        payload = task.get("payload", {})
        provider = payload.get("provider", "未知")
        media_type = task.get("media_type", "未知")

        provider_counter[provider] += 1
        media_type_counter[media_type] += 1
        provider_media_counter[(provider, media_type)] += 1

    print("供应商分布:")
    for provider, count in provider_counter.most_common():
        print(f"  {provider}: {count}")

    print("\n媒体类型分布:")
    for media_type, count in media_type_counter.most_common():
        print(f"  {media_type}: {count}")

    print("\n供应商 + 媒体类型组合:")
    for (provider, media_type), count in sorted(provider_media_counter.items(), key=lambda x: -x[1]):
        print(f"  {provider} / {media_type}: {count}")

    # 显示前 10 个任务的详细信息
    print("\n前 10 个任务详情:")
    for i, task in enumerate(tasks[:10], 1):
        payload = task.get("payload", {})
        provider = payload.get("provider", "未知")
        media_type = task.get("media_type", "未知")
        error = task.get("error_message", "")
        print(f"{i}. {task['task_id']}")
        print(f"   类型: {task['task_type']} | 媒体: {media_type} | 供应商: {provider}")
        if error:
            print(f"   错误: {error[:100]}")


if __name__ == "__main__":
    asyncio.run(main())
