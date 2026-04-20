## ADDED Requirements

### Requirement: Bailian R2V 接受参考素材输入
系统 MUST 支持在使用 `wan2.7-r2v` 时向 DashScope 请求体的 `input.media` 传递参考素材，并将每个参考素材映射为 `reference_image` 或 `reference_video` 条目；当参考素材携带声音参考时，系统 MUST 在对应条目上附带 `reference_voice` 字段。

#### Scenario: 使用图片和视频参考构造 media
- **WHEN** 调用方使用 `wan2.7-r2v` 提交包含参考图片、参考视频和部分声音参考的生成请求
- **THEN** 系统生成的 `input.media` MUST 保留素材顺序，并为图片映射 `type=reference_image`、为视频映射 `type=reference_video`
- **THEN** 对于带声音参考的素材，系统 MUST 在同一条目中附带 `reference_voice`

### Requirement: Bailian R2V 校验素材数量与类型约束
系统 MUST 在提交 `wan2.7-r2v` 请求前校验输入约束：参考视频数量不得超过 3 个，参考图片数量不得超过 9 个，总参考素材数量不得超过 5 个，且仅允许图片和视频类型素材作为 R2V 参考输入。

#### Scenario: 参考视频数量超限
- **WHEN** 调用方提交超过 3 个参考视频的 `wan2.7-r2v` 请求
- **THEN** 系统 MUST 在本地拒绝请求并返回明确的校验错误

#### Scenario: 参考素材总数超限
- **WHEN** 调用方提交总数超过 9 个的参考素材
- **THEN** 系统 MUST 在创建远端任务前返回校验错误

#### Scenario: 出现不支持的参考素材类型
- **WHEN** 调用方在 `wan2.7-r2v` 请求中传入既非图片也非视频的参考素材
- **THEN** 系统 MUST 拒绝请求并指出该素材类型不被支持

### Requirement: Bailian R2V 复用现有异步任务链路
系统 MUST 通过现有 DashScope 异步视频任务流程执行 `wan2.7-r2v`，包括创建任务、轮询状态、提取 `video_url` 并下载输出视频；生成结果 MUST 与现有视频后端结果结构保持一致。

#### Scenario: R2V 任务成功完成
- **WHEN** `wan2.7-r2v` 任务返回 `SUCCEEDED` 且响应中包含 `video_url`
- **THEN** 系统 MUST 下载视频到请求指定的输出路径
- **THEN** 系统 MUST 返回包含 provider、model、duration、task_id、request_id 和输出路径的生成结果

### Requirement: Bailian R2V 处理本地与 OSS 参考资源
系统 MUST 支持 `wan2.7-r2v` 参考素材使用本地文件路径、HTTP/HTTPS URL 或 `oss://` URL；当输入为本地文件时，系统 MUST 先上传到 DashScope 临时 OSS，再在请求头中启用 `X-DashScope-OssResourceResolve` 以解析 OSS 资源。

#### Scenario: 使用本地文件作为参考素材
- **WHEN** 调用方在 `wan2.7-r2v` 请求中提供本地图片、视频或声音文件路径
- **THEN** 系统 MUST 先将对应文件上传为临时 OSS 资源
- **THEN** 系统 MUST 在请求体中使用上传后的 `oss://` URL，并设置 `X-DashScope-OssResourceResolve: enable`

#### Scenario: 混合使用公网 URL 与 OSS URL
- **WHEN** 调用方同时提供 HTTP/HTTPS URL 与 `oss://` URL 作为 `wan2.7-r2v` 参考素材
- **THEN** 系统 MUST 原样保留公网 URL
- **THEN** 系统 MUST 对 `oss://` 资源启用 OSS 解析请求头
