## Why

ArcReel 已接入阿里云百炼 Wan 2.7 的基础视频生成能力，但尚不支持 `wan2.7-r2v` 参考视频生成，无法利用角色图片、参考视频和参考声音生成角色一致的视频内容。

补齐 R2V 能力可以让用户基于现有角色资产与参考素材生成更稳定的剧情视频，提升国内 DashScope 供应商在视频生成链路中的可用性。

## What Changes

- 为阿里云百炼视频后端新增 `wan2.7-r2v` 参考生视频能力。
- 支持向 DashScope 视频生成接口提交 `reference_image`、`reference_video` 与可选 `reference_voice` 参考素材。
- 支持 R2V 参数约束：分辨率、比例、2-10 秒时长、prompt 扩展、水印控制。
- 复用现有异步任务提交、轮询、结果下载与版本管理链路。
- 不引入破坏性变更。

## Capabilities

### New Capabilities

- `bailian-reference-to-video`: 定义阿里云百炼 `wan2.7-r2v` 参考视频生成能力，包括参考素材输入、请求参数约束、异步任务处理与结果产出要求。

### Modified Capabilities

无。

## Impact

- 影响 `lib/video_backends/bailian.py` 的请求构造、能力分发与输入素材处理。
- 可能影响 `lib/media_generator.py` 中视频生成参数向后端传递的兼容性。
- 可能影响 `lib/config/registry.py` 中 `wan2.7-r2v` 模型能力声明或默认约束。
- 需要补充或更新针对百炼视频后端的单元测试与 lint 验证。
