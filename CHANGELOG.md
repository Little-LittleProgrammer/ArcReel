# Changelog

## [0.10.0](https://github.com/Little-LittleProgrammer/ArcReel/compare/v0.9.0...v0.10.0) (2026-04-20)


### ✨ 新功能

* **agent:** 参考生视频模式 Agent 工作流 ([#337](https://github.com/Little-LittleProgrammer/ArcReel/issues/337)) ([a521eac](https://github.com/Little-LittleProgrammer/ArcReel/commit/a521eac1f1c8456aeab855af29b1e64034697d81))
* **backend:** reference-to-video mode API + executor (PR3/7) ([#332](https://github.com/Little-LittleProgrammer/ArcReel/issues/332)) ([0846691](https://github.com/Little-LittleProgrammer/ArcReel/commit/08466910d417214a9be885a0811c0c32c801bece))
* **frontend:** 参考生视频前端编辑器（PR5/7） ([#342](https://github.com/Little-LittleProgrammer/ArcReel/issues/342)) ([847c151](https://github.com/Little-LittleProgrammer/ArcReel/commit/847c151de378f54f97a3f402d228bd460d74787e))
* **frontend:** 参考生视频模式选择器 + Canvas 外壳（PR4/7） ([#338](https://github.com/Little-LittleProgrammer/ArcReel/issues/338)) ([64c3f5f](https://github.com/Little-LittleProgrammer/ArcReel/commit/64c3f5f652e6d0f391b3a79a68b91ecee7a21cb5))
* integrate release-please for automated versioning ([#312](https://github.com/Little-LittleProgrammer/ArcReel/issues/312)) ([dda244c](https://github.com/Little-LittleProgrammer/ArcReel/commit/dda244cff89472d4dc61d9f7a7a2fde3747751c0))
* **script-models:** 参考生视频数据模型 + shot parser (PR2/7) ([#330](https://github.com/Little-LittleProgrammer/ArcReel/issues/330)) ([ba0dd6b](https://github.com/Little-LittleProgrammer/ArcReel/commit/ba0dd6b138101aa9a28ad84480c7431519265c6e))
* **sdk-verify:** 参考生视频四家供应商 SDK 验证脚本与能力矩阵 ([#328](https://github.com/Little-LittleProgrammer/ArcReel/issues/328)) ([0aefaab](https://github.com/Little-LittleProgrammer/ArcReel/commit/0aefaab4ee011db3e58086910b7afc623b7344e0))
* **source:** 源文件格式扩展（.txt/.md/.docx/.epub/.pdf 统一规范化） ([#350](https://github.com/Little-LittleProgrammer/ArcReel/issues/350)) ([13a3bb6](https://github.com/Little-LittleProgrammer/ArcReel/commit/13a3bb6a15d52d67f2a1338ac4d78276b982d62b))
* 全局资产库 + 线索重构拆分为场景和道具（scenes/props 拆分） ([#307](https://github.com/Little-LittleProgrammer/ArcReel/issues/307)) ([51dde36](https://github.com/Little-LittleProgrammer/ArcReel/commit/51dde363d3c8492e0b0ac45bc0932d48cf8e362c))
* 自定义供应商支持 NewAPI 格式（统一视频端点） ([#305](https://github.com/Little-LittleProgrammer/ArcReel/issues/305)) ([433124d](https://github.com/Little-LittleProgrammer/ArcReel/commit/433124d87b299c9a99799adc65a35c2ff00df0c0))


### 🐛 Bug 修复

* **ci:** pin setup-uv to v7 in release-please workflow ([#315](https://github.com/Little-LittleProgrammer/ArcReel/issues/315)) ([b602779](https://github.com/Little-LittleProgrammer/ArcReel/commit/b602779aa5476061bc73cb118f52f15c332ad646))
* **docs,ci:** address review feedback from PR [#310](https://github.com/Little-LittleProgrammer/ArcReel/issues/310)-314 ([#316](https://github.com/Little-LittleProgrammer/ArcReel/issues/316)) ([81ff8ce](https://github.com/Little-LittleProgrammer/ArcReel/commit/81ff8ce6b9ff8a3ff5c6f136d62e8a4cc66fc58f))
* **frontend:** regenerate pnpm-lock.yaml to fix duplicate keys ([#331](https://github.com/Little-LittleProgrammer/ArcReel/issues/331)) ([a91fd8b](https://github.com/Little-LittleProgrammer/ArcReel/commit/a91fd8be1167a2f6e55eb3ad7210e810242b5312))
* **video:** seedance-2.0 模型不传 service_tier 参数 ([#325](https://github.com/Little-LittleProgrammer/ArcReel/issues/325)) ([66aa423](https://github.com/Little-LittleProgrammer/ArcReel/commit/66aa42394bc303473a4903fdbd815a5ac007a238))


### ⚡ 性能优化

* **backend:** 消除 _serialize_value 对 Pydantic 的双遍历 ([#298](https://github.com/Little-LittleProgrammer/ArcReel/issues/298)) ([#335](https://github.com/Little-LittleProgrammer/ArcReel/issues/335)) ([f945fad](https://github.com/Little-LittleProgrammer/ArcReel/commit/f945fad5c780dbd1531c55e0e87da0fdedcc3baa))


### ♻️ 重构

* **backend:** 后端 AssetType 统一抽象（关闭 [#326](https://github.com/Little-LittleProgrammer/ArcReel/issues/326)） ([#336](https://github.com/Little-LittleProgrammer/ArcReel/issues/336)) ([9dcd221](https://github.com/Little-LittleProgrammer/ArcReel/commit/9dcd221d57bd1b3bf182ff3bc254813503b9acf6))
* PR [#307](https://github.com/Little-LittleProgrammer/ArcReel/issues/307) tech-debt follow-up（P1 + P2 低风险） ([#327](https://github.com/Little-LittleProgrammer/ArcReel/issues/327)) ([c23972a](https://github.com/Little-LittleProgrammer/ArcReel/commit/c23972a2f017b825aa09ffff86bcfccfaec7f23d))
