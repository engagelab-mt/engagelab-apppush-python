# 更新日志

本项目的所有重要更改都将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [未发布]

### 新增

- 日本、巴西数据中心
- Device Token 换取 Registration ID 与 App VIP 状态 API

### 变更

- 补齐 Push、Schedule、Status、Plan 和 Group Push 协议字段
- Voice 改为官网 multipart 文件协议，OPPO Image 改为官网 JSON URL 协议
- Tag 计数/配额及 Plan Detail 查询参数改为官网协议

## [0.1.0] - 2026-03-20

### 新增

- `Client` 客户端初始化，支持 `base_url`、`timeout` 等参数
- 四大数据中心常量：`DataCenter.SINGAPORE`（默认）、`HONG_KONG`、`VIRGINIA`、`FRANKFURT`
- **Push** — 推送服务：`send`、`send_raw`、`validate`、`withdraw`、`batch_by_regid`、`batch_by_alias`
- **Group Push** — 应用分组推送：独立 `GroupPushClient` + `send`
- **Device** — 设备管理：`get`、`set`、`delete`、`get_status`
- **Tag** — 标签管理：`list`、`set`、`delete`、`get_count`、`get_device_status`、`get_quota`
- **Alias** — 别名管理：`get`、`delete`
- **Schedule** — 定时推送：`create`、`update`、`delete`、`get`、`list`、`get_msg_ids`
- **Status** — 统计查询：`users`、`message_detail`、`message_lifecycle`、`batch_message_detail`、`plan_detail`
- **Plan** — 推送计划：`create_or_update`、`list`、`query_msg`、`delete`、`batch_delete`
- **Voice** — 语音/TTS 模板：`create`、`list`、`get`、`delete`
- **Image** — 图片上传：`upload_oppo`、`upload_oppo_from_reader`
- `ApiError` 结构化异常类型，包含 HTTP 状态码和业务错误码
- 完整的单元测试（使用 `http.server` 模拟，零外部依赖）
- 零第三方依赖，仅使用 Python 标准库
