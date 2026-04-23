#!/usr/bin/env python3
"""
查询数据库中的配置，找出当前使用的视频供应商
"""

import asyncio

from sqlalchemy import select

from lib.db import safe_session_factory
from lib.db.models.config import ProviderConfig, SystemSetting


async def main():
    async with safe_session_factory() as session:
        # 查询系统设置
        print("系统设置:")
        result = await session.execute(select(SystemSetting))
        settings = result.scalars().all()
        for setting in settings:
            print(f"  {setting.key}: {setting.value}")

        # 查询供应商配置
        print("\n供应商配置:")
        result = await session.execute(select(ProviderConfig))
        configs = result.scalars().all()
        for config in configs:
            secret_marker = " (secret)" if config.is_secret else ""
            value = "***" if config.is_secret else config.value
            print(f"  {config.provider}.{config.key}: {value}{secret_marker}")


if __name__ == "__main__":
    asyncio.run(main())
