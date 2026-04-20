## Context

当前 `lib/video_backends/bailian.py` 已实现百炼视频异步任务链路，包括任务创建、轮询、结果下载与基础参数校验，但 `_SUPPORTED_MODELS` 仅允许 `wan2.7-t2v` 和 `wan2.7-i2v`，`wan2.7-r2v` 虽然已在模型能力映射中预留项，实际请求构造与校验逻辑尚未落地。文档要求 R2V 支持最多 5 个参考素材，其中视频最多 3 个、图片最多 9 个，并允许为参考角色附带 `reference_voice`。

本次变更需要在不破坏现有 T2V/I2V 行为的前提下，将 R2V 接入现有 VideoBackend 与 MediaGenerator 链路，复用异步任务机制和 OSS 临时资源上传能力，同时约束 DashScope 文档定义的输入上限与时长范围。

## Goals / Non-Goals

**Goals:**
- 让 `BailianVideoBackend` 正式支持 `wan2.7-r2v`。
- 为 R2V 增加参考图片、参考视频和可选参考声音的请求构造逻辑。
- 在后端请求前完成模型级输入校验，包括素材类型、数量及时长限制。
- 尽量复用已有上传、轮询、下载、Usage 统计与版本管理流程。

**Non-Goals:**
- 不在本次设计中实现 `wan2.7-videoedit`。
- 不新增前端独立配置页或新的交互协议。
- 不扩展超出当前数据模型所需的通用多模态抽象。

## Decisions

1. **在现有 `VideoGenerationRequest` 能力范围内扩展 R2V 输入，而不新建独立后端接口**  
   - 原因：R2V 与 T2V/I2V 共用同一 DashScope endpoint 和异步任务生命周期，主要差异是 `input.media` 的构造方式，继续沿用单一 `BailianVideoBackend.generate()` 可以保持调用方透明。  
   - 备选方案：单独新增一个 R2V 专用 backend。该方案会重复任务提交、轮询和下载逻辑，增加工厂分发复杂度，因此不采用。

2. **以“参考素材列表”驱动 payload 构造，并在构造前做模型级校验**  
   - 原因：R2V 的核心差异是 `media` 数组中混合 `reference_image`、`reference_video` 与 `reference_voice`。先在请求对象层提供参考素材列表，再由 `BailianVideoBackend` 统一映射到 DashScope 字段，可以最小化对上层调用方式的影响。  
   - 备选方案：在 `prompt` 中拼接参考描述，或把声音参考拆成独立字段。前者无法满足官方 API 要求，后者会让图片/视频/声音关联关系分散，不利于校验。

3. **声音参考仅作为附着在单个参考素材上的可选属性处理**  
   - 原因：官方示例中 `reference_voice` 绑定在某个 `reference_image` 或 `reference_video` 条目上，而非全局参数。保持这种一对一结构，能表达“哪个角色使用哪段声音”的语义。  
   - 备选方案：提供全局 `driving_audio` 风格字段。该字段属于 I2V 模式，不适用于 R2V，因此不采用。

4. **严格限制 R2V 输入组合：视频最多 3 个，图片最多 5 个，总素材数最多 5 个**  
   - 原因：文档明确给出上限，提前在本地报错可以避免无效请求进入远端队列。  
   - 备选方案：完全交给远端接口返回错误。该方案反馈更慢，也不利于调用方定位问题。

5. **保持 MediaGenerator 和版本管理链路不感知 R2V 细节，只负责把请求参数传给视频后端**  
   - 原因：版本管理关注输出文件，不应耦合供应商特定输入协议。R2V 的供应商差异应收敛在 `lib/video_backends/bailian.py` 和相关基础 request 模型中。  
   - 备选方案：在 MediaGenerator 中做参考素材上传和分类。这样会让中间层承担供应商细节，破坏职责边界。

## Risks / Trade-offs

- **[风险] 现有 `VideoGenerationRequest` 可能缺少表达 R2V 参考素材所需的结构** → **缓解**：在基础模型中做最小增量扩展，只新增 R2V 所需字段，不改动既有 T2V/I2V 字段语义。
- **[风险] 本地路径、HTTP URL、`oss://` URL 混用时，请求头 `X-DashScope-OssResourceResolve` 处理不一致** → **缓解**：继续复用 `_resolve_media_url()`，只在解析到 `oss://` 或本地上传后统一设置请求头。
- **[风险] 参考声音与参考素材绑定关系错误，导致接口接受但生成结果不符合预期** → **缓解**：定义清晰的数据结构，并在测试中覆盖“素材带声音”和“不带声音”两类 payload。
- **[风险] 增加 R2V 支持后影响现有 T2V/I2V 校验分支** → **缓解**：保持分模型分支校验，补充针对三种模型的单元测试，确保旧模型行为不回归。
- **[风险] 官方文档与实际接口行为存在偏差，例如 `ratio`、`prompt_extend` 或音频能力字段支持不一致** → **缓解**：先按已确认文档实现，遇到真实 API 差异时优先通过后端兼容处理，而不是扩大调用方接口面。
