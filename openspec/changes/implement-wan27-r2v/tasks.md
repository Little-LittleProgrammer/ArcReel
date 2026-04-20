## 1. 扩展百炼视频请求模型

- [x] 1.1 为视频生成请求补充 R2V 所需的参考素材数据结构，支持图片、视频与可选声音参考
- [x] 1.2 确保新增请求字段不影响现有 T2V/I2V 调用路径与类型校验

## 2. 实现 Bailian R2V 后端能力

- [x] 2.1 更新 `lib/video_backends/bailian.py` 的模型白名单、能力声明与参数校验，使 `wan2.7-r2v` 可用
- [x] 2.2 实现 `wan2.7-r2v` 的 `input.media` 构造逻辑，正确映射 `reference_image`、`reference_video` 与 `reference_voice`
- [x] 2.3 复用现有资源解析与上传逻辑，支持本地文件、HTTP/HTTPS 与 `oss://` 参考素材

## 3. 接通生成链路与回归验证

- [x] 3.1 调整必要的调用链参数传递，确保 MediaGenerator 与视频生成入口可向百炼后端传递 R2V 参考素材
- [x] 3.2 为百炼视频后端补充 R2V 的单元测试，覆盖 payload 构造、数量校验与资源解析行为
- [x] 3.3 运行与本次改动相关的 `ruff check`、`ruff format` 和测试，只修复 error 级别问题
